import sys
from FactorioTypes import Blueprinter

if len(sys.argv) != 2:
    print("Syntax: python3 modifyBlueprint.py stringfilename")
    exit()

# Read in blueprint string file
bp = Blueprinter(inputStrFile=sys.argv[1])

# Read/modify the loaded data
# class/field names from https://wiki.factorio.com/Blueprint_string_format), with some exceptions.
# check FactorioTypes.py for details
#for entity in bp.entities:
#    print(entity.name)

# Alright, now output it
bp.toCSV("fromStrFile.csv")  # if you want an easy to read csv to view/edit
bp.toStrFile("fromStrFile.txt")  # if you want to reimport your blueprint

# Now read that csv back into Blueprinter (maybe you edited it between the .toCSV() call and now)
bp.openFromCSV(inputCSV="fromStrFile.csv")

# do some data manipulation if you want
#for entity in bp.entities:
#    print(entity.name)

# and output it
bp.toCSV("fromCSVFile.csv")
bp.toStrFile("fromCSVFile.txt")  # if you want to reimport your blueprint

