from types_descriptors.positive_integer import PositiveInteger


class Phone:
    memory = PositiveInteger()
    battery_status = PositiveInteger(False, 0, 100)

    def __init__(self, model:str):
        self.__model = model
        self.color = None
        self.memory = 0
        self.battery_status = 0
        self.__defects = set()

    @property
    def model(self) -> str:
        return self.__model

    def get_defects(self) -> list[str]:
        return self.__defects

    def add_defects(self, defects:list[str]):
        if defects:
            self.__defects = self.__defects | set(defects)

    def add_defect(self, defect:str):
        self.__defects.add(defect)

    def remove_defect(self, defect:str):
        self.__defects.remove(defect)

    def __repr__(self):
        return f"""Phone
Model:{self.__model}
Color:{self.color}
Memory:{self.memory}
Battery:{self.battery_status}
defects:\n{"\n".join(self.__defects)}"""
