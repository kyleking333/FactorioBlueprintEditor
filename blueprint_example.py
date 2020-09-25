import sys
from FactorioTypes import Blueprinter
import numpy

# Description:
#   This file is an example file to show the functionality of the Blueprinter class.
#   Part 1:
#   It takes an input filename (containing a factorio blueprint string) from the command line,
#   loads it into a Blueprinter object, prints the entities in it,
#   saves it as a new factorio string file, and saves it as a csv file.
#   Part 2:
#   Then it loads that csv file into Blueprinter and repeats the process.

if len(sys.argv) != 2:
    print("Syntax: python3 blueprint_example.py stringfilename")
    exit(0)

### PART 1 ###

# Read in blueprint string file
bp = Blueprinter(inputStrFile=sys.argv[1])

# All data is now stored in the blueprinter object (see FactorioTypes for class/field names)
# class/field names from https://wiki.factorio.com/Blueprint_string_format), with some exceptions.

# Let's see a sample of what was in there
names, counts = numpy.unique([a.name for a in bp.entities], return_counts=True)
for i in range(len(names)):
    print(names[i], counts[i])

# let's output our data (as a factorio blueprint string and also as an editable csv
bp.toCSV("exampleOutputFromStrFile.csv")  # if you want an easy to read csv to view/edit
bp.toStrFile("exampleOutputFromStrFile.fac")  # if you want to reimport your blueprint to factorio. I use 'fac' but any extension (like .txt) is file
#print(bp)  # if you want the program to print the string instead of outputting to a file

print("-"*80)

### PART 2 ###

# Now read that csv back into Blueprinter (maybe you edited it between the .toCSV() call and now)
bp.fromCSV("exampleOutputFromStrFile.csv")

# Let's see if entities went through any changes
names, counts = numpy.unique([a.name for a in bp.entities], return_counts=True)
for i in range(len(names)):
    print(names[i], counts[i])

# let's output our data again
bp.toCSV("exampleOutputFromCSVFile.csv")
bp.toStrFile("exampleOutputFromCSVFile.fac")  # if you want to reimport your blueprint
#print(bp)  # if you want the program to print the string instead of outputting to a file

