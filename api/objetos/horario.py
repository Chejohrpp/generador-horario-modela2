class Horario:
    def __init__(self, materia, horario, seccion, profesor, salon, carrera,semestre):
        self.materia = materia
        self.horario = horario
        self.seccion = seccion
        self.profesor = profesor
        self.salon = salon
        self.carrera = carrera
        self.semestre = semestre
        self.color = 'green'

    def __str__(self):
        return f"Materia: {self.materia}\nHorario: {self.horario}\nSección: {self.seccion}\nProfesor: {self.profesor}\nSalón: {self.salon}\nCarrera: {self.carrera}"
    
    def estilo(self, color='green'):
        self.color = color
        
