class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""


class DuplicateRecordError(Exception):
    """Used if trying to create data already exists"""
