// ============================================================
//  FICHIER : src/pages/Etablissements.jsx
//  RÔLE    : Gestion des établissements de santé du réseau.
//            Mise à jour des lits disponibles.
// =====================================================

import React, { useState } from "react";
import { mettreAJourLits } from "../api/patientApi";

// Données des établissements (en production : chargées depuis l'API)
const ETABLISSEMENTS_INITIAUX = [
  { id: "CSB-01",   nom: "CSB Manakambahiny",            niveau: 2, lits_dispo: 15, capacite: 20 },
  { id: "HOP-DIS",  nom: "Hôpital District Antananarivo", niveau: 3, lits_dispo: 12, capacite: 80 },
  { id: "HOP-REF",  nom: "Hôpital Référence Analakely",   niveau: 4, lits_dispo: 35, capacite: 200 },
  { id: "CHUR-ANT", nom: "CHUR Antananarivo",             niveau: 5, lits_dispo: 60, capacite: 500 },
  { id: "HOP-SAT",  nom: "Hôpital Saturé (exemple)",      niveau: 3, lits_dispo: 0,  capacite: 60 },
];

const NIVEAUX = { 1: "CSB I", 2: "CSB II", 3: "Hôp. District", 4: "Hôp. Référence", 5: "CHUR" };

function Etablissements() {
  const [etabs, setEtabs]         = useState(ETABLISSEMENTS_INITIAUX);
  const [editId, setEditId]       = useState(null);
  const [nouveauxLits, setNouveauxLits] = useState("");
  const [message, setMessage]     = useState(null);

  const ouvrirEdition = (etab) => {
    setEditId(etab.id);
    setNouveauxLits(etab.lits_dispo);
  };

  const sauvegarder = async (id) => {
    try {
      // Appel API Flask : PUT /etablissements/:id/lits
      await mettreAJourLits(id, parseInt(nouveauxLits));
      setEtabs(etabs.map(e =>
        e.id === id ? { ...e, lits_dispo: parseInt(nouveauxLits) } : e
      ));
      setEditId(null);
      setMessage({ type: "succes", texte: "✅ Disponibilité mise à jour. Graphe recalculé." });
    } catch (err) {
      setMessage({ type: "erreur", texte: "Erreur lors de la mise à jour." });
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ color: "#1A5276", fontSize: 22, marginBottom: 4 }}>
          🏨 Établissements de santé
        </h1>
        <p style={{ color: "#555", fontSize: 13 }}>
          Gestion du réseau hospitalier. La mise à jour des lits recalcule
          automatiquement les poids du graphe pour Dijkstra.
        </p>
      </div>

      {message && (
        <div className={`alerte alerte-${message.type === "succes" ? "succes" : "critique"}`}
             style={{ marginBottom: 16 }}>
          {message.texte}
        </div>
      )}

      <div className="card">
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Niveau</th>
                <th>Lits disponibles</th>
                <th>Occupation</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {etabs.map(etab => {
                const occupation = Math.round((1 - etab.lits_dispo / etab.capacite) * 100);
                return (
                  <tr key={etab.id}>
                    <td><code>{etab.id}</code></td>
                    <td>{etab.nom}</td>
                    <td><span className="badge" style={{ background: "#EAF2F8", color: "#1A5276" }}>
                      {NIVEAUX[etab.niveau]}
                    </span></td>
                    <td>
                      {editId === etab.id ? (
                        <input type="number" value={nouveauxLits}
                               onChange={e => setNouveauxLits(e.target.value)}
                               style={{ width: 60, padding: "4px 8px", border: "1px solid #ccc", borderRadius: 4 }} />
                      ) : (
                        <span style={{ color: etab.lits_dispo === 0 ? "#C0392B" : "#27AE60", fontWeight: "bold" }}>
                          {etab.lits_dispo} / {etab.capacite}
                        </span>
                      )}
                    </td>
                    <td>
                      <div style={{ width: 80, background: "#eee", borderRadius: 4, height: 8 }}>
                        <div style={{
                          width: `${occupation}%`,
                          background: occupation > 90 ? "#C0392B" : occupation > 70 ? "#E67E22" : "#27AE60",
                          height: 8, borderRadius: 4
                        }} />
                      </div>
                      <span style={{ fontSize: 11 }}>{occupation}%</span>
                    </td>
                    <td>
                      {editId === etab.id ? (
                        <div style={{ display: "flex", gap: 6 }}>
                          <button className="btn btn-success" onClick={() => sauvegarder(etab.id)}
                                  style={{ padding: "4px 10px", fontSize: 12 }}>✅</button>
                          <button className="btn btn-secondary" onClick={() => setEditId(null)}
                                  style={{ padding: "4px 10px", fontSize: 12 }}>✖</button>
                        </div>
                      ) : (
                        <button className="btn btn-primary" onClick={() => ouvrirEdition(etab)}
                                style={{ padding: "4px 10px", fontSize: 12 }}>Modifier</button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Etablissements;
