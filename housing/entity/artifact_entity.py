from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file","test_file","is_ingested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",["report","report_page","is_validated","message"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",["transformed_train_file","preprocessed_file","is_transformed","message"])