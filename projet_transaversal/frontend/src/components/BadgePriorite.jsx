// ============================================================
//  FICHIER : src/components/BadgePriorite.jsx
//  RÔLE    : Badge coloré affichant le niveau de priorité.
//            Rouge/Orange/Jaune/Vert/Bleu
// ============================================================

import React from "react";

function BadgePriorite({ niveau, couleur }) {
  // Correspondance niveau → classe CSS
  const classes = {
    1: "badge badge-rouge",
    2: "badge badge-orange",
    3: "badge badge-jaune",
    4: "badge badge-vert",
    5: "badge badge-bleu",
  };

  const emojis = {
    1: "🔴",
    2: "🟠",
    3: "🟡",
    4: "🟢",
    5: "🔵",
  };

  return (
    <span className={classes[niveau] || "badge"}>
      {emojis[niveau]} {couleur || `Niveau ${niveau}`}
    </span>
  );
}

export default BadgePriorite;


// ============================================================
//  FICHIER : src/components/CartePatient.jsx
//  RÔLE    : Carte affichant les informations d'un patient.
// ============================================================

export function CartePatient({ patient, onTraiter }) {
  return (
    <div
      className="card"
      style={{
        borderLeft: `4px solid ${getCouleurBordure(patient.niveau_priorite)}`,
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <h4 style={{ color: "#1A5276", marginBottom: 4 }}>
            {patient.prenom} {patient.nom}
          </h4>
          <p style={{ fontSize: "12px", color: "#555" }}>
            ID : {patient.id_patient} | Âge : {patient.age} ans
          </p>
          <p style={{ fontSize: "12px", color: "#555", marginTop: 4 }}>
            Score de triage : <strong>{patient.score_triage}</strong>
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <BadgePriorite niveau={patient.niveau_priorite} couleur={patient.couleur} />
          {patient.alerte_requise && (
            <p style={{ fontSize: "11px", color: "#C0392B", marginTop: 6 }}>
              ⚠ Alerte envoyée
            </p>
          )}
        </div>
      </div>

      {onTraiter && (
        <div style={{ marginTop: 12, textAlign: "right" }}>
          <button className="btn btn-primary" onClick={() => onTraiter(patient)}>
            Traiter ce patient
          </button>
        </div>
      )}
    </div>
  );
}

function getCouleurBordure(niveau) {
  const couleurs = { 1: "#C0392B", 2: "#E67E22", 3: "#F1C40F", 4: "#27AE60", 5: "#2980B9" };
  return couleurs[niveau] || "#1A5276";
}
