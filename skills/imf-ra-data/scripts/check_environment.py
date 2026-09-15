#!/usr/bin/env python3
"""Inspect the current Python for RA work; never install, fetch, or create an env.

Uses stdlib only. Imports run in bounded child processes so one broken SDK
module does not hide other results. Exit 0 means the requested Python profile
passed, 1 means missing/broken dependencies, 2 is a CLI/report-write error.
Haver file availability and live network access are reported separately.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

PROFILES = {
    "catalog": (),
    "data": ("imf_datatools", "imf_datatools.idata_utilities",
             "imf_datatools.haver_utilities", "pandas", "openpyxl"),
    "charts": ("pandas", "matplotlib"),
}
INSTALLER = r"\\ecnswn12p\ems_shared\pub\datatools\installer.py"
_MARKER = "RA_ENV_RESULT:"
_PROBE = '''import importlib, json, sys
try:
    module = importlib.import_module(sys.argv[1])
    result = {"status": "ok", "location": getattr(module, "__file__", None),
              "version": str(getattr(module, "__version__", "unknown"))}
except ModuleNotFoundError as exc:
    target = sys.argv[1]
    missing_target = exc.name == target or target.startswith(str(exc.name) + ".")
    result = {"status": "missing" if missing_target else "broken",
              "missing_module": exc.name, "error": str(exc)[:2000]}
except Exception as exc:
    result = {"status": "broken", "error": type(exc).__name__ + ": " + str(exc)[:2000]}
print("RA_ENV_RESULT:" + json.dumps(result))
'''


def probe_module(name: str, timeout: float) -> dict:
    try:
        proc = subprocess.run([sys.executable, "-c", _PROBE, name],
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "timeout_seconds": timeout}
    except OSError as exc:
        return {"status": "broken", "error": str(exc)}
    for line in reversed(proc.stdout.splitlines()):
        if line.startswith(_MARKER):
            try:
                result = json.loads(line[len(_MARKER):])
            except json.JSONDecodeError:
                break
            if proc.returncode == 0:
                return result
            break
    return {"status": "broken", "exit_code": proc.returncode,
            "error": proc.stderr[-2000:] or "Import subprocess returned no valid result"}


def haver_status() -> dict:
    explicit = os.environ.get("HAVER_DB_PATH")
    if explicit:
        path = Path(explicit).expanduser()
        source = "HAVER_DB_PATH"
    else:
        path = next((parent / "haver.db" for parent in Path(__file__).resolve().parents
                     if (parent / "haver.db").exists()), None)
        source = "script_ancestors"
    if path is None:
        return {"status": "missing", "source": source, "path": None}
    try:
        with path.open("rb") as stream:
            header = stream.read(16)
        status = "readable_sqlite_file" if header == b"SQLite format 3\x00" else "invalid_header"
    except OSError as exc:
        return {"status": "unavailable", "source": source,
                "path": str(path.absolute()), "error": str(exc)}
    return {"status": status, "source": source, "path": str(path.absolute()),
            "schema_verified": False}


def inspect_environment(profile: str, timeout: float) -> dict:
    modules = {name: probe_module(name, timeout) for name in PROFILES[profile]}
    # The managed workstation Python is provisioned through Software Center.
    minimum = (3, 9)
    supported = sys.version_info[:2] >= minimum
    report = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "python": {"executable": sys.executable, "version": sys.version,
                   "minimum_version": ".".join(map(str, minimum)),
                   "supported": supported},
        "data_skill_directory": str(Path(__file__).resolve().parents[1]),
        "modules": modules,
        "python_ready": supported and all(r["status"] == "ok" for r in modules.values()),
        "live_data_access": "not_tested",
    }
    if profile == "data":
        report["haver_metadata"] = haver_status()
        report["stable_installer"] = {
            "path": INSTALLER,
            "readable": os.name == "nt" and os.path.isfile(INSTALLER) and os.access(INSTALLER, os.R_OK),
        }
    return report


def write_report(path: Path, report: dict) -> None:
    path = path.expanduser().absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=path.name + ".", suffix=".tmp",
                                         delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=PROFILES, default="data")
    parser.add_argument("--timeout", type=float, default=15,
                        help="Maximum seconds per module import (default 15)")
    parser.add_argument("--output", type=Path,
                        help="Optional user-local readiness JSON; no file written by default")
    args = parser.parse_args()
    if not 0 < args.timeout <= 60:
        parser.error("--timeout must be greater than 0 and at most 60")
    report = inspect_environment(args.profile, args.timeout)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.output:
        try:
            write_report(args.output, report)
        except OSError as exc:
            print(f"Could not save readiness report: {exc}", file=sys.stderr)
            return 2
    return 0 if report["python_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
