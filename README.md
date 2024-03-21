Welcome to the GitHub repository associated with our research on single-molecule microfluidic diffusional sizing (smMDS), as detailed in Krainer et al. 2023 BioRxiv (doi: https://doi.org/10.1101/2023.07.12.548675). This repository hosts two distinct scripts crucial for analysis of smMDS experiments: the first script (see folder "SingleMoleculeAnalysis") is dedicated to the analysis of single-molecule events from step scan measurements by counting the number of bursts, or single molecules, as they pass through the confocal spot. This code was written by Raphael Jacquat. The second script (see folder "DiffusionProfileAnalysis") utilizes the data gathered by the first to calculate the hydrodynamic radius of the particles under observation. This code is adapted from code originally written by Quentin Peter. For the most recent updates, please visit the Git repository: https://github.com/impact27/diffusion_device. This README guide will assist you in setting up the necessary software environment and provide a tutorial with an example data set (see folder "Example") for using these scripts to analyze .ptu files for diffusional sizing in microfluidic chips. The codes here are published under the GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

# Installation instructions

This code package is compatible with Python 3.6. We recommend ensuring that your system runs this version for optimal performance. While later versions up to currently used (3.11) should also function, their compatibility is not guaranteed. For users needing to install Python, Anaconda is our suggested platform for its ease of use and comprehensive package management. The commands given below should be written in the Anaconda prompt application or any terminal which accept pip.

The burst detection script (in folder "SingleMoleculeAnalysis") is designed to run independently, requiring no additional installation process. The code for diffusion profile analysis (in folder "DiffusionProfileAnalysis") requires an installation process (see Section 'Code DiffusionProfileAnalysis - Installation of dependency', 'Code DiffusionProfileAnalysis - Installation' and 'Code DiffusionProfileAnalysis - Installation check'). This code is designed to be flexible, capable of working with data profiles obtained from confocal microscopy or extracting such profiles directly from images. It incorporates several dependencies, such as opencv3, which, while not directly utilized for the experiments described in our paper, are necessary for the code's full functionality.

## Code DiffusionProfileAnalysis - Installation of dependency
First, install opencv3 and tifffile with pip OR conda (if you use the recommended Anaconda platform):

Installation with pip:
- `pip install tifffile`
- `pip install opencv-python`

Installation with conda:
- `conda install -c menpo opencv3`
- `conda install -c conda-forge tifffile`

You should now be able to import the following from python:
- `import cv2`
- `import tifffile`

If your operating system is Windows and cv2 does not install with the import prompt, you might need to download the wheel yourself:
- https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
You can then install the package with pip:
- `pip install opencv_python‑3.3.1‑cp36‑cp36m‑win_amd64.whl`

## Code DiffusionProfileAnalysis - Installation
From the Anaconda prompt or the terminal where pip works, move into the folder "DiffusionProfileAnalysis":

In Windows/UNIX environment:
- `cd DiffusionProfileAnalysis`

Then use pip to install the package:
- `pip install .`

This will install the code for diffusion profile analysis.

## Code DiffusionProfileAnalysis - Installation check
Open the DiffusionProfileAnalysis/Samples folder and run in that order:
`generate_metadata.py`
`generate_settings.py`
`sizescript.py`
If everything is running fine, you can proceed and not use the DiffusionProfileAnalysis folder.

# Tutorial for extracting hydrodynamic radius from exmaple data set
The extraction of hydrodynamic radius is divided into two main steps, each corresponding to the use of one of the scripts provided in this repository.

1.-Extracting Single Molecule Profiles:
The initial phase involves extracting the profile of single molecules from your data. Ensure you have your data ready in the appropriate format (.ptu files).
2.-Running the Diffusional Sizing Code:
Once you have the single molecule profiles, the next step is to employ the diffusional sizing code, previously installed. This code analyzes the extracted profiles to calculate the hydrodynamic radius of the particles in your sample.

## Extracting Single Molecule Profiles
The script which take several .ptu files and creat a profile of single molecule count per position is  'getBursts_severalfiles_extractprofilesMDS.py', located within the 'singlemoleculeanalysiscambridge-smac' directory.
Upon launch, a Tkinter window will appear, prompting you to select a .ptu file from your scan profile folder. Navigate to 'Example/HSA_20pM_PBS_0p01tween_100ulph_400steps_2sec_27' and choose any .ptu file. The script will then select every .ptu files from the same folder to extract the number of counted molecule per position (meaning per .ptu file).
It not only extracts the number of bursts (or molecules) but also several parameters at each scan step. These include the minimum, maximum, and median intensity (photon count) of detected bursts, the scan position, and the total intensity of photon receive (SumPhoton). Everything is extracted in an output folder within the selected file folder 'Example/HSA_20pM_PBS_0p01tween_100ulph_400steps_2sec_27/output/'. Alldata.txt concatenate all the extracted parameters.

###Customization and Parameters

You can change different parameters of the extraction of the burst if you open the file, getBursts_severalfiles_extractprofilesMDS.py
All the parameter called with noise are not used for the moment, and was created for futur application in order to separate automatically noise and molecule.
The important parameter are "set_lee_filter", "threshold_iT_signal", "min_phs_burst", "filter_name", and "output_folder"
AAll parameters, except "output_folder", are detailed in the Supplementary Information of the associated paper.
The "output_folder" allows you to choose in which folder you want to save the extracted data from the root of the file selected.
You can choose to see intermediate plot with "show_plot" as True but it is mostly used internally to debug an unusual trace (be aware and careful as for a 400 step scan it will generate 400 plots).

###Important Note on Data Format
Each .ptu file within your folder must include position information in its name, following the format "_X.XXum_" where the first X represents a number from 0 to 10000, and the subsequent XX are two digits. This naming convention is critical for ensuring the accurate extraction and analysis of your data.


## Running Diffusional Sizing
After extracting single molecule profiles, proceed with the diffusional sizing analysis. This step requires two metadata files created by generate_metadata.py and generate_settings.py. Both python script are located in the Example directory. Run them prior to execute sizescript.py to size the profiles. The sizing results will be available in Example/Output_results/settings/output/, with "Alldata_fig.pdf" presenting the calculated sizes.


###Customization and Parameters
1. Generating Metadata with generate_metadata.py
generate_metadata.py is designed to define the structure and conditions of your dataset for analysis. It requires information such as the data path, type, chip characteristics, and experiment characteristic (flowrate and sample used). Use "multi_pos_scan" if your data combines four profiles in a single file; otherwise, opt for "single_pos_scan" for datasets with one peak profile per file. The script also gathers details on microfluidic chip characteristics like channel height, wall width, number of channels, flow rate, and the positions traversed between profiles. Additionally, it defines the pixel size, indicating the distance between scan positions.

2. Generating Settings with generate_setting.py
generate_setting.py focuses on the analytical settings for the fitting process, including the radius range to test, the spacing between tested radii (either linear or logarithmic), and whether to filter or pre-bin profiles for more efficient fitting. Normally, processing 400 points takes under a minute, but increasing the number of points per profile set can significantly impact the computation time going easily further 10min to an hour.

3. Configuring sizescript.py
To run sizescript.py, specify three inputs: the paths to the metadata files generated by "generate_metadata.py" and "generate_settings.py", and the path to the output folder. This script integrates the provided information to perform the diffusional sizing analysis.
