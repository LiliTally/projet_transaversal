// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/App.jsx
//  RÔLE    : Composant racine de l'application React.
//            Configure le routeur et la mise en page principale.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Styles globaux
import "./styles/global.css";

// Composants
import Sidebar from "./components/Sidebar";

// Pages
import Dashboard      from "./pages/Dashboard";
import Admission      from "./pages/Admission";
import FileTriage     from "./pages/FileTriage";
import Orientation    from "./pages/Orientation";
import Etablissements from "./pages/Etablissements";
import Rapports       from "./pages/Rapports";

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">

        {/* Barre de navigation latérale */}
        <Sidebar />

        {/* Contenu principal */}
        <main className="main-content">
          <Routes>
            <Route path="/"               element={<Dashboard />} />
            <Route path="/admission"      element={<Admission />} />
            <Route path="/triage"         element={<FileTriage />} />
            <Route path="/orientation"    element={<Orientation />} />
            <Route path="/etablissements" element={<Etablissements />} />
            <Route path="/rapports"       element={<Rapports />} />
          </Routes>
        </main>

      </div>
    </BrowserRouter>
  );
}

export default App;
