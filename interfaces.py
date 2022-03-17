"""
Todos os devidos sinais que aparecem durante a descretização
devem ser considerados nas classes de interface.
"""
from abc import ABC, abstractmethod


class Interface(ABC):
    def __init__(self, celula, ds, area, tipo = None):
        """
        celula (objeto Celula): Célula que conterá a interface
        ds (float): Tamanho da celula na direção s
        area (float): Área da interface
        tipo (str): Tipo da interface (entrada ou saida)
        """
        self.cel = celula
        self.ds = ds
        self.area = area
        self.tipo = tipo

    def definir_mod(self):
        if self.tipo.lower() == 'saida':
            self.mod = -1
        elif self.tipo.lower() == 'entrada':
            self.mod = 1
        else:
            raise ValueError("Tipo especificado inválido.")

    @abstractmethod
    def calc_a(self):
        pass


    @abstractmethod
    def calc_anb(self):
        pass


    @abstractmethod
    def calc_b(self):
        pass


class InterfaceDifusiva(Interface):
    def calc_a(self):
        numerador = self.area*self.cel.gama2
        denominador = self.cel.vol*self.cel.gama1*self.ds
        return numerador/denominador


    def calc_anb(self):
        numerador = -self.area*self.cel.gama2
        denominador = self.cel.vol*self.cel.gama1*self.ds
        return numerador/denominador


    def calc_b(self):
        return 0


class InterfaceCCTipo1(Interface):
    """ Condição de Contorno com Phi descrito
    """
    def __init__(self, phi_f, *args, **kwargs):
        """
        phi_f (float): Valor de phi na fronteira
        """
        super().__init__(*args, **kwargs)
        self.phi_f = phi_f


    def calc_a(self):
        numerador = self.area*self.cel.gama2
        denominador = self.cel.vol*self.cel.gama1*self.ds
        return numerador/denominador


    def calc_anb(self):
        return 0


    def calc_b(self):
        numerador = self.area*self.cel.gama2
        denominador = self.cel.vol*self.cel.gama1*self.ds
        return numerador/denominador


class InterfaceCCTipo2(Interface):
    """ Condição de Contorno com fluxo na interface descrito
    """
    def __init__(self, fluxo, *args, **kwargs):
        """
        fluxo (float): Valor do fluxo de phi na fronteira
        """
        super().__init__(*args, **kwargs)
        self.fluxo = fluxo
        self.definir_mod()

    def calc_a(self):
        return 0


    def calc_anb(self):
        return 0


    def calc_b(self):
        numerador = self.mod*self.area*self.fluxo
        denominador = self.cel.vol*self.cel.gama1
        return numerador/denominador


class InterfaceCCTipo3(Interface):
    """ Condição de Contorno com convecção
    """
    def __init__(self, phi_inf, *args, **kwargs):
        """
        phi_inf (float): Valor de phi na vizinhança
        foo_h (function): Função para calclo docoeficiente convectivo
        """
        super().__init__(*args, **kwargs)
        self.phi_inf = phi_inf
        self.definir_mod()
        self.calcular_h = self.cel.propriedades.coeficiente_convectivo


    def calc_a(self):
        h = self.calcular_h()
        numerador = self.mod*self.area*h
        denominador = self.cel.vol*self.cel.gama1
        return numerador/denominador


    def calc_anb(self):
        return 0


    def calc_b(self):
        h = self.calcular_h()
        numerador = self.mod*self.area*h*self.phi_inf
        denominador = self.cel.vol*self.cel.gama1
        return numerador/denominador


