import React from "react";
import "../styles/Barra.css";
import { AiFillDingtalkSquare } from "react-icons/ai";
import { TfiMenuAlt } from "react-icons/tfi";
import { FiUser } from "react-icons/fi";
import { MdOutlineCalendarToday } from "react-icons/md";
import { MdAssessment } from "react-icons/md";
import { AiOutlineCloudUpload } from "react-icons/ai";
import { FaRegMap } from "react-icons/fa";
import { RiListSettingsLine } from "react-icons/ri";
import { useState } from "react";

function Barra() {
  const [mostrarMapa, setMostrarMapa] = useState(false);

  const handleMapClick = () => {
    setMostrarMapa(!mostrarMapa);
  };

  const handleMapFalse = () => {
    setMostrarMapa(false);
  };

  return (
    <>
      <div className="barra">
        <div className="dots">
          <span className="dot"></span>
          <span className="dot"></span>
          <span className="dot"></span>
        </div>
        <AiFillDingtalkSquare className="icon" onClick={handleMapFalse} />
        <TfiMenuAlt className="icon" />
        <FiUser className="icon" />
        <MdOutlineCalendarToday className="icon" />
        <MdAssessment className="icon" />
        <AiOutlineCloudUpload className="icon" />
        <FaRegMap className="icon" onClick={handleMapClick} />
        <RiListSettingsLine className="icon" />
      </div>

      {mostrarMapa && (
        <div className="mapa-overlay">
          <iframe
            src="/mapa_estaciones.html"
            className="mapa-iframe"
            title="Mapa de estaciones"
          />
        </div>
      )}
    </>
  );
}

export default Barra;
