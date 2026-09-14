\# WYLASR V1 Hardware



WYLASR V1 is the first fabricated hardware revision of the WYLASR

experimental electromagnetic multispectral sensor project.



\## Sensor Array



WYLASR V1 consists of an 8 × 8 spatial array containing 64 planar

bifilar coil cells.



Each cell uses two interleaved octagonal planar coils arranged around

a central 5 mm non-plated hole. The center hole is intended for

experimentation with alignment pins, ferromagnetic cores, nails,

and other materials.



\### Nominal Coil Geometry



\- Array: 8 × 8

\- Sensor cells: 64

\- Coil geometry: Octagonal planar bifilar

\- Coil 1 inner diameter: 13.0 mm

\- Coil 2 inner diameter: 13.7 mm

\- Copper trace width: 0.175 mm

\- Trace gap: 0.175 mm

\- Independent coil pitch: 0.700 mm

\- Central core/alignment hole: 5 mm NPTH

\- Electrical connection holes: 1 mm PTH

\- Exposed interconnection copper: 3 mm nominal width



\## PCB Construction



The first fabricated WYLASR V1 array was designed as a two-layer

flexible PCB.



Manufacturing configuration:



\- PCB type: Flexible PCB

\- Layers: 2

\- Board dimensions: approximately 203.1 × 203.1 mm

\- Copper weight: 1 oz

\- Surface finish: ENIG

\- Substrate: Polyimide flex

\- Cutting method: Laser

\- Stiffener: None

\- EMI shielding film: None



The exact fabrication settings used for the first production run are

preserved in the `renders` and fabrication documentation associated

with this revision.



\## Electrical Architecture



The two coils within each sensor cell are interconnected using the

bottom copper layer.



Array-level interconnections and row-to-row bridges are routed on the

top copper layer and intentionally exposed where required for

soldering, testing, stacking, and future circuit experiments.



Ordinary internal vias are intended to remain covered.



The array forms a serpentine electrical path through the 64 cells.



\## Experimental Purpose



WYLASR V1 is an experimental sensor platform.



It is intended to establish baseline measurements for:



\- individual coil response

\- cell-to-cell repeatability

\- spatial electromagnetic response

\- frequency-dependent response

\- stacked sensor configurations

\- different core materials

\- alternate resistance and capacitance configurations

\- future multi-channel measurements



No specific detection capability is claimed for WYLASR V1.



The purpose of this revision is to characterize what the physical

sensor actually measures and establish reproducible baseline datasets.



\## Manufacturing Files



The `gerbers` directory contains the fabrication package for WYLASR V1.



Always inspect the Gerber and drill files with the intended PCB

manufacturer before ordering.



\## License



WYLASR V1 hardware design materials are licensed under the CERN Open

Hardware Licence Version 2 - Strongly Reciprocal.



See:



`../../LICENSES/HARDWARE-LICENSE.txt`

