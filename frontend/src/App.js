import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import Result from './components/results/Result'
import Sidebar from './components/sidebar/sidebar';
import Parameters from './components/parameter/parameter';
import Horariopic from './components/horariopic/horariopic';

function App() {

  const sidebar_options = [
    { label: "Inicio", href: "/" },
    { label: "Parametros", href: "#parametros" },
    { label: "Resultado", href: "#resultado" },
  ];

  const [getMessage, setGetMessage] = useState({})
  const [getContent, setContent] = useState('inicio')
  const [resultData, setResultData] = useState({})

  const cambiar_contenido = (contenido) => {
    setContent(contenido)
  }

  const obtener_results = (data) => {
    setResultData(data)
  }

  useEffect(()=>{
    axios.get('http://localhost:5000/flask/hello', { withCredentials: true }).then(response => {
      console.log("SUCCESS", response)
      setGetMessage(response)
    }).catch(error => {
      console.log(error)
    })

  }, [])
  return (
    <div className="App">
      <div>
      <Sidebar items={sidebar_options} cambiar_contenido={cambiar_contenido} />
      </div>
      <div>
      <main className='App-header'>
        { getContent.toLowerCase() === 'inicio' && <div>
          {getMessage.status === 200 ? 
            <h3>{getMessage.data.message}</h3>
            :
            <h3>{getContent}</h3>}
            <Horariopic />
          </div>}
        { getContent.toLowerCase() === 'parametros' && <Parameters obtener_results={obtener_results} />}
        { getContent.toLowerCase() === 'resultado' && <Result data={resultData} />}
      </main>
      </div>
    </div>
  );
}

export default App;