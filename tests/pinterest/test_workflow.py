import copy
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock
from urllib.error import HTTPError
from scripts.pinterest import adapters, content, research, results
from scripts.pinterest.core import ROOT, Invalid, atomic, read, digest, validate, load_run

F=ROOT/'tests/pinterest/fixtures'

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.d=Path(self.temp.name)/'pilot'
        research.collect(self.d,F/'profile.json','fixture',read(F/'signals.json'),read(F/'references.json'))
        self.assess=read(F/'assessments.json')
        research.rank(self.d,self.assess)

    def tearDown(self):self.temp.cleanup()

    def briefs(self):
        return [content.package(self.d,read(p)) for p in sorted(F.glob('*-brief.json'))]

    def register(self):
        self.briefs()
        for i,fmt in enumerate(('static','video')):
            results.register(self.d,{'asset_id':'harvest-flecks-'+fmt+'-v1','pin_url':'https://www.pinterest.com/pin/'+str(900000000000000001+i)+'/',
                 'published_date':'2026-08-01','account_id':'fixture-pinterest','authorization_reference':'SYNTHETIC publication for automated tests only'})

    def test_contract_rejections(self):
        for key,value in [('schema_version',2),('unit','absolute_searches'),('retrieved_at','yesterday')]:
            s=read(F/'signals.json')[0];s[key]=value
            with self.assertRaises(Invalid):validate('signal',s)
        s=read(F/'signals.json')[0];del s['source_url']
        with self.assertRaises(Invalid):validate('signal',s)
        for file,kind in [('profile.json','profile'),('signals.json','signal'),('references.json','reference'),('assessments.json','candidate_input'),('results.json','result')]:
            data=read(F/file)
            for row in data if isinstance(data,list) else [data]:validate(kind,row)

    def test_atomic_failure_preserves_file(self):
        path=self.d/'atomic.json';atomic(path,{'before':True})
        with patch('os.replace',side_effect=OSError('simulated interruption')):
            with self.assertRaises(OSError):atomic(path,{'after':True})
        self.assertEqual(read(path),{'before':True})
        self.assertEqual(list(self.d.glob('*.tmp')),[])

    def test_dedup_and_resume(self):
        research.collect(self.d,F/'profile.json','fixture',read(F/'signals.json'),read(F/'references.json'))
        run=load_run(self.d)
        self.assertEqual(len(run['signals']),3);self.assertEqual(len(run['references']),3)
        self.assertEqual(run['paid_calls'],0);self.assertEqual(run['publish_calls'],0)

    def test_real_run_rejects_fixture(self):
        with self.assertRaises(Invalid):research.collect(self.d.parent/'real',F/'profile.json','manual',read(F/'signals.json'))

    def test_ranking_missing_and_mismatch(self):
        a=copy.deepcopy(self.assess)
        a[0]['signal_ids']=[]
        a[1]['scores']['product_fit']['value']=0
        ranked=research.rank(self.d,a)
        by={x['id']:x for x in ranked}
        self.assertEqual(by[a[0]['id']]['status'],'exploratory')
        self.assertEqual(by[a[0]['id']]['scores']['demand_evidence']['value'],0)
        self.assertEqual(by[a[1]['id']]['status'],'excluded')
        self.assertEqual(sum(x['status']=='qualified' for x in ranked),1)
        a[0]['signal_ids']=['missing']
        with self.assertRaises(Invalid):research.rank(self.d,a)

    def test_three_briefs_and_immutable_version(self):
        packs=self.briefs()
        self.assertEqual(len({x['brief']['hook'] for x in packs}),3)
        b=read(F/'harvest-flecks-brief.json');b['hook']='Changed hook'
        with self.assertRaises(Invalid):content.package(self.d,b)
        b['version']=2
        new=content.package(self.d,b)
        self.assertIn('v2',new['variants'][0]['asset_id'])
        self.assertTrue((self.d/'briefs/harvest-flecks-v1/brief.json').exists())

    def test_tracking_and_destination(self):
        url=content.tracking('https://example.com/p?variant=3&utm_source=old#details','campaign','asset')
        self.assertIn('variant=3',url);self.assertIn('utm_source=pinterest',url);self.assertNotIn('old',url);self.assertTrue(url.endswith('#details'))
        opener=Mock()
        self.assertEqual(content.check_destination('https://unapproved.example/x',['www.cincohranchnaturals.com'],opener)['status'],'blocked')
        opener.open.assert_not_called()
        opener.open.side_effect=HTTPError('x',404,'not found',{},None)
        self.assertEqual(content.check_destination('https://www.cincohranchnaturals.com/x',['www.cincohranchnaturals.com'],opener)['status'],'blocked')

    def test_export_stays_free_and_blocked(self):
        self.briefs();out=content.export(self.d,'harvest-flecks-v1')
        self.assertEqual(out['mode'],'export_only');self.assertEqual(out['credit_ceiling'],0)
        self.assertTrue(any('Destination' in x for x in out['blockers']))
        self.assertEqual(out['paid_calls'],0)

    def test_bad_audio_and_storyboard(self):
        b=read(F/'harvest-flecks-brief.json');b['audio']['choice']=''
        with self.assertRaises(Invalid):content.package(self.d,b)
        b=read(F/'harvest-flecks-brief.json');b['shots'][1]['start']=2
        with self.assertRaises(Invalid):content.package(self.d,b)

    def test_review_invalidates_on_asset_and_media_change(self):
        p=read(self.d/'profile.json')
        media=Path(self.temp.name)/'original.png';media.write_bytes(b'synthetic image bytes')
        p['assets'][0].update(path=str(media),sha256=digest(media.read_bytes()),rights='owned',rights_evidence='fixture ownership',approved=True)
        for c in p['claims']:c['approved']=True
        atomic(self.d/'profile.json',p)
        b=read(F/'harvest-flecks-brief.json');b['audio']={'choice':'silence','direction':'Explicitly selected silence for fixture','rights_evidence':None}
        content.package(self.d,b)
        r={'stage':'image','decision':'approved','reviewer':'fixture reviewer','evidence':'synthetic quality review','media_path':str(media),'checks':{x:True for x in content.CHECKS}}
        accepted=content.review(self.d,'harvest-flecks-v1',r)
        self.assertEqual(accepted['decision'],'approved')
        pack=read(self.d/'briefs/harvest-flecks-v1/brief.json')
        binding,_=content.current_binding(self.d,pack)
        self.assertTrue(content.valid_review(accepted,binding))
        media.write_bytes(b'changed')
        changed,_=content.current_binding(self.d,pack)
        self.assertFalse(content.valid_review(accepted,changed))
        r['checks']['product_identity']=False
        self.assertEqual(content.review(self.d,'harvest-flecks-v1',r)['decision'],'rejected')

    def test_results_idempotency_and_attribution(self):
        self.register();rows=read(F/'results.json')
        results.import_results(self.d,rows)
        a=results.report(self.d)
        self.assertEqual(results.import_results(self.d,rows)['status'],'already_imported')
        b=results.report(self.d)
        self.assertEqual(a['experiments'],b['experiments'])
        self.assertEqual(a['experiments'][0]['outbound_ctr'],.03)
        self.assertEqual(a['experiments'][0]['money_by_currency']['USD']['net_attributed_revenue'],18)
        self.assertEqual(results.report(self.d,14)['experiments'][0]['metrics']['impressions'],None)
        unatt=copy.deepcopy(rows[4]);unatt.update(asset_id=None,experiment_id=None,pin_id=None)
        results.import_results(self.d,[unatt])
        self.assertEqual(len(results.report(self.d)['unattributed_snapshots']),1)
        self.assertEqual(results.report(self.d)['experiments'][0]['metrics']['orders'],2)

    def test_results_conflicts_overlap_and_unknowns(self):
        self.register();rows=read(F/'results.json');results.import_results(self.d,rows)
        altered=copy.deepcopy(rows[0]);altered['value']=2000
        with self.assertRaises(Invalid):results.import_results(self.d,[altered])
        altered['extracted_at']='2026-08-10T00:00:00+00:00';results.import_results(self.d,[altered])
        self.assertEqual(results.report(self.d)['experiments'][0]['metrics']['impressions'],2000)
        overlapping=copy.deepcopy(altered);overlapping['period']['end']='2026-08-15';overlapping['extracted_at']='2026-08-16T00:00:00+00:00';overlapping['value']=3000
        results.import_results(self.d,[overlapping])
        self.assertEqual(results.report(self.d,7)['experiments'][0]['metrics']['impressions'],2000)
        self.assertEqual(results.report(self.d,14)['experiments'][0]['metrics']['impressions'],3000)
        absent=copy.deepcopy(rows[3]);absent['value']=None;absent['extracted_at']='2026-08-11T00:00:00+00:00'
        results.import_results(self.d,[absent])
        self.assertIsNone(results.report(self.d)['experiments'][0]['purchase_conversion'])

    def test_results_account_currency_and_zero(self):
        self.register();rows=read(F/'results.json')
        bad=copy.deepcopy(rows[0]);bad['account_id']='wrong'
        with self.assertRaises(Invalid):results.import_results(self.d,[bad])
        bad=copy.deepcopy(rows[0]);bad['period']['start']='2026-08-02'
        with self.assertRaises(Invalid):results.import_results(self.d,[bad])
        rows[0]['value']=0;rows[5]['currency']='EUR'
        results.import_results(self.d,rows)
        r=results.report(self.d)['experiments'][0]
        self.assertIsNone(r['outbound_ctr'])
        self.assertIsNone(r['money_by_currency']['EUR']['net_attributed_revenue'])
        self.assertEqual(r['assessment'],'insufficient evidence')

    def test_readonly_adapter_errors_and_limits(self):
        with patch.dict(os.environ,{'PINTEREST_OPENCLI_BIN':'/fixture/opencli'}):
            runner=Mock(return_value=Mock(returncode=0,stdout=json.dumps(read(F/'opencli.json')),stderr=''))
            with self.assertRaises(Invalid):adapters.opencli('pin-delete','123',runner=runner)
            runner.assert_not_called()
            data=adapters.opencli('search-pins','soap',runner=runner)
            self.assertEqual(adapters.references(data,'soap')[0]['rights'],'reference_only')
            runner.return_value=Mock(returncode=1,stdout='',stderr='401 SECRET')
            with self.assertRaises(adapters.Unavailable) as e:adapters.opencli('pin','123',runner=runner)
            self.assertNotIn('SECRET',str(e.exception))
            runner.reset_mock();runner.return_value=Mock(returncode=1,stdout='',stderr='429')
            with self.assertRaises(adapters.Unavailable):adapters.opencli('search-pins','soap',runner=runner,sleep=lambda _:None)
            self.assertEqual(runner.call_count,3)
            runner.return_value=Mock(returncode=0,stdout='not json',stderr='')
            with self.assertRaises(adapters.Unavailable):adapters.opencli('search-pins','soap',runner=runner)

    def test_trends_schema_and_api_failures(self):
        sig=adapters.trends(read(F/'trends-api.json'),'US','tallow soap','https://api.pinterest.com/v5/test','fixture')[0]
        self.assertEqual(sig['growth']['wow'],50);self.assertIsNone(sig['growth']['mom'])
        self.assertEqual(sig['time_series']['2026-08-31'],60)
        with self.assertRaises(adapters.Unavailable):adapters.trends({'items':[]},'US','x','https://api.pinterest.com/x')
        opener=Mock();opener.open.side_effect=HTTPError('x',401,'token',{},None)
        with self.assertRaises(adapters.Unavailable):adapters.get_json('https://api.pinterest.com/x','secret',opener)
        self.assertEqual(opener.open.call_count,1)
        with self.assertRaises(Invalid):adapters.get_json('https://evil.example/x','secret',opener)
        opener.reset_mock();opener.open.side_effect=HTTPError('x',429,'limited',{'Retry-After':'0'},None)
        with self.assertRaises(adapters.Unavailable):adapters.get_json('https://api.pinterest.com/x','secret',opener,sleep=lambda _:None)
        self.assertEqual(opener.open.call_count,3)

    def test_live_checkpoints_survive_final_write_interruption(self):
        target=self.d.parent/'live'
        with patch('scripts.pinterest.adapters.opencli',return_value=read(F/'opencli.json')) as pins, patch('scripts.pinterest.adapters.fetch_trends',side_effect=adapters.Unavailable('not configured')) as trends:
            with patch('scripts.pinterest.research.save_run',side_effect=OSError('interrupted')):
                with self.assertRaises(OSError):research.collect(target,F/'profile.json','live',live=True)
            self.assertEqual(pins.call_count,3)
            research.collect(target,F/'profile.json','live',live=True)
            self.assertEqual(pins.call_count,3);self.assertEqual(trends.call_count,3)
            self.assertEqual(len(load_run(target)['references']),1)

    def test_csv_import_and_utc_timestamp(self):
        import csv
        from scripts.pinterest.core import records
        self.register()
        row=read(F/'results.json')[0];row['extracted_at']='2026-08-09T00:00:00Z'
        file=self.d/'input.csv'
        with file.open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(row));writer.writeheader()
            writer.writerow({k:json.dumps(v) if isinstance(v,(dict,list)) else '' if v is None else v for k,v in row.items()})
        parsed=records(file)
        self.assertEqual(parsed[0]['period'],row['period'])
        results.import_results(self.d,parsed)
        self.assertEqual(results.report(self.d)['experiments'][0]['metrics']['impressions'],1000)

    def test_doctor_never_exposes_token(self):
        with patch.dict(os.environ,{'PINTEREST_ACCESS_TOKEN':'unique-secret-token'}):
            data=adapters.doctor()
        self.assertNotIn('unique-secret-token',json.dumps(data))
        self.assertEqual(data['pinterest_trends']['status'],'unverified')

    def test_cli_from_unrelated_directory(self):
        p=subprocess.run(['python3',str(ROOT/'scripts/pinterest/cli.py'),'doctor'],cwd='/tmp',capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout)['paid_calls'],0)

if __name__=='__main__':unittest.main()
