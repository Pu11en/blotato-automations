"""Reproducible offline acceptance run; synthetic evidence and results are explicit."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.pinterest.core import ROOT, read, atomic
from scripts.pinterest import research, content, results


def run(out):
    f=ROOT/'tests/pinterest/fixtures'
    research.collect(out,f/'profile.json','fixture',read(f/'signals.json'),read(f/'references.json'))
    research.rank(out,read(f/'assessments.json'))
    for path in sorted(f.glob('*-brief.json')):
        pack=content.package(out,read(path))
        content.export(out,pack['experiment_id']+'-v1')
    for i,fmt in enumerate(('static','video')):
        results.register(out,{'asset_id':'harvest-flecks-'+fmt+'-v1','pin_url':'https://www.pinterest.com/pin/'+str(900000000000000001+i)+'/',
                         'published_date':'2026-08-01','account_id':'fixture-pinterest','authorization_reference':'SYNTHETIC fixture registration, no actual publication'})
    rows=read(f/'results.json');results.import_results(out,rows)
    repeated=results.import_results(out,rows)
    report=results.report(out)
    evidence={'mode':'fixture','briefs':3,'variants_per_brief':2,'repeated_import':repeated['status'],
              'paid_calls':0,'publish_calls':0,'report':str(Path(out)/'results-7d.md')}
    atomic(Path(out)/'acceptance.json',evidence)
    return evidence

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True)
    print(json.dumps(run(p.parse_args().out),indent=2))
