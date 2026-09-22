\# WYLASR Experimental Plan



\## Purpose



WYLASR is an experimental research project investigating whether a controlled resonant electromagnetic system can produce repeatable measurements that contain useful spatial and geophysical information.



The project is inspired in part by Nikola Tesla's work involving resonance, sensitive receivers, terrestrial electrical phenomena, and what he later described as \*\*telegeodynamics\*\*. WYLASR is not intended to assume that Tesla's interpretations were correct. Instead, the project takes the underlying experimental idea—\*\*apply a controlled excitation, measure the response, and allow repeatable observations to determine what information is present\*\*—and evaluates it using modern instrumentation, positioning, signal processing, phased arrays, and machine learning.



The fundamental philosophy of the project is:




> \*\*Let the data tell the story.\*\*



Claims about subsurface sensing, propagation mechanisms, resonance, or imaging should therefore follow experimental evidence rather than precede it.



\---



\# 1. Core Research Question



The initial research question is deliberately simple:



> Can a controlled transmitter and resonant receiver system produce repeatable electromagnetic measurements as a receiver moves through a precisely measured three-dimensional space?



If the answer is yes, subsequent experiments will investigate:



1\. What portion of the measured response can be explained by transmitter/receiver geometry?

2\. What portion is associated with conductive coupling through the ground?

3\. What portion is associated with airborne electromagnetic coupling?

4\. How do multiple resonant elements interfere with one another?

5\. Can phased-array techniques improve signal isolation or spatial discrimination?

6\. Can known subsurface objects measurably alter the response?

7\. Can machine-learning methods identify repeatable patterns without requiring a predetermined analytical model?

8\. Can those patterns ultimately provide useful geophysical information?



\---



\# 2. General System Concept



The experimental system consists of two primary components:



\## Base Station / Transmitter



The base station generates a precisely controlled and recorded excitation signal.



The signal is coupled to:



\* a ground electrode or electrode system;

\* the resonant transmitter array;

\* or both, depending upon the experiment.



The transmitter therefore acts as a controlled reference source.



The repeating reference waveform is informally referred to within the project as the \*\*heartbeat\*\*.



The heartbeat does not imply any assumed natural Earth frequency or special geophysical phenomenon. It simply provides a known, repeatable excitation against which received measurements can be compared.



\## Rover / Receiver



The rover contains:



\* resonant receiver array;

\* independent receiver channels where practical;

\* rover ground electrode(s);

\* GNSS positioning;

\* IMU attitude measurement;

\* precise time;

\* data logging.



Possible navigation hardware includes systems such as:



\* Emlid Reach M2;

\* CubePilot Orange Cube;

\* Holybro Pixhawk 6X Pro;

\* comparable GNSS/IMU instrumentation.



Every electromagnetic observation should therefore be associated with:



$$

X,Y,Z

$$



and:



$$

Roll,\\ Pitch,\\ Yaw

$$



as well as precise time.



The rover consequently becomes a \*\*position- and attitude-referenced electromagnetic measurement platform\*\*.



\---



\# 3. Measurement Model



A simplified representation of the experiment is:



$$

TX\_{reference}

\\rightarrow

TX\_{array/ground}

\\rightarrow

Environment

\\rightarrow

RX\_{array/ground}

\\rightarrow

Measurement

$$



The recorded response can be represented conceptually as:



$$

R =

f(x,y,z,\\phi,\\theta,\\psi,f\_{TX},A\_{TX},P\_{TX},

RX\_1...RX\_n,G\_{TX},G\_{RX},t)

$$



where:



\* \\(x,y,z\\) = rover position;

\* \\(\\phi,\\theta,\\psi\\) = rover roll, pitch, and yaw;

\* \\(f\_{TX}\\) = transmitted frequency;

\* \\(A\_{TX}\\) = transmitter amplitude;

\* \\(P\_{TX}\\) = transmitter phase configuration;

\* \\(RX\_1...RX\_n\\) = individual receiver-channel measurements;

\* \\(G\_{TX}\\) = transmitter ground response;

\* \\(G\_{RX}\\) = rover ground response;

\* \\(t\\) = synchronized time.



Environmental variables should eventually be added where they are demonstrated to influence measurements.



\---



\# 4. Transfer-Function Approach



Rather than considering received voltage alone, WYLASR should characterize the relationship between transmitted and received signals.



For a particular frequency:



$$

H(f)=\\frac{RX(f)}{TX(f)}

$$



Phase difference can similarly be measured:



$$

\\Delta\\phi(f)=\\phi\_{RX}(f)-\\phi\_{TX}(f)

$$



Potential features include:



\* received amplitude;

\* attenuation;

\* phase delay;

\* coherence;

\* signal-to-noise ratio;

\* resonant peak frequency;

\* resonant peak width;

\* Q factor;

\* harmonic content;

\* individual array-element response;

\* inter-element phase;

\* ground-electrode response;

\* ground/array amplitude ratio;

\* ground/array phase relationship;

\* neighboring-position differences;

\* temporal stability.



Raw measurements should be preserved whenever possible so that future processing methods can revisit earlier experiments.



\---



\# 5. Phased Array Research



One goal of WYLASR is to determine whether phased-array principles can improve controlled-source measurements.



The eventual system may use transmitter and/or receiver arrays whose relative phase can be adjusted.



A future transmitter could use rover coordinates to calculate a phase configuration intended to maximize coupling in the rover's direction.



However, adaptive steering should \*\*not be the only measurement mode\*\*.



Fixed and repeatable phase states provide important calibration information.



An experimental sequence could include:



$$

S\_0=\[0^\\circ,0^\\circ,0^\\circ,\\ldots]

$$



$$

S\_1=\[0^\\circ,45^\\circ,90^\\circ,\\ldots]

$$



$$

S\_2=\[0^\\circ,90^\\circ,180^\\circ,\\ldots]

$$



followed by:



$$

S\_N=\\text{Calculated Rover-Directed State}

$$



Each phase state effectively becomes a known excitation code.



The system should also periodically record a:



$$

TX=OFF

$$



state.



This provides a measurement of ambient electromagnetic conditions and receiver noise under nearly identical circumstances.



\---



\# 6. Ground and Airborne Measurements



An important experimental feature is the simultaneous observation of different coupling mechanisms.



The rover may measure:



\### Receiver Array



Electromagnetic response detected by the resonant coil/antenna system.



\### Rover Ground Electrode



Electrical response measured through a ground-coupled electrode.



These measurements should initially remain separate rather than being combined.



This allows comparison between:



\* predominantly inductive/radiated response;

\* conductive ground response;

\* common signal components;

\* differential signal components.



One useful derived measurement may eventually be:



$$

R\_{GA}(f)=\\frac{Ground(f)}{Array(f)}

$$



along with their phase relationship.



The objective is not initially to decide which propagation mechanism produced a signal, but to collect sufficient independent measurements to experimentally separate them.



\---



\# 7. GNSS and IMU Referencing



Receiver orientation can strongly influence electromagnetic measurements.



A change in signal caused by rotating an antenna must not be mistaken for a change caused by geology.



Every rover observation should therefore contain synchronized:



\* latitude/longitude or projected coordinates;

\* ellipsoidal/orthometric height as appropriate;

\* GNSS quality;

\* roll;

\* pitch;

\* yaw;

\* timestamp.



The IMU permits measurements collected in the rover coordinate frame to be transformed into a common reference frame.



Orientation itself should also become an experimental variable.



At calibration stations, the rover can deliberately be rotated through known orientations to empirically measure:



$$

R(\\phi,\\theta,\\psi)

$$



This produces an orientation-response model that can later be used for correction or incorporated directly into machine-learning models.



\---



\# 8. Experiment 0 — Instrument Characterization



Before attempting spatial or geophysical experiments, each component should be characterized independently.



\## Objective



Determine whether the instrumentation itself is stable and repeatable.



\## Tests



Measure:



\* oscillator frequency stability;

\* transmitter amplitude stability;

\* transmitter phase stability;

\* individual coil resonant frequency;

\* individual coil Q;

\* channel-to-channel differences;

\* ADC noise;

\* receiver noise floor;

\* temperature sensitivity;

\* power-supply sensitivity;

\* mutual coupling between neighboring coils;

\* grounding-electrode impedance.



Repeated measurements should be performed over time.



\## Success Criterion



The variation of the instrument must be sufficiently characterized that subsequent changes can be distinguished from normal system drift.



\---



\# 9. Experiment 1 — Repeatability



\## Question



Can the system reproduce the same measurement under nominally identical conditions?



\## Procedure



Establish fixed TX and RX positions.



Record a predetermined sequence containing:



1\. TX OFF;

2\. reference frequency;

3\. frequency sweep;

4\. predetermined phase states;

5\. TX OFF.



Repeat the complete sequence numerous times.



Repeat the experiment on different days.



\## Primary Analysis



Compare:



\* amplitude;

\* phase;

\* resonant frequency;

\* Q;

\* inter-channel response;

\* ground response;

\* noise.



\## Success Criterion



The system produces statistically distinguishable and repeatable responses beyond its measured instrument noise and drift.



\---



\# 10. Experiment 2 — Spatial Repeatability



\## Question



Does the electromagnetic response change predictably with rover position?



\## Proposed Test Area



Establish a controlled grid around the transmitter.



An initial example could be:



\*\*10 m × 10 m\*\*



with surveyed observation points.



The actual dimensions and spacing should be selected based upon measured system behavior rather than assumed beforehand.



\## Procedure



At every point:



1\. establish rover position;

2\. record GNSS solution;

3\. record IMU orientation;

4\. maintain controlled receiver height;

5\. execute identical TX sequence;

6\. record every RX channel;

7\. record rover ground electrode;

8\. record TX reference;

9\. record TX current/voltage where available;

10\. record environmental/background state.



Repeat the entire grid.



Repeat again on another day.



\## Success Criterion



Measurements collected at the same positions should resemble one another more closely than measurements from unrelated positions after accounting for known experimental variables.



\---



\# 11. Experiment 3 — Electromagnetic Position Recovery



This is an important blind validation experiment.



\## Question



Does the electromagnetic field contain enough repeatable spatial information to determine rover position?



GNSS provides the known answer.



The learning system is given electromagnetic measurements and attempts to estimate:



$$

(X,Y)\_{EM}

$$



The prediction is compared against:



$$

(X,Y)\_{GNSS}

$$



The model should not be evaluated using observations it was trained upon.



Entire passes, spatial regions, or collection sessions should be withheld for validation.



\## Why This Matters



This test does not require assuming anything about underground geology.



If rover location can be independently estimated from the electromagnetic response, WYLASR has demonstrated that the measured field contains stable spatial information.



Failure is equally informative because it establishes limits on repeatability or spatial discrimination.



\---



\# 12. Experiment 4 — Orientation Characterization



\## Question



How much of the observed response is caused by receiver orientation?



\## Procedure



At a fixed surveyed position, systematically vary:



\* yaw;

\* pitch;

\* roll.



Record the complete TX sequence at each orientation.



Repeat at several distances and directions from the transmitter.



\## Output



Develop an empirical model:



$$

R(\\phi,\\theta,\\psi)

$$



This model may subsequently be used to:



\* normalize observations;

\* provide correction parameters;

\* identify orientation-sensitive channels;

\* supply additional features to machine-learning models.



\---



\# 13. Experiment 5 — Known Target Introduction



Only after the background field has been characterized should controlled subsurface targets be introduced.



\## Question



Does introducing a known object produce a repeatable change in the measured field?



Possible test objects could include:



\* conductive plate;

\* pipe;

\* buried conductor;

\* water-filled container;

\* controlled trench;

\* different known materials.



The target geometry, depth, orientation, and material should be documented.



\## Procedure



Collect:



\### Dataset A



Baseline grid without target.



\### Dataset B



Same grid with target installed.



\### Dataset C



Repeated target survey.



Where practical, additional datasets should alter:



\* target orientation;

\* target depth;

\* target location.



\## Success Criterion



The target produces a repeatable change that exceeds measured background variability and instrumentation uncertainty.



\---



\# 14. Experiment 6 — Blind Target Detection



Once known-target responses have been demonstrated, testing should become blind.



One person places or modifies targets without providing their locations to the person/model performing the analysis.



The analysis attempts to determine:



\* whether a target exists;

\* approximate location;

\* possibly depth;

\* possibly orientation;

\* possibly target class.



Results are compared with surveyed ground truth only after predictions have been recorded.



This experiment is particularly important for preventing confirmation bias.



\---



\# 15. Machine Learning



Machine learning should assist interpretation rather than substitute for experimental controls.



Initial models do not need to be complex.



Decision trees, random forests, gradient-boosted trees, and similar interpretable approaches may be particularly useful during early research because they can reveal which measured variables contribute to classification or regression.



Potential features include:



\* frequency;

\* TX phase state;

\* RX amplitude;

\* RX phase;

\* amplitude ratios;

\* phase differences;

\* harmonics;

\* resonant peak;

\* Q;

\* individual coil response;

\* coil-to-coil response;

\* ground-electrode response;

\* array/ground ratios;

\* rover orientation;

\* distance from transmitter;

\* environmental measurements.



Raw data should always remain available.



A successful ML result should subsequently be investigated to determine \*\*what physical measurement the model is exploiting\*\*.



\---



\# 16. Avoiding Data Leakage



Position and attitude information are essential experimental metadata, but care must be taken when testing whether electromagnetic measurements contain positional or geological information.



For example, a model intended to determine rover location from electromagnetic measurements cannot simply be given GNSS coordinates as an input.



Likewise, randomly dividing neighboring observations between training and validation sets may produce misleadingly good results because adjacent samples are highly related.



Preferred validation methods include withholding:



\* complete survey passes;

\* entire grid regions;

\* entire days;

\* entire target configurations.



Ultimately, the strongest tests should involve data collected after a model or hypothesis has already been established.



\---



\# 17. Suggested Data Record



Each observation should eventually receive a unique identifier.



A conceptual record could contain:



```text

experiment\_id

observation\_id

timestamp



TX\_X

TX\_Y

TX\_Z



RX\_X

RX\_Y

RX\_Z



roll

pitch

yaw



GNSS\_quality



TX\_frequency

TX\_amplitude

TX\_current

TX\_phase\_state



RX1\_amplitude

RX1\_phase

RX2\_amplitude

RX2\_phase

...

RXn\_amplitude

RXn\_phase



TX\_ground\_voltage

TX\_ground\_current



RX\_ground\_voltage

RX\_ground\_current



temperature

battery\_voltage



target\_configuration

operator\_notes

```



This structure will evolve as the hardware develops.



Raw high-rate waveform data should be retained separately and linked to the observation record rather than discarded after feature extraction.



\---



\# 18. Experimental Progression



The project should advance only as earlier questions become sufficiently understood.



The intended progression is:



\*\*Instrument Characterization\*\*



↓



\*\*Signal Repeatability\*\*



↓



\*\*Spatial Repeatability\*\*



↓



\*\*Electromagnetic Position Recovery\*\*



↓



\*\*Orientation Characterization\*\*



↓



\*\*Known Target Detection\*\*



↓



\*\*Blind Target Detection\*\*



↓



\*\*Geological Experiments\*\*



↓



\*\*Field Geophysical Interpretation\*\*



This progression intentionally postpones claims about geology until the instrument itself has demonstrated repeatable behavior.



\---



\# 19. Positive and Negative Results



WYLASR should document negative results.



Examples include:



\* a coil configuration that provides no useful response;

\* apparent anomalies that disappear during replication;

\* ML models that fail on independent datasets;

\* responses explained entirely by antenna orientation;

\* apparent ground signals determined to be airborne coupling;

\* environmental variables that overwhelm the desired measurement.



These are not failed experiments.



They establish boundaries on what the system can and cannot measure and prevent future researchers from repeating the same experiments unnecessarily.



\---



\# 20. Relationship to Tesla and Telegeodynamics



Nikola Tesla's experiments provide historical inspiration for WYLASR, particularly his investigations involving:



\* resonance;

\* sensitive electrical receivers;

\* terrestrial electrical disturbances;

\* controlled oscillators;

\* Earth-coupled transmission;

\* stationary-wave concepts;

\* long-distance detection.



Tesla's historical interpretations should be distinguished from modern experimental evidence.



WYLASR therefore does not begin with the assumption that Tesla's proposed terrestrial mechanisms were correct.



Instead, the project asks a modern experimental question inspired by the same general concept:



> \*\*If a precisely characterized excitation is introduced into an Earth-coupled electromagnetic system, what repeatable information can be recovered from the response?\*\*



Modern GNSS, IMUs, digital acquisition, synchronized clocks, phased arrays, signal processing, and machine learning make it possible to investigate that question in ways unavailable during Tesla's lifetime.



\---



\# 21. Research Philosophy



WYLASR should remain measurement-driven.



A useful hierarchy is:



\*\*Observation\*\*



What happened?



\*\*Replication\*\*



Does it happen again?



\*\*Correlation\*\*



What variables change with it?



\*\*Isolation\*\*



Can competing explanations be experimentally separated?



\*\*Prediction\*\*



Can the measured relationship correctly predict previously unseen observations?



\*\*Physical Interpretation\*\*



What mechanism best explains the demonstrated behavior?



Interpretation should come after repeatability.



\---



\# 22. Contribution Opportunities



Researchers and contributors could assist with:



\* electromagnetic modeling;

\* coil and PCB design;

\* resonant-circuit characterization;

\* phased-array theory;

\* embedded electronics;

\* synchronized ADC design;

\* GNSS/IMU integration;

\* signal processing;

\* geophysics;

\* statistics;

\* machine learning;

\* experiment design;

\* Python analysis tools;

\* visualization;

\* field testing;

\* historical research into Tesla and early geophysics.



Alternative explanations and attempts to falsify results are particularly valuable.



The objective is not to prove a predetermined theory.



The objective is to determine experimentally \*\*what the system measures, why it measures it, and whether that information can ultimately be useful.\*\*



\---



\## Guiding Principle



> \*\*Build a repeatable source. Build a measurable receiver. Know exactly where both are. Change one variable at a time. Preserve the raw data. Replicate the result. Then let the data tell the story.\*\*



