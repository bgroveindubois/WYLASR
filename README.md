# WYLASR

**Open-source experimental electromagnetic multispectral sensing using
spatial arrays of planar bifilar coils.**

WYLASR is an open-source experimental electromagnetic sensing project.

The project investigates whether spatial arrays of planar bifilar coils
can produce repeatable, frequency-dependent electromagnetic measurements
that can be converted into spatially registered datasets and imagery.

WYLASR is an experimental research platform. It does not assume in
advance what materials, structures, or phenomena the sensor will be
capable of distinguishing. The objective is to characterize the physical
response of the hardware, preserve the raw measurements, establish
repeatable calibration procedures, and determine experimentally what
information can be extracted from those measurements.


## Inspiration and Prior Work

### ESPARGOS

A major inspiration for WYLASR is the **ESPARGOS** project and its work
with low-cost, spatially distributed, phase-synchronous antenna arrays.

ESPARGOS demonstrates how multiple inexpensive sensing elements can be
combined into larger spatial arrays, calibrated, synchronized, and used
to collect multidimensional measurements for subsequent spatial signal
processing.

Of particular importance to the development of the WYLASR concept was
the ESPARGOS work on **combined and distributed arrays**. ESPARGOS
demonstrates that multiple physical sub-arrays can be treated as a
larger measurement system when their geometry, synchronization, and
calibration are properly characterized.

The ESPARGOS project helped establish the practical feasibility of
several concepts that influenced the development of WYLASR:

- constructing spatial sensing systems from many relatively inexpensive
  sensing elements,
- combining physical sub-arrays into larger measurement geometries,
- preserving the spatial location of individual measurements,
- calibrating differences between sensing elements,
- collecting multidimensional measurement datasets,
- examining amplitude, phase, frequency, and spatial information, and
- applying computational processing to extract information that may not
  be apparent from an individual sensing element.

WYLASR explores these general concepts using a substantially different
physical sensing architecture.

ESPARGOS operates as a Wi-Fi channel sounder using phase-synchronous
antenna arrays and Channel State Information (CSI). WYLASR instead
investigates planar bifilar inductive structures operating at much lower
frequencies and examines their electrical and electromagnetic responses
to excitation, geometry, nearby materials, core materials, and spatial
position.

Accordingly, ESPARGOS should not be interpreted as validation of the
WYLASR sensing mechanism. Rather, it is acknowledged as important prior
work and a major inspiration for the distributed-array, calibration,
data-acquisition, and spatial-processing concepts being explored by
WYLASR.

ESPARGOS project:

https://espargos.net/

ESPARGOS phase-coherent combined-array documentation:

https://espargos.net/docs/combined-arrays.html

ESPARGOS Python client and processing software (`pyespargos`):

https://github.com/ESPARGOS/pyespargos


## WYLASR V1

The first hardware revision uses an 8 × 8 array of 64 planar bifilar
coil cells.

The initial goals are to:

- characterize the passive response of individual cells,
- characterize the full 64-cell array,
- measure repeatability and cell-to-cell variation,
- experiment with multiple electromagnetic response channels,
- convert array measurements into spatially registered datasets and
  images,
- preserve raw measurements for later analysis and machine learning,
- investigate stacked and three-dimensional sensor configurations, and
- explore whether different materials, geometries, depths, excitation
  conditions, and electromagnetic environments produce repeatable and
  distinguishable responses.

WYLASR V1 is deliberately intended as a baseline experimental platform.
More complex electrical configurations can be introduced after the
behavior of the basic sensing structure has been characterized.


## Multispectral Concept

Traditional multispectral imaging records multiple wavelength bands and
uses differences between those measurements to distinguish properties of
a scene or material.

WYLASR investigates whether an analogous multidimensional measurement
approach can be useful at substantially lower electromagnetic
frequencies using inductive coil structures.

The term **multispectral** within WYLASR therefore refers to the
experimental use of multiple independently characterized electromagnetic
response channels rather than conventional optical spectral bands.

Potential channels may include measurements made under different:

- excitation frequencies,
- amplitudes,
- phases,
- electrical configurations,
- coil configurations,
- core materials, or
- other controlled experimental conditions.

For example:

- Channel A — baseline coil response
- Channel B — alternate excitation frequency
- Channel C — independently calibrated electrical response

A measurement of the 64-cell array can be spatially represented as an
8 × 8 matrix.

Three independently calibrated channels could therefore form an
8 × 8 × 3 experimental data cube.

Additional channels can extend this concept into higher-dimensional
datasets while preserving the physical location and experimental
conditions associated with every measurement.


## Experimental Method

The development of WYLASR follows a measurement-first approach.

Experiments should, whenever practical:

1. establish a baseline,
2. change one controlled variable,
3. record the raw measurements,
4. preserve calibration and experimental metadata,
5. repeat measurements to determine variability,
6. compare responses spatially and electrically, and
7. only then apply interpolation, statistical analysis, or machine
   learning.

Raw experimental data should be retained whenever possible so that
future analysis methods can be applied without repeating the original
experiment.


## Open-Source Philosophy

WYLASR is intended to remain open so that others can:

- reproduce the hardware,
- improve the sensor geometry,
- improve the software,
- develop new experiments,
- contribute calibration methods,
- analyze shared datasets,
- challenge or validate results,
- compare alternative sensing architectures, and
- develop applications that were not originally anticipated.

The guiding principle is:

> **Do not tell the sensor what it should see. Measure what it sees,
> preserve the raw data, and determine experimentally what those
> measurements mean.**


## Repository Structure

- `hardware/` — PCB hardware, fabrication files, and physical designs
- `software/` — software tools, data-acquisition software, and
  sensor-generation code
- `experiments/` — experimental procedures and calibration methods
- `data/` — raw and processed experimental datasets
- `docs/` — project documentation, theory, references, and design notes
- `LICENSES/` — hardware and software license files


## References and Acknowledgments

WYLASR builds upon ideas and techniques developed throughout the
open-source hardware, electromagnetic sensing, array processing, and
scientific instrumentation communities.

Projects and publications that materially influence WYLASR will be
identified and cited in the project documentation.

ESPARGOS is specifically acknowledged as a major inspiration for the
initial WYLASR concept, particularly its demonstration of low-cost
spatial sensing arrays, combined-array geometries, calibration,
multidimensional measurement acquisition, and computational spatial
processing.

A more complete bibliography and discussion of related work is maintained
in:

`docs/REFERENCES.md`


## Project Status

**WYLASR V1** is the first fabricated experimental sensor revision.

The project is currently in the hardware characterization and
experimental-method development stage.

Results should be considered experimental unless independently
reproduced and validated.


## License

WYLASR software and hardware are licensed separately.

See the `LICENSES/` directory for the applicable licenses.