from interfazbd import InterfazBD
import random

class CreadorDistribucion(object):
    def __init__(self, n_registros):
        self.n_registros = n_registros

    def crear(self):
        bd = InterfazBD("datasets/" + self.nombre + ".sqlite3")
        bd.borrar_tabla("datos")    # para reiniciarla si ya existia
        bd.crear_tabla("datos", "c integer")
        registros = [(self.get_random(),) for i in range(self.n_registros)]
        bd.insertar_registros("datos", registros)

    def get_random(self):
        raise NotImplementedError


class CreadorUniforme(CreadorDistribucion):
    def __init__(self, n_registros=10000, valor_max=1000):
        super(CreadorUniforme, self).__init__(n_registros)
        self.nombre = "uniforme"
        self.valor_max = valor_max

    def get_random(self):
        return random.randint(1, self.valor_max)


class CreadorNormal(CreadorDistribucion):
    def __init__(self, n_registros=10000, mu=500, sigma=100):
        super(CreadorNormal,self).__init__(n_registros)
        self.nombre = "normal"
        self.mu = mu
        self.sigma = sigma

    def get_random(self):
        return int(random.gauss(self.mu, self.sigma))


class CreadorRaro(CreadorDistribucion):
    # crea la distribucion con muy pocos valores, muy repetidos
    def __init__(self, n_registros=10000):
        super(CreadorRaro,self).__init__(n_registros)
        self.nombre = "raro"

    def get_random(self):
        items = [1,1,1,1,400,400,400,132,16,16,1034,1034,1034,1034,1034,503,503,503,503,503,503]
        return random.choice(items)


if __name__ == "__main__":
    CreadorUniforme().crear()
    CreadorNormal().crear()
    CreadorRaro().crear()
