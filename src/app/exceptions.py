class IncorrectInputFileFormatException(Exception):
    """Exception raised for an invalid input file format."""

    def __init__(self, file_name: str):
        self.message = f"The input file format is not accepted, only CSV files are accecpted, input file: {file_name}"
        super().__init__(self.message)


class SchemaValidationErrorException(Exception):
    """Exception raised for invalid data in input file."""

    def __init__(self, exception: str):

        self.message = f"\
            \n\nSchema errors and failure cases:\n\
            {exception.failure_cases} \n\
            \nDataFrame object that failed validation: \n\
            {exception.data}"
        super().__init__(self.message)


class AccountAlreadyExistsInDBException(Exception):
    """Exception raised when trying to create an existing account."""

    def __init__(self: str):
        self.message = "The account already existes in the database."
        super().__init__(self.message)


class TransactionsNotFound(Exception):
    """Exception raised when trying to send a balance for an account without transactions."""

    def __init__(self: str):
        self.message = "The account has no transactions."
        super().__init__(self.message)
