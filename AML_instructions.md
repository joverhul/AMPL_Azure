# Azure Instructions
This is instructions to run the ATOM Modeling PipeLine (AMPL) using Azure Machine Learning.  

## Environment Setup

Before beginning, an AML environment should be created. The enviornment should be created with the dockerfile provided. Adjust the dockerfile to match if you are creating a cpu or a cuda environment.

A prepare_image job will be created, and the build should be successful.

## Job Setup
Create a yaml file for job submission. An example yaml file can be found at "qmugs-ampl.yaml". This yaml file can be modified to include your own folder and file names.
This contains files and folders that are inputs as "ro_mount" file types, and outputs as "rw_mount" file types. Ensure the output you are saving is a folder or a file.

### Two job examples are provided in this use-case.
#### Sleep Job
qmugs-ampl-sleep.yaml
This is a job to submit if you are interested in working interactively within Jupyter or VSCode. Adjust the sleep time to the desired time. Save the data you generate in the respected output directory that can be found in the AML output from the echo in the yaml file. 
Note: The files will not save in the output unless the job runs to completion (cannot be canceled), adjust the amount of time on the sleep job accordingly.

#### Job Submission
qmugs-ampl.yaml
This is a job to submit if you do not need to work interactively. Upon completion, the output of the job can be found in your output directory you list in the yaml file.

### yaml file contents
#### code
Folder that contains your source code.

#### command
Contains the .sh file, along with the inputs and outputs.

#### inputs
Input files and input names mounted on the AML space.

#### outputs
Output files that will be written to AML.

#### environment
The name of the environment you created to run the job in.

#### compute
The name of the compute cluster the job will be run on.

#### naming
The display name, experiment name, and description are all customizable for what you will call the job.

### sh script edits
To submit the job, create a .sh file that will run your desired code. A runnable example can be found in `train_model.sh`.
AMPL/script-ggmd.sh

### submit job

Once all files are updated, run the cell: 

`!az ml job create -f qmugs-ampl.yaml`

in the AMPL_submitjob.ipynb notebook.

Estimated time for jobs using provided values:
~3 hours.
