class Salon:
    def __init__(self, nombre, cantidad_asientos):
        self.nombre = nombre
        self.cantidad_asientos = cantidad_asientos

    def __str__(self):
        return f"Salón: {self.nombre}, Asientos: {self.cantidad_asientos}"

# Ejemplo de uso
#salon1 = Salon("SALON 1", 50)
