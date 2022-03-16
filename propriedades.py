from abc import ABC, abstractmethod


class Propriedade(ABC):

    @abstractmethod
    def gama1(self):
        pass
    
    
    @abstractmethod
    def gama2(self):
        pass


class PropTemperatura(Propriedade):
    pass


class PropMassa(Propriedade):
    pass