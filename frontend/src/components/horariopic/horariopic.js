import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Horariopic() {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    // Hacer una solicitud GET para obtener la imagen desde el servidor Flask
    axios.get('http://127.0.0.1:5000/horario.png', { responseType: 'arraybuffer' })
      .then(response => {
        // Convierte los datos binarios en una URL de datos
        const base64 = btoa(
          new Uint8Array(response.data).reduce(
            (data, byte) => data + String.fromCharCode(byte),
            ''
          )
        );
        setImageSrc(`data:image/png;base64,${base64}`);
      })
      .catch(error => {
        console.error('Error al cargar la imagen:', error);
      });
  }, []);

  return (
    <div>
      {imageSrc && <img src={imageSrc} alt="Horario" style={{ width: '900px', height: '500px' }} />}
    </div>
  );
}

export default Horariopic;
