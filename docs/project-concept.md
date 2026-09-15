**WYLASR V1**

**Hardware and Initial Experiment Plan**



Experimental electromagnetic multispectral sensing platform

Development configuration - September 2026



This document records the first WYLASR hardware configuration, the purpose of each component, and the planned sequence of characterization experiments. The goal of V1 is measurement first: create a known excitation, record what the receiving array actually produces, preserve the raw observations, and use those measurements to determine the requirements for later custom instrumentation.



**1. System Overview**



WYLASR V1 uses separate transmitter and receiver assemblies. The transmitter creates a controlled electromagnetic excitation. The receiver behaves conceptually like an electromagnetic microphone: the WYLASR array produces a small electrical response, a preamplifier raises that response to a measurable level, and a precision ADC records it.



TRANSMITTER: ESP32-S3 -> DDS signal generator -> power driver -> WYLASR TX array



COUPLING: controlled electromagnetic field between spatially aligned arrays



RECEIVER: WYLASR RX array -> preamplifier -> ADS1256 ADC -> ESP32-S3 -> computer



PROCESSING: raw waveform -> spectral analysis -> resonance curves -> spatial products



**2. WYLASR Sensor Hardware**



Hardware



Configuration



Purpose



V1 Notes



WYLASR flex PCB array



8 x 8; 64 planar bifilar cells



Primary experimental electromagnetic sensing structure.



First fabricated revision; raw response is not assumed in advance.



TX array stack



Initially 3 WYLASR boards in parallel



Creates the controlled calibration/excitation field.



Corresponding terminals are intended to be paralleled; exact drive limits will be established experimentally.



RX array stack



Initially up to 10 WYLASR boards in parallel



Receives the electromagnetic response for characterization.



Stack count can be varied as an experimental variable.



Roofing nails



One through each 5 mm cell opening



Alignment and ferromagnetic core material.



Material, insertion depth, orientation, and dimensions should be standardized for repeatability.



**3. Initial Instrumentation Hardware**



The initial electronics are development modules rather than final WYLASR instrument PCBs. They are being used to establish actual signal levels, useful bandwidth, gain requirements, noise floor, and resonance behavior before committing those parameters to a custom design.



Item



Qty / Type



Side



Purpose



Status / limitation



ESP32-S3 N16R8



3 development boards



TX / RX / spare



Control, timing, data handling, Wi-Fi communication, and experiment automation.



Not relied upon as the precision ADC.



AD9850 DDS



2 modules, 0-40 MHz class



TX



Wide-range programmable frequency source for resonance sweeps and controlled excitation.



Signal source only; requires a separate power driver before the TX array.



AD828 preamp modules



6 modules



RX



Experimental low-level signal amplification before digitization.



Temporary characterization preamps; gain, noise and frequency response must be measured.



ADS1256 ADC



24-bit, 8-channel module



RX



Primary precision digitizer for ULF and lower-frequency measurements.



Up to about 30 kSPS; not a direct hundreds-of-kHz oscilloscope.



100 uF / 100 V non-polar capacitors



10



Experiment



Large-capacitance tuning and resonance experiments without polarized-electrolytic reversal concerns.



Experimental value, not assumed to be the final cell capacitor.



10 uF ceramic capacitors



100



Experiment



Non-polar tuning components for comparison with the 100 uF condition.



Actual capacitance and voltage behavior should be characterized where practical.



Initial instrumentation electronics purchase: approximately $101.57. This figure is the development electronics order and does not include the previously fabricated WYLASR flex arrays, ordinary bench wiring, power supplies, or future transmitter power-stage hardware.



**4. Receiver Concept**



The receiver is intentionally treated like a scientific microphone. The WYLASR array is the transducer, the AD828 is the first experimental preamplifier, and the ADS1256 records the amplified voltage as a time series.



WYLASR RX -> input/protection interface -> AD828 preamp -> ADS1256 -> ESP32-S3



Preserve raw ADC samples before normalization or image generation.



Record amplifier gain/settings, sample rate, array stack count, capacitor state, core configuration, and TX settings with every dataset.



**5. Transmitter Concept**



The transmitter creates a known electromagnetic calibration source. The ESP32-S3 programs the AD9850 frequency source. A separate power driver will be selected or designed to provide the voltage/current required by the TX array without requiring the DDS module itself to drive the coils.



Initial low-frequency heartbeat/modulation interest: approximately 1-13 Hz.



Resonance search must not be restricted to the heartbeat rate; the coil/stack may respond in the kHz or higher-frequency region.



The AD9850 provides broad frequency-generation headroom for automated sweeps.



Actual TX voltage, current, waveform and harmonics should be measured rather than inferred from the programmed frequency.



**6. Planned Experiments**



**Experiment 1 - Instrument Chain Calibration**



Characterize the electronics before connecting the sensor. Feed a known DDS signal through the AD828 and record it with the ADS1256. Measure gain, offset, noise, clipping, and frequency response. This establishes what the instrument itself contributes to later WYLASR measurements.



**Experiment 1.1 - Passive Receiver Baseline**



Record the RX array with no intentional transmitter excitation. Establish the baseline noise floor, drift, environmental pickup, and repeatability. Repeat with and without roofing-nail cores.



**Experiment 2 - Controlled TX/RX Coupling**



Align the TX and RX arrays at a known zero lateral offset. Drive the TX at low amplitude and record the RX response. Begin conservatively and increase excitation only after the received and transmitter voltages are understood.



**Experiment 3 - Frequency Sweep / Resonance Search**



Sweep the programmed transmitter frequency over progressively wider ranges. Direct waveform capture with the ADS1256 is appropriate at lower frequencies. At frequencies above its direct sampling range, an envelope or amplitude detector can later be used to convert high-frequency response magnitude into a slowly varying value that the ADS1256 can measure. Peaks are candidate resonant regions, not proof of mechanism.



Experiment 4 - Capacitor Comparison



Repeat the same geometry and excitation with no added capacitor, 10 uF ceramic, and 100 uF non-polar capacitor conditions. Compare resonance location, amplitude, bandwidth, phase where measurable, and damping. Exact row/cell capacitor topology must be documented before the multi-capacitor experiments are wired.



**Experiment 5 - Core and Stack Characterization**



Vary board count and core condition while holding the remainder of the setup constant. Candidate conditions include no core versus standardized roofing nails and different TX/RX stack counts. Measure inductance and resistance whenever practical so observed frequency shifts can be tied to physical changes.



Experiment 6 - Dynamic Known-Signal Test



After the basic response is understood, excite the system with a known repeatable time-varying waveform and observe transient response, coupling, ringing, saturation, and recovery. Public datasets should favor generated or public-domain signals so experiments can be reproduced freely.



**7. Three-Band Spatial Experiment Concept**



The longer-term V1 concept is to compare three controlled electrical conditions and derive an 8 x 8 spatial product for each condition. The present hardware is a continuous serpentine array, so the assumption that individual cells can be uniquely recovered from one composite electrical output remains an experimental hypothesis. If individual cells do not naturally separate spectrally, later hardware may require taps, multiplexing, coded excitation, deliberate tuning differences, or individual addressing.



Band



Planned condition



Purpose



Band 1



No added tuning capacitor



Baseline electromagnetic response.



Band 2



Row-level capacitor condition (planned)



Test whether row-scale tuning creates a repeatable second response channel.



Band 3



Cell-level capacitor condition (planned)



Test whether cell-scale tuning creates a repeatable third response channel.



The exact Band 2 and Band 3 capacitor wiring topology is intentionally not fixed in this document. A schematic should be completed before those experiments so that 'across a row' and 'across a cell' have an unambiguous electrical definition.



**8. Data Products**



Raw time-series samples: retained at the ADC's native numerical precision.



Experiment metadata: frequency, waveform, drive level, gain, sample rate, board count, capacitor state, core state, geometry, date/time, and firmware/software version.



Spectral products: FFT, peak frequency, amplitude, phase where available, bandwidth, damping and estimated Q where justified.



Frequency-response curves: received amplitude versus programmed transmitter frequency.



Spatial products: derived 8 x 8 floating-point arrays when the measurement method supports cell localization.



Visualization products: normalized 8-bit single-band TIFFs and, eventually, three-band RGB composites. These are derived products, not replacements for raw data.



**9. Measurement Rules for V1**



Calibrate the electronics before interpreting the sensor.



Change one major variable at a time whenever practical.



Preserve raw data before filtering, interpolation, normalization, or image creation.



Do not assume that 64 cells will naturally produce 64 unique spectral peaks; test that hypothesis.



Do not assume that the 1-13 Hz excitation rate is the electrical resonance frequency.



Record null results and unexpected results; they are part of the characterization.



Standardize geometry, nail/core condition, board orientation, spacing, and wiring before comparing datasets.



Begin at low transmitter drive and measure actual peak voltage/current before increasing power.



**10. Deferred Hardware**



A high-speed ADC/FPGA oscilloscope path (for example, an AD9226-class converter) is deliberately deferred from the first purchase. The ADS1256 system can establish the low-frequency response and can support swept-frequency amplitude measurements at higher excitation frequencies when paired with a suitable detector. High-speed direct waveform capture should be added after the first measurements demonstrate a specific need to inspect kHz-to-MHz ringing, harmonics, or waveform shape.



**11. Development Principle**



Do not tell the sensor what it should see.

Measure what it sees, preserve the raw data,

and determine experimentally what those measurements mean.



The calibration array creates a known electromagnetic heartbeat. The receiving array listens. WYLASR records what it actually hears.



WYLASR V1 - Hardware and Initial Experiment Plan

