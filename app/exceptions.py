class InvalidTypeError(Exception):
    types = {
        str: "string",
        int: "integer",
        float: "float",
        list: "list",
        dict: "dictionary",
        bool: "boolean",
    }

    def __init__(self, name, email):
        self.message = {
            "wrong fields": [
                {
                    "nome": self.types[type(name)]
                },
                {
                    "email": self.types[type(email)]
                }
            ]
        }
        super().__init__(self.message)

class ConflictEmailError(Exception):
   def __init__(self):
        self.message = {
            "error": "User already exists."
        }
        super().__init__(self.message)