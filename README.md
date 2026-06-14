# Mapping the Milky Way: CMD & HRD from Scratch

## What and Why
This is a personal data science project to see if I could recreate the Hertzsprung-Russell Diagram (HRD) and Color-Magnitude Diagram (CMD) for the Milky Way using raw, real-world survey data. 

The main goal was to pull data from two major telescopes, merge them, and observe the physical effects of stellar metallicity—specifically, how a high metal content in a star's atmosphere shifts its apparent color (the line-blanketing effect) on observational plots versus physical ones.

## The Data Sources
The dataset is a crossmatch between two major astronomical surveys:
* **DESI (Dark Energy Spectroscopic Instrument):** Provided the redshift (`zpix` table), and the core physical parameters like Metallicity and Temperature (`mws` table).
* **Gaia (ESA):** Provided the distance metrics (parallax) and the three distinct light-band brightness measurements (Main G-band, BP, and RP).

## Data Cleaning & Quality Cuts
Raw space data is messy, so the dataset was filtered using strict quality constraints:
* **`parallax_over_error > 5.0`:** Ensures the distance measurements are at least 5x larger than their margin of error (filtering out noisy, unreliable distances).
* **`phot_bp_rp_excess_factor < 1.3`:** A photometric contamination check. It removes instances where Gaia accidentally measured two closely orbiting stars as one, or where background galactic light bled into the lens and corrupted the color measurement.
* **Math/Logic Checks:** Dropped rows missing parameter arrays and removed stars with negative or zero parallaxes (a mathematical impossibility caused by instrument noise).

## The Astrophysics Math
To plot the diagrams, the raw observational data was converted into physical absolute metrics. 

**1. Distance:** Calculated in parsecs using the inverse of the parallax angle:
$d = \frac{1000}{\text{parallax (mas)}}$

**2. Absolute Magnitude ($M_G$):** Calculated using the experimentally derived distance modulus formula ($m - M = 5\log_{10}(d/D)$). 
Where $m$ is the apparent magnitude, and $D$ is the standard baseline distance of 10 parsecs. The derivation used in the code looks like this:
$m - M = 5\log_{10}(d) - 5\log_{10}(10)$
$m - M = 5\log_{10}(d) - 5(1)$
$M = m - 5\log_{10}(d) + 5$

**3. Observed Color Index:**
Calculated simply by subtracting the Red Photometer band from the Blue Photometer band ($BP - RP$).

## The Experiment
With the physical metrics calculated, the stars were sliced into two distinct groups based on their Iron content ([Fe/H]):
* **Standard Stars:** -0.4 to +0.3
* **Super Metal-Rich (SMR) Stars:** +0.4 to +0.6

Finally, the data was plotted into a 2x2 Matplotlib grid comparing the observational CMDs against the physical HRDs for both metallicity sets to visualize the structural changes and color shifts.
