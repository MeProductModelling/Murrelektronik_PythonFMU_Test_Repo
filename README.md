This Repo is a PythonFMU3 and PythonFMU2 test repo. Which also contains working modules of MVK and an Example of MVK54531


1. What is all about the FMU?
2. What are the code modules? What is their purpose?
3. Installation, setup and build instructions. (Provide some examples)
4. References to the sub-model documentations.
5. (Do readme.md)
6. Licences information.
7. Reference to the author.

#### INTRODUCTION #####

Functional-Mockup-Unit (FMU) is a simulation model that holds the behaviour of the actual device which could be simulated in simulation tools.
FMU is a standard file format of Simulation model suggested by Functional Mockup Interface(FMI) to be simulated in multiple simulation tools.

PythonFMU is a lightweight framework of generating FMUs which could generate 2.0 and 3.0 versions.
There are two types of FMUs that are Model-Exchange and Co-Simulation.
In this project we develop Co-simulation models and Version 3.0 FMUs. Co-Simulation models are packed with solvers that could be coupled with
Simulation tools to avoid the Simulation errors from the model.

#### CODE MODULES ######
Code modules are the helping functions to the FMU main function. The behaviour of the actual device is divided in to
Sub-functions and these functions are modeled using Python modules.

In this project there is folder called "Modules" that contains the functions of a real-time device.
It is possible to re-use these functions for modelling different simulation models.
This "Modules" folder is exclusively made for the MVK devices in Murrelektronik catalogue.
To generate a simulation module of MVK device it is possible to use the pre-defined functions.

The devices on the Murrelektronik Catalgue are categorised in to various sections and their sub-functions shall be
programmed in Python and stored in "Modules". They can be later plugged into main function to generate the FMU.

#####  Installation, setup and Build Instructions #####

    ##### Installation #####
    A lightweight framework that enables the packaging of Python 3 code or CSV files as co-simulation FMUs (following FMI version 2.0).
    Download the PythonFMU project from the Git-hub  https://github.com/NTNU-IHB/PythonFMU

    ##### Setup #####
    Setup the project in a IDE
    Download PyCharm community edition from https://www.jetbrains.com/pycharm/download/?section=windows
    Download required modules such as Numpy, PythonFMU libraries for generating FMUs.
    Set up the Virtual environment (See the documentation for setting up the virtual environment)

    #### Build Instructions #####
    Often, Python scripts depends on non-builtin libraries like numpy, scipy, etc. PythonFMU does not package
    a full environment within the FMU. However, you can package a requirements.txt or environment.yml file
    within your FMU following these steps:

    1. Install pythonfmu package: pip install pythonfmu
    2. Create a new class extending the Fmi2Slave class declared in the pythonfmu.fmi2slave module (see below for an example).
    3. Create a requirements.txt file (to use pip manager) and/or a environment.yml file (to use conda manager) that
       defines your dependencies.
    4. Run pythonfmu build -f myscript.py requirements.txt to create the fmu including the dependencies file.

    And using pythonfmu deploy, end users will be able to update their local Python environment. The steps to achieve that:
        1. Install pythonfmu package: "pip install pythonfmu"
        2. Be sure to be in the Python environment to be updated. Then execute "pythonfmu deploy -f my.fmu"

        ##### EXAMPLE SCRIPT #####

            from pythonfmu import Fmi2Causality, Fmi2Slave, Boolean, Integer, Real, String


            class PythonSlave(Fmi2Slave):

                author = "John Doe"
                description = "A simple description"

                def __init__(self, **kwargs):
                    super().__init__(**kwargs)

                    self.intOut = 1
                    self.realOut = 3.0
                    self.booleanVariable = True
                    self.stringVariable = "Hello World!"
                    self.register_variable(Integer("intOut", causality=Fmi2Causality.output))
                    self.register_variable(Real("realOut", causality=Fmi2Causality.output))
                    self.register_variable(Boolean("booleanVariable", causality=Fmi2Causality.local))
                    self.register_variable(String("stringVariable", causality=Fmi2Causality.local))

                    # Note:
                    # it is also possible to explicitly define getters and setters as lambdas in case the variable is not backed by a Python field.
                    # self.register_variable(Real("myReal", causality=Fmi2Causality.output, getter=lambda: self.realOut, setter=lambda v: set_real_out(v))

                def do_step(self, current_time, step_size):
                    return True

        #### Create the FMU #####
        "pythonfmu build -f pythonslave.py myproject"
        In this example a python class named PythonSlave that extends Fmi2Slave is declared in a file named
        pythonslave.py, where myproject is an optional folder containing additional project files required by the
        python script. Project folders such as this will be recursively copied into the FMU. Multiple
        project files/folders may be added.

        #### Note ####
        PythonFMU does not bundle Python, which makes it a tool coupling solution. This means that you can not
        expect the generated FMU to work on a different system (The system would need a compatible Python version
        and libraries). But to ease its usage the wrapper uses the limited Python API, making the pre-built binaries
        for Linux and Windows 64-bits compatible with any Python 3 environment. If you need to compile the wrapper for
        a specific configuration, you will need CMake and a C++ compiler. The commands for building the wrapper on
        Linux and on Windows can be seen in the GitHub workflow.

        PythonFMU does not automatically resolve 3rd party dependencies. If your code includes e.g. numpy, the target
        system also needs to have numpy installed.


#### References to the sub-model documentations ####

In this context the sub-models are python files in "Modules" folder. It is necessary to have documentation for every
function in the Sub-modules.


#### License Information ####
The PythonFMU itself does not need the license to use it.
While programming FMU, third party libraries might be needed. It is necessary to list the license of the third party
library. If the third party library is free the license is not necessary.

It is necessary to include a document in the FMU that describes about the licenses.

#### Author Information ####
This project is forked from Git-hub "PythonFMU" and further developed by Murrelektronik to make FMUs exclusively for
Murrelektronik. On Questions regarding Installation, Setup and generating FMUs write an E-mail to
rajkumar.pulaparthi@murr.services
