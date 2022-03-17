from abc import ABC, abstractmethod


class Propriedade(ABC):

    @abstractmethod
    def gama1(self):
        pass
    
    
    @abstractmethod
    def gama2(self):
        pass
    

    @staticmethod
    def reynolds(ro, vel, visc, comprimento_caracteristico):
        return ro*vel*comprimento_caracteristico/visc
        


class PropTemperatura(Propriedade):

    def gama1(self, w, temperatura):
        cp = self.capacidade_calorifica(w, temperatura)
        ro = self.densidade(w,temperatura)
        return cp*ro
    

    def gama2(self, w, temperatura):
        return self.condutividade_termica(w, temperatura)


    @staticmethod
    def condutividade_termica(w, temperatura):
        # W/m.K
        k = 0.127
        return k

    @staticmethod
    def capacidade_calorifica(w, temperatura):
        #J/kg.K
        c = 1542.432
        return c


    @staticmethod
    def densidade(w, temperatura):
        # kg/m3
        ro = 194
        return ro
    

    @staticmethod
    def entalpia_vaporizacao(temperatura):
        # J/mol
        hv = 2000*10**3
        return hv


    @staticmethod
    def difusividade_termica(w, temperatura):
        # m^2/s
        k = PropTemperatura.condutividade_termica(w, temperatura)
        cp = PropTemperatura.capacidade_calorifica(w, temperatura)
        ro = PropTemperatura.densidade(w, temperatura)
        dif_termica = k/(ro*cp)
        return dif_termica


    @staticmethod
    def coeficiente_convectivo(prop_ar, l_car):
        re = PropTemperatura.reynolds(prop_ar.dens_ar, prop_ar.u_ar,
                                     prop_ar.visc_ar, l_car)
        pr = PropTemperatura.prandtl(prop_ar.visc_ar/prop_ar.dens_ar,
                                    prop_ar.alfa_ar)
        nu = PropTemperatura.nusselt(re, pr)
        h = nu*prop_ar.k_ar/l_car
        return h


    @staticmethod
    def prandtl(visc_cinem, dif_termica):
        return visc_cinem/dif_termica


    @staticmethod
    def nusselt(re, pr):
        # TODO: Adicionar equações com base no regime de escoamento
        return 0.664*re^(1/2)*pr**(1/3)



class PropMassa(Propriedade):
    pass