#Definição de constantes físicas
R = 8.314 # J/mol.K


#Valores ambientes e constantes
l_car = 0.15             #m - Comprimento característico
u_ar = 1                 #m/s - Velociddade do ar
dens_ar = 1.073          #kg/m3 - Densidade ar
visc_ar = 19.907*10**-6  #Pa.s - Viscosidade ar
k_ar = 0.287             #W/m.K - condutividade térmica ar
cp_ar = 1004.8           #J/kg.K - Capacidade calorífica ar a 21.1ºC
t_ar = 293               #K - Temperatura do ar

#Definição do problema
tipo_problema = 'temperatura' #Opções: massa ou temperatura

#Condições iniciais:
temperatura_ini = 293    #K
c_ini = 8178.22          #mol/m3
tempo_inicial = 0        #s

tempo_simulacao = 3800   # s

eqacao_h_std = True      # Define  qual equação de h será usada (padrão ou custom)

#Geometria:
dimensao1 = 0.15/2       #m (R / x)
dimensao2 = 0.005        #m (z / y)
geometria = 'cilindrico'   #Opções: cilindrico ou cartesiano

#Parametros de simulação
n_s1 = 6                 #  (R / x)
n_s2 = 7                 #  (z / y)
n_t = 3                  # tempo

tolerancia = 10**-3
it_max = 100
