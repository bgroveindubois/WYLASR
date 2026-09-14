# WYLASR

Open-source experimental electromagnetic multispectral sensor using spatial arrays of planar bifilar coils.
# WYLASR



WYLASR is an open-source experimental electromagnetic multispectral sensing project.



The project investigates whether a spatial array of planar bifilar coils can produce repeatable, frequency-dependent electromagnetic measurements that can be converted into spatial imagery.



\## WYLAR V1



The first hardware revision uses an 8 × 8 array of 64 planar bifilar coil cells.



The initial goals are to:



\- characterize the passive response of individual cells

\- characterize the full 64-cell array

\- measure repeatability and cell-to-cell variation

\- experiment with multiple electromagnetic response channels

\- convert array measurements into spatially registered images

\- preserve raw measurements for later analysis and machine learning

\- explore whether different materials, geometries, depths, and electromagnetic environments produce distinguishable signatures



WYLASR does not assume in advance what the sensor will detect.



The project is intended to measure what the hardware actually responds to, calibrate those responses, and determine experimentally what information can be extracted.



\## Multispectral concept



Traditional multispectral imaging uses multiple wavelength bands to identify differences in material response.



WYLASR explores a related idea at much lower electromagnetic frequencies using inductive coil sensors.



The long-term goal is to create multiple independently calibrated response channels. Three response channels can be represented as three spatial data matrices and mapped into a conventional three-band image.



For example:



\- Channel A: baseline coil response

\- Channel B: alternate frequency or electrical response

\- Channel C: another independently calibrated response



Each 64-cell measurement can then be represented as an 8 × 8 spatial matrix.



Three channels can form an 8 × 8 × 3 experimental data cube.



\## Open-source philosophy



WYLASR is intended to remain open so that others can:



\- reproduce the hardware

\- improve the sensor geometry

\- improve the software

\- develop new experiments

\- contribute calibration methods

\- analyze shared datasets

\- challenge or validate results

\- develop applications that were not originally anticipated



The guiding principle is:



> Do not tell the sensor what it should see. Measure what it sees, preserve the raw data, and determine experimentally what those measurements mean.



\## Repository structure



\- `hardware/` — PCB hardware, fabrication files, and physical design

\- `software/` — software tools and sensor-generation code

\- `experiments/` — experiment procedures and calibration methods

\- `data/` — raw and processed experimental datasets

\- `docs/` — project documentation and theory

\- `LICENSES/` — hardware and software license files



\## Project status



WYLAR V1 is currently the first fabricated experimental sensor revision.



The project is in the hardware characterization stage.



\## License



Software and hardware are licensed separately.



See the `LICENSES` directory for details.

