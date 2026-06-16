# Python Project Reference

Use this reference when a scientific Python repository needs practical defaults
for packaging, dependencies, editable installs, and project layout.

## Tool Choice

Prefer one primary toolchain and make it obvious:

- `mamba` or `conda` when the environment must also manage non-Python
  scientific dependencies such as BLAS implementations, MPI stacks, HDF5,
  compiler runtimes, CUDA toolkits, or other binary libraries that are painful
  to treat as out-of-band system prerequisites;
- `uv` for a fast modern default when the repository is open to choosing a
  tool and you want one command path for environments, locking, and installs;
- `pip` plus `venv` when the project is intentionally minimal or already built
  around standard-library tooling;
- `poetry` when the repository already uses it or clearly benefits from its
  workflow and lockfile model.

Avoid keeping multiple equally official workflows unless the repository already
requires them.

For scientific Python, prefer `mamba` first when binary compatibility and
system-library management are part of the real problem rather than an external
deployment detail.

## Core Files

For a package-oriented project, prefer:

- `pyproject.toml` as the main metadata file;
- `environment.yml` when a conda-style environment is the main developer entry
  point;
- `README.md` if the project is user-facing;
- `src/<package_name>/` for importable code;
- `tests/` for automated tests;
- `notebooks/` or `analysis/` for exploratory work;
- `scripts/` only for thin wrappers or operational helpers.

If the project is not meant to be imported as a package, keep it simpler, but
still avoid mixing notebooks, source files, and generated outputs together.

## Suggested Layout

```text
project/
├── environment.yml
├── pyproject.toml
├── src/
│   └── package_name/
├── tests/
├── notebooks/
├── scripts/
└── README.md
```

Use `src/` layout when:

- tests should verify installed-package behavior;
- import bugs from the repository root would otherwise be hidden;
- the repository is intended to be reused as a library or tool.

Flat layouts are acceptable for tiny single-purpose repositories, but they
become fragile sooner.

## pyproject.toml Guidance

Prefer `pyproject.toml` to contain:

- project name and versioning approach;
- runtime dependencies;
- optional dependency groups such as `test`, `dev`, `docs`, or `profile`;
- build backend choice if packaging is required;
- tool configuration only when the repository actually uses those tools.

Keep metadata minimal but correct. Do not add unused tool sections.

If `mamba` or `conda` is the primary environment manager, use
`pyproject.toml` for Python package metadata and editable-install behavior, and
use `environment.yml` for the full environment including non-Python packages.
Do not rely on one file to implicitly replace the other when both concerns
exist.

## Dependencies

Separate concerns clearly:

- runtime dependencies for normal use;
- developer dependencies for linting, typing, tests, docs, or profiling;
- optional heavy scientific dependencies when they are not always required;
- platform-specific dependencies only when unavoidable.

Be explicit when packages influence performance or numerical behavior, not just
import success.

For conda-style workflows, also distinguish:

- packages that belong in `environment.yml` because they are environment-level
  or binary dependencies;
- packages that belong in `pyproject.toml` because they are part of the Python
  package contract;
- packages that may need to appear in both places only if the repository
  intentionally accepts that duplication and documents which file is the source
  of truth.

## Editable Installs

For active development, prefer editable installs over path hacks.

Typical patterns:

Using `mamba`:

```bash
mamba env create -f environment.yml
mamba activate myenv
python -m pip install -e .[test]
```

Or, for an existing environment:

```bash
mamba env update -f environment.yml --prune
python -m pip install -e .[test]
```

Using `uv`:

```bash
uv sync
```

Using `pip` and `venv`:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .[test]
```

Using `poetry`:

```bash
poetry install
```

The exact command may vary with extras, but the principle is the same:
install the project as a project.

For scientific repositories, a practical pattern is:

1. Use `mamba` to solve the environment, including binary and accelerator
   dependencies.
2. Install the local project in editable mode inside that environment.
3. Run tests and notebooks against the installed package, not against the
   repository root by accident.

## Lockfiles and Reproducibility

Use lockfiles when:

- the repository needs consistent developer or CI environments;
- performance, profiling, or numerical behavior is sensitive to versions;
- the project is actively shared across multiple machines.

Do not claim strict environment reproducibility if the repository only declares
loose dependency ranges and no lockfile or export path exists.

For `mamba` or `conda`, prefer a checked-in `environment.yml` at minimum. If
the repository needs stricter reproducibility across machines, add an explicit
export or lock workflow and document how it is generated.

## Tests, Notebooks, and CLI Entry Points

- Keep tests importing package code the same way users do.
- Keep notebooks importing from the package rather than duplicating core logic.
- Keep CLI entry points thin and push logic into reusable modules.
- Avoid burying the only implementation of a workflow inside notebook cells.

## Migration Signals

Consider moving toward a stronger package layout when:

- imports depend on the working directory;
- notebooks contain most of the reusable logic;
- there is no stable place to add tests;
- contributors need setup instructions longer than the project itself;
- dependency breakage is common because environment state is implicit.

## Anti-Patterns

- `requirements.txt` as the only source of truth when the repository is clearly
  a package;
- treating BLAS, MPI, CUDA, or other binary dependencies as undocumented manual
  prerequisites when the environment manager could capture them;
- manually exporting `PYTHONPATH` for normal development;
- putting notebooks inside `src/`;
- broad `pip install ...` instructions with no environment isolation;
- mixing generated data, cached models, and importable modules in one tree.
