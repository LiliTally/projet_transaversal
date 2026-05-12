// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/index.js
//  RÔLE    : Point d'entrée de l'application React.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Monter l'application React dans le div #root de index.html
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
