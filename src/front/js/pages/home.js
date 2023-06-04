import React from "react";
import { Link } from "react-router-dom";
import "../../styles/home.css";

export const Home = () => {

  return (
    <div>
      <div className="home card w-50 text-center">
        <div className="card-body"></div>
        <div className="boton-registro">
          <Link
            className="nav-link text-dark"
            aria-current="page"
            to="/registro"
          >
            <button type="submit" className="registrate btn btn-block p-2 px-3 ">
              <strong>Registrarme</strong>
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};
