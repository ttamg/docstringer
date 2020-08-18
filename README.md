# docstringer

A simple decorator to create documentation of your function calls from their docstrings

## Scope

### What package does?

This utility allows you to add a simple `@docstringer` decorator to any function calls you wish to document when you are running your code. This will then track the calls to these functions and output documentation of the call-stack flow.

This utility is focused on documentation of the call stack of functions and uses the function doc strings to document the call order.

### What package does not do?

This function is purely focused on documenting the call order, the call parameters and the return values and using the docstrings to make this auto documentation.

This package does _not_ intermediate values tracked at each stage within functions. There are many great packages already available to do this such as [snoop](https://github.com/alexmojaki/snoop).

This package also does _not_ profile the time taken to run each function in the call stack. There are many great packages already available to do this such as [profiling](https://github.com/what-studio/profiling).

## Quickstart

Install the package using:

    pip install docstringer

On any function in your code that you wish to document the calling order, add the `@docstringer` decorator. By default the _docstringer_ package will print the output.

## An example

We have a simple program that rolls a number of dice and returns the result.

We decorate the functions we want to document function calls to using the `@docstringer` decorator.

```python
@docstringer
def roll_the_dice(rolls: int, sides: int = 6) -> tuple:
    """
    Rolls a number of dice and returns the result.
    """
    results = []
    for _ in range(rolls):
        results.append(roll(sides))

    return (sum(results), results)

@docstringer
def roll(sides: int = 6) -> int:
    """
    An individual die (of side count=sides) roll.
    """
    return random.randint(1, sides)
```

An example output from running this code:

```
CALL to roll_the_dice (id=4441740768)
with {'args': (), 'kwargs': {'rolls': 2, 'sides': 6}}

    Rolls a number of dice and returns the result.

CALL to roll (id=4442233152)
with {'args': (6,), 'kwargs': {}}

    An individual die (of side count=sides) roll.

RETURN from roll (id=4442233152
result = 5

CALL to roll (id=4442233152)
with {'args': (6,), 'kwargs': {}}

    An individual die (of side count=sides) roll.

RETURN from roll (id=4442233152
result = 3

RETURN from roll_the_dice (id=4441740768
result = (8, [5, 3])
```

## Deactivating docstringer in production

By default _docstringer_ is active and will log the call stack on the decorated functions. When using in production you will want to switch this off. This will also speed up running.

To switch off the `@docstringer` decorator without removing it, pass the `active=False` parameter to the decorator. This can be done globally using a configuration. For example:

```python
DEBUG = False  # Set to True in debug mode when decorator should be active\

@docstringer(active=DEBUG)
def my_function():
    """ My function to be documented when it is called """
    ...

```

## Different output formats

Different _Formatters_ can be used to push the output in different formats by passing an instance of the _Formatter_ you want to the `DOCSTRINGER_FORMATTER` variable.

By default _docstringer_ outputs the function call information as print statements to the console. This default formatter is the `PrintFormatter`

You can set a different formatter by passing this to the `formatter` parameter in the docstring. The built in formatters are outlined below. Or you can customise your own

```python
from docstringer.formatters import LoggerFormatter

formatter = LoggerFormatter(logger=logger, log_level='info')

@docstringer(formatter=formatter)
def my_function():
    """ My function to be documented when it is called """
    ...

```

### LoggerFormatter

This formatter outputs the function call information to the logger of your choice instead of printing to the screen. When instantiating the `LoggerFormatter`, pass it the logger and log=level you want to use:

```python
from docstringer.formatters import LoggerFormatter
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

@docstringer(formatter=LoggerFormatter(logger=logging, log_level='info')
def my_function():
    ...

```

This will now output function calls as log items.

### EventListFormatter

The `EventListFormatter` will return the function call information a a list of `FunctionEvent` objects. These objects contain the name, docstring, call values and return values of each function call in the order that they were called.

This formatter is passed a list (usually an empty list) when it is instantiated and it will populate this list with the FunctionEvent objects that occur on decorated functions.

```python
from docstringer.formatters import EventListFormatter

event_list = []

@docstringer(formatter=EventListFormatter(event_list))
def my_function():
    ...

```

# Combining with other tracing or introspection packages

This package focuses on documenting the call stack and showing the docstring for the decorated functions.

This can be combined with a more detailed tracing or profiling package to give a combined output. We recommend that the tracing decorator is placed inside the docstringer decorator.

## Example combining with snoop

In this example we use the `PrintSimpleFormatter` which does not show the parameters and return values as these are already provided by snoop. We also configure snoop to print in a similar format

```python
import snoop
from docstringer import docstringer

snoop_formatted = snoop.Config(color=False, prefix="", columns=[]).snoop

@docstringer(formatter=PrintSimpleFormatter())
@snoop_formatted
def roll(sides: int = 6) -> int:
    """
    An individual die (of side count=sides) roll.
    """
    return random.randint(1, sides)
```

The output contains both the snoop and docstringer outputs:

```
...

CALL to roll (id=4343471264)

    An individual die roll.

    Parameters:
    - sides (int) - the number of sides on the dice (default = 6)

    Returns:
    - the value of the die roll


>>> Call to roll in File "/Users/matt/Projects/docstringer/demo.py", line 50
...... sides = 6
50 | def roll(sides: int = 6) -> int:
60 |     return random.randint(1, sides)
<<< Return value from roll: 1

...
```
