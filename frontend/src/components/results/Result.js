import React from "react";
import Horariopic from "../horariopic/horariopic";
import './Results.css'

const Result = ({ data }) => {
  if (!data.eficiencia) {
    return (
      <div>
        <h1>Aun no ha parametrizado</h1>
      </div>
    )
  }
  return (
    <div>
      <h1>Resultados</h1>
      <h4>Eficiencia: {(data.eficiencia * 100).toFixed(2)}%</h4>
      {data.conflictos && (
        <ul class="conflictos">
          {data.conflictos.map((conflicto) => (
            <li key={conflicto}>{conflicto}</li>
          ))}
        </ul>
      )}
      <div>
      <Horariopic />
      </div>
    </div>
  );
};

export default Result;
