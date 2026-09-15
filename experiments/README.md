\# WYLASR V1 — Initial Three-Band Experiment



\## Purpose



The first WYLASR V1 experiment will establish a controlled electromagnetic

source and use a second, spatially aligned WYLASR array as a receiver.



The objective is not to assume what the receiver should detect. The

experiment will determine whether the individual coil cells exhibit

repeatable spatial and spectral responses to a known electromagnetic

excitation and whether changes to the electrical configuration of the

receiver produce distinguishable response channels.



These initial experiments will establish the first three experimental

WYLASR bands.





\## Experimental Geometry



Two WYLASR assemblies will be positioned in direct spatial alignment.



Each assembly contains an 8 × 8 array of 64 planar bifilar coil cells.



Roofing nails will be installed through the 5 mm center holes of the

cells and used as repeatable ferromagnetic cores and mechanical alignment

features.



The transmitting and receiving arrays will initially be positioned with

approximately zero lateral offset so that:



A1 corresponds spatially with A1,

A2 corresponds with A2,

...

H8 corresponds with H8.



The serpentine physical ordering of the array is:



A8 → A1  

B1 → B8  

C8 → C1  

D1 → D8  

E8 → E1  

F1 → F8  

G8 → G1  

H1 → H8



This provides 64 known physical locations that can ultimately be

represented as an 8 × 8 spatial matrix.





\## Transmitting / Calibration Array



The initial transmitting assembly will consist of three WYLASR V1 flex

boards stacked in parallel.



Corresponding ENTER terminals will be vertically interconnected and

corresponding EXIT terminals will be vertically interconnected.



The purpose of paralleling three boards is to reduce effective conductor

resistance and increase available current capability while maintaining

the same spatial coil geometry.



A stepper-motor driver will initially provide controlled low-frequency

pulsed excitation.



The first frequency sweep will cover approximately:



1–13 Hz



The transmitting assembly is therefore not intended to represent an

unknown target. It is a repeatable calibration source whose geometry,

frequency, timing, and spatial relationship to the receiver are known.



A 100 µF capacitor is also planned across the transmitter terminals as

an experimental reactive element.



Its effect will be characterized experimentally rather than assuming a

particular resonant frequency. The actual resonant behavior will depend

on the inductance, resistance, mutual coupling, capacitance, core

material, and parasitic properties of the completed assembly.





\## Receiving Array



The initial receiving assembly will consist of ten WYLASR V1 boards

stacked in parallel.



Corresponding ENTER terminals will be vertically interconnected and

corresponding EXIT terminals will be vertically interconnected.



Roofing nails will again be used as the initial core material.



An ESP32-based acquisition system will observe the electrical response

of the receiving assembly.



The signal will be analyzed spectrally so that amplitude and frequency

response can be preserved rather than reducing each measurement

immediately to a single voltage value.





\# Three Experimental Bands



The first WYLASR multispectral dataset will use three physical receiver

configurations.





\## Band 1 — Baseline



Band 1 is the unmodified receiver configuration.



No additional tuning capacitors are connected to the receiver array.



This measurement establishes the baseline response of the stacked

bifilar array and its roofing-nail cores.





\## Band 2 — Row-Level Capacitive Configuration



Band 2 will be selected using physical switches.



Eight 100 µF capacitors will be introduced, corresponding to the eight

rows of the array.



This configuration is intended to investigate how row-level capacitance

changes the amplitude, phase, spectral response, coupling, and possible

resonant behavior of the receiving structure.



Band 2 therefore differs from Band 1 by one controlled electrical

configuration change.





\## Band 3 — Cell-Level Capacitive Configuration



Band 3 will introduce capacitance at the individual-cell level.



Each of the 64 cells will be associated with a 100 µF capacitive

configuration selected through the experimental switching system.



This configuration is intended to determine whether local capacitive

loading produces a measurably different spatial and spectral response

from the baseline and row-level configurations.





\# Calibration Sweep



The first calibration signal will be a controlled pulse train swept

through approximately 1–13 Hz.



Measurements will initially be divided into eight-second acquisition

windows.



For each window, the raw time-domain signal will be retained and a

frequency-domain representation calculated.



The initial analysis will examine whether the spatially aligned

transmitter/receiver system produces stable and repeatable spectral

features that can be associated with particular cells or groups of

cells.



A central experimental hypothesis is that the coupled array may produce

multiple distinguishable spectral features resulting from the geometry,

inductance, mutual coupling, core response, and electrical configuration

of the 64-cell structure.



Whether 64 independently identifiable cell responses actually exist is

a question to be determined experimentally.





\## Spectral Refinement



The first sweep will identify regions of the spectrum containing

repeatable responses.



Once a repeatable feature has been identified, subsequent measurements

can concentrate on a narrower frequency interval surrounding that

feature.



A 256-bin representation can then be used to describe the measured

spectral shape within the selected interval.



The original time-domain measurements and physically meaningful

frequency values will always be retained. The 256-bin representation is

a data representation and does not itself increase the physical

frequency resolution of the measurement.





\# Spatial Data Products



Each identified cell response will retain its physical array coordinate.



For example:



A1 → pixel (1,1)  

A2 → pixel (2,1)  

...

H8 → pixel (8,8)



The fundamental spatial product for one response channel is therefore:



8 × 8 = 64 pixels



Raw measurements should be stored at floating-point precision so that

information is not discarded during acquisition or calibration.



Normalized 8-bit products can subsequently be generated for

visualization.



For each receiver configuration:



Band 1 → 8 × 8 response image  

Band 2 → 8 × 8 response image  

Band 3 → 8 × 8 response image



The three normalized bands can then be combined into an experimental

RGB composite:



R → Band 1  

G → Band 2  

B → Band 3



A uniform calibration response should tend toward a neutral/gray

composite when the three independently normalized bands respond

similarly.



Differences between the electrical configurations will instead appear

as color differences in the composite.



The RGB image is therefore a visualization of three measured response

channels, not a conventional visible-light photograph.





\# Known-Signal Dynamic Experiment



After calibration with controlled pulse trains, a second experiment will

use a known audio waveform as the excitation source.



A repeatable music recording can provide a much more complex waveform

containing simultaneous and changing frequency components.



The same recording will be applied independently while observing each of

the three receiver configurations.



The objective is to examine:



\- transient response,

\- spectral response,

\- cell-to-cell coupling,

\- row-to-row coupling,

\- magnetic-core behavior,

\- saturation and recovery,

\- temporal persistence,

\- and the effect of receiver tuning configuration.



The resulting measurements can be treated as a time sequence of 8 × 8

spatial frames.



Conceptually:



time → 8 × 8 × 3



This creates the possibility of displaying the experiment as a live

three-band spatial data stream.





\# Why Perform the Audio Experiment?



The audio experiment is not intended to demonstrate a practical sensing

application.



It provides a repeatable, information-rich excitation waveform whose

timing and spectral content are already known.



That makes it useful for observing how a complex electromagnetic signal

propagates through, couples into, and is reconstructed by the WYLASR

array.



The initial transmitter and receiver are deliberately aligned with

approximately zero spatial offset. This removes an important geometric

variable from the first experiment.



Later experiments can introduce controlled:



\- Z separation,

\- X/Y displacement,

\- rotation,

\- different core materials,

\- intervening materials,

\- different excitation amplitudes,

\- different frequencies,

\- and different transmitter geometries.





\# Relationship to Resonant-Coil Experiments



WYLASR is partly motivated by the long history of resonant and tuned

electromagnetic circuits, including historical experiments involving

Tesla coils and very-low-frequency electrical phenomena.



The initial WYLASR experiments do not assume that a particular natural

or geophysical resonance will be detected.



Instead, the first "heartbeat" will be deliberately generated by the

calibration transmitter.



Because its timing is known, the transmitted pulse train provides a

reference against which the receiving array can be characterized.



Only after the response to controlled artificial sources is understood

will experiments involving uncontrolled environmental electromagnetic

signals be scientifically interpretable.





\# Guiding Principle



The calibration array creates a known electromagnetic heartbeat.



The receiving array listens.



WYLASR records what it actually hears.

