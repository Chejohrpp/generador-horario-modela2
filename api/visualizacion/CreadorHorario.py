import matplotlib.pyplot as plt
from api.objetos.horario import Horario

def ajustar_fuente_celda(fig , cell, text):
    fontsize = 8  # Tamaño inicial de fuente
    text.set_fontsize(fontsize)
    text.set_va('center')  # Centra verticalmente el texto

def generar_imagen(array_salones, array_hora_dia, horarios):
    # Datos de ejemplo: días de la semana y horas del día
    dias_semana = array_salones
    #
    horas_dia = array_hora_dia
    #
    lista_horarios = horarios
    # Crear una tabla vacía
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.axis('off')  # Ocultar ejes

    # Crear la tabla
    tabla = plt.table(cellText=[['' for _ in range(len(dias_semana))] for _ in range(len(horas_dia))],
                      colLabels=dias_semana,
                      cellLoc='center',
                      rowLabels=horas_dia,
                      loc='center'
                      )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1.1, 3.5)  # Ajusta el tamaño de la tabla

    # Itera sobre la lista de horarios y coloca la información en la tabla
    for horario in lista_horarios:
        # Obtén la hora y el salón del horario
        hora_horario, salon_horario = horario.horario, horario.salon

        # Encuentra la fila y columna correspondiente
        fila = horas_dia.index(hora_horario)
        columna = dias_semana.index(salon_horario)

        # Coloca el nombre de la materia en la celda correspondiente
        cell = tabla.get_celld()[(fila + 1, columna)]
        
        # Dividimos la cadena de texto en dos partes        
        materia_primera_parte, materia_segunda_parte = dividir_cadena(horario.materia, 26)

        cell.get_text().set_text(materia_primera_parte + materia_segunda_parte + '\n Seccion ' + horario.seccion + '\n' 
                                 + horario.profesor + '\n' + horario.carrera + '\n' + horario.semestre )
        # Añadir un fondo de color según el valor de horario.color
        if horario.color == "red":
            cell.set_facecolor("red")
        elif horario.color == "green":
            cell.set_facecolor("green")
        elif horario.color == "yellow":
            cell.set_facecolor("yellow")
        ajustar_fuente_celda(fig, cell, cell.get_text())  # Ajusta fuente y centrado

    # guardar la imagen
    # plt.savefig("horario.jpg", format="jpg")
    fig.set_size_inches(20, 10)
    plt.savefig('api/resources/horario.png')

    # Mostrar la tabla
    # plt.show()

def dividir_cadena(cadena, longitud):
  """
  Divide una cadena de texto en dos partes, la primera de longitud `longitud` y la segunda el resto de la cadena.

  Args:
    cadena: La cadena de texto a dividir.
    longitud: La longitud de la primera parte de la cadena.

  Returns:
    Un tuple con la primera y segunda parte de la cadena.
  """

  if len(cadena) <= longitud:
    return cadena, ''
  else:
    return cadena[:longitud], '\n' + cadena[longitud:]
