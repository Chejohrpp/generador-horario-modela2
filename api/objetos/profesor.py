class Profesor:
    def __init__(self, nombre, carrera):
        self.nombre = nombre
        self.carrera = carrera

    def __str__(self):
        return f"Profesor: {self.nombre}, Carrera: {self.carrera}"

# Ejemplo de uso
# profesor1 = Profesor("Profesor A", 'comun')
