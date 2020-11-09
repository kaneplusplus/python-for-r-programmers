
# Install reticulate if it's not already there.
if (!require(reticulate)) {
  install.packages("reticulate")
}

library(reticulate)

# Install miniconda.
install_miniconda()

# Install a newer version.
conda_install(python_version = "3.6",
              envname="python-for-r-developers",
              packages = c("numpy", "pandas", "seaborn", 
                           "plotnine", "statsmodels"))

use_condaenv("python-for-r-developers", required = TRUE)

# List the available conda environments.
conda_list()

# Install extra packages like this - after use_condaenv() has been called.
#py_install("pandas")

# See your current setup.
py_config()
