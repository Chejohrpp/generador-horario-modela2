
def array_hora_dia (hora_inicio,duracion_clase, hora_fin ):
    # Pedir al usuario la hora de inicio en formato HH:MM
    #hora_inicio = input("Ingresa la hora de inicio (HH:MM): ")

    # Dividir la hora de inicio en horas y minutos
    hora_inicio = hora_inicio.split(':')
    hora_inicio_hora = int(hora_inicio[0])
    hora_inicio_minutos = int(hora_inicio[1])

    # Pedir al usuario la duración de la clase en minutos
    #duracion_clase = int(input("Ingresa la duración de la clase en minutos: "))

    # Calcular la hora de finalización
    #hora_fin = input("Ingresa la hora de fin (HH:MM): ")
    # Dividir la hora de fin en horas y minutos
    hora_fin = hora_fin.split(':')
    hora_fin_hora = int(hora_fin[0])
    hora_fin_minutos = int(hora_fin[1])

    # Crear el array horas_dia
    horas_dia = []
    while hora_inicio_hora < hora_fin_hora or (hora_inicio_hora == hora_fin_hora and hora_inicio_minutos < hora_fin_minutos):
        hora_actual = f"{hora_inicio_hora:02d}:{hora_inicio_minutos:02d}"
        hora_inicio_minutos += duracion_clase
        if hora_inicio_minutos >= 60:
            hora_inicio_hora += 1
            hora_inicio_minutos -= 60
        hora_siguiente = f"{hora_inicio_hora:02d}:{hora_inicio_minutos:02d}"
        horas_dia.append(f"{hora_actual}-{hora_siguiente}")

    return horas_dia
