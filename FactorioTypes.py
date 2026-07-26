# https://wiki.factorio.com/Blueprint_string_format
# https://lua-api.factorio.com/latest/Concepts.html
import json
import base64
import zlib
import csv
from abc import ABC, abstractmethod
from typing import List

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
            self.bpColor = Color({'r': 1, 'g': 1, 'b': 1, 'a': 1})
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
            self.bpColor = Color({'r': 1, 'g': 1, 'b': 1, 'a': 1})
        
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
                writer.writerow([Blueprinter.spaceout(e.dict()) for e in self.entities])
            if self.tiles:
                writer.writerow(["Tiles"])
                writer.writerow([Blueprinter.spaceout(e.dict()) for e in self.tiles])
            if self.icons:
                writer.writerow(["Icons"])
                writer.writerow([Blueprinter.spaceout(e.dict()) for e in self.icons])
            if self.schedules:
                writer.writerow(["Schedules"])
                writer.writerow([Blueprinter.spaceout(e.dict()) for e in self.schedules])

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
        res["blueprint"]["label_color"] = Blueprinter.toDict(self.bpColor)
        res["blueprint"]["version"] = self.mapVersion
        #write data lists 
        if self.entities:
            res["blueprint"]["entities"]  = [Blueprinter.toDict(e) for e in self.entities]
        if self.tiles:
            res["blueprint"]["tiles"]     = [Blueprinter.toDict(t) for t in self.tiles]
        if self.icons:
            res["blueprint"]["icons"]     = [Blueprinter.toDict(i) for i in self.icons]
        if self.schedules:
            res["blueprint"]["schedules"] = [Blueprinter.toDict(s) for s in self.schedules]
        
        # convert to json
        resjson = json.dumps(res)
        # compress
        compressed_res = zlib.compress(bytes(resjson, 'utf-8'))
        #encode base 64
        return "0" + base64.b64encode(compressed_res).decode('utf-8')

    def __repr__(self):
        return self.__str__()

    # This can be called on any object
    # if called on a custom object it calls object.dict()
    # else it tries to iterate through the object and call itself recursively on it's children
    @staticmethod
    def toDict(obj):
        try:
            return obj.dict()  # object is a custom class with the dict field
        except:
            if isinstance(obj, dict):  # object is a dictionary. Let's reconstruct it and call dict() on it's children
                res = {}
                for k,v in obj.items():
                    res[k] = Blueprinter.toDict(v)
                return res
            elif isinstance(obj, list) or isinstance(obj, tuple):
                res = []
                for v in obj:
                    res.append(Blueprinter.toDict(v))
                return res
            else:  # must be a primitive type, leave as is
                return obj

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


#############################
# Factorio JSON Class Def's #
#############################
# Class/Field names correlate with https://wiki.factorio.com/Blueprint_string_format)
# Notable exceptions include the control_behavior and connection objects.
class BlueprintComponent(ABC):
    @abstractmethod
    def available_fields(self) -> dict[str, type]:
        pass
    
    def __init__(self, input_dict: Dictionary = None):
        for k, t in self.available_fields().items():
            if k in input_dict:
                if hasattr(t, "get_origin") and t.get_origin() == List.get_origin():
                    param_type = t.get_args()[0]
                    if param_type == bool:
                        setattr(self, k,  [v.lower() == "true" for v in input_dict[k]])
                    else:
                        setattr(self, k,  [param_type(v) for v in input_dict[k]])
                else:
                    if t == bool:
                        setattr(self, k,  True if input_dict[k].lower() == "true" else False)
                    else:
                        print(f"setting {type(self)}.{k} ({t})")
                        setattr(self, k,  t(input_dict[k]))
            else:
                setattr(self, k, None)

    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"

    def __repr__(self):
        return self.__str__()

    def dict(self):
        d = {}
        for attr,val in self.__dict__.items():
            if val is not None:
                d[attr] = Blueprinter.toDict(val)
        return d

class Icon(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "index": int,
            "signal": SignalID,
        }

class SignalID(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "name": str,
            "type": str,
        }

class Entity(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "entity_number": int,
            "name": str,
            "position": Position,
            "direction": int,
            "orientation": float,
            "connections": Connection,
            "control_behavior": ControlBehavior,
            "items": int,
            "recipe": str,
            "bar": int,
            "inventory": Inventory,
            "infinity_settings": InfinitySettings,
            "input_priority": str,
            "output_priority": str,
            "filter": str,
            "filters": list[ItemFilter],
            "filter_mode": str,
            "override_stack_size": int,
            "drop_position": Position,
            "pickup_position": Position,
            "request_filters": LogisticFilter,
            "request_from_buffers": bool,
            "parameters": SpeakerParameter,
            "alert_parameters": SpeakerAlertParameter,
            "auto_launch": bool,
            "variation": int,
            "color": Color,
            "station": str,
        }

class Inventory(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "filters": ItemFilter,
            "bar": int,
        }

class Schedule(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "schedule": list[ScheduleRecord],
            "locomotives": list[int],
        }
    
class ScheduleRecord(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "station": str,
            "wait_conditions": WaitCondition(a),
        }

class WaitCondition(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "type": str,
            "compare_type": str,
            "ticks": int,
            "condition": CircuitCondition,
        }

class Tile(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "name": str,
            "position": Position,
        }

class Position(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "x": int,
            "y": int,
        }
    def __add__(self, other):  # may come in handy
        if isinstance(other, tuple) and len(other)==2:
            return Position({"x": self.x + other[0], "y":self.y + other[1]})
        elif isinstance(other, Position):
            return Position({"x": self.x + other.x, "y":self.y + other.y})
    def __sub__(self, other):  # may come in handy
        if isinstance(other, tuple) and len(other)==2:
            return Position({"x": self.x - other[0], "y":self.y - other[1]})
        elif isinstance(other, Position):
            return Position({"x": self.x - other.x, "y":self.y - other.y})
    def __copy__(self):
        return Position({"x": self.x, "y":self.y})

class ControlBehavior(BlueprintComponent):  
    # subclass' definitions: https://lua-api.factorio.com/latest/Concepts.html#Signal
    # signal naming: https://wiki.factorio.com/Data.raw#constant-combinator
    class ConstantCombinatorParameters:
        def available_fields(self) -> dict[str, type]:
            return {
                "signal": SignalID,
                "count": int,
                "index": int,
            }
    class DeciderCombinatorParameters(BlueprintComponent):
        def available_fields(self) -> dict[str, type]:
            return {
                "first_signal": SignalID,
                "second_signal": SignalID,
                "constant": int,
                "comparator": str,
                "output_signal": SignalID,
                "copy_count_from_input": list[bool],
            }
    class ArithmeticCombinatorParameters(BlueprintComponent):
        def available_fields(self) -> dict[str, type]:
            return {
                "first_signal": SignalID,
                "second_signal": SignalID,
                "first_constant": int,
                "second_constant": int,
                "operation": str,
                "output_signal": SignalID,
            }

    def available_fields(self) -> dict[str, type]:
        return {
            "filters": list[self.ConstantCombinatorParameters],
            "decider_conditions": list[self.DeciderCombinatorParameters],
            "arithmetic_conditions": list[self.ArithmeticCombinatorParameters],
        }

class Connection(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "1": ConnectionPoint,
            "2": ConnectionPoint,
        }

class ConnectionPoint(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "red": ConnectionData,
            "green": ConnectionData,
        }

class ConnectionData(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "entity_id": int,
            "circuit_id": int,
        }

class ItemFilter(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "name": str,
            "index": int,
        }

class InfinitySettings(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "remove_unfiltered_items": list[bool],
            "filters": InfinityFilter,
        }

class InfinityFilter(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "name": str,
            "count": int,
            "mode": str,
            "index": int,
        }

class LogisticFilter(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "name": str,
            "count": int,
            "index": int,
        }

class SpeakerParameter(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "playback_volume": float,
            "playback_globally": bool,
            "allow_polyphany": bool,
        }

class SpeakerAlertParameter(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "show_alert": bool,
            "show_on_map": bool,
            "icon_signal_id": SignalID,
            "alert_message": str,
        }

class Color(BlueprintComponent):
    def available_fields(self) -> dict[str, type]:
        return {
            "r": float,
            "g": float,
            "b": float,
            "a": float,
        }

    def as_ints(self):
        return (int(r * 255), int(g * 255), int(b * 255), int(a * 255))

