from toolbox import solve_linear_system as tdma
from toolbox.progress_bar import pb

class Engine:
    
    def __init__(self, grid_temperature = None, grid_mass = None):
        self.temperature_grid = grid_temperature
        self.mass_grid = grid_mass
        self.check_grids()
        self.n_times_steps = self.temperature_grid.nt
        self.tolerance = 1E-3
        self.max_iterations = 100


    def check_grids(self):
        if self.temperature_grid is None and self.mass_grid is None:
            raise ValueError('No grids were given')
        if self.temperature_grid is not None and self.mass_grid is not None:
            if self.temperature_grid.nt != self.mass_grid.nt:
                raise ValueError("Grids must have same time discretization")


    def compute_current_time_state(self, grid):
        grid.gerar_sistema_linear()
        #Solve by modified TMDA 
        resp_tdma = tdma(grid.coeficientes, grid.vetor_independente, grid.phi, grid.ns1)
        grid.atualizar_celulas(resp_tdma)
        return self.time_index, self.n_times_steps-1


    def calculate(self): #TODO: pensar em um nome melhor para essa função
        #FIXME: Generalizar o calculo para o tipo de malha
        for self.time_index in range(self.n_times_steps):
            self.compute_current_time_state(self.temperature_grid)
            pb(self.time_index, self.n_times_steps-1)

    def solve_coupled(self): #TODO: adicionar verificação se o problema é acoplado
        current_temperatures = self.temperature_grid.pegar_phis(0)
        last_temperatures = self.temperature_grid.pegar_phis(0)
        current_masses = self.mass_grid.pegar_phis(0)
        last_masses = self.mass_grid.pegar_phis(0)
        for self.time_index in range(self.n_times_steps):
            error = 1
            it = 0

            while error > self.tolerance and it <= self.max_iterations:
                
                self.temperature_grid.atualizar_phis(current_temperatures,
                                                     current_masses)
            
                self.temperature_grid.gerar_sistema_linear()
                
                #Solve by modified TMDA 
                current_temperatures = tdma(self.temperature_grid.coeficientes,
                                 self.temperature_grid.vetor_independente,
                                 self.temperature_grid.phi,
                                 self.temperature_grid.ns1)


                self.mass_grid.atualizar_phis(current_masses, current_temperatures)
                self.mass_grid.gerar_sistema_linear()

                current_masses = tdma(self.mass_grid.coeficientes,
                                 self.mass_grid.vetor_independente,
                                 self.mass_grid.phi,
                                 self.mass_grid.ns1)
                
                mass_error = self.evaluate_error(current_masses, last_masses)
                temperature_error = self.evaluate_error(current_temperatures, last_temperatures)

                last_masses = current_masses
                last_temperatures = current_temperatures

                error = max(mass_error, temperature_error)
                it += 1
            
            self.temperature_grid.atualizar_celulas(current_temperatures)
            self.mass_grid.atualizar_celulas(current_masses)
            pb(self.time_index, self.n_times_steps-1)

    def evaluate_error(self, current, last):
        return max(abs(current - last))
