import React, { useState, useEffect } from "react";
import axios from "axios";
import './parameter.css'

const Parameters = ( {obtener_results}) => {
    // no me da tiempo para la carga de datos (dejarlo de utlimo), add button
    // y luego con un cuadro abajo se muestre si se realizo o no
  const [horarioInicial, setHorarioInicial] = useState("15:20");
  const [horarioFinal, setHorarioFinal] = useState("22:00");
  const [duracion, setDuracion] = useState(50)
  const [prioridad, setPrioridad] = useState("materia");
  const [mensaje, setMensaje] = useState("");

  const handleHorarioInicialChange = (event) => {
    setHorarioInicial(event.target.value);
  };

  const handleduracion = (event) => {
    setDuracion(event.target.files);
  };

  const handleHorarioFinalChange = (event) => {
    setHorarioFinal(event.target.value);
  };

  const handlePrioridadChange = (event) => {
    setPrioridad(event.target.value);
  };

  const handleSubmit = async () => {
    const data = {
      hora_incio: horarioInicial,
      hora_final: horarioFinal,
      duracion: duracion,
      prioridad: prioridad
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/genhor/parameter", data);
      if (response.status === 200) {
        setMensaje("Horario generado con éxito!");
        obtener_results(response.data)
      } else {
        setMensaje("Hubo un error al generar el horario.");
      }
    } catch (error) {
      setMensaje("Hubo un error al generar el horario.");
    }
  };

  useEffect(() => {
    if (mensaje !== "") {
      setTimeout(() => {
        setMensaje("");
      }, 3000);
    }
  }, [mensaje]);

  return (
    <div className="parameters">
      <h1>Parámetros</h1>
      <div>
        <label>Horario inicial:</label>
        <input
          type="time"
          value={horarioInicial}
          onChange={handleHorarioInicialChange}
        />
      </div>
      <div>
        <label>Horario final:</label>
        <input
          type="time"
          value={horarioFinal}
          onChange={handleHorarioFinalChange}
        />
      </div>
      <div>
        <label>Tiempo de duracion de periodos</label>
        <input type="number" value={duracion} onChange={handleduracion} />
      </div>
      <div>
        <label>Prioridad:</label>
        <select value={prioridad} onChange={handlePrioridadChange}>
          <option value="materia">Materias</option>
          <option value="salon">Salones</option>
        </select>
      </div>
      <div>
        <button onClick={handleSubmit}>Generar horario</button>
      </div>
      <div>
        <p>{mensaje}</p>
      </div>
    </div>
  );
};

export default Parameters;
