---
name: scientific-data-analysis-and-visualization
description: Analyze and visualize scientific results in a defensible,
  reproducible, mostly language-agnostic way, including summaries, figures,
  uncertainty, comparisons, and artifact provenance.
---

# Scientific Data Analysis And Visualization

Use this skill when turning scientific outputs, benchmark results, simulation
data, measurements, or validation results into tables, figures, summaries, or
decision-relevant analysis.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- choosing analyses and visualizations that match the scientific question;
- preserving provenance from raw data to derived figures and tables;
- showing uncertainty, variability, and comparison baselines honestly;
- making analysis scripts rerunnable and reviewable;
- avoiding misleading plots, aggregations, and statistical summaries.

## When To Use

Use this skill when:

- benchmark, profiling, simulation, experiment, or validation outputs need to
  be summarized;
- results need figures, tables, or comparison reports;
- the user asks what a dataset or result set shows;
- uncertainty, variance, scaling, or outliers affect interpretation;
- analysis code or plotting workflows need cleanup.

This skill is mostly programming-language and framework agnostic. Use the
repository's existing analysis stack when it is already clear and working.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the scientific question before choosing a plot or statistic.
3. Inspect data provenance, units, dimensions, and missing-value behavior.
4. Separate raw data, cleaned data, derived summaries, and generated figures.
5. Prefer reproducible scripts or notebooks that can be rerun from documented
   inputs.
6. State what was analyzed, what was visualized, and what interpretation limits
   remain.

Do not optimize for decorative plots before the comparison, uncertainty, and
scientific claim are clear.

## Language and Framework Position

Prefer repository-native tools:

- Python projects may use Matplotlib, Seaborn, Plotly, Altair, pandas, Polars,
  NumPy, xarray, or domain-specific libraries;
- R projects may use ggplot2, tidyverse, data.table, lattice, or base graphics;
- Julia projects may use Makie, Plots, Gadfly, AlgebraOfGraphics, DataFrames,
  or domain-specific plotting tools;
- command-line workflows may produce CSV, JSON, Parquet, NetCDF, HDF5, images,
  or Markdown/HTML reports.

Do not migrate plotting frameworks only for preference. Change tools only when
the current stack cannot represent the analysis clearly, reproducibly, or
maintainably.

## Analysis Design

- Start from the comparison or claim the user needs to support.
- Preserve units and scales through every derived table.
- Keep filtering, grouping, normalization, and aggregation explicit.
- Check missing data, failed runs, censored values, and outliers before
  plotting.
- Compare like with like: same inputs, hardware context, compiler settings,
  seeds, versions, or data preprocessing where relevant.
- Keep raw measurements available when summaries could hide important
  variability.

A figure should answer a question, not merely display available columns.

## Visualization Choices

Prefer:

- line plots for ordered trends, scaling curves, convergence, or time series;
- scatter plots for relationships and outliers;
- bar charts for a small number of categorical comparisons;
- box, violin, or interval plots for distributions and variability;
- heatmaps for dense matrix-like comparisons;
- small multiples when comparisons share scales and structure;
- tables when exact values matter more than visual pattern detection.

Avoid:

- 3D plots unless the third dimension is genuinely useful;
- dual axes unless the relationship is unambiguous and clearly labeled;
- truncated axes that exaggerate differences without disclosure;
- pie charts for scientific comparison work;
- excessive smoothing that hides data or implies unsupported continuity.

## Uncertainty and Variability

- Show uncertainty when measurements or stochastic results vary.
- Report sample size, repeats, and aggregation method.
- Distinguish standard deviation, standard error, confidence intervals, and
  quantile intervals.
- For benchmarks, report runtime variability and avoid overinterpreting tiny
  differences.
- For stochastic workflows, show seed behavior or distributional summaries when
  one run is not representative.

If uncertainty is unknown, say so explicitly instead of implying precision.

## Benchmark and Scaling Results

For performance results:

- include baseline runtime and speedup where relevant;
- show parallel efficiency when comparing thread or rank counts;
- record hardware, compiler, runtime, affinity, and input size context;
- separate warmup, failed, and timed runs;
- avoid comparing debug builds with optimized builds unless that is the point;
- include correctness checks that make timed cases comparable.

Use `scientific-cli-benchmark` for timing collection and
`scientific-profiling` for bottleneck diagnosis.

## Reproducible Analysis Artifacts

- Keep analysis scripts under version control.
- Keep generated figures and tables in documented output locations.
- Avoid committing generated plots unless they are part of the repository's
  documentation or release contract.
- Make figure generation deterministic when practical.
- Record input data paths, filters, parameters, environment, and code version
  when figures support a public claim.
- Prefer one obvious command to regenerate important figures or reports.

Use `scientific-reproducibility` when run metadata or provenance capture needs
implementation work.

## Notebooks

- Keep notebooks as reviewable analysis artifacts, not the only home of core
  logic.
- Factor reusable data loading, cleaning, and plotting helpers into scripts or
  modules when they are shared.
- Strip or control outputs when notebook output churn would obscure review.
- Provide a tiny input or cached summary for notebook smoke execution when
  notebooks are part of the project contract.

Use `scientific-notebook-workflows` if that skill is added later.

## Reporting

When producing a result summary:

- lead with the answer or main pattern;
- state the data source, filters, and comparison baseline;
- include enough numbers to verify the visual impression;
- distinguish observation from interpretation;
- call out caveats, missing data, and untested explanations;
- include commands or scripts needed to regenerate the result.

Figures and tables should make the conclusion easier to audit, not harder.

## Validation Defaults

- Re-run the analysis script or smallest representative analysis when
  practical.
- Check figure files or tables were regenerated where expected.
- Inspect at least one generated figure or summary for axis labels, units,
  legends, scales, and missing context.
- Verify that ignored/generated artifacts are handled intentionally.
- If data are too large to analyze fully, use a documented subset and state the
  limitation.

## Anti-Patterns

- choosing a chart before defining the scientific question;
- plotting only averages when variability determines the conclusion;
- hiding failed runs or missing data without explanation;
- comparing results from different environments without recording context;
- committing large generated figures or tables without a release reason;
- using notebook-only workflows that cannot be rerun;
- overclaiming causality from descriptive plots.

## Output Expectations

When using this skill, briefly note:

- which data, filters, comparisons, and units were used;
- which scripts, figures, tables, or reports were added or changed;
- how uncertainty, variability, outliers, and failed runs were handled;
- which regeneration or validation commands were run;
- what interpretation limits remain.
