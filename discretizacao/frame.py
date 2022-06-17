from discretizacao.condicoes import Condicoes

class Frame:
    def __init__(self, ns1, ns2):
        """
        ns1 (int): Número de volumes na direção 1 (Horizontal)
        ns2 (int): Número de volumes na direção 2 (Vertical)
        """
        self.tipo_padrao = Condicoes.Tipo_2
        self.valor_padrao = 0
        self.ns1 = ns1
        self.ns2 = ns2
        self.borda_padrao()
        self.opcoes = {
                        "superior": self.borda_superior,
                        "inferior": self.borda_inferior,
                        "exterior": self.borda_exterior,
                        "interior": self.borda_interior,
                    }

    def borda_padrao(self):
        #horizontal = [{"pos": (0, self.ns1), "tipo":self.tipo_padrao, "valor": self.valor_padrao}] 
        #vertical = [{"pos": (0, self.ns2), "tipo": self.tipo_padrao, "valor": self.valor_padrao}]
        vertical = [{"pos": (0, self.ns2), "tipo": Condicoes.Tipo_2, "valor": 0}]
        horizontal = [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_2, "valor": 0}]
        
        self.borda_superior = horizontal
        self.borda_inferior = horizontal
        self.borda_interior = vertical
        self.borda_exterior = vertical


    def verifica_condicoes(self, lista):
        chaves = ("pos", "tipo", "valor")
        if not isinstance(lista, list):
            raise TypeError("Objetos de atribuição devem ser lista.") 
        for dicionario in lista:
            if not isinstance(dicionario, dict):
                raise TypeError("Objetos da lista devem ser dicionários.")

            for chave in chaves:
                if not chave in dicionario.keys():
                    raise ValueError(f"A chave '{chave}' está faltando.") #TODO: levantar exceção adequada - mudar o ValueError


    def switcher(self, borda):
        return self.opcoes.get(borda.lower())


    def definir_borda_superior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_superior = lista
        self.opcoes.update({"superior": self.borda_superior})


    def definir_borda_inferior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_inferior = lista
        self.opcoes.update({"inferior": self.borda_inferior})

    def definir_borda_exterior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_exterior = lista
        self.opcoes.update({"exterior": self.borda_exterior})

    def definir_borda_interior(self, lista):
        """
        lista (lista): Lista com todas as condições de contorno nessa fronteira
        Exemplo: 
        [{"pos": (0, self.ns1), "tipo": Condicoes.Tipo_1, "valor": 273},...]
        """
        self.verifica_condicoes(lista)
        self.borda_interior = lista
        self.opcoes.update({"interior": self.borda_interior})

    #FIXME: A definição de CCs na borda exterior inverte o posicionamento das CCs
    def get_condicao(self, pos, borda):
        condicoes = self.switcher(borda)
        for dicionario in condicoes:
            if dicionario["pos"][0] <= pos < dicionario["pos"][1]:
                return (dicionario["tipo"],  dicionario["valor"])
        #TODO:Melhorar maneira de levantar exceção
        raise ValueError("Não foi encontrado nenhuma condição de contorno na posição especificada.")


