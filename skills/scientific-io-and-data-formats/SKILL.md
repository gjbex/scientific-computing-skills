---
name: scientific-io-and-data-formats
description: Design and maintain I/O paths and data formats for
  scientific-computing and HPC software, especially when file layout, metadata,
  checkpointing, large arrays, portability, reproducibility, and I/O
  performance all matter together.
---

# Scientific I/O And Data Formats

Use this skill when editing or reviewing scientific, numerical, or parallel
software where data layout, file formats, metadata, or checkpoint behavior
materially affect correctness, performance, or reproducibility.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- choosing data representations that fit the workload and lifecycle;
- organizing scientific outputs so they are interpretable and reproducible;
- balancing portable formats against throughput and storage efficiency;
- treating I/O as part of the computation pipeline rather than an afterthought.

## When To Use

Use this skill when:

- the user asks to add or revise scientific file formats or I/O logic;
- outputs include large arrays, checkpoints, grids, timeseries, or tabular data;
- metadata, provenance, or schema clarity is missing;
- I/O throughput or storage overhead is affecting performance;
- the repository needs clearer conventions for reading, writing, or validating
  scientific artifacts.

Do not use this skill to replace domain-specific data standards that the
repository is already committed to.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the data's purpose: transient, checkpoint, analysis, interchange,
   or published result.
3. Match the format choice to access pattern, size, and portability needs.
4. Keep scientific values and provenance metadata equally deliberate.
5. Prefer explicit schemas and versioning when formats may evolve.
6. State what is optimized for: readability, portability, throughput, storage,
   restart safety, or interoperability.

Prefer extending existing repository conventions unless they are clearly causing
correctness, performance, or maintenance problems.

## Format Selection

Choose formats based on workload characteristics:

- plain text or CSV for small, human-inspectable tabular outputs;
- JSON, YAML, or TOML for structured metadata and configuration;
- binary array-oriented formats for large numerical data where throughput and
  space matter;
- HDF5 or NetCDF-style containers when arrays, dimensions, metadata, and
  grouping should live together;
- checkpoint-specific layouts when restart speed and robustness matter more than
  human readability.

Do not default to text for large numerical outputs that will be expensive to
  parse, store, or compare.

## Metadata and Provenance

- Record units, dimensions, coordinate conventions, and field meanings.
- Store enough provenance to interpret or rerun the workflow later.
- Keep metadata close to the data it describes when practical.
- Prefer explicit names over positional assumptions.
- Version schemas or file-layout conventions when future changes are likely.

If results depend on toolchain, precision mode, mesh setup, seed, or runtime
configuration, capture that metadata somewhere stable.

## Large Arrays and Layout

- Match array layout to expected access patterns.
- Avoid unnecessary copies or format conversions in hot paths.
- Distinguish row-major versus column-major assumptions clearly.
- Be explicit about shape, strides, endianness, and precision when using custom
  binary formats.
- Prefer chunking or tiling strategies only when the read/write pattern justifies
  the added complexity.

For large outputs, format decisions affect not just disk usage but also cache
behavior, memory pressure, and downstream analysis speed.

## Checkpointing

- Make checkpoints restartable, not merely inspectable.
- Prefer atomic or failure-aware write patterns when partial files are risky.
- Separate durable checkpoints from lightweight logs or previews.
- Include enough metadata to reject incompatible restarts cleanly.
- Document whether checkpoints are portable across versions, machines, or
  precisions.

Checkpoint format stability matters for long-running scientific workflows.

## Performance Considerations

- Treat I/O time as part of end-to-end performance for realistic workloads.
- Avoid writing more precision or more frequency than the use case needs.
- Separate performance-critical write paths from rich analysis exports when both
  are needed.
- Measure whether text conversion, compression, or frequent flushes dominate the
  cost.
- Consider batching, buffering, or reduced output frequency before redesigning
  the whole format.

For parallel codes, distinguish local write cost, global coordination cost, and
filesystem behavior.

## Parallel and HPC Context

- Be explicit about whether output is per-rank, aggregated, or postprocessed.
- Avoid hidden assumptions that only work at one rank count.
- Record decomposition or global shape information when needed to reconstruct
  distributed data.
- Treat shared-filesystem contention as a design concern, not just a runtime
  annoyance.
- Prefer restart and output schemes that degrade gracefully at larger scale.

What works on a laptop may fail badly on a shared cluster filesystem.

## Validation and Schema Discipline

- Validate file structure and metadata, not just file existence.
- Add lightweight readers or smoke tests for important formats.
- Prefer backward-compatible evolution when old artifacts must remain useful.
- Fail clearly on malformed, truncated, or version-incompatible files.
- If a custom format is used, document the schema close to the code.

Treat readers and writers as part of the software interface.

## Anti-Patterns

- large text dumps with no schema or units;
- binary blobs with undocumented layout;
- outputs that cannot be traced back to parameters or input data;
- checkpoint files that are not safe against partial writes;
- format choices driven only by convenience of first implementation;
- rewriting all data through expensive conversions in performance-critical paths.

## Validation Defaults

- Run at least one round-trip or read-after-write check for important formats.
- Verify that metadata is sufficient to interpret the stored values.
- State what was validated for structure, restartability, or compatibility.
- If performance motivated the change, record what aspect of I/O cost was
  targeted.
- State explicitly what could not be tested in the current environment.

## Output Expectations

When using this skill, briefly note:

- which data formats or I/O paths were added or changed;
- what metadata or schema assumptions were introduced or preserved;
- whether the design prioritizes readability, portability, throughput, restart
  safety, or interoperability;
- which read/write or round-trip validations were run;
- which performance or reproducibility risks remain.
