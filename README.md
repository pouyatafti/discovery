# discovery

small collection of Python utilities for inferring types of files and variables using regular expressions.  there is some support for localisation (for dates, numbers, and booleans), mainly with the help of [babel](babel.pocoo.org/en/latest/).

## status

there is no documentation other than the source code.  not really tested (esp. for non-English locales).  there are also some quirks.  use at your own risk.

## usage

there are more features and utilities, but here is an example of what you can do.  assuming datetime is using the en_US locale, the script below
```python
from datetime import datetime
from discovery import infer_format

dt = [datetime.fromtimestamp(s).strftime("%Y-%b-%d %H:%M") for s in range(1234567890,9876543210,1000000)]
print(infer_format(dt))

fl = [str(n/73) for n in range(1000,11000)]
print(infer_format(fl))
```
will print the following lines, listing all "common" type variants that match each column (you can also add your own variants):
```
{TypeVar(type=<Type.DATETIME: 'datetime'>, variant='%Y-%b-%d %H:%M'): 8642, TypeVar(type=<Type.STRING: 'string'>, variant=''): 8642}

{TypeVar(type=<Type.DECIMAL: 'decimal'>, variant='%sign%?%int%?%frac'): 10000, TypeVar(type=<Type.DECIMAL: 'decimal'>, variant='%sign%?%int%?%frac%exp%?'): 10000, TypeVar(type=<Type.STRING: 'string'>, variant=''): 10000}
```