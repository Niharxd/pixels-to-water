# Wageningen Environmental Research
# swap.wur.nl
# H.M. Mulder
#------------------------------------------------

# set start of program
TIMPRGSTART <- Sys.time()

# --- load arguments ---

# set modus
test <- FALSE

if (!test) {
  command_args <- commandArgs(trailingOnly = TRUE)
  if (length(command_args) != 1) stop("wrong usage of arguments\n\narguments needed: \n- controlfile")
} else {
  setwd("c:/SWAP")
  command_args <- NULL
  command_args[1] <- "control_meteo.inp"
}

# set arguments
ctrl <- command_args[1]

# --- load libraries ---

source("../../tools/R/libraries.R")

# --- initial part of procedure ---

if(!interactive()) pdf(NULL)

message("\nProgram R-PROG started...\n")

# --- main part of procedure ---

# create plot
create_precipitation_SWAP(ctrl = ctrl)

# --- return part of procedure ---

TIMPRGEND <- Sys.time()
TIMPRGCALC <- as.numeric(difftime(time1 = TIMPRGEND, time2 = TIMPRGSTART, units = "secs"))
message(paste0("\nProgram R-PROG successfully ended in ", floor(TIMPRGCALC / 60), " minutes and ", ceiling(TIMPRGCALC %% 60), " seconds"))
q(save = "no")
