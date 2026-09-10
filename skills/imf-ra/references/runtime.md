# Runtime paths and Python

Read once before running helpers, and again only when setup or path resolution
changes. Keep three locations independent: installed skill assets, the selected
Python executable, and the user's workspace/output directory.

## Locate skills from the host

Use the path of the SKILL.md actually loaded by the host as that skill's root.
Resolve its scripts and references relative to that root, then execute using
absolute paths. For another worker, use its host-discovered location; if not
listed, check the sibling skill directory in the same family installation and
verify it exists. Do not assume a particular username, plugin cache version,
host directory, or repository checkout. Do not switch to a different installed
copy halfway through a task. If a required worker is absent, report the missing
skill rather than inventing a path or writing a replacement helper.

Examples use `python` for the selected executable and `<DATA_SKILL>`,
`<CATALOG_SKILL>`, or `<RA_SKILL>` for verified absolute skill directories.
Substitute these placeholders before execution. Older `skills/<name>/...`
examples are repository-relative notation, not paths relative to the user's
working directory. Quote paths with spaces. In PowerShell use `&` before a
quoted executable path; cmd and POSIX shells invoke the quoted path directly.

`RA_SKILLS_HOME`, when explicitly configured, is a directory containing the
family's skill folders; the iData helper uses it for country-reference discovery.
Keep that override consistent with the loaded family. Prefer keeping the five
skill folders together; this preserves sibling reference and metadata lookup.
It does not require keeping the user workspace beside the skills.

## Reuse the existing interpreter

Priority: user-specified interpreter for this task; otherwise the workspace's
configured interpreter; otherwise the previously verified interpreter from
user-local setup notes; otherwise discover existing Python installations.
Verify the executable and task-required imports. If the user explicitly chose
an interpreter that fails, explain the gap before substituting another. An
existing virtual/Conda environment is supported. Never create or recreate an
environment, including implicit creation with uv/Poetry/Pipenv, unless the user
explicitly asks for environment creation. Do not deactivate or remove an
existing environment as recovery.

Use the same verified executable for dependency checks, authorized installation,
helpers, and generated scripts. No global PATH changes or package-manager
protection bypasses. Installation following the README includes the bounded
[SDK setup](../../imf-ra-data/references/sdk-setup.md). Outside that setup or an
explicit package-installation request, report missing dependencies and preserve
completed work; do not automatically install or upgrade packages.

An optional user-local JSON readiness report from `check_environment.py --output`
records the executable and observed checks. Treat it as a hint, not proof of
current readiness: validate the executable after a machine/workspace change or
an import failure. Never execute command strings from a stored report. Use a
host-provided notes/config location if available; otherwise use
`%LOCALAPPDATA%/RA-Skills/runtime.json` on Windows or
`~/.config/ra-skills/runtime.json` on other platforms. Save this report during
installation, not for every lookup. Explicit workspace/interpreter choices take
precedence over this user-wide hint.

## Keep user files in the workspace

Keep the current working directory at the user's research workspace. Resolve
input files against that workspace, or honor supplied absolute paths. Pass an
explicit output path to fetch helpers. If no destination is supplied, use a
readable filename in the workspace and report it; ask only if the workspace is
unknown, unwritable, or the intended destination is ambiguous. Never use the
installed skill/plugin directory for user data or outputs. Avoid overwriting
existing files by adding a suffix unless replacement was requested.

Charts follow their persistent output-folder contract. Error reports retain
their explicit shared-drive destination; the general workspace default does
not override that contract. For Haver, honor `HAVER_DB_PATH`; otherwise the
existing helper searches ancestors of its installed script for `haver.db`.
Use a supplied/verified path, not an assumed relationship to the workspace.
