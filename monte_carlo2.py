import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Example: define inputs
n_simulations = 10000
plant_size = 1000 #t/d waste
# got to size the plant to calculate the capex, our literature base the capex off of 
# plant elec generation capacity and this depends on the following inputs which 
# are literature averages
cal_val_waste_assume = 10 #GJ/t waste
elec_effic_assume = 0.25 #% overall plant efficiency
cap_fac_assumed = 0.85 
plant_power_rating = plant_size * cal_val_waste_assume * elec_effic_assume * cap_fac_assumed * 365.25 #GJ/y
plant_power_rating = plant_power_rating / 3.6 #MWh/y
print(plant_power_rating)
capex = np.random.normal(loc=168831666, scale= 23022500.00, size=n_simulations) # USD. taken from excel
opex = np.random.normal(loc= 16883166.67, scale= 2302250.00 , size=n_simulations) #USD/y

# calculate the cash flow
cal_val_waste = np.random.normal(loc=10, scale=2.5, size=n_simulations) #GJ/t waste
elec_effic = np.random.normal(loc = 0.25, scale= 0.05, size= n_simulations) #% overall plant efficiency
cap_fac = np.random.normal(loc = 0.841, scale= 0.0822, size= n_simulations) 
elec_tarrif = 0.64/3.62 # USD/kWh
elec_prod_MWh_y = cal_val_waste * plant_size * elec_effic * 365 * cap_fac/3.6 #GJ/t * t/d * effic * d/y * cap_fac * MWh/GJ
elec_prod_kWh_y = elec_prod_MWh_y * 1000
revenue = elec_prod_kWh_y *elec_tarrif
print(np.average(revenue))

# Simple NPV calculation 
discount_rate = 0.07
plant_life = 22.5 # from literature average
npv = -capex + np.sum([(revenue - opex) / (1 + discount_rate)**t for t in np.arange(1, plant_life+1.00, 1)], axis=0)

# Plot the histogram
plt.hist(npv, bins=50, edgecolor='k')
plt.xlabel('NPV ($)')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation of NPV')
plt.show()
