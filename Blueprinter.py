# Contains the Blueprinter class which manages importing/exporting data, as well as instantiating python
# 'BlueprintComponent' objects
# https://wiki.factorio.com/Blueprint_string_format
# https://lua-api.factorio.com/latest/Concepts.html

import json
import base64
import zlib
import csv

from BlueprintComponent import *

##############################
# Main program functionality #
##############################
class Blueprinter:
    def __init__(self, inputStrFile=None, inputCSVFile=None):
        self.inputStrFile = inputStrFile
        self.inputCSVFile = inputCSVFile

        if inputStrFile is not None:
            self.fromStrFile()
        elif inputCSVFile:
            self.fromCSV()
        else:
            self.bpItem = "blueprint"
            self.bpName = "blueprint"
            self.bpColor = Color({'r': 1.0, 'g': 1.0, 'b': 1.0, 'a': 1.0})
            self.mapVersion = None

            self.currPosition = Position()
            self.currPosition.x = 0
            self.currPosition.y = 0

            self.numEntities = 0
            self.entities = []

            self.numTiles = 0
            self.tiles = []

            self.numIcons = 0
            self.icons = []

            self.numSchedules= 0
            self.schedules = []

    def fromStrFile(self, inputStrFile=None):
        if not inputStrFile:
            inputStrFile = self.inputStrFile
        with open(inputStrFile, "r") as f:
            txt = f.read()
        
        bpjson = base64.b64decode(txt[1:])
        bpjson = zlib.decompress(bpjson)
        
        bpjson = json.loads(bpjson)
        
        
        if "blueprint" not in bpjson:
            print("Invalid JSON format: expected upper level 'blueprint' string to be found (mods may change)")
            exit(1)
        
        
        # Metadata
        if "item" in bpjson["blueprint"]:
            self.bpItem = bpjson["blueprint"]["item"]
        else:
            self.bpItem = "blueprint"
        
        if "label" in bpjson["blueprint"]:
            self.bpName = bpjson["blueprint"]["label"]  # overwrites above
        else:
            self.bpName = "blueprint"
        
        if "label_color" in bpjson["blueprint"]:
            #bpColor is tuple (r, g, b, a)
            self.bpColor = Color(bpjson["blueprint"]["label_color"])
        else:
            self.bpColor = Color({'r': 1.0, 'g': .0, 'b': 1.0, 'a': 1.0})
        
        if "version" in bpjson["blueprint"]:
            self.mapVersion = int(bpjson["blueprint"]["version"])
        else:
            self.mapVersion = 0
        
        # Lists of data
        self.entities = []
        if "entities" in bpjson["blueprint"]:
            entitiesJson = bpjson["blueprint"]["entities"]
            for entity in entitiesJson:
                self.entities.append(Entity(entity))
        
        self.tiles = []
        if "tiles" in bpjson["blueprint"]:
            tilesJson = bpjson["blueprint"]["tiles"]
            for tile in tilesJson:
                self.tiles.append(Tile(tile))
        
        self.icons = []
        if "icons" in bpjson["blueprint"]:
            iconsJson = bpjson["blueprint"]["icons"]
            for icon in iconsJson:
                self.icons.append(Icon(icon))
        
        self.schedules = []
        if "schedules" in bpjson["blueprint"]:
            schedulesJson = bpjson["blueprint"]["schedules"]
            for schedule in schedulesJson:
                self.schedules.append(Schedule(schedule))
        
    def fromCSV(self, inputCSV=None):
        if not inputCSV:
            inputCSV = self.inputCSVFile

        with open(inputCSV, "r", newline='') as csvfile:
            # this csv should have quotes around every field
            reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            rows = [a for a in reader]

            self.entities=None
            self.tiles=None
            self.icons=None
            self.schedules=None

            for i in range(0, len(rows), 2):  # i will always be index of a 'label row'
                if rows[i][0]=="Entities":
                    entitiesList = rows[i+1]  # list of strings
                    self.entities = []
                    for e in entitiesList:
                        ent = e.replace('\n', '').replace('\t', '')
                        if ent is not "":
                            self.entities.append(Entity(eval(ent)))
                    
                if rows[i][0]=="Tiles":
                    tilesList = rows[i+1]  # list of strings
                    self.tiles = []
                    for e in tilesList:
                        tile = e.replace('\n', '').replace('\t', '')
                        if tile is not "":
                            self.tiles.append(Tile(eval(tile)))

                if rows[i][0]=="Icons":
                    iconsList = rows[i+1]  # list of strings
                    self.icons = []
                    for e in iconsList:
                        icon = e.replace('\n', '').replace('\t', '')
                        if icon is not "":
                            self.icons.append(Icon(eval(icon)))

                if rows[i][0]=="Schedules":
                    schedulesList = rows[i+1]  # list of strings
                    self.schedules = []
                    for e in schedulesList:
                        schedule = e.replace('\n', '').replace('\t', '')
                        if schedule is not "":
                            self.schedules.append(Schedule(eval(schedule)))

    def toCSV(self, outputCSVFile=None):
        if not outputCSVFile:
            outputCSVFile = self.outFile
        with open(outputCSVFile, "w", newline='') as csvfile:
            # this csv will have quotes around every field
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        
            if self.entities:
                writer.writerow(["Entities"])
                writer.writerow([self.spaceout(e.dict()) for e in self.entities])
            if self.tiles:
                writer.writerow(["Tiles"])
                writer.writerow([self.spaceout(e.dict()) for e in self.tiles])
            if self.icons:
                writer.writerow(["Icons"])
                writer.writerow([self.spaceout(e.dict()) for e in self.icons])
            if self.schedules:
                writer.writerow(["Schedules"])
                writer.writerow([self.spaceout(e.dict()) for e in self.schedules])

    def toStrFile(self, outputStrFile=None):
        if not outputStrFile:
            outputStrFile = self.outFile

        with open(outputStrFile, "w") as f:
            f.write(self.__str__())

    def __str__(self):  # prints the factorio string this object would generate
        res = {}
        res["blueprint"] = {}
        
        #write metadata
        res["blueprint"]["item"] = self.bpItem
        res["blueprint"]["label"] = self.bpName
        res["blueprint"]["label_color"] = toDict(self.bpColor)
        res["blueprint"]["version"] = self.mapVersion
        #write data lists 
        if self.entities:
            res["blueprint"]["entities"]  = [toDict(e) for e in self.entities]
        if self.tiles:
            res["blueprint"]["tiles"]     = [toDict(t) for t in self.tiles]
        if self.icons:
            res["blueprint"]["icons"]     = [toDict(i) for i in self.icons]
        if self.schedules:
            res["blueprint"]["schedules"] = [toDict(s) for s in self.schedules]
        
        # convert to json
        resjson = json.dumps(res)
        # compress
        compressed_res = zlib.compress(bytes(resjson, 'utf-8'))
        #encode base 64
        return "0" + base64.b64encode(compressed_res).decode('utf-8')

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def spaceout(obj):
        res = ""
        inString = False
        numTabs = 0
        operators = [ "+", "=", ":", "/", "*"]  # not doing hyphen. negative numbers and variable names don't want it spaced

        for c in str(obj):
            if c == "'":  # strings are single quote
                inString = not inString

            if inString:
                res += c
            else:
                if c == ")" or c == "]" or c == "}":
                    res += "\n"
                    numTabs -= 1
                    res += "\t"*numTabs

                if c in operators:
                    res += " " + c + " "
                elif c != " " and c != "\n" and c != "\t":  # ignore formatting
                    res += c

                if c == "(" or c == "[" or c == "{":
                    res += "\n"
                    numTabs += 1
                    res += "\t"*numTabs
                if c == ",":
                    res += "\n"
                    res += "\t"*numTabs
        return res
