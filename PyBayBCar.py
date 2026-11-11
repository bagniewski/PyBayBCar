"""
DESCRIPTION

This function uses BayBCar PSM calibrations to perform probabilistic forward
and inverse modelling of benthic δ13C.

Depending on the input variables, one of 8 BayBCar formulations will be
selected:

    A3Dp  : 3 predictors (d13C_dic, Depth, Species)
    A3Op  : 3 predictors (d13C_dic, Omega, Species)
    A4DIp : 4 predictors (d13C_dic, Depth, SIC, Species)
    A4DIp : 4 predictors (d13C_dic, Omega, SIC, Species)
    W2D   : 2 predictors (d13C_dic, Depth)
    W2O   : 2 predictors (d13C_dic, Omega)
    W3DI  : 3 predictors (d13C_dic, Depth, SIC)
    W3OI  : 3 predictors (d13C_dic, Omega, SIC)
   
The function also returns the upper and lower bounds of the confidence
interval specified by the user.

For a detailed description of BayBCar PSMs please see:
    Bagniewski, W., Osman, M., Aquino-López, M., Rathburn, A., &
    Muschitiello, F. (2026). BayBCar: A Bayesian calibration model for
    δ13C in benthic foraminifera. Paleoceanography and Paleoclimatology.

Author: Witold Bagniewski
Date: 11/11/2026

-------------------------------------------------------------------------
REQUIRED PACKAGES

    pip install numpy scipy PyCO2SYS
    
PyCO2SYS:    
    When Omega is not provided by the user, the function will attempt to
    calculate it from other available variables using the PyCO2SYS toolbox:
    Humphreys, M. P., Schiller, A. J., Sandborn, D. E., Gregor, L., Pierrot, 
    D., van Heuven, S. M. A. C., Lewis, E. R., and Wallace, D. W. R. (2024).
    PyCO2SYS: marine carbonate system calculations in Python. Zenodo. 
    doi:10.5281/zenodo.3744275.

-------------------------------------------------------------------------
USAGE

Keep BayBCar_calibrations.mat in the same directory as this file (or provide
its path with calibration_file=...).

Function call:
    d13C_pred, upper, lower = PyBayBCar(
        d13C_x, Depth, Omega, SIC, Species, CI,
        DIC, TA, pH, pCO2, T, S, Si, PO4, direction
    )

Forward modelling syntax:
    d13C_cib, upper, lower = PyBayBCar(
        d13C_dic, Depth, Omega, SIC, Species, CI,
        DIC, TA, pH, pCO2, T, S, Si, PO4, direction="forward"
    )
    
Inverse modelling syntax:
    d13C_dic, upper, lower = PyBayBCar(
        d13C_cib, Depth, Omega, SIC, Species, CI,
        DIC, TA, pH, pCO2, T, S, Si, PO4, direction="inverse"
    )

Use 'None' to skip arguments, for example:
    d13C_cib,upper,lower = PyBayBCar(d13C_dic,Depth,None,SIC,None,0.75)

Prediction direction ("forward" or "inverse") can be specified with the 
'direction' argument. When not specified, "forward" is used. Example:
    d13C_dic,upper,lower = PyBayBCar(d13C_cib,None,Omega,direction="inverse")

Required Inputs:
    d13C_x : First input argument, represents either d13C_dic (in forward 
             modelling) or d13C_cib (in inverse modelling):
     - d13C_dic : d13C of dissolved inorganic carbon (permil)
     - d13C_cib : d13C of Cibicidoides foraminifera (permil, C. wuellerstorfi
                  by default)
    At least one of these:
     - Depth : Water depth (meters)
     - Omega : Calcite saturation state

Optional Inputs:
    Depth     : Water depth (meters)
    Omega     : Calcite saturation state
    SIC       : Summer sea ice concentration (decimal)
    Species   : Foraminiferal species. 1 = C. spp; 2 (default) = C. 
                wuellerstorfi; 3 = C. kullenbergi; 4 = C. lobatulus; 
                5 = C. pachyderma; 6 = C. floridanus; 7 = C. mckannai
    CI        : Confidence interval in decimal format. 
                0.95 (default) = 95% CI.
    direction : Direction of prediction. "forward" (default) = forward 
                modelling to predict d13C_cib; "inverse" = inverse modelling 
                to predict d13C_dic.

Optional PyCO2SYS inputs for calculating Omega (at least two of these are 
required: DIC, TA, pH, pCO2):
    DIC       : Dissolved inorganic carbon (µmol/kg)
    TA        : Total alkalinity (µmol/kg)
    pH        : pH
    pCO2      : pCO2 (µatm)
    T         : Temperature (Celsius)
    S         : Salinity
    Si        : Silicate (µmol/kg)
    PO4       : Phosphate (µmol/kg)

Output:
    d13C_pred   : represents either d13C_cib (in forward modelling) or d13C_dic
                (in inverse modelling)
     - d13C_cib : d13C of Cibicidoides foraminifera (permil, C. wuellerstorfi
                  by default)
     - d13C_dic : d13C of dissolved inorganic carbon (permil)
    upper    : upper bound of the confidence interval (95% by default)
    lower    : lower bound of the confidence interval (95% by default)

-------------------------------------------------------------------------
EXAMPLES

# Install dependencies
    pip install numpy scipy PyCO2SYS

# Sample data:
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

# Forward modelling 
# Example 1: W2D model
    d13C_cib1,upper1,lower1 = PyBayBCar(d13C_dic,Depth)
# Example 2: A4OIp model
    d13C_cib2,upper2,lower2 = PyBayBCar(d13C_dic,Depth,Omega,SIC,1)
# Example 3: A4OIp model using PyCO2SYS
    d13C_cib3,upper3,lower3 = PyBayBCar(d13C_dic,Depth,None,SIC,1,None,DIC,TA)
    
# Inverse modelling
# Example 4: A4OIp model
    d13C_dic4,upper4,lower4 = PyBayBCar(d13C_cib,Depth,Omega,SIC,1,
                                        direction="inverse")

"""

from pathlib import Path

import numpy as np
from scipy.io import loadmat
from scipy.stats import t as student_t


def _make_vector(value, name, n, default=None):
    """Convert an input to a column-vector equivalent and expand scalars."""
    if value is None:
        value = default
    if value is None:
        return None

    value = np.asarray(value, dtype=float)
    if value.ndim == 0 or value.size == 1:
        return np.full(n, float(value.reshape(-1)[0]))

    value = value.reshape(-1)
    if value.size != n:
        raise ValueError(
            f"{name} must be a scalar or contain {n} values; "
            f"received {value.size}."
        )
    return value


def _load_PSMs(calibration_file):
    """Load the calibrated PSM parameters from BayBCar_calibrations.mat."""
    calibration_file = Path(calibration_file).expanduser()

    if not calibration_file.is_file():
        raise FileNotFoundError(
            f"Calibration file not found: {calibration_file.resolve()}\n"
            "Place BayBCar_calibrations.mat beside PyBayBCar.py or specify "
            "calibration_file='path/to/BayBCar_calibrations.mat'."
        )

    PSMs = loadmat(calibration_file, squeeze_me=True, struct_as_record=False)
    return PSMs


def _calculate_Omega_calcite(
    Depth, DIC, TA, pH, pCO2, T, S, Si, PO4
):
    """Calculate Omega calcite using PyCO2SYS when two inputs are available."""
    import PyCO2SYS as pyco2

    # Identify the first available pair.
    carbonate_parameters = {
        "DIC": DIC,
        "TA": TA,
        "pH": pH,
        "pCO2": pCO2,
    }
    parameter_pairs = [
        ("TA", "DIC", 1, 2),
        ("TA", "pH", 1, 3),
        ("DIC", "pH", 2, 3),
        ("TA", "pCO2", 1, 4),
        ("DIC", "pCO2", 2, 4),
        ("pH", "pCO2", 3, 4),
    ]

    for name1, name2, type1, type2 in parameter_pairs:
        if (
            carbonate_parameters[name1] is not None
            and carbonate_parameters[name2] is not None
        ):
            # pH scale = Total; K1/K2 = Lueker et al. (2000);
            # KSO4 = Dickson (1990); KF = Perez & Fraga (1987);
            # total borate = Lee et al. (2010).
            Co2s = pyco2.sys(
                par1=carbonate_parameters[name1],
                par2=carbonate_parameters[name2],
                par1_type=type1,
                par2_type=type2,
                salinity=S,
                temperature=20,
                temperature_out=T,
                pressure=0,
                pressure_out=Depth,
                total_silicate=Si,
                total_phosphate=PO4,
                opt_pH_scale=1,
                opt_k_carbonic=10,
                opt_k_bisulfate=1,
                opt_k_fluoride=2,
                opt_total_borate=2,
            )

            if "saturation_calcite_out" in Co2s:
                Omega = np.asarray(
                    Co2s["saturation_calcite_out"], dtype=float
                ).reshape(-1)
            elif "OmegaCAout" in Co2s:
                Omega = np.asarray(Co2s["OmegaCAout"], dtype=float).reshape(-1)
            else:
                raise KeyError(
                    "PyCO2SYS did not return Omega calcite. "
                    f"Available output keys: {list(Co2s.keys())}"
                )
            return Omega

    return None


def PyBayBCar(
    d13C_x,
    Depth=None,
    Omega=None,
    SIC=None,
    Species=None,
    CI=None,
    DIC=None,
    TA=None,
    pH=None,
    pCO2=None,
    T=None,
    S=None,
    Si=None,
    PO4=None,
    direction="forward",
    calibration_file=None,
):
    ##
    ## Preprocessing the variables
    ##
    
    d13C_x = np.asarray(d13C_x, dtype=float)
    if d13C_x.size == 0:
        raise ValueError("Error. d13C_x is not provided")
    d13C_x = d13C_x.reshape(-1)
    n = d13C_x.size

    # Check prediction direction.
    if direction not in ("forward", "inverse"):
        raise ValueError('Error. Direction must be either "forward" or "inverse"')

    # Default values.
    if Species is None:
        Species = 2  # C. wuellerstorfi
    if CI is None:
        CI = 0.95  # 95% CI

    # Make sure all variables are column-vector equivalents and expand
    # scalar variables to match d13C_x.
    Depth = _make_vector(Depth, "Depth", n)
    Omega = _make_vector(Omega, "Omega", n)
    SIC = _make_vector(SIC, "SIC", n)
    Species = _make_vector(Species, "Species", n)
    DIC = _make_vector(DIC, "DIC", n)
    TA = _make_vector(TA, "TA", n)
    pH = _make_vector(pH, "pH", n)
    pCO2 = _make_vector(pCO2, "pCO2", n)

    # Default carbonate-system conditions.
    T = _make_vector(T, "T", n, default=4)
    S = _make_vector(S, "S", n, default=35)
    Si = _make_vector(Si, "Si", n, default=1)
    PO4 = _make_vector(PO4, "PO4", n, default=1)

    if not (0 < float(CI) < 1):
        raise ValueError("CI must be between 0 and 1.")

    ##
    ## If Omega is not available, attempt to calculate it using PyCO2SYS
    ##
    
    if Omega is None and Depth is not None:
        if sum(value is not None for value in (DIC, TA, pH, pCO2)) >= 2:
            Omega = _calculate_Omega_calcite(
                Depth, DIC, TA, pH, pCO2, T, S, Si, PO4
            )

    ##
    ## BayBCar modelling
    ##
    
    # Output NaNs if neither Omega nor Depth are available.
    if Omega is None and Depth is None:
        d13C_pred = np.full(n, np.nan)
        upper = np.full(n, np.nan)
        lower = np.full(n, np.nan)
        return d13C_pred, upper, lower

    # Load calibrated PSM parameters.
    if calibration_file is None:
        calibration_file = Path(__file__).with_name(
            "BayBCar_calibrations.mat"
        )
    PSMs = _load_PSMs(calibration_file)

    # W3OI
    if Omega is not None and SIC is not None and np.all(Species == 2):
        PSM_name = "W3OI"
        mu = np.asarray(PSMs["mu_W3OI"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_W3OI"], dtype=float)
        a = float(PSMs["a_W3OI"])
        b = float(PSMs["b_W3OI"])
        X = np.column_stack((np.ones(n), d13C_x, np.log(Omega), SIC))

    # W3DI
    elif (
        Omega is None and SIC is not None and Depth is not None
        and np.all(Species == 2)
    ):
        PSM_name = "W3DI"
        mu = np.asarray(PSMs["mu_W3DI"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_W3DI"], dtype=float)
        a = float(PSMs["a_W3DI"])
        b = float(PSMs["b_W3DI"])
        X = np.column_stack((np.ones(n), d13C_x, Depth, SIC))

    # W2O
    elif Omega is not None and SIC is None and np.all(Species == 2):
        PSM_name = "W2O"
        mu = np.asarray(PSMs["mu_W2O"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_W2O"], dtype=float)
        a = float(PSMs["a_W2O"])
        b = float(PSMs["b_W2O"])
        X = np.column_stack((np.ones(n), d13C_x, np.log(Omega)))

    # W2D
    elif (
        Omega is None and SIC is None and Depth is not None
        and np.all(Species == 2)
    ):
        PSM_name = "W2D"
        mu = np.asarray(PSMs["mu_W2D"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_W2D"], dtype=float)
        a = float(PSMs["a_W2D"])
        b = float(PSMs["b_W2D"])
        X = np.column_stack((np.ones(n), d13C_x, Depth))

    # A4OIp
    elif Omega is not None and SIC is not None and np.any(Species != 2):
        PSM_name = "A4OIp"
        mu = np.asarray(PSMs["mu_A4OIp"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_A4OIp"], dtype=float)
        a = float(PSMs["a_A4OIp"])
        b = float(PSMs["b_A4OIp"])

        X_Species = np.zeros((n, 7))
        species_codes = Species.astype(int)
        if np.any(species_codes < 1) or np.any(species_codes > 7):
            raise ValueError("Species must be integers from 1 to 7.")
        X_Species[np.arange(n), species_codes - 1] = 1
        X = np.column_stack(
            (np.ones(n), d13C_x, np.log(Omega), SIC,
             X_Species[:, [0, 2, 3, 4, 5, 6]])
        )

    # A4DIp
    elif (
        Omega is None and SIC is not None and Depth is not None
        and np.any(Species != 2)
    ):
        PSM_name = "A4DIp"
        mu = np.asarray(PSMs["mu_A4DIp"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_A4DIp"], dtype=float)
        a = float(PSMs["a_A4DIp"])
        b = float(PSMs["b_A4DIp"])

        X_Species = np.zeros((n, 7))
        species_codes = Species.astype(int)
        if np.any(species_codes < 1) or np.any(species_codes > 7):
            raise ValueError("Species must be integers from 1 to 7.")
        X_Species[np.arange(n), species_codes - 1] = 1
        X = np.column_stack(
            (np.ones(n), d13C_x, Depth, SIC,
             X_Species[:, [0, 2, 3, 4, 5, 6]])
        )

    # A3Op
    elif Omega is not None and SIC is None and np.any(Species != 2):
        PSM_name = "A3Op"
        mu = np.asarray(PSMs["mu_A3Op"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_A3Op"], dtype=float)
        a = float(PSMs["a_A3Op"])
        b = float(PSMs["b_A3Op"])

        X_Species = np.zeros((n, 7))
        species_codes = Species.astype(int)
        if np.any(species_codes < 1) or np.any(species_codes > 7):
            raise ValueError("Species must be integers from 1 to 7.")
        X_Species[np.arange(n), species_codes - 1] = 1
        X = np.column_stack(
            (np.ones(n), d13C_x, np.log(Omega),
             X_Species[:, [0, 2, 3, 4, 5, 6]])
        )

    # A3Dp
    elif (
        Omega is None and SIC is None and Depth is not None
        and np.any(Species != 2)
    ):
        PSM_name = "A3Dp"
        mu = np.asarray(PSMs["mu_A3Dp"], dtype=float).reshape(-1)
        Sigma = np.asarray(PSMs["Sigma_A3Dp"], dtype=float)
        a = float(PSMs["a_A3Dp"])
        b = float(PSMs["b_A3Dp"])

        X_Species = np.zeros((n, 7))
        species_codes = Species.astype(int)
        if np.any(species_codes < 1) or np.any(species_codes > 7):
            raise ValueError("Species must be integers from 1 to 7.")
        X_Species[np.arange(n), species_codes - 1] = 1
        X = np.column_stack(
            (np.ones(n), d13C_x, Depth,
             X_Species[:, [0, 2, 3, 4, 5, 6]])
        )

    else:
        raise ValueError(
            "The supplied variables do not correspond " 
            "to any of the BayBCar model variants."
        )

    if Omega is not None and np.any(Omega <= 0):
        raise ValueError("Omega must be positive because log(Omega) is used.")

    if X.shape[1] != mu.size:
        raise ValueError(
            f"{PSM_name}: X has {X.shape[1]} columns, "
            "but mu has {mu.size} coefficients."
        )

    # Forward or inverse modelling.
    if direction == "forward":
        d13C_pred = X @ mu

    elif direction == "inverse":
        columns_other_than_d13C = np.arange(X.shape[1]) != 1
        d13C_pred = (
            d13C_x - X[:, columns_other_than_d13C]
            @ mu[columns_other_than_d13C]
        ) / mu[1]

    ##
    ## Confidence interval
    ##
    
    if direction == "forward":
        # Calculate variance.
        Var = (b / a) * (1 + np.diag(X @ Sigma @ X.T))

    elif direction == "inverse":
        # Jacobian of the inverse prediction with respect to coefficients.
        J = np.zeros_like(X)
        J[:, 1] = -d13C_pred / mu[1]
        columns_other_than_d13C = np.arange(X.shape[1]) != 1
        J[:, columns_other_than_d13C] = (
            -X[:, columns_other_than_d13C] / mu[1]
        )

        # Propagation of uncertainty.
        Var = (b / a) * (
            1 / mu[1] ** 2 + np.diag(J @ Sigma @ J.T)
        )

    # Confidence intervals using Student's t-distribution.
    alpha = 1 - CI
    tval = student_t.ppf(1 - alpha / 2, df=2 * a)
    halfCI = tval * np.sqrt(np.maximum(Var, 0))
    upper = d13C_pred + halfCI
    lower = d13C_pred - halfCI

    return d13C_pred, upper, lower
