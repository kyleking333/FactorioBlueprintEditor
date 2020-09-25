# FactorioBlueprintEditor

### Dependencies:
- [Python3](https://www.python.org/downloads/)
- [zlib](https://www.zlib.net/)

### Tested on Ubuntu 18.04

### ToDo
- Test modifications to CSV propogating to output string

## Description
Factorio Blueprint Editor is a tool to read Factorio Blueprint strings (from a file) into a Python object with can be manipulated and then exported back to a blueprint string (also saved to a file).
The main class is `Blueprinter` and it has a few useful functions:
- `fromStrFile()`
  - Updates `Blueprinter` with the data from the blueprint string file. Called implicitly if `Blueprinter` is passed in a filename to it's `inputStrFile` argument.
- `fromCSV()`
  - Updates `Blueprinter` with the data from a csv file (probably generated previously by `Blueprinter`). Called implicitly if `Blueprinter` is passed in a filename to it's `inputCSVFile` argument.
- `toCSV()`
  - Outputs the contents of `Blueprinter` to a CSV file in a human readable format.
- `toStrFile()`
  - Outputs the contents of `Blueprinter` to a specified file as a Factorio-importable string
- calls to `__str__()` or `__repr__()` (such as `print()`) return the Factorio-importable string

`Blueprinter` also has a few useful fields:
- `bpItem`
- `bpName`
- `bpColor`
- `entities`
- `tiles`
- `icons`
- `schedules`
- `mapVersion`

(All of these fields have analogs with descriptions [here](https://wiki.factorio.com/Blueprint_string_format#Blueprint_object))

`blueprint_example.py` has some example code of an application using the `Blueprinter` class. I named my input string files with a `.fac` extension (although any extension is valid).



