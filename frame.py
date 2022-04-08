from condicoes import Condicoes

class Frame:
    def __init__(self, ns1, ns2):
        """
        ns1 (int): Número de volumes na direção 1 (Horizontal)
        ns2 (int): Número de volumes na direção 2 (Vertical)
        """
        self.ns1 = ns1
        self.ns2 = ns2
        self.borda_padrao()


    def borda_padrao(self):
        # TODO: Adicionar valores padrão por arquivo de config
        horizontal = [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273}] 
        vertical = [{"pos": (0, self.ns2), "tipo": Condicoes.Tipo_1, "valor": 273}]
        self.borda_superior = horizontal
        self.borda_inferior = horizontal
        self.borda_interior = vertical
        self.borda_exterior = vertical


    def verifica_condicoes(self, lista):
        chaves = ("pos", "tipo", "valor")
        if not isinstance(lista, list):
            raise TypeError("Objetos de atribução devem ser lista.") 
        for dicionario in lista:
            if not isinstance(dicionario, dict):
                raise TypeError("Objetos da lista devem ser dicionários.")
            if not chaves in dicionario.keys():
                chave = [k for k in dicionario.keys() if not k in chaves]
                raise ValueError(f"A(s) chave(s) {chave} deve(m) ser passada(s).")


    def switcher(self, borda):
        opcoes = {
            "superior": self.borda_superior,
            "inferior": self.borda_inferior,
            "exterior": self.borda_exterior,
            "interior": self.borda_interior,
            }
        return opcoes.get(borda.lower())


    def definir_borda_superior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_superior = lista


    def definir_borda_inferior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_inferior = lista


    def definir_borda_exterior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_exterior = lista


    def definir_borda_interior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_interior = lista


    def get_condicao(self, pos, borda):
        condicoes = self.switcher(borda)
        for dicionario in condicoes:
            if dicionario["pos"][0] <= pos < dicionario["pos"][1]:
                return (dicionario["tipo"],  dicionario["valor"])

