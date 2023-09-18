import React from "react";
import './sidebars.css'

const Sidebar = ({ items, cambiar_contenido }) => {
  const handleClick = (item) => {
    // Acción cuando se hace clic en un elemento de la barra lateral
    cambiar_contenido(item.label)
    console.log(item.label)
  };

  return (
    <div className="sidebar">
      <ul>
        {items.map((item, index) => (
          <li key={index} onClick={() => handleClick(item)}>
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
