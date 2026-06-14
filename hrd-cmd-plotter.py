import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. DATA INGESTION & PARSING ---
print("Loading data... (This might take a few seconds)")
df = pd.read_csv('local_milky_way_data.csv')

print("Unpacking stellar parameters...")
# Remove any rows where the param string might be missing to prevent errors
df = df.dropna(subset=['param']).copy() 

# Strip the '{}' brackets, split by comma, and grab the correct index
# Index 0 is [Fe/H] (Metallicity), Index 3 is Teff (Temperature)
df['feh'] = df['param'].apply(lambda x: float(str(x)[1:-1].split(',')[0]))
df['teff'] = df['param'].apply(lambda x: float(str(x)[1:-1].split(',')[3]))

# Remove rows with unphysical parallax values
df = df[df['parallax'] > 0].copy()

# --- 2. ASTROPHYSICS MATH PIPELINE ---
print("Calculating physical parameters...")

# Distance in parsecs
df['distance_pc'] = 1000.0 / df['parallax']

# Absolute G-band Magnitude 
df['M_G'] = df['phot_g_mean_mag'] - 5 * np.log10(df['distance_pc']) + 5

# Observed color index
df['bp_rp_color'] = df['phot_bp_mean_mag'] - df['phot_rp_mean_mag']

# --- 3. METALLICITY FILTERING ---
print("Slicing data by metallicity...")
mask_standard = (df['feh'] >= -0.5) & (df['feh'] <= 0.3)
mask_smr = (df['feh'] >= 0.4) & (df['feh'] <= 0.6)

df_standard = df[mask_standard]
df_smr = df[mask_smr]

# --- 4. PLOTTING THE 2x2 GRID ---
print("Generating 2D Histograms...")
fig, axs = plt.subplots(2, 2, figsize=(14, 14))
cmap = 'magma'
bins = 200 

# --- AXES INTERPRETATION ---
cmd_x = [-0.5, 3.5]       # Color (BP - RP)
hrd_x = [10000, 3000]     # Temperature (Hotter on left, Cooler on right)
mag_y = [15, -2]          # Absolute Magnitude (Fainter at bottom, Brighter at top)

# Graph 1: Standard CMD
axs[0, 0].hist2d(df_standard['bp_rp_color'], df_standard['M_G'], bins=bins, cmap=cmap, cmin=1, range=[[-0.5, 3.5], [-2, 15]])
axs[0, 0].set_title('Graph 1: Standard Metallicity CMD (Observed Color)')
axs[0, 0].set_xlabel('Color (BP - RP)')
axs[0, 0].set_ylabel('Absolute Magnitude ($M_G$)')
axs[0, 0].set_xlim(cmd_x)
axs[0, 0].set_ylim(mag_y) 

# Graph 2: SMR CMD
axs[0, 1].hist2d(df_smr['bp_rp_color'], df_smr['M_G'], bins=bins, cmap=cmap, cmin=1, range=[[-0.5, 3.5], [-2, 15]])
axs[0, 1].set_title('Graph 2: Super Metal-Rich CMD (Observed Color)')
axs[0, 1].set_xlabel('Color (BP - RP)')
axs[0, 1].set_ylabel('Absolute Magnitude ($M_G$)')
axs[0, 1].set_xlim(cmd_x)
axs[0, 1].set_ylim(mag_y)

# Graph 3: Standard HRD
axs[1, 0].hist2d(df_standard['teff'], df_standard['M_G'], bins=bins, cmap=cmap, cmin=1, range=[[3000, 10000], [-2, 15]])
axs[1, 0].set_title('Graph 3: Standard Physical HRD ($T_{eff}$)')
axs[1, 0].set_xlabel('Effective Temperature ($T_{eff}$)')
axs[1, 0].set_ylabel('Absolute Magnitude ($M_G$)')
axs[1, 0].set_xlim(hrd_x)
axs[1, 0].set_ylim(mag_y)

# Graph 4: SMR HRD
axs[1, 1].hist2d(df_smr['teff'], df_smr['M_G'], bins=bins, cmap=cmap, cmin=1, range=[[3000, 10000], [-2, 15]])
axs[1, 1].set_title('Graph 4: Super Metal-Rich Physical HRD ($T_{eff}$)')
axs[1, 1].set_xlabel('Effective Temperature ($T_{eff}$)')
axs[1, 1].set_ylabel('Absolute Magnitude ($M_G$)')
axs[1, 1].set_xlim(hrd_x)
axs[1, 1].set_ylim(mag_y)

plt.tight_layout()
print("Done! Displaying plots...")
plt.show()
