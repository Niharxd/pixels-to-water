# libraries.R
# Wageningen Environmental Research
# H.M. Mulder
#________________________________________________
#

# --- initial part of procedure ---

# R-repository
repos_CRAN <- "https://cloud.r-project.org/"             # default CRAN-repository
repos_LOCAL <- "file:../../tools/R/local"                # path to LOCAL-repository

# install settings
dir_pkg <- NULL                                          # directory additional R-packages; in case of default R settings use 'NULL'
online <- TRUE                                           # online modus (should be TRUE if additional R-packages need to be installed)
update <- TRUE                                           # check for package updates

# set packages to load
pkg_load <- c("fs", "stringr", "readr", "progress", "controlR", "KNMItools", "SWAPtools")

# --- main part of procedure ---

if (update & !online) stop("can not check for updates if offline!")

# set repository
options(repos = c(repos_CRAN, repos_LOCAL))

# create local directory (optional)
if (!is.null(dir_pkg)) {
  dir.create(path = dir_pkg, recursive = TRUE, showWarnings =  FALSE)
  dir_pkg <- normalizePath(dir_pkg)
  Sys.setenv(R_LIBS = dir_pkg)
} else {
  dir_pkg <- Sys.getenv("R_LIBS")
  if (dir_pkg[1] == "") dir_pkg <- .libPaths()[1]
}

# set CRAN mirror in case packages need to be installed
if (online) {
  CRAN_mirrors <- getCRANmirrors()
  rec <- match(repos_CRAN,CRAN_mirrors$URL)
  if (all(is.na(rec))) stop(paste("\nUnable to select CRANmirror: ", repos_CRAN, sep=""))
  chooseCRANmirror(ind = rec[!is.na(rec)][1])
}

# try to update R-packages (before installing required packages)
if (online & update) {

  message("\nUpdate packages...")
  
  # list of installed packages
  pkg_installed <- installed.packages()[, "Package"]

  # list of dependency packages
  pkg_depend <- unique(c(unlist(tools::package_dependencies(packages = pkg_load)), pkg_load))

  # update required CRAN-packages
  pkg_check <- pkg_depend[pkg_depend %in% pkg_installed]
  pkg_update <- pkg_check[pkg_check %in% old.packages(repos = repos_CRAN)[, "Package"]]
  if (length(pkg_update) > 0) update.packages(lib.loc = dir_pkg, repos = repos_CRAN, oldPkgs = pkg_update, ask = FALSE)
  
  # update required LOCAL-packages
  if (!is.null(repos_LOCAL)) {
    pkg_update <- pkg_check[pkg_check %in% old.packages(repos = repos_LOCAL)[, "Package"]]
    if (length(pkg_update) > 0) update.packages(lib.loc = dir_pkg, repos = repos_LOCAL, oldPkgs = pkg_update, ask = FALSE)
  }
}

message("\nLoad packages...")

# loop over packages
for (s_pkg in pkg_load) {
  if (suppressWarnings(suppressPackageStartupMessages(require(package = s_pkg, lib.loc = dir_pkg, character.only = TRUE, warn.conflicts = FALSE, quietly = TRUE)))) {
    message(paste0("- package '", s_pkg, "' loaded"))
  } else {
    if (!online) {
      stop(paste0("failed to load package: ", s_pkg))
    } else {
      suppressWarnings(suppressPackageStartupMessages(install.packages(pkg = s_pkg, dependencies = TRUE, lib = dir_pkg, quiet = TRUE)))
      if (suppressWarnings(suppressPackageStartupMessages(require(package = s_pkg, lib.loc = dir_pkg, character.only = TRUE, warn.conflicts = FALSE, quietly = TRUE)))) {
        message(paste0("- package '", s_pkg, "' installed"))
      } else {
        stop(paste0("failed to install package: ", s_pkg))
      }
    }
  }
}

# check if update are available after installing
if (online) {
  df_update <- data.frame(old.packages())
  pkg_update <- df_update[rownames(df_update) %in% pkg_load, "Package"]
  if (length(pkg_update)) {
    message("\nUpdate available for package:")
    message(paste0("- package '", pkg_update, "' version ", df_update[pkg_update, "Installed"], " installed (", df_update[pkg_update, "ReposVer"], " available)\n"))
  }
}
