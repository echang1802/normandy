
class Error(Exception):
    pass

class test_error(Error):
    # Exception raised for testing.

    def __init__(self, message):
        self.message = message

class step_error(Error):
    # Step exception without errors tolerance

    def __init__(self, message):
        self.message = message

class excecution_error(Error):
    # Step exception without errors tolerance

    def __init__(self, message):
        self.message = message
