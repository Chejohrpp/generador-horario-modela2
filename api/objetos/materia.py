class Materia:
    def __init__(self, carrera, nombre, semestre):
        self.nombre = nombre
        self.semestre = semestre
        self.carrera = carrera

    def __str__(self):
        return f"Materia: {self.nombre}, Semestre: {self.semestre}, Carrera: {self.carrera}"

# Ejemplo de uso
# carrera_sistemas = Carrera("Ingeniería de Sistemas")
# materia1 = Materia("Programación 1", 2, carrera_sistemas)
