from math import pi

class Cartesiano:
    def __init__(self, dx, dy, dz):
        """
        dx (float): Tamanho do V.C. na direção x
        dy (float): Tamanho do V.C. na direção y
        dz (float): Tamanho do V.C. na direção desconsiderada (Tamanho total do domínio nessa dir)
        """
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.volume = dx*dy*dz
        self.area_externa = dx*dy
        self.area_interna = dx*dy
        self.area_superior = dx*dy
        self.area_inferior = dx*dy
    
    @property
    def ds1(self):
        return self.dx
    
    @property
    def ds2(self):
        return self.dy


class Cilindrico:
    def __init__(self, dz, dr, r_ext, r_int):
        """
        dz (float): Tamanho do V.C. na direção z
        dr (float): Tamanho do V.C. na direção r
        r_ext (float): Raio na interface externa
        r_int (float): Raio na interface interna
        """
        self.dz = dz
        self.dr = dr
        self.r_ext = r_ext
        self.r_int = r_int
        self.volume = dz*pi*(r_ext**2 - r_int**2)
        self.area_externa = dz*2*pi*r_ext
        self.area_interna = dz*2*pi*r_int
        self.area_superior = pi*(r_ext**2 - r_int**2)
        self.area_inferior = pi*(r_ext**2 - r_int**2)

    @property
    def ds1(self):
        return self.dr
    
    @property
    def ds2(self):
        return self.dz
