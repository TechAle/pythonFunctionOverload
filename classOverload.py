import inspect
import re


def wrapper(name):
    def fun(myFunctions, *args, **kwargs):
        myFunctions = getattr(myFunctions, name + "_MINE")
        toCall = "(self"
        for i in args:
            toCall += ", " + type(i).__name__.replace("int", "number").replace("float", "number")
        toCall += ")"
        if toCall in myFunctions:
            b = myFunctions[toCall](myFunctions['cls'], *args, **kwargs)
        elif myFunctions.__contains__("(self, *args, **kwargs)"):
            b = myFunctions["(self, *args, **kwargs)"](myFunctions['cls'], *args, **kwargs)
        else:
            # Raise an error if the function is not found
            raise AttributeError("Function not found")
        return b

    return fun

def remove_colon_content(s):
    # Define the regular expression pattern to match the comma followed by any characters until the colon
    pattern = r',[^,:]*:'
    # Replace the matched pattern with a comma
    result = re.sub(pattern, ',', s)
    return result


class myOverload(dict):
    def __setitem__(self, key, value):
        if callable(value) and not key.startswith("__"):
            # Replace the function in the class with the new function
            if key + "_MINE" not in self.keys():
                self[key + "_MINE"] = {}
            self[key + "_MINE"][remove_colon_content(str(inspect.signature(value)))] = value
            value = wrapper(key)
        # Optionally customize how items are set
        super().__setitem__(key, value)


class metaClass(type):

    @classmethod
    def __prepare__(metacls, name, bases):
        return myOverload()

    def __new__(cls, name, bases, dct):
        cls.__dct__ = dct
        return super().__new__(cls, name, bases, dct)

    def __call__(self, *args, **kwargs):
        b = super().__call__(*args, **kwargs)
        for key in self.__dct__.keys():
            if key + "_MINE" in self.__dct__.keys():
                self.__dct__[key + "_MINE"]["cls"] = b

        return b


