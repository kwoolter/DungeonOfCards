
class BaseException(Exception):
    def __init__(self, name : str, description : str):
        super().__init__()
        self.name = name
        self.description = description

class ApplicationException(Exception):
    def __init__(self, name, description):
        super().__init__(name, description)