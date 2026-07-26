# Contains helper functions

# This can be called on any object
# if called on a custom object it calls object.dict()
# else it tries to iterate through the object and call itself recursively on it's children
def toDict(obj):
    try:
        return obj.dict()  # object is a custom class with the dict field
    except:
        if isinstance(obj, dict):  # object is a dictionary. Let's reconstruct it and call dict() on it's children
            res = {}
            for k,v in obj.items():
                res[k] = toDict(v)
            return res
        elif isinstance(obj, list) or isinstance(obj, tuple):
            res = []
            for v in obj:
                res.append(toDict(v))
            return res
        else:  # must be a primitive type, leave as is
            return obj
