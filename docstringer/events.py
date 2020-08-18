class FunctionEvent:
    """ An event which includes a function call and return """

    name = None
    id = None
    docstring = None
    params = None
    return_value = None

    def __init__(self, func, *args, **kwargs):

        self.params = locals()
        self.params.pop("self")
        self.params.pop("func")

        self.name = func.__name__
        self.id = id(func)
        self.docstring = func.__doc__

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f"< FunctionEvent {self.name} ({self.params}) -> {self.return_value}"
