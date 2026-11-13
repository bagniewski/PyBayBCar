# PyBayBCar

BayBCar is a class of Bayesian proxy system models (PSMs) for benthic δ13C, incorporating the effects of carbonate chemistry, sea ice concentration, and species-specific differences. 

This repository contains a Python function, which enables probabilistic forward and inverse modelling of benthic foraminiferal δ13C and δ13C of DIC, respectively. PyBayBCar is a Python implementation of [BayBCar](https://github.com/bagniewski/BayBCar), originally written for MATLAB.

Depending on the input variables, one of 8 BayBCar formulations will be selected:
* A3Dp: 3 predictors (δ13C_dic, Depth, Species)
* A3Op: 3 predictors (δ13C_dic, Omega, Species)
* A4DIp: 4 predictors (δ13C_dic, Depth, SIC, Species)
* A4DIp: 4 predictors (δ13C_dic, Omega, SIC, Species)
* W2D: 2 predictors (δ13C_dic, Depth)
* W2O: 2 predictors (δ13C_dic, Omega)
* W3DI: 3 predictors (δ13C_dic, Depth, SIC)
* W3OI: 3 predictors (δ13C_dic, Omega, SIC)  

For a detailed description of BayBCar PSMs please see: Bagniewski, W., Osman, M., Aquino-López, M., Rathburn, A., & Muschitiello, F. (in press). BayBCar: A Bayesian calibration model for δ13C in benthic foraminifera. *Paleoceanography and Paleoclimatology*.

## External dependencies

* [PyCO2SYS](https://zenodo.org/records/23009807) - calculates Omega from available variables if not provided by the user. BayBCar will work without it by defaulting to a formulation that uses depth in place of Omega.

## Files

* **PyBayBCar.py**: a Python function that selects the appropriate BayBCar calibration based on input data provided by the user and performs probabilistic forward and inverse modelling of benthic δ13C. 

* **BayBCar_calibrations.mat**: a data file used by **PyBayBCar.py**, containing the calibrated BayBCar parameters.

## Usage

### Syntax
* Forward modelling:
```
d13C_cib, upper, lower = PyBayBCar(
        d13C_dic, Depth, Omega, SIC, Species, CI,
        DIC, TA, pH, pCO2, T, S, Si, PO4, direction="forward"
    )
```
* Inverse modelling:
```
d13C_dic, upper, lower = PyBayBCar(
        d13C_cib, Depth, Omega, SIC, Species, CI,
        DIC, TA, pH, pCO2, T, S, Si, PO4, direction="inverse"
    )
```
Use `None` to skip arguments, for example:
`d13C_cib,upper,lower = PyBayBCar(d13C_dic,Depth,None,SIC,None,0.75)`

Prediction direction (`"forward"` or `"inverse"`) can be specified as the `direction` argument. When not specified, `"forward"` is used. Example:
`d13C_dic,upper,lower = PyBayBCar(d13C_cib,None,Omega,direction="inverse")`

### Required Inputs
- `d13C_x`: First input argument, represents either d13C_dic (in forward modelling) or d13C_cib (in inverse modelling):
  - `d13C_dic`: δ13C of dissolved inorganic carbon (permil)
  - `d13C_cib`: δ13C of Cibicidoides foraminifera (permil, C. wuellerstorfi by default)
- At least one of these:
  - `Depth`: Water depth (meters)
  - `Omega`: Calcite saturation state

### Optional Inputs
- `Depth`: Water depth (meters)  
- `Omega`: Calcite saturation state  
- `SIC`: Summer sea ice concentration (decimal)  
- `Species`: Foraminiferal species. 1 = C. spp; 2 (default) = C. wuellerstorfi; 3 = C. kullenbergi; 4 = C. lobatulus; 5 = C. pachyderma; 6 = C. floridanus; 7 = C. mckannai
- `CI`: Confidence interval in decimal format. 0.95 (default) = 95% CI.
- `direction`: Direction of prediction. "forward" (default) = forward modelling to predict d13C_cib; "inverse" = inverse modelling to predict d13C_dic.

### Optional CO2SYS inputs for calculating Omega (at least two of these are required: DIC, TA, pH, pCO2)
- `DIC`: Dissolved inorganic carbon (µmol/kg)  
- `TA`: Total alkalinity (µmol/kg)  
- `pH`: pH  
- `pCO2`: pCO2 (µatm)  
- `T`: Temperature (Celsius)  
- `S`: Salinity  
- `Si`: Silicate (µmol/kg)  
- `PO4`: Phosphate (µmol/kg)  

### Output
- `d13C_pred`: represents either d13C_cib (in forward modelling) or d13C_dic (in inverse modelling)
  - `d13C_cib`: δ13C of Cibicidoides foraminifera (permil, C. wuellerstorfi by default)
  - `d13C_dic`: δ13C of dissolved inorganic carbon (permil)  
- `upper`: upper bound of the confidence interval (95% by default)  
- `lower`: lower bound of the confidence interval (95% by default)

## Examples

Sample data:
```
import numpy as np
time = np.linspace(1, 10, num=10)
d13C_dic = np.array([0.43, 0.43, 0.42, 0.40, 0.41, 
		     0.33, 0.33, 0.30, 0.22, 0.31])
Omega = np.array([0.85, 0.83, 0.81, 0.82, 0.80, 
		  0.70, 0.71, 0.70, 0.68, 0.66])
SIC = 0.1
Depth = 3420
DIC = np.array([2255, 2250, 2255, 2251, 2264, 
                2265, 2270, 2276, 2280, 2278])
TA = np.array([2365, 2361, 2366, 2361, 2374, 
               2377, 2380, 2386, 2393, 2397])
# Sample d13C_cib data for inverse modelling:
d13C_cib = np.array([0.33, 0.33, 0.32, 0.30, 0.31, 
                     0.23, 0.23, 0.20, 0.12, 0.21])
```

### Forward modelling

Example 1: W2D model
```
d13C_cib1,upper1,lower1 = PyBayBCar(d13C_dic,Depth)
```
Example 2: A4OIp model. Using `PyBayBCar(d13C_dic,None,Omega,SIC,1)` gives identical result.
```
d13C_cib2,upper2,lower2 = PyBayBCar(d13C_dic,Depth,Omega,SIC,1)
```
Example 3: A4OIp model using CO2SYS
```
d13C_cib3,upper3,lower3 = PyBayBCar(d13C_dic,Depth,None,SIC,1,None,DIC,TA)
```
Plot the forward modelled d13C_cib from the 3 examples above:
```
import matplotlib.pyplot as plt
plt.figure()
plt.plot(time, d13C_cib1, 'o-r', label='W2D')
plt.fill_between(time, lower1, upper1, color='r', alpha=0.15)
plt.plot(time, d13C_cib2, 'o-b', label='A4OIp')
plt.fill_between(time, lower2, upper2, color='b', alpha=0.15)
plt.plot(time, d13C_cib3, 'o-k', label='A4OIp (CO2SYS)')
plt.fill_between(time, lower3, upper3, color='k', alpha=0.15)
plt.xlabel('time')
plt.ylabel(r'Forward modelled d13C_cib')
plt.legend()
plt.show()
```

### Inverse modelling

Example 4: A4OIp model
```
d13C_dic4,upper4,lower4 = PyBayBCar(d13C_cib,Depth,Omega,SIC,1,direction="inverse")
```
Plot the inverse modelled d13C_dic:
```
import matplotlib.pyplot as plt
plt.figure()
plt.plot(time, d13C_dic4, 'o-b', label='A4OIp')
plt.fill_between(time, lower4, upper4, color='b', alpha=0.15)
plt.xlabel('time')
plt.ylabel(r'Inverse modelled d13C_dic')
plt.legend()
plt.show()
```
