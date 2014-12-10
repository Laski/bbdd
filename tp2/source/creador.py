from interfazbd import InterfazBD
import random


def creador_uniforme():
  bd = InterfazBD("uniforme.sqlite3")
  bd.borrar_tabla("datos")
  bd.crear_tabla("datos", "c1 integer, c2 integer, c3 integer")

  for i in range(10000):
    x = random.randint(1,100)
    y = random.randint(1,10)
    z = random.randint(1,1000)
    bd.insertar_registro("datos", (x, y, z))

def creador_normal(mu, sigma):
  bd = InterfazBD("normal.sqlite3")
  bd.borrar_tabla("datos")
  bd.crear_tabla("datos", "c1 integer, c2 integer, c3 integer")

  for i in range(10000):
    x = random.gauss(mu, sigma)
    y = random.randint(1,10)
    z = random.randint(1,1000)
    bd.insertar_registro("datos", (x, y, z))

if __name__ == "__main__":
  creador_uniforme()
  creador_normal(1, 0.3)
