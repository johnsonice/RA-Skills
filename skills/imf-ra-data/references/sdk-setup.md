# IMF SDK setup during skillset installation

Use this workflow when the user asks to install RA-Skills following its README,
or explicitly asks to configure the IMF SDK. That request includes the checks,
official missing-SDK installation, and missing pandas/openpyxl installation
below; do not ask again for SDK permission. Honor explicit skills-only requests
and host execution restrictions. A standalone lookup or pull request does not
by itself authorize package installation.

## 1. Select an existing Python

The user must install the latest company-provided Python through **Software
Center** first. The official instructions recorded Python 3.11.11 as of June
2026; that is a dated reference, not a permanent version pin. Do not install
Python through another channel or create a virtual/Conda environment.

Check the current interpreter:

```cmd
python -c "import sys; print(sys.executable); print(sys.version)"
```

If `python` is unavailable, inspect existing interpreter discovery mechanisms
(e.g. `where.exe python`, `py -0p`, or the editor's selected Python) before
concluding Python is absent. Ignore Store launcher aliases that do not execute
Python. Prefer the existing IMF-configured interpreter; reuse an already working
SDK environment. Do not scan the whole disk or change global PATH. If Python is
absent, complete skill-file installation and tell the user to install Python
from Software Center and reopen the terminal/editor, then resume these steps.

Use the resolved executable for **all** checks, installation, and fetch commands.
The examples use `python` as shorthand. For a path containing spaces, use
`"C:\path to\python.exe" ...` in cmd or `& "C:\path to\python.exe" ...` in
PowerShell. Do not switch interpreters between installation and verification.

## 2. Check before installing

Run the standard-library environment checker from the installed skill:

```cmd
python "<DATA_SKILL>/scripts/check_environment.py" --profile data
```

Substitute the installed directory and selected interpreter using the
[shared runtime contract](../../imf-ra/references/runtime.md). It probes each
module in a separate bounded process, distinguishing missing modules, broken
imports, and timeouts. It also reports the executable, SDK location, official
installer availability, and Haver file status. Exit 1 is a diagnostic result,
not a reason to install everything. `python_ready` covers imports only; live
access and Haver metadata schema are not verified by this check.

If the SDK checks work, skip the SDK installer. If an import fails because of a
missing dependency or another runtime error, preserve the actual exception and
diagnose it; do not classify every import exception as an absent SDK. Check a
known existing configured interpreter before installing anything.

## 3. Install only what is missing

On an IMF-managed Windows machine, check that this official network-share file
is readable before executing it:

```text
\\ecnswn12p\ems_shared\pub\datatools\installer.py
```

When the SDK itself is absent, run the official **stable** installer with the
selected interpreter:

```cmd
python \\ecnswn12p\ems_shared\pub\datatools\installer.py
```

Do **not** append `dev`. The official documentation says this same command also
updates an installed library, so do not run it on a working SDK merely to obtain
the latest version. Do not attempt `pip install imf_datatools` or copy the SDK
from an unofficial source. The official installer manages its SDK dependencies;
do not add a broad upgrade step. An existing broken SDK is a repair case: report
the diagnostic rather than silently reinstalling/upgrading it.

After the SDK step, recheck pandas and openpyxl. If either is still absent, install
only the absent package(s) with this same interpreter's pip, for example:

```cmd
python -m pip install pandas
python -m pip install openpyxl
```

Execute each example only when that package is missing. These two packages cover
basic data handling and Excel output; no chart, Plotly, Dealogic, or full
`requirements.txt` installation is part of this SDK setup. Do not use `--upgrade`,
`--break-system-packages`, administrator escalation, or a new environment to
work around an installation failure. If pip is unavailable or provisioning is
blocked, report the exact blocker for IMF IT. Do not loop the installer after a
failure; retry only after identifying and correcting a concrete cause.

Outside supported IMF Windows/network access, finish the skill installation and
report SDK setup as blocked unless an existing SDK already passes the checks.
A network or permissions failure is not a reason to create an environment.

## 4. Verify and hand off

Repeat the checker from step 2 with `--output` pointing to the user-local
readiness report described in the runtime contract, using the same executable.
Then run both installed helpers with `--help` (resolve paths from the installed
`imf-ra-data` directory, not an assumed repository working directory):

```cmd
python "<DATA_SKILL>/scripts/fetch_idata.py" --help
python "<DATA_SKILL>/scripts/fetch_haver.py" --help
```

These are local runtime checks, not proof of data access. Do not fetch arbitrary
series merely to test installation. If the user supplied a data request too,
continue through the normal catalog/data workflow and validate that actual pull.

Haver additionally needs a readable `haver.db`: honor `HAVER_DB_PATH` first,
otherwise use the helpers' ancestor-path discovery. If its location is already
known, carry it into the fetch process; do not guess a path or claim Haver-ready
when it is missing. The SDK installer does not supply this database or grant
iData/Haver permissions.

Finish with a short status containing:

- Skills installed and any host reload needed.
- Verified Python executable and SDK location; installed now or reused.
- SDK/data/Excel import and helper checks: passed or specific failure.
- Network/data access: verified by an actual requested pull, or not tested.
- Haver metadata path: available, missing, or not checked.

Save the readiness report during installation and use its verified interpreter
for subsequent pulls, subject to explicit user/workspace overrides in the
runtime contract. If a stored path is stale, rediscover an existing interpreter
and recheck; do not reinstall just because the conversation context was lost.

## Source

Official IMF datatools documentation, section 2.1.1, “Python Library
Installation,” supplied by the project owner (June 2026 version note):
[IMF datatools documentation](https://intlmonetaryfund.sharepoint.com/sites/fw-datatools/DatatoolsDocuments/imf_datatools_doc.aspx).
