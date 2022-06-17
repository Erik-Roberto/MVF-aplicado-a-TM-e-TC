from abc import ABC, abstractmethod

import config as conf

class Propriedade(ABC):
    @abstractmethod
    def gama1(self, *args):
        pass
    
    
    @abstractmethod
    def gama2(self, *args):
        pass
    

    @staticmethod
    def reynolds(ro, vel, visc, comprimento_caracteristico):
        return ro*vel*comprimento_caracteristico/visc
        
    @staticmethod
    def difusividade_ar(pressao, temperatura):
        #m2/s
        d_ar = 2.3056*10**(-5)*(9.81*10^4)*((temperatura+273)/273)**(1.81)/pressao
        return d_ar


    @staticmethod
    def alfa_ar():
        return conf.k_ar/(conf.dens_ar*conf.cp_ar)


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
    def coeficiente_convectivo():
        re = PropTemperatura.reynolds(conf.dens_ar, conf.u_ar,
                                     conf.visc_ar, conf.l_car)
        pr = PropTemperatura.prandtl(conf.visc_ar/conf.dens_ar,
                                    PropTemperatura.alfa_ar())
        nu = PropTemperatura.nusselt(re, pr)
        h = nu*conf.k_ar/conf.l_car
        return h


    @staticmethod
    def prandtl(visc_cinem, dif_termica):
        return visc_cinem/dif_termica


    @staticmethod
    def nusselt(re, pr):
        # TODO: Adicionar equações com base no regime de escoamento
        return 0.664*re^(1/2)*pr**(1/3)


class PropMassa(Propriedade):
    def gama1(self, *args):
        return 1
    

    def gama2(self, temperatura, w):
        return self.difusividade_efetiva(w, temperatura)
    

    @staticmethod
    def difusividade_efetiva(temperatura, w):
        # m2/s
        #Ea = 5000
        #D0 = 1E-2
        #D_efetiva = D0*exp(-Ea/(R*T))
        d_efetiva = 3.216*10**-9
        return d_efetiva


    @staticmethod
    def coef_convectivo():
        re = PropMassa.reynolds(conf.dens_ar, conf.u_ar,
                                 conf.visc_ar, conf.l_car)
        sc = PropMassa.schmidt(conf.visc_ar, conf.dens_ar, conf.d_ar)
        
        sh = PropMassa.sherwoods(re, sc)
        hm = sh*conf.d_ar/conf.l_car
        return hm


    @staticmethod
    def schmidt(visc, ro, d_ab):
        return visc/(ro*d_ab)


    @staticmethod
    def sherwoods(re, sc):
        # TODO: Adicionar equações de acordocom o escoamento
        return 0.664*re**(1/2)*sc**(1/3)