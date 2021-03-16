class Contragent:

    def __init__(self):
        self.name = ""
        self.inn = ""
        self.isorg = False

    def __get__(self, instance, owner) -> dict:
        return self.__dict__
