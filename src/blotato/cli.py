"""The `blotato` command: list -> plan -> approve -> submit.

Only `submit` spends credits. `list`, `show` and `plan` are free and offline;
`balance` and `inspect` are free but hit the API for read-only metadata.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

from . import api, inspect as inspect_mod, runner as br
from .catalog import UnknownModelError, get_model, list_models
from .digest import verify_plan_digest
from .download import DownloadTooLarge
from .studio.plan import build_plan
from .studio.submit import poll, submit
from .workspace import load_env


def _api_key(workspace=None) -> str:
    return br.load_api_key(env=load_env(root=workspace))


def _status(model) -> str:
    if model.broken:
        return "BROKEN"
    return f"verified {model.verified_at}" if model.verified_at else "unverified"


def _cost(model) -> str:
    return f"~{model.observed_credits:g} cr" if model.observed_credits else "cost unknown"


def _media_item(value: str) -> dict:
    return {"url": value} if value.startswith(("http://", "https://")) else {"path": value}


def _coerce_setting(model, name: str, raw: str):
    spec = model.settings.get(name)
    if spec is None:
        known = sorted(model.settings) or "(none)"
        raise SystemExit(f"model '{model.id}' has no setting '{name}'; known: {known}")
    if spec.kind == "boolean":
        if raw.lower() not in {"true", "false"}:
            raise SystemExit(f"setting '{name}' is a boolean; got {raw!r}")
        return raw.lower() == "true"
    if spec.kind == "range":
        try:
            value = float(raw) if "." in raw else int(raw)
        except ValueError:
            raise SystemExit(f"setting '{name}' must be a number; got {raw!r}") from None
        if spec.min is not None and value < spec.min:
            raise SystemExit(f"setting '{name}' must be >= {spec.min}; got {value}")
        if spec.max is not None and value > spec.max:
            raise SystemExit(f"setting '{name}' must be <= {spec.max}; got {value}")
        return value
    if spec.kind == "enum" and spec.values and raw not in spec.values:
        raise SystemExit(f"setting '{name}' must be one of {list(spec.values)}; got {raw!r}")
    return raw


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_list(args) -> int:
    models = list_models(surface=args.surface, include_broken=not args.usable_only)
    if args.json:
        payload = [
            {
                "id": m.id,
                "surface": m.surface,
                "label": m.label,
                "status": _status(m),
                "broken": m.broken,
                "verified_at": m.verified_at,
                "observed_credits": m.observed_credits,
                "roles": {role: list(counts) for role, counts in m.roles.items()},
                "settings": sorted(m.settings),
                "known_issues": list(m.known_issues),
            }
            for m in models
        ]
        print(json.dumps(payload, indent=2))
        return 0
    if not models:
        print("no catalog entries match")
        return 0
    width = max(len(m.id) for m in models)
    for m in models:
        print(f"{m.id:<{width}}  {m.surface:<5}  {_status(m):<18}  {_cost(m):<13}  {m.label}")
    print(f"\n{len(models)} technique(s). `blotato show <id>` for inputs and known issues.")
    return 0


def cmd_show(args) -> int:
    model = get_model(args.model_id)
    print(f"{model.id}  [{model.surface}]  {_status(model)}")
    print(f"  {model.label}")
    print(f"\n{model.description}\n")
    print(f"blotato template id: {model.blotato_template_id}")
    if model.observed_credits:
        print(f"observed cost: {model.observed_credits:g} credits (measured, not a price list)")
    if model.prompt_min_length or model.prompt_max_length:
        print(f"prompt length: {model.prompt_min_length or 0}-{model.prompt_max_length or 'unbounded'} characters")
    print("media roles:")
    for role, (lo, hi) in model.roles.items():
        print(f"  {role}: {lo}-{hi} item(s)")
    if model.settings:
        print("settings:")
        for name, spec in model.settings.items():
            detail = f"kind={spec.kind} default={spec.default!r}"
            if spec.values:
                detail += f" values={list(spec.values)}"
            if spec.min is not None or spec.max is not None:
                detail += f" range=[{spec.min}, {spec.max}]"
            print(f"  {name}: {detail}")
    if model.known_issues:
        print("known issues (observed live, not guessed):")
        for issue in model.known_issues:
            print(f"  - {issue}")
    if model.broken:
        print("\nThis entry is BROKEN. `submit` will refuse it.")
    elif not model.verified_at:
        print("\nNever submitted live. Treat its behavior as unconfirmed.")
    return 0


def cmd_balance(args) -> int:
    credits = api.get_credits(_api_key(args.workspace))
    print(
        json.dumps(
            {
                "creditsRemaining": credits.get("creditsRemaining"),
                "accountEmail": credits.get("accountEmail"),
            },
            indent=2,
        )
    )
    return 0


def cmd_inspect(args) -> int:
    snapshot_dir = inspect_mod.run(workspace=args.workspace)
    summary = json.loads((snapshot_dir / "summary.json").read_text())
    print(json.dumps({"snapshot_dir": str(snapshot_dir), "summary": summary}, indent=2))
    return 0


def cmd_plan(args) -> int:
    model = get_model(args.model)
    media: dict = {}
    for role, values in (("reference", args.reference), ("start", args.start), ("end", args.end)):
        if values:
            media[role] = [_media_item(v) for v in values]
    settings = {}
    for pair in args.setting:
        if "=" not in pair:
            raise SystemExit(f"--setting expects name=value; got {pair!r}")
        name, _, raw = pair.partition("=")
        settings[name] = _coerce_setting(model, name, raw)

    plan = build_plan(
        model_id=args.model,
        prompt=args.prompt,
        media=media,
        settings=settings,
        workspace=args.workspace,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2, sort_keys=True))
    print(f"wrote {out_path}  (no credits spent)")
    print(f"digest {plan['approval_digest']}")
    print(f"\nnext:  blotato approve {out_path} --max-credits <N> --reference <who-approved>")
    return 0


def cmd_approve(args) -> int:
    plan_path = Path(args.plan)
    plan = json.loads(plan_path.read_text())
    verify_plan_digest(plan)
    if args.max_credits <= 0:
        raise SystemExit("--max-credits must be positive")
    if plan.get("broken"):
        raise SystemExit(f"refusing to approve: model {plan['model_id']!r} is marked BROKEN")
    plan["max_credits_ceiling"] = args.max_credits
    plan["approval"] = {
        "reference": args.reference,
        "decided_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    plan_path.write_text(json.dumps(plan, indent=2, sort_keys=True))
    print(f"approved {plan_path} up to {args.max_credits} credit(s)")
    print(f"\nnext:  blotato submit {plan_path}   <- this spends credits")
    return 0


def cmd_submit(args) -> int:
    result = submit(
        Path(args.plan),
        workspace=args.workspace,
        poll_interval=args.poll_interval,
        poll_timeout=args.poll_timeout,
    )
    print(json.dumps(result, indent=2))
    return 0 if result.get("final_status") == "done" else 1


def cmd_poll(args) -> int:
    result = poll(
        Path(args.run_dir),
        workspace=args.workspace,
        poll_interval=args.poll_interval,
        poll_timeout=args.poll_timeout,
    )
    print(json.dumps(result, indent=2))
    return 0 if result.get("final_status") == "done" else 1


def cmd_pinterest(args) -> int:
    from .workflows.pinterest.cli import main as pinterest_main

    return pinterest_main(args.pinterest_args) or 0


# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blotato",
        description=(
            "Generate images and videos through Blotato. Plan for free, approve a "
            "credit ceiling, then submit one bounded call."
        ),
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Directory that relative asset paths and outputs/ resolve against "
        "(default: $BLOTATO_WORKSPACE, else the current directory).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="list catalog techniques (free, offline)")
    p.add_argument("--surface", choices=["image", "video"])
    p.add_argument("--usable-only", action="store_true", help="hide entries known to be broken")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="show one technique's inputs and known issues (free, offline)")
    p.add_argument("model_id")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("balance", help="current credit balance (free, read-only API call)")
    p.set_defaults(func=cmd_balance)

    p = sub.add_parser("inspect", help="snapshot live templates + credits to outputs/ (free)")
    p.set_defaults(func=cmd_inspect)

    p = sub.add_parser("plan", help="build a reviewable plan.json (free, offline)")
    p.add_argument("--model", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument(
        "--reference", action="append", default=[],
        help="local path or https URL (repeatable)",
    )
    p.add_argument("--start", action="append", default=[], help="start-frame media (repeatable)")
    p.add_argument("--end", action="append", default=[], help="end-frame media (repeatable)")
    p.add_argument("--setting", action="append", default=[], metavar="NAME=VALUE")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("approve", help="record a human credit-spend approval on a plan")
    p.add_argument("plan")
    p.add_argument("--max-credits", type=float, required=True)
    p.add_argument("--reference", required=True, help="who approved this and where it is recorded")
    p.set_defaults(func=cmd_approve)

    p = sub.add_parser("submit", help="SPENDS CREDITS: run one approved plan")
    p.add_argument("plan")
    p.add_argument("--poll-interval", type=float, default=5.0)
    p.add_argument("--poll-timeout", type=float, default=240.0)
    p.set_defaults(func=cmd_submit)

    p = sub.add_parser(
        "poll", help="resume an already-paid-for run: finish polling and download its media (free)"
    )
    p.add_argument("run_dir", help="a directory under outputs/blotato-studio-runs/")
    p.add_argument("--poll-interval", type=float, default=5.0)
    p.add_argument("--poll-timeout", type=float, default=240.0)
    p.set_defaults(func=cmd_poll)

    p = sub.add_parser(
        "pinterest", help="local Pinterest research workflow (no publishing, no paid calls)"
    )
    p.add_argument("pinterest_args", nargs=argparse.REMAINDER)
    p.set_defaults(func=cmd_pinterest)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except UnknownModelError as exc:
        print(f"unknown technique: {exc}. `blotato list` shows what exists.", file=sys.stderr)
        return 2
    except br.MissingCredentialError as exc:
        print(f"{exc}. Export it, or put it in <workspace>/.env", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"no such file: {exc.filename}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"not valid JSON: {exc}", file=sys.stderr)
        return 2
    except KeyError as exc:
        print(f"plan is missing the field {exc}; rebuild it with `blotato plan`", file=sys.stderr)
        return 2
    except urllib.error.URLError as exc:
        print(f"network error reaching Blotato: {exc.reason}", file=sys.stderr)
        return 1
    except (api.BlotatoHttpError, DownloadTooLarge, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
