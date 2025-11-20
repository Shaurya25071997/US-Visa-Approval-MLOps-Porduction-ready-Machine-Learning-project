from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str 


@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_data_path: str
    invalid_data_path: str
    drift_report_path: str