class IncorrectInputFileFormatException(Exception):
    """Exception raised for an invalid input file format.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, file_name: str):
        self.message = f"The input file format is not accepted, only CSV files are accecpted, input file: {file_name}"
        super().__init__(self.message)


class SchemaValidationErrorException(Exception):
    """Exception raised for invalid data in input file.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, exception: str):

        self.message = f"\
            \n\nSchema errors and failure cases:\n\
            {exception.failure_cases} \n\
            \nDataFrame object that failed validation: \n\
            {exception.data}"
        super().__init__(self.message)
