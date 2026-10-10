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
  command_args[1] <- "control.inp"
}

# set arguments
ctrl <- command_args[1]

# --- load libraries ---

source("../../tools/R/libraries.R")

# --- initial part of procedure ---

quiet <- TRUE

message("\nProgram R-PROG started...\n")

# load controlfile
text <- read_lines(file = ctrl, progress = FALSE)

file_sql <- get_record(text = text, item = "FILSQL")

pre_process <- get_switch(text = text, item = "PREPROCESS")
if (pre_process) {
  file_xls <- get_record(text = text, item = "FILXLS")
}

run_id <- NULL
main_process <- get_switch(text = text, item = "MAINPROCESS")
post_process <- get_switch(text = text, item = "POSTPROCESS")
if (main_process | post_process) {
  dir_run <- get_dir(text = text, item = "DIRRUN", create = FALSE)
  run_id <- get_record(text = text, item = "RUNID")

  zip_output <- get_switch(text = text, item = "ZIP", item_exists= FALSE, default = TRUE)
}

if (main_process) {
  command <- get_record(text = text, item = "PRGSWP")
  tmplt_swp <- get_record(text = text, item = "FILSWP")
  tmplt_dra <- get_record(text = text, item = "FILDRA", item_exists = FALSE)
  tmplt_bbc <- get_record(text = text, item = "FILBBC", item_exists = FALSE)
  tmplt_irg <- get_record(text = text, item = "FILIRG", item_exists = FALSE)

  dir_crp <- get_record(text = text, item = "DIRCRP", item_exists = FALSE)
  dir_met <- get_record(text = text, item = "DIRMET")
  dir_atm <- get_record(text = text, item = "DIRATM", item_exists = FALSE)
  dir_ini <- get_record(text = text, item = "DIRINI", item_exists = FALSE)
  dir_dra <- get_record(text = text, item = "DIRDRA", item_exists = FALSE)
  dir_bbc <- get_record(text = text, item = "DIRBBC", item_exists = FALSE)
  dir_irg <- get_record(text = text, item = "DIRIRG", item_exists = FALSE)

  create_input <- get_switch(text = text, item = "CREATE", item_exists= FALSE, default = TRUE)
  create_output <- get_switch(text = text, item = "RUN", item_exists= FALSE, default = TRUE)
}

if (post_process) {
  dir_fig <- get_dir(text = text, item = "DIRFIG", create = FALSE)
  dir_obs <- get_dir(text = text, item = "DIROBS", item_exists = FALSE, create = FALSE)
  dir_out <- get_dir(text = text, item = "DIROUT")
}

# --- main part of procedure ---

# pre process

if (pre_process) {

  message(str_c("\nCreate SQL-database...\n"))

  create_database_SWAP(file_xls = file_xls, file_sql = file_sql, quiet = quiet)
}

# main process

if (main_process || post_process) {
  # set run_id
  if (!is.null(run_id)) {
    if (run_id == "ALL") {
      run_id <- get_run_id_CTRL(text = text)
    } else {
      run_id <- string_sequence(string = run_id)
    }
  }
}

if (main_process) {

  message(str_c("\nSimulate SWAP runs...\n"))

  # run SWAP
  pb <- progress_bar$new(total = length(run_id) + 1, format = " SWAP run: :what (:percent)", clear = TRUE)
  for (s_run_id in run_id) {

    # set progress
    pb$tick(tokens = list(what = s_run_id))    

    # set swp-file
    file_swp <- str_c(dir_run, "/run_", str_run_id(run_id = s_run_id), "/swap.swp")

    # prepare swap run
    if (create_input) create_SWAP(file_swp = file_swp, file_sql = file_sql, run_id = s_run_id, tmplt_swp = tmplt_swp, dir_met = dir_met, dir_atm = dir_atm, dir_ini = dir_ini, dir_crp = dir_crp, dir_dra = dir_dra, dir_bbc = dir_bbc, dir_irg = dir_irg, tmplt_dra = tmplt_dra, tmplt_bbc = tmplt_bbc, tmplt_irg = tmplt_irg, quiet = quiet)

    # execute swap
    
    if (create_output) {
      run_SWAP(command = command, file_swp = file_swp, file_sql = file_sql, run_id = s_run_id, quiet = quiet)
      if (zip_output) zip_SWAP(file_swp = file_swp, glob = "*.swp|*.dra|*.bbc|*.crp|*.csv|*.end|*.ok", file_sql = file_sql, run_id = s_run_id)
    }

    # end progress
    if (s_run_id == run_id[length(run_id)]) pb$tick(tokens = list(what = s_run_id))
  }
}

# post process

if (post_process) {

  message(str_c("\nAnalyse SWAP runs...\n"))

  # analyse SWAP
  pb <- progress_bar$new(total = length(run_id) + 1, format = " SWAP run: :what (:percent)", clear = TRUE)
  for (s_run_id in run_id) {

    # set progress
    pb$tick(tokens = list(what = s_run_id))

    # extract run_info
    run_info <- get_run_info_SQL(file_sql = file_sql, run_id = s_run_id)
    run_info$run_id <- str_run_id(run_id = s_run_id)
    run_info$dir_run <- str_c(dir_run, "/run_", run_info$run_id)
    run_info$DIRRUN <- dir_run
    run_info$DIROBS <- ifelse(!is.null(dir_obs), dir_obs, "observed")
    run_info$DIROUT <- dir_out

    # extract run
    if (zip_output) extract_run_id(run_id = s_run_id, dir_run = dir_run, dir_out = dir_run)

    # set file_swp
    file_swp <- str_c(run_info$dir_run, "/swap.swp")

    # check if simulation is successful
    file_ok <- str_c(run_info$dir_run, "/swap.ok")
    if (!file.exists(file_ok)) stop(str_c("simulation: '", s_run_id, "' stopped!"))

    # get figure control
    ctrl_plots <- dir_ls(path = dir_fig, regexp = "*.inp$")

    # loop over figures
    for (ctrl_plot in ctrl_plots) {

      # create control
      text <- set_variable(file = ctrl_plot, info = run_info)
      write_lines(x = text, file = "./control_plot.inp")

      # create plot
      plot_SWAP(ctrl = "./control_plot.inp", create_meta = FALSE)

      # clean
      file_delete(path = "./control_plot.inp")
    }

    # clean
    if (zip_output) dir_delete(path = run_info$dir_run)

    # end progress
    if (s_run_id == run_id[length(run_id)]) pb$tick(tokens = list(what = s_run_id))
  }

}

# --- return part of procedure ---

TIMPRGEND <- Sys.time()
TIMPRGCALC <- as.numeric(difftime(time1 = TIMPRGEND, time2 = TIMPRGSTART, units = "secs"))
message(paste0("\nProgram R-PROG successfully ended in ", floor(TIMPRGCALC / 60), " minutes and ", ceiling(TIMPRGCALC %% 60), " seconds"))
q(save = "no")
