## This first set of classes describes blueprint objects described here:
# https://wiki.factorio.com/Blueprint_string_format

class Icon:
    def __init__(self, dic):
        self.index = int(dic["index"])
        self.signal = SignalID(dic["signal"])
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class SignalID:
    def __init__(self, dic):
        self.name = dic["name"]
        self.type = dic["type"]
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()


class Entity:
    def __init__(self, dic):
        self.entity_number       = int(dic["entity_number"])
        self.name                = dic["name"]
        self.position            = Position(dic["position"])

        if "direction" in dic:
            self.direction           = int(dic["direction"])  # TODO: handle uint differently?
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
            self.items               = int(dic["items"])  # TODO: uint32
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
            self.override_stack_size = int(dic["override_stack_size"])  # TODO: uint8
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
            self.variation           = int(dic["variation"])  # TODO: um is it a uint8?
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

class Inventory:
    def __init__(self, dic):
        self.filters = [ItemFilter(a) for a in dic["filters"]]
        self.bar = int(dic["bar"])  # TODO: uint16?
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class Schedule:
    def __init__(self, dic):
        self.schedule = [ScheduleRecord(a) for a in dic["schedule"]]
        self.locomotives = [int(trainEntityNumer) for trainEntityNumber in dic["locomotives"]]
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()
    
class ScheduleRecord:
    def __init__(self, dic):
        self.station = dic["station"]
        self.wait_conditions = [WaitCondition(a) for a in dic["wait_conditions"]]
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class WaitCondition:
    def __init__(self, dic):
        self.type = dic["type"]
        self.compare_type = dic["compare_type"]
        self.ticks = int(dic["ticks"])  # TODO: uint
        self.condition = CircuitCondition(dic["condition"])
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class Tile:
    def __init__(self, dic):
        self.name = dic["name"]
        self.position = Position(dic["position"])
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()


class Position:
    def __init__(self, dic):
        self.x, self.y = [float(a) for a in dic.values()]
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class ControlBehavior:  # not documented properly, here are the subclass' definitions: https://lua-api.factorio.com/latest/Concepts.html#Signal
    class ConstantCombinatorParameters:
        def __init__(self, dic):
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
    class DeciderCombinatorParameters:
        def __init__(self, dic):
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
    class ArithmeticCombinatorParameters:
        def __init__(self, dic):
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

    def __init__(self, dic):  # ControlBehavior constructor
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

class Connection:
    def __init__(self, dic):
        if "1" in dic:
            self._1 = ConnectionPoint(dic["1"])
        else:
            self._1 = None
        if "2" in dic:
            self._2 = ConnectionPoint(dic["2"])
        else:
            self._1 = None
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class ConnectionPoint:
    def __init__(self, dic):
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

class ConnectionData:
    def __init__(self, dic):
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

class ItemFilter:
    def __init__(self, dic):
        self.name = dic["name"]
        self.index = int(dic["index"])
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class InfinitySettings:
    def __init__(self, dic):
        self.remove_unfiltered_items = True if dic["remove_unfiltered_items"]=="true" else False
        self.filters = [InfinityFilter(a) for a in dic["filters"]]
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class InfinityFilter:
    def __init__(self, dic):
        self.name = dic["name"]
        self.count = int(dic["count"])
        self.mode = dic["mode"]
        self.index = int(dic["index"])
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class LogisticFilter:
    def __init__(self, dic):
        self.name = dic["name"]
        self.index = int(dic["index"])
        self.count = int(dic["count"])
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class SpeakerParameter:
    def __init__(self, dic):
        self.playback_volume = float(dic["playback_volume"])
        self.playback_globally = True if dic["playback_globally"]=="true" else False
        self.allow_polyphany = True if dic["allow_polyphany"]=="true" else False
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

class SpeakerAlertParameter:
    def __init__(self, dic):
        self.show_alert = True if dic["show_alert"]=="true" else False
        self.show_on_map = True if dic["show_on_map"]=="true" else False
        self.icon_signal_id = SignalID(dic["icon_signal_id"])
        self.alert_message = dic["alert_message"]
    def __str__(self):
        return f"{self.__class__.__name__}(" + ", ".join([f"{k}={v}" for k,v in self.__dict__.items() if v != None]) + ")"
    def __repr__(self):
        return self.__str__()

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

    def tofacDict(self):
        res = {}
        res["r"] = "{:04f}".format(self.r/255)
        res["g"] = "{:04f}".format(self.g/255)
        res["b"] = "{:04f}".format(self.b/255)
        res["a"] = "{:04f}".format(self.a/255)
        return res

## Below classes describe factorio lua concepts described here:
# https://lua-api.factorio.com/latest/Concepts.html

class CircuitCondition:
    def __init__(self, dic):
        for i in dic.items():
            print(i)

