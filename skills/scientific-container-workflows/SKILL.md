---
name: scientific-container-workflows
description: Design and maintain scientific container workflows, preferring
  Apptainer/Singularity for HPC runtime use and Docker or Podman for local
  image development when appropriate.
---

# Scientific Container Workflows

Use this skill when a scientific project needs containerized environments for
portable builds, reproducible runs, workflow execution, or HPC deployment.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- choosing when containers are the right reproducibility mechanism;
- using Apptainer or Singularity as the preferred HPC runtime format;
- using Docker or Podman locally when convenient for development or CI;
- keeping container recipes reproducible and reviewable;
- documenting what remains outside the container boundary.

## When To Use

Use this skill when:

- dependencies include compilers, MPI, CUDA, BLAS/LAPACK, HDF5, NetCDF,
  Python/R/Julia stacks, or system libraries;
- local and HPC environments need a shared runtime contract;
- a Nextflow or other scientific workflow should run in containers;
- container recipes or images have drifted from documented usage;
- a project needs smoke tests for a containerized workflow.

Do not use this skill to replace language-level package management for simple
projects. Use `scientific-package-management` when a normal Python, R, or Julia
environment is enough.

## Default Position

Prefer Apptainer or Singularity for scientific and HPC runtime environments.
They fit shared clusters, unprivileged execution, scheduler workflows, and site
filesystem constraints better than Docker on compute nodes.

Use Docker or Podman locally for image development, dependency debugging, or CI
builds when that is the practical path. Make the HPC runtime contract explicit
through Apptainer or Singularity.

Do not assume Docker is available on HPC compute nodes.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify whether the container is for development, CI, workflow execution,
   release reproducibility, or HPC runtime use.
3. Find the source of truth: `Apptainer.def`, an HPCCM recipe, Dockerfile, OCI
   image reference, or documented external image.
4. Keep image recipes version-controlled; keep large built images out of Git.
5. Add or run a tiny smoke test that exercises the intended runtime path.
6. State what is inside the image and what still depends on the host system.

Prefer improving an existing container path over introducing a second competing
container workflow.

## Recommended Layout

For a single image:

```text
containers/
  container.py
  container.def
  README.md
```

For multiple images:

```text
containers/
  hpccm/
    runtime.py
    build.py
  apptainer/
    runtime.def
    build.def
  README.md
```

Use different names if the repository already has a clear convention. Keep the
source-of-truth recipe and generated definition file close enough that drift is
obvious in review.

## Apptainer and Singularity

- Prefer checked-in definition files or documented OCI sources over
  undocumented `.sif` images.
- Build images from reproducible recipes when practical.
- Keep `.sif` files out of Git unless there is an exceptional, documented
  reason.
- Bind project, data, scratch, and output paths explicitly.
- Avoid assuming writable container filesystems at runtime.
- Document required host modules, drivers, filesystems, and scheduler behavior.

Apptainer improves runtime portability, but it does not eliminate all host
coupling.

## Docker and Podman

- Use Docker or Podman as local build and debugging tools when useful.
- Keep Dockerfiles or OCI image references pinned enough for reproducibility.
- Avoid unpinned `latest` tags for public or archival workflows.
- Document how local images become Apptainer-compatible images when HPC runtime
  matters.
- Do not design the public workflow around Docker-only runtime assumptions if
  the intended users run on shared clusters.

Local container convenience should not obscure the HPC execution contract.

## HPCCM-Generated Definition Files

Prefer HPCCM for non-trivial Apptainer or Singularity definition files,
especially when the container includes compilers, MPI, CUDA, math libraries,
Python/R/Julia, or multi-stage build logic.

Treat HPCCM Python recipes as the source of truth. Regenerate the `.def` file
every time the `.py` recipe changes. Do not hand-edit generated `.def` files
unless the change is immediately backported into the HPCCM recipe.

Typical generation command:

```bash
python3 containers/container.py --format singularity > containers/container.def
```

For recipe variants:

```bash
python3 containers/container.py \
  --format singularity \
  --cuda-version 12.4 \
  --mpi openmpi \
  > containers/container.def
```

Freshness check for CI or local review:

```bash
python3 containers/container.py --format singularity > /tmp/container.def
diff -u containers/container.def /tmp/container.def
```

For multiple recipes:

```bash
for recipe in containers/hpccm/*.py; do
  name=$(basename "$recipe" .py)
  python3 "$recipe" --format singularity > "/tmp/$name.def"
  diff -u "containers/apptainer/$name.def" "/tmp/$name.def"
done
```

Pin the HPCCM version when exact generated output stability matters. If an
HPCCM upgrade changes generated definitions, treat the `.def` diff as a
reviewed generated-file update.

## Dependencies and Host Coupling

- Document compiler, MPI, CUDA, BLAS/LAPACK, HDF5, NetCDF, and language runtime
  assumptions clearly.
- For GPU images, document host driver and container runtime requirements.
- For MPI images, state whether MPI is fully inside the image or coupled to the
  host MPI stack.
- For Python/R/Julia stacks, keep language dependencies reproducible inside the
  image or clearly delegated to project package metadata.
- Do not hide required host modules or bind mounts in one user's job script.

GPU and MPI containers are often host-coupled. Document that coupling rather
than pretending the image is fully portable.

## Workflow Integration

- For Nextflow workflows, keep Apptainer/Singularity settings in profiles or
  config files, not scattered across shell snippets.
- Align container names, tags, and paths with workflow parameters.
- Keep tiny input smoke tests available for validating image and workflow
  integration together.
- Record the image URI, digest, SIF path, or definition-file commit when results
  must be reproducible.

Container guidance should reinforce `scientific-workflow-automation` and
`scientific-reproducibility`, not replace them.

## Validation Defaults

- Regenerate `.def` files from HPCCM recipes before building or submitting jobs.
- Build the image when practical, or state clearly why build validation was not
  possible.
- Run a smoke test from the image: version checks, imports, executable startup,
  or one tiny workflow example.
- Verify `.gitignore` excludes `.sif`, work directories, caches, and generated
  outputs unless there is a deliberate exception.
- For HPC-bound images, validate the job script or workflow profile separately
  from the image build.

Do not treat a successful container build as proof that the scientific workflow
is correct.

## Anti-Patterns

- committing large `.sif` images to source control;
- building containers interactively with no recipe;
- assuming Docker is available on HPC compute nodes;
- relying on unpinned `latest` images for reproducible workflows;
- hiding required host modules, GPU drivers, or MPI coupling;
- mixing build caches, datasets, and durable results into the image;
- hand-editing generated `.def` files without updating the HPCCM recipe;
- treating a container as a substitute for tests.

## Output Expectations

When using this skill, briefly note:

- which recipe, definition file, image, or workflow profile was changed;
- whether Apptainer/Singularity, Docker, Podman, or HPCCM is the source of
  truth;
- which `.def` regeneration, image build, or smoke test was run;
- what remains host-specific, HPC-specific, or untested.
