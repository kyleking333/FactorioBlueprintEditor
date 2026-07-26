# Contains a template class and the definitions of all Components which can be included in a blueprint
from abc import ABC, abstractmethod
from typing import List

from helpers import toDict

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
                d[attr] = toDict(val)
        return d

#############################
# Factorio JSON Class Def's #
#############################
# Class/Field names correlate with https://wiki.factorio.com/Blueprint_string_format)
# Notable exceptions include the control_behavior and connection objects.

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
    
    @classmethod
    def from_ints(cls, r, g, b, a=1.0):
        return cls(a / 255, b / 255, c / 255, d / 255)
