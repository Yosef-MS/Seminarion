import numpy as np
import matplotlib.pyplot as plt

# Number of simulations
n_simulations = 10000
plant_size = 1000  # tonnes/day

# Fixed parameters
cal_val_waste_assume = 10  # GJ/t
elec_effic_assume = 0.25
cap_fac_assumed = 0.85

# Plant power rating (MWh/year)
plant_power_rating = (plant_size * cal_val_waste_assume * elec_effic_assume *
                      cap_fac_assumed * 365.25) / 3.6
print("Plant power rating (MWh/y):", plant_power_rating)

# CAPEX and OPEX
capex = np.random.normal(loc=585, scale=206, size=n_simulations) * plant_size * cap_fac_assumed*365 #USD/t*y * t/d * d/y
opex = capex/10

# Variable assumptions
cal_val_waste = np.random.normal(loc=10, scale=2.5, size=n_simulations)
elec_effic = np.random.normal(loc=0.25, scale=0.05, size=n_simulations)
cap_fac = np.random.normal(loc=0.841, scale=0.0822, size=n_simulations)

# Revenue
elec_tariff = 0.64 / 3.62  # USD/kWh
elec_prod_MWh_y = cal_val_waste * plant_size * elec_effic * 365 * cap_fac / 3.6
elec_prod_kWh_y = elec_prod_MWh_y * 1000
revenue = elec_prod_kWh_y * elec_tariff
print("Average annual revenue (USD):", np.mean(revenue))

# NPV calculation
discount_rate = np.random.normal(loc=0.065, scale=0.035, size=n_simulations)
plant_life = 22
npv = -capex + np.sum(
    [(revenue - opex) / (1 + discount_rate)**t for t in range(1, plant_life + 1)],
    axis=0
)

# Percent above/below zero
pct_above = 100 * np.sum(npv > 0) / n_simulations
pct_below = 100 - pct_above

# Create bins with one edge at NPV = 0
bin_width = (np.max(npv) - np.min(npv)) / 30
left_edge = np.floor(np.min(npv) / bin_width) * bin_width
right_edge = np.ceil(np.max(npv) / bin_width) * bin_width
bins = np.arange(left_edge, right_edge + bin_width, bin_width)

# Shift bins so that 0 is exactly a bin edge
zero_offset = 0 - (left_edge % bin_width)
bins = np.arange(left_edge - zero_offset, right_edge + bin_width, bin_width)

# Histogram
counts, bins, patches = plt.hist(npv, bins=bins, edgecolor='black')

# Color bars
for bin_left, bin_right, patch in zip(bins[:-1], bins[1:], patches):
    if bin_left < 0:
        patch.set_facecolor('red')
    else: 
        patch.set_facecolor('green')
   
# Plot formatting
plt.axvline(x=0, color='black', linestyle='--', label='NPV = 0')
plt.xlabel("Net Present Value (USD)")
plt.ylabel("Frequency")
plt.title("NPV - 2000 t/d")
plt.legend()

# Add bold percentage text in plot
plt.text(0.98, 0.95, f"{pct_above:.1f}% above 0",
         color='green', weight='bold', ha='right', transform=plt.gca().transAxes)
plt.text(0.98, 0.90, f"{pct_below:.1f}% below 0",
         color='red', weight='bold', ha='right', transform=plt.gca().transAxes)

plt.grid(True)
plt.tight_layout()
plt.show()
