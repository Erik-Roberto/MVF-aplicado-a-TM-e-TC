from condicoes import Condicoes

class Frame:
    bordas = ("superior", "inferior", "interna", "externa")

    def __init__(self, ns1, ns2):
        """
        ns1 (int): Número de volumes na direção 1 (Horizontal)
        ns2 (int): Número de volumes na direção 2 (Vertical)
        """
        self.ns1 = ns1
        self.ns2 = ns2
        self.borda_padrao()

    def borda_padrao(self):
        horizontal = 0
        vertical = 0
        self.borda_superior(horizontal)
        self.borda_inferior(horizontal)
        self.borda_interior(vertical)
        self.borda_exterior(vertical)

    def borda_superior(self, bordas):
        """
        bordas (lista): Exemplo - [{"pos": (inicio, fim), "tipo": Condicoes.Tipo_1}]
                                       Posição               Tipo da condição
        """
        pass

    def borda_inferior(self, bordas):
        """
        bordas (lista): Exemplo - [{"pos": (inicio, fim), "tipo": Condicoes.Tipo_1}]
                                       Posição               Tipo da condição
        """
        pass
    
    def borda_interior(self, bordas):
        """
        bordas (lista): Exemplo - [{"pos": (inicio, fim), "tipo": Condicoes.Tipo_1}]
                                       Posição               Tipo da condição
        """
        pass
    
    def borda_exterior(self, bordas):
        """
        bordas (lista): Exemplo - [{"pos": (inicio, fim), "tipo": Condicoes.Tipo_1}]
                                       Posição               Tipo da condição
        """
        pass

        