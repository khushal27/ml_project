from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file","test_file","is_ingested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",["report","report_page","is_validated","message","schema_file_path"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",["transformed_train_file","transformed_test_file","preprocessed_file","is_transformed","message"])