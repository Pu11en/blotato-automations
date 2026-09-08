import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.pinterest import adapters, content, research, results
from scripts.pinterest.core import Invalid, read, records, atomic


def main(argv=None):
    parser=argparse.ArgumentParser(description='Pinterest research, original briefs and results. No paid generation or publishing.')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('doctor');p.add_argument('--out')
    p=sub.add_parser('collect');p.add_argument('--run',required=True);p.add_argument('--profile',required=True);p.add_argument('--mode',choices=['manual','live','fixture'],default='manual');p.add_argument('--signals');p.add_argument('--references');p.add_argument('--live',action='store_true')
    p=sub.add_parser('rank');p.add_argument('--run',required=True);p.add_argument('--input',required=True)
    p=sub.add_parser('brief');p.add_argument('--run',required=True);p.add_argument('--input',required=True);p.add_argument('--check-url',action='store_true')
    p=sub.add_parser('review');p.add_argument('--run',required=True);p.add_argument('--brief',required=True);p.add_argument('--input',required=True)
    p=sub.add_parser('export');p.add_argument('--run',required=True);p.add_argument('--brief',required=True);p.add_argument('--check-url',action='store_true')
    p=sub.add_parser('results');r=p.add_subparsers(dest='action',required=True)
    for action in ('register','import','report'):
        a=r.add_parser(action);a.add_argument('--run',required=True)
        if action=='report':a.add_argument('--days',type=int,choices=[7,14,30],default=7)
        else:a.add_argument('--input',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='doctor':
            out=adapters.doctor()
            if args.out:atomic(args.out,out)
        elif args.command=='collect':
            out=research.collect(args.run,args.profile,args.mode,records(args.signals) if args.signals else [],records(args.references) if args.references else [],args.live)
            out={'run':str(Path(args.run).resolve()),'mode':out['mode'],'signals':len(out['signals']),'references':len(out['references']),'sources':out['sources']}
        elif args.command=='rank':out=research.rank(args.run,records(args.input))
        elif args.command=='brief':out=content.package(args.run,read(args.input),args.check_url)
        elif args.command=='review':out=content.review(args.run,args.brief,read(args.input))
        elif args.command=='export':out=content.export(args.run,args.brief,args.check_url)
        elif args.action=='register':out=results.register(args.run,read(args.input))
        elif args.action=='import':out=results.import_results(args.run,records(args.input))
        else:out=results.report(args.run,args.days)
        print(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False))
    except (Invalid, adapters.Unavailable) as e:
        print(str(e),file=sys.stderr);return 2
    except (OSError, ValueError, KeyError, TypeError):
        print('Input or local file unavailable/invalid; check the documented contract.',file=sys.stderr);return 2
    return 0

if __name__=='__main__':
    sys.exit(main())
