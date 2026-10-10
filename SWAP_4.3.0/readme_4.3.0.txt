=== README_4.2.0.TXT =============
============================
This file is part of:

Program      :  SWAP
Version      :  4.3.0
Release date :  26-May-2026
Platform     :  MS-windows11, 64-bit operating system; Linux
Website      :  swap.wur.nl

This file README_4.3.0.TXT contains the following information:
1. Short product description
2. Installation procedure
3. How to get started
4. What's new?
5. Disclaimer
6. References
============================
1. Short product description

SWAP (Soil-Water-Atmosphere-Plant) simulates transport of water, solutes 
and heat in variably saturated soils. The program is designed to simulate the
transport processes at field scale level and during whole growing seasons. 
The program is developed by Wageningen University and Research.

============================
2. Installation procedure

This version of SWAP is offered to you in a zip-file (SWAP_4.3.0.zip)
Unzip this file to a folder where you have write-access. 
Leave the folder-structure intact to enable an easy start.
The executables are located in the folder .\tools\swap\
   * for windows: swap_4.3.0.exe
   * for Linux: swap_430
The Fortran source files are located in the folder .\tools\swap\source\
   * compiler settings can be found in .\tools\swap\compiler_settings\

============================
3. How to get started

Please read section 1.4 of the manual (accessible in the folder \doc\) to discover how to
properly start SWAP.

A quick start of a simulation for case 1 '1.hupselbrook' can be carried out as follows:

  - Change to the sub-directory \cases\1.hupselbrook\;
  - On this directory you can simulate the reference situation by starting the batch-file run_swap.cmd;
  - Verify results by using an ASCII-editor. 
    The water balance of the first year 2002, as given in the file result.bal, should read:

            Water balance components (cm)
            
            In                           Out
            =========================    ============================
            Rain + snow    :    84.18    Interception      :     4.25
            Runon          :     0.00    Runoff            :     0.03
            SSDI           :     0.00
            Irrigation     :     2.40    Transpiration     :    34.73
            Bottom flux    :     0.00    Soil evaporation  :    11.99
                                         Crack flux        :     0.00
                                         Drainage level 1  :    32.76
            =========================    ============================
            Sum            :    86.58    Sum               :    83.76

The standard manual is on-line available at the website: http://swap.wur.nl

The program has been tested on MS Windows11 and linux (Ubuntu) using different cases. 
An update of the description of the 4 test cases is described in the on-line manual.
Note: when using the linux version all folder and filenames MUST be lowercase (on disk and where supplied in input files).

============================
4. What's new?

SWAP version 4.3.0 is an update of SWAP 4.2.0. See for major changes the file Differences between SWAP 4_2_0 and 4_3_0.docx.

============================
5. Disclaimer

The author(s) and Wageningen Environmental Research disclaim all liability for 
direct, incidental or consequential damage resulting from use of the program.

Please read the license information in the folder 'license'.

============================
6. References:

An explanation of theory and ins and outs of this version of the model is given in the 
on-line manual at https://swap.wur.nl.

Other references:
Van Dam, J.C. 2000. Field scale water flow and solute transport. SWAP model concepts, 
    parameter estimation and case studies. PhD thesis, Wageningen Universiteit, 167 p.
    https://edepot.wur.nl/121243.
Van Dam, J.C., Groenendijk, P., Hendriks, R.F.A. & Kroes, J.G. 2008. Advances of Modeling 
    Water Flow in Variably Saturated Soils with SWAP. Vadose Zone Journal, 7, 640–653. 
    https://doi.org/10.2136/vzj2007.0060
Heinen, M., Mulder, M., van Dam, J., Bartholomeus, R., de Jong van Lier, Q., de Wit, J., 
    de Wit, A. & Hack - ten Broeke, M. 2024. SWAP 50 years: Advances in modelling 
    soil-water-atmosphere-plant interactions. Agricultural Water Management, 108883, 
    https://doi.org/10.1016/j.agwat.2024.108883
De Wit, A., Boogaard, H., Fumagalli, D., Janssen, S., Knapen, R., van Kraalingen, D., 
    Supit, I., van der Wijngaart, R. & van Diepen, K. 2019. 25 years of the WOFOST 
    cropping systems model. Agricultural Systems, 168, 154-167. 
    https://doi.org/10.1016/j.agsy.2018.06.018

----------------------------
For information please contact:
Internet : swap.wur.nl
E-mail   : swap.wenr@wur.nl
----------------------------

Copyright Wageningen Environmental Research (WENR), 2022-2026
============================

=== end of README_4.3.0.TXT =====
