# https://wiki.factorio.com/Blueprint_string_format
# https://lua-api.factorio.com/latest/Concepts.html
import json
import base64
import zlib
import csv

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
            self.bpColor = Color(r=255,g=255,b=255, a=255)
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
            #bpColor is tuple (r,g,b, a)
            self.bpColor = Color(dic=bpjson["blueprint"]["label_color"])
        else:
            self.bpColor = Color(r=255,g=255,b=255, a=255)
        
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

class Icon:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "index" in dic:
            self.index = int(dic["index"])
        else:
            self.index = None
        if "signal" in dic:
            self.signal = SignalID(dic["signal"])
        else:
            self.signal = None
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

class SignalID:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "name" in dic:
            self.name = dic["name"]
        else:
            self.name = None
        if "type" in dic:
            self.type = dic["type"]
        else:
            self.type = None
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


class Entity:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "entity_number" in dic:
            self.entity_number       = int(dic["entity_number"])
        else:
            self.entity_number = None
        if "name" in dic:
            self.name                = dic["name"]
        else:
            self.name =  None
        if "position" in dic:
            self.position            = Position(dic["position"])
        else:
            self.position = None

        if "direction" in dic:
            self.direction           = int(dic["direction"])
        else:
            self.direction           = None
        if "orientation" in dic:
            self.orientation         = float(dic["orientation"])
        else:
            self.direction           = None
        if "connections" in dic:
            self.connections         = Connection(dic["connections"])
        else:
            self.connections         = None
        if "control_behavior" in dic:
            self.control_behavior   = ControlBehavior(dic["control_behavior"])
        else:
            self.control_behaviour   = None
        if "items" in dic:
            self.items               = int(dic["items"])
        else:
            self.items               = None
        if "recipe" in dic:
            self.recipe              = dic["recipe"]
        else:
            self.recipe              = None
        if "bar" in dic:
            self.bar                 = int(dic["bar"])
        else:
            self.bar                 = None
        if "inventory" in dic:
            self.inventory           = Inventory(dic["inventory"])
        else:
            self.inventory           = None
        if "infinity_settings" in dic:
            self.infinity_settings   = InfinitySettings(dic["infinity_settings"])
        else:
            self.infinity_settings   = None
        if "type" in dic:
            self.type                = dic["type"]
        else:
            self.type                = None
        if "input_priority" in dic:
            self.input_priority      = dic["input_priority"]
        else:
            self.input_priority      = None
        if "output_priority" in dic:
            self.output_priority     = dic["output_priority"]
        else:
            self.output_priority     = None
        if "filter" in dic:
            self.filter              = dic["filter"]
        else:
            self.filter              = None
        if "filters" in dic:
            self.filters             = [ItemFilter(a) for a in dic["filters"]]
        else:
            self.filters             = None
        if "filter_mode" in dic:
            self.filter_mode         = dic["filter_mode"]
        else:
            self.filter_mode         = None
        if "override_stack_size" in dic:
            self.override_stack_size = int(dic["override_stack_size"])
        else:
            self.override_stack_size = None
        if "drop_position" in dic:
            self.drop_position       = Position(dic["drop_position"])
        else:
            self.drop_position       = None
        if "pickup_position" in dic:
            self.pickup_position     = Position(dic["pickup_position"])
        else:
            self.pickup_position     = None
        if "request_filters" in dic:
            self.request_filters     = LogisticFilter(dic["request_filters"])
        else:
            self.request_filters     = None
        if "request_from_buffers" in dic:
            self.request_from_buffers= True if dic["request_from_buffers"]=="true" else False
        else:
            self.request_from_buffers= None
        if "parameters" in dic:
            self.parameters          = SpeakerParameter(dic["parameters"])
        else:
            self.parameters          = None
        if "alert_parameters" in dic:
            self.alert_parameters    = SpeakerAlertParameter(dic["alert_parameters"])
        else:
            self.alert_parameters    = None
        if "auto_launch" in dic:
            self.auto_launch         = True if dic["auto_launch"]=="true" else False
        else:
            self.auto_launch         = None
        if "variation" in dic:
            self.variation           = int(dic["variation"])
        else:
            self.variation           = None
        if "color" in dic:
            self.color               = Color(dic=dic["color"])
        else:
            self.color               = None
        if "station" in dic:
            self.station             = dic["station"]
        else:
            self.station             = None

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

class Inventory:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "filters" in dic:
            self.filters = [ItemFilter(a) for a in dic["filters"]]
        else:
            self.filters = None
        if "bar" in dic:
            self.bar = int(dic["bar"])
        else:
            self.bar = None
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

class Schedule:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "schedule" in dic:
            self.schedule = [ScheduleRecord(a) for a in dic["schedule"]]
        else:
            self.schedule = None
        if "locomotives" in dic:
            self.locomotives = [int(trainEntityNumer) for trainEntityNumber in dic["locomotives"]]
        else:
            self.locomotives = None
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
    
class ScheduleRecord:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "station" in dic:
            self.station = dic["station"]
        else:
            self.station = None
        if "wait_conditions" in dic:
            self.wait_conditions = [WaitCondition(a) for a in dic["wait_conditions"]]
        else:
            self.wait_conditions = None
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

class WaitCondition:
    def __init__(self, dic=None):
        if not dic:
            dic = {}

        if "type" in dic:
            self.type = dic["type"]
        else:
            self.type = None
        if "compare_type" in dic:
            self.compare_type = dic["compare_type"]
        else:
            self.compare_type = None
        if "ticks" in dic:
            self.ticks = int(dic["ticks"])
        else:
            self.ticks = None
        if "condition" in dic:
            self.condition = CircuitCondition(dic["condition"])
        else:
            self.condition = None
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

class Tile:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "name" in dic:
        	self.name = dic["name"]
        else:
            self.name = None
        if "position" in dic:
        	self.position = Position(dic["position"])
        else:
            self.position = None
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




class Position:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "x" in dic:
            self.x = dic["x"]
        else:
            self.x = None
        if "y" in dic:
            self.y = dic["y"]
        else:
            self.y = None
    def __add__(self, other):  # may come in handy
        if isinstance(other, tuple) and len(other)==2:
            self.x += other[0]
            self.y += other[1]
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

class ControlBehavior:  # not documented properly, here are the subclass' definitions: https://lua-api.factorio.com/latest/Concepts.html#Signal
    class ConstantCombinatorParameters:
        def __init__(self, dic=None):
            if not dic:
                dic = {}
            if "signal" in dic:
                self.signal = SignalID(dic["signal"])
            else:
                self.signal = None
            if "count" in dic:
                self.count = int(dic["count"])
            else:
                self.count = None
            if "index" in dic:
                self.index = int(dic["index"])
            else:
                self.index = None
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
    class DeciderCombinatorParameters:
        def __init__(self, dic=None):
            if not dic:
                dic = {}
            if "first_signal" in dic:
                self.first_signal = SignalID(dic["first_signal"])
            else:
                self.first_signal = None
            if "second_signal" in dic:
                self.second_signal = SignalID(dic["second_signal"])
            else:
                self.second_signal = None
            if "constant" in dic:
                self.constant = int(dic["constant"])
            else:
                self.constant = None
            if "comparator" in dic:
                self.comparator = dic["comparator"]
            else:
                self.comparator = None
            if "output_signal" in dic:
                self.output_signal = SignalID(dic["output_signal"])
            else:
                self.output_signal = None
            if "copy_count_from_input" in dic:
                self.copy_count_from_input = True if int(dic["copy_count_from_input"])=="true" else False
            else:
                self.copy_count_from_input = None
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
    class ArithmeticCombinatorParameters:
        def __init__(self, dic=None):
            if not dic:
                dic = {}
            if "first_signal" in dic:
                self.first_signal = SignalID(dic["first_signal"])
            else:
                self.first_signal = None
            if "second_signal" in dic:
                self.second_signal = SignalID(dic["second_signal"])
            else:
                self.second_signal = None
            if "first_constant" in dic:
                self.first_constant = int(dic["first_constant"])
            else:
                self.first_constant = None
            if "second_constant" in dic:
                self.second_constant = int(dic["second_constant"])
            else:
                self.second_constant = None
            if "operation" in dic:
                self.operation = dic["operation"]
            else:
                self.operation = None
            if "output_signal" in dic:
                self.output_signal = SignalID(dic["output_signal"])
            else:
                self.output_signal = None
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

    def __init__(self, dic=None):
        if not dic:
            dic = {}  # ControlBehavior constructor
        if "filters" in dic:  # for some reason, this is called filters but it deals with constant combinators
            self.filters = [self.ConstantCombinatorParameters(a) for a in dic["filters"]]
        else:
            self.filters = None
        if "decider_conditions" in dic:
            self.decider_conditions = self.DeciderCombinatorParameters(dic["decider_conditions"])
        else:
            self.decider_conditions = None
        if "arithmetic_conditions" in dic:
            self.arithmetic_conditions = self.ArithmeticCombinatorParameters(dic["arithmetic_conditions"])
        else:
            self.arithmetic_conditions = None
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

class Connection:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "1" in dic:
            self._1 = ConnectionPoint(dic["1"])
        else:
            self._1 = None
        if "2" in dic:
            self._2 = ConnectionPoint(dic["2"])
        else:
            self._2 = None
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()
    def dict(self):
        d = {}
        for attr,val in self.__dict__.items():
            if val is not None:
                d[attr[1:]] = Blueprinter.toDict(val)  # customized due to only _# attributes in this class
        return d

class ConnectionPoint:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "red" in dic:
            self.red   = [ConnectionData(a) for a in dic["red"]]
        else:
            self.red = None
        if "green" in dic:
            self.green = [ConnectionData(a) for a in dic["green"]]
        else:
            self.green = None

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

class ConnectionData:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "entity_id" in dic:
            self.entity_id   = int(dic["entity_id"])
        else:
            self.entity_id = None
        if "circuit_id" in dic:
            self.circuit_id  = int(dic["circuit_id"])
        else:
            self.circuit_id = None
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

class ItemFilter:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "name" in dic:
        	self.name = dic["name"]
        else:
            self.name = None
        if "index" in dic:
        	self.index = int(dic["index"])
        else:
            self.index = None
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()
    def dict(self):
        d = {}
        for attr,val in self.__dict__.items():
            if val is not None:
                d[attr] = Blueprinter.toDict(val)
        return d

class InfinitySettings:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "remove_unfiltered_items" in dic:
            self.remove_unfiltered_items = True if dic["remove_unfiltered_items"]=="true" else False
        else:
            self.remove_unfiltered_items = None
        if "filters" in dic:
        	self.filters = [InfinityFilter(a) for a in dic["filters"]]
        else:
            self.filters = None
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

class InfinityFilter:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "name" in dic:
            self.name = dic["name"]
        else:
            self.name = None
        if "count" in dic:
            self.count = int(dic["count"])
        else:
            self.count = None
        if "mode" in dic:
            self.mode = dic["mode"]
        else:
            self.mode = None
        if "index" in dic:
            self.index = int(dic["index"])
        else:
            self.index = None
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

class LogisticFilter:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "name" in dic:
            self.name = dic["name"]
        else:
            self.name = None
        if "index" in dic:
            self.index = int(dic["index"])
        else:
            self.index = None
        if "count" in dic:
            self.count = int(dic["count"])
        else:
            self.count = None
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

class SpeakerParameter:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "playback_volume" in dic:
        	self.playback_volume = float(dic["playback_volume"])
        else:
            self.playback_volume = None
        if "playback_globally" in dic:
        	self.playback_globally = True if dic["playback_globally"]=="true" else False
        else:
            self.playback_globally = None
        if "allow_polyphany" in dic:
        	self.allow_polyphany = True if dic["allow_polyphany"]=="true" else False
        else:
            self.allow_polyphany = None
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

class SpeakerAlertParameter:
    def __init__(self, dic=None):
        if not dic:
            dic = {}
        if "show_alert" in dic:
            self.show_alert = True if dic["show_alert"]=="true" else False
        else:
            self.show_alert = None
        if "show_on_map" in dic:
            self.show_on_map = True if dic["show_on_map"]=="true" else False
        else:
            self.show_on_map = None
        if "icon_signal_id" in dic:
            self.icon_signal_id = SignalID(dic["icon_signal_id"])
        else:
            self.icon_signal_id = None
        if "alert_message" in dic:
            self.alert_message = dic["alert_message"]
        else:
            self.alert_message = None
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

class Color:
    def __init__(self, dic=None, r=None, g=None, b=None, a=None):
        if dic:
            self.r, self.g, self.b, self.a = [int(255*float(i)) for i in dic.values()]
        else:
            self.r, self.g, self.b, self.a = r, g, b, a
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

