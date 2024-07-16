from classOverload import metaClass


# noinspection PyRedeclaration
class ciao(metaclass=metaClass):
    def __init__(self):
        print("Ciao")

    def hello(self, *args, **kwargs):
        print("Hello")
    def hello(self):
        print("Hello")
    def hello(self, name: str):
        print("Hello " + name)
    def hello(self, name: str, surname: str):
        print("Hello " + name + " " + surname)
    def hello(self, number):
        print("Hello " + str(number*2))


b = ciao()
b.hello("si", "boh", "cioè")
b.hello(1)
b.hello("John")
b.hello()
b.hello("lol", "si")
