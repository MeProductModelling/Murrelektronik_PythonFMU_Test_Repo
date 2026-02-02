def EnvironmentVAR ():
    Env = {}

    TestedToolSolverAlgorithm = {
        "SolverAlgorithm": "FMU created using PythonFMU 3.0 and tested in FMPy",
        "ToolSolverFurtherDescription": "To simulate the FMU in different",
        "Tolerance": "0.0"
    }

    SolverAndTolerances = {
        "StepSizeControlNeeded": "false",
        "FixedStepSize": "0.001",
        "StiffSolverNeeded": "false",
        "SolverIncluded": "true",
        "TestedToolSolverAlgorithm": TestedToolSolverAlgorithm
    }

    SimulationTool = {
        "SimToolName": "FMPy 0.3.22",
        "DependencySimTool": "Python shall be installed on the target",
        "Compiler": "(Note: Mandatory field)",
        "SolverAndTolerances": SolverAndTolerances
    }

    Env ={
        "OperatingSystem": "Windows 10 64-bit",
        "ToolEnvironment": "FMPy, SIMULINK, ISG-Virtuos, FEE SCREEN SIM",
        "VisualizationInformation": "No visualisations are integrated in this model",
        "SimulationTool": SimulationTool
    }

    return Env