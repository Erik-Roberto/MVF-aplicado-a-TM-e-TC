from operator import index
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd
import seaborn as sns


FRAME_RATE = 100


class Heatmap:
    def __init__(self, malha, cmap = "Spectral_r"):
        grid_kws = {'width_ratios': (0.9, 0.05), 'wspace': 0.2}
        self.fig, (self.ax, self.cbar_ax) = plt.subplots(1,2, gridspec_kw = grid_kws, figsize = (10, 8))
        self.malha = malha
        self.cmap = cmap


    def plot_heatmap(self, index_temporal):
        x = self.malha.s1_plot
        y = self.malha.s2_plot
        tempo = self.malha.t[index_temporal]
        z = self.malha.pegar_valores_celulas(index_temporal)

        df = pd.DataFrame(z, index = y[::-1], columns = x)

        self.ax.cla()
        plot = sns.heatmap(
                            data = df,
                            ax = self.ax,
                            cbar_ax = self.cbar_ax,
                            cmap = self.cmap,
                            vmin = 200, #TODO: criar métodos encontrar vmin e vmax ideais
                            vmax = 293,
                          )
        #TODO: Criar legenda dinâmica com o índice temporal e valor do tempo.
        self.ax.set_xticklabels(['{:.2f}'.format(float(t.get_text())) for t in self.ax.get_xticklabels()])
        self.ax.set_yticklabels(['{:.3f}'.format(float(t.get_text())) for t in self.ax.get_yticklabels()])
        self.update_titulo(tempo)


    def update_titulo(self, tempo):
        self.ax.set_title(f"Tempo: {tempo:.1f}s")


    def call_animation(self):
        self.ani = animation.FuncAnimation(
                                    self.fig,
                                    self.plot_heatmap,
                                    frames = self.malha.nt,
                                    repeat = False,
                                    interval = 1000/FRAME_RATE
                                    )
        plt.show()