import json

from AASX.Environment import EnvironmentVAR
from AASX.Ports import PortsVAR


def AASXSimulationSubModelGenerator (data, data_connectors,Component_Id, Output_file):

    Ports = PortsVAR(data, data_connectors)

    Model = {}


    Phone ={
        "TypeOfTelephone": "TBD",
        "TelephoneNumber": "TBD",
        "AvailableTime": "TBD"
    }

    Email = {
        "TypeOfEmailAddress": "@murr.services",
        "EmailAddress": "rajkumar.pulparthi@murr.services",
        "TypeOfPublicKey": "Not defined",
        "PublicKey": "Not defined",
    }

    SimModManufacturerInformation ={
        "Company": "Murrelektronik",
        "Language01": "Deutsch",
        "Email": Email,
        "Phone": Phone,
        "Language02": "English"
    }

    ModelFileVersion ={
        "ModelVersionId": "V1.0",
        "ModelPreviewImage": f"/aasx/files/MVK{Component_Id}.png",
        "DigitalFile": f"/aasx/files/MVK{Component_Id}.fmu",
        "ModelFileReleaseNotesTxt": {"en": "This is version V1.0 of the MVK"+ f"{Component_Id}" +" from Murrelektornik I / O component catalogue."},
        "ModelFileReleaseNotesFile": "(Note: Mandatory field)"

    }

    ModelFile ={
        "ModelFileType": "FMI 3.0 Co-Simulation",
        "ModelFileVersion": ModelFileVersion
    }

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

    Environment = {
        "OperatingSystem": "Windows 10 64-bit",
        "ToolEnvironment": "FMPy, SIMULINK, ISG-Virtuos, FEE SCREEN SIM",
        "VisualizationInformation": "No visualisations are integrated in this model",
        "SimulationTool": SimulationTool
    }

    Simpurpose = {"PosSimPurpose": "Virtual Commissioning",
                  "NegSimPurpose": "(Note: Mandatory field)" }


    SimulationModel = {
        "Summary" : {"en": "MVK" + Component_Id +".fmu is a behaviour model of a I/O device from Murrelektronik. This device exchanges data between field devices and PLC."},
        "Simpurpose" : Simpurpose,
        "TypeOfModel": "Linear model",
        "ScopeOfModel": "Behaviour",
        "LicenseModel": "Not defined",
        "EngineeringDomain": "Data Transfer",
        "Environment": EnvironmentVAR(),
        "RefSimDocumentation": f"/aasx/files/MVK_{Component_Id}_Python_FMU.pdf",
        "ModelFile": ModelFile,
        "ParamMethod": "Pre-Parameterised",
        "ParamFile": "Not needed",
        "InitStateMethod": "(Note: Mandatory field)",
        "InitStateFile": "Not needed",
        "DefaultSimTime": "100.00",
        "SimModManufacturerInformation": SimModManufacturerInformation,
        "Ports" : Ports


    }

    SimulationModels ={
        "SimulationModel": SimulationModel
    }

    Parent = {
        "SimulationModels": SimulationModels
    }

    Model.update(Parent)


    # Write to JSON
    with open(Output_file, "w", encoding="utf-8") as f:
        json.dump(Model, f, indent = 2)
        #json.loads(Submodel, f, indent=4, ensure_ascii=False)


    return True