// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/components/Sidebar.jsx
//  RÔLE    : Barre de navigation latérale de l'application.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import React from "react";
import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Logo / Titre */}
      <div className="sidebar-logo">
        <h2>🏥 Smart Santé</h2>
        <p>2035 – Madagascar</p>
      </div>

      {/* Menu de navigation */}
      <ul className="sidebar-nav">
        <li>
          <NavLink to="/" end className={({ isActive }) => isActive ? "active" : ""}>
            📊 Tableau de bord
          </NavLink>
        </li>
        <li>
          <NavLink to="/admission" className={({ isActive }) => isActive ? "active" : ""}>
            ➕ Admettre patient
          </NavLink>
        </li>
        <li>
          <NavLink to="/triage" className={({ isActive }) => isActive ? "active" : ""}>
            🚨 File de triage
          </NavLink>
        </li>
        <li>
          <NavLink to="/orientation" className={({ isActive }) => isActive ? "active" : ""}>
            🗺 Orientation
          </NavLink>
        </li>
        <li>
          <NavLink to="/etablissements" className={({ isActive }) => isActive ? "active" : ""}>
            🏨 Établissements
          </NavLink>
        </li>
        <li>
          <NavLink to="/rapports" className={({ isActive }) => isActive ? "active" : ""}>
            📈 Rapports
          </NavLink>
        </li>
      </ul>

      {/* Info version */}
      <div style={{ position: "absolute", bottom: 16, left: 0, right: 0, textAlign: "center" }}>
        <p style={{ fontSize: "10px", color: "rgba(255,255,255,0.4)" }}>
          Licence 2 Informatique – GPI
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
