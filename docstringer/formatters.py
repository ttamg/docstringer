import logging
from abc import ABC, abstractmethod

from .events import FunctionEvent


class BaseFormatter:
    """ 
    Controls how the output from the docstringer decorator is output.

    A Formatter needs to return a 'write(event)' method that receives 
    the event and outputs or processes that event.
    """

    @abstractmethod
    def call(self, event: FunctionEvent) -> None:
        """ Processes the function output at CALL time """
        pass

    @abstractmethod
    def end(self, event: FunctionEvent) -> None:
        """ Processes the function output at RETURN time """
        pass


class PrintFormatter(BaseFormatter):
    """ Outputs the function call documentation as print statements to stdout """

    def call(self, event: FunctionEvent) -> None:
        output = f"CALL to {event.name} (id={event.id})\nwith {event.params}\n{event.docstring}\n"
        print(output)

    def end(self, event: FunctionEvent) -> None:
        output = (
            f"RETURN from {event.name} (id={event.id}\nresult = {event.return_value}\n"
        )
        print(output)


class PrintSimpleFormatter(BaseFormatter):
    """ Outputs only the docstring as a simple output """

    def call(self, event: FunctionEvent) -> None:
        output = f"CALL to {event.name} (id={event.id})\n{event.docstring}\n"
        print(output)

    def end(self, event: FunctionEvent) -> None:
        pass


class DefaultFormatter(PrintFormatter):
    """ Determines the current default formatter to use """

    pass


class LoggerFormatter(BaseFormatter):
    """ Outputs the function call documentation as log items """

    def __init__(self, logger: logging.getLogger, log_level: str):
        self.logger = logger
        if not log_level in ["debug", "info", "error", "warning", "critical"]:
            raise Exception(f"Unrecognised log_level {log_level}.")
        self.log_level = log_level

    def call(self, event: FunctionEvent) -> None:
        output = f"CALL to {event.name} (id={event.id}) with {event.params}\n{event.docstring}"
        getattr(self.logger, self.log_level)(output)

    def end(self, event: FunctionEvent) -> None:
        output = f"RETURN from {event.name} (id={event.id} with result = {event.return_value}"
        getattr(self.logger, self.log_level)(output)


class EventListFormatter(BaseFormatter):
    """ Assembles a list of FunctionEvent objects that have been called  """

    def __init__(self, list_: list):
        self.list = list_

    def call(self, event: FunctionEvent) -> None:
        self.list.append(event)

    def end(self, event: FunctionEvent) -> None:
        pass
