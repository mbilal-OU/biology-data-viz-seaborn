# Biological Data Visualization with Seaborn

This site documents a tested collection of statistical visualization patterns
for biology and bioinformatics. The project treats transformations, thresholds,
distance metrics, uncertainty, and biological interpretation as part of the
figure design.

## Start here

- [Advanced gallery](gallery.md)
- [Methods and guardrails](methods.md)
- [Environment setup](setup.md)
- [Repository README](https://github.com/mbilal-OU/biology-data-viz-seaborn#readme)
- [Complete data dictionary](https://github.com/mbilal-OU/biology-data-viz-seaborn/blob/main/data/data_dictionary.md)

## Architecture

1. `scripts/generate_datasets.py` creates deterministic tables with known
   biological and statistical structure.
2. `bioviz/` contains importable plotting and analysis helpers.
3. `notebooks/` connects each method to a biological question and limitation.
4. `scripts/build_advanced_gallery.py` recreates portfolio figures.
5. `tests/` checks rendering, numerical results, schemas, and simulation truth.
6. CI regenerates data, executes notebooks, builds the package, and builds this
   documentation in strict mode.

The data are simulated for reproducible testing. They are not experimental
evidence and should not be used for biological conclusions.
