// ============================================================
//  FICHIER : src/pages/Orientation.jsx
//  RÔLE    : Page de calcul de l'orientation hospitalière.
//            Exécute l'algorithme de Dijkstra via l'API Flask.
// ============================================================

import React, { useState } from "react";
import { calculerOrientation } from "../api/patientApi";

function Orientation() {
  const [idPatient, setIdPatient] = useState("");
  const [idSource, setIdSource]   = useState("CSB-01");
  const [resultat, setResultat]   = useState(null);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur]       = useState(null);

  const lancer = async (e) => {
    e.preventDefault();
    setChargement(true);
    setErreur(null);
    setResultat(null);
    try {
      // Appel API Flask : GET /orientation/:idPatient/:idSource
      // → Exécute Dijkstra sur le graphe hospitalier
      const data = await calculerOrientation(idPatient, idSource);
      setResultat(data);
    } catch (err) {
      setErreur(err.response?.data?.erreur || "Erreur de connexion.");
    } finally {
      setChargement(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ color: "#1A5276", fontSize: 22, marginBottom: 4 }}>
          🗺 Orientation Hospitalière
        </h1>
        <p style={{ color: "#555", fontSize: 13 }}>
          Calcul du chemin optimal vers le meilleur établissement de santé
          via l'algorithme de Dijkstra — O((V+E) × log V).
        </p>
      </div>

      {/* Explication Dijkstra */}
      <div className="card" style={{ borderLeft: "4px solid #534AB7", marginBottom: 16 }}>
        <p style={{ fontSize: 13, color: "#555" }}>
          <strong>Algorithme de Dijkstra :</strong><br/>
          🔹 Le réseau hospitalier est modélisé comme un <strong>graphe orienté pondéré</strong><br/>
          🔹 Nœuds = établissements de santé | Arcs = routes avec distance/temps<br/>
          🔹 Le poids d'un arc intègre : temps de trajet × état route × disponibilité lits<br/>
          🔹 Pour Madagascar : V≈3000 établissements, E≈15000 routes → ≈207 000 opérations<br/>
          🔹 Complexité : <code>O((V+E) × log V)</code> — exécution en quelques millisecondes ✅
        </p>
      </div>

      {/* Formulaire */}
      <div className="card">
        <div className="card-header"><h3>🔍 Calculer une orientation</h3></div>
        <form onSubmit={lancer}>
          <div className="form-row">
            <div className="form-group">
              <label>ID du patient *</label>
              <input value={idPatient} onChange={e => setIdPatient(e.target.value)}
                     placeholder="Ex: PAT-001" required />
            </div>
            <div className="form-group">
              <label>Établissement de départ *</label>
              <select value={idSource} onChange={e => setIdSource(e.target.value)}>
                <option value="CSB-01">CSB Manakambahiny</option>
                <option value="HOP-DIS">Hôpital District Antananarivo</option>
                <option value="HOP-REF">Hôpital Référence Analakely</option>
                <option value="CHUR-ANT">CHUR Antananarivo</option>
              </select>
            </div>
          </div>
          <button type="submit" className="btn btn-primary" disabled={chargement}>
            {chargement ? "⏳ Dijkstra en cours..." : "🚀 Calculer le chemin optimal"}
          </button>
        </form>
      </div>

      {/* Erreur */}
      {erreur && (
        <div className="alerte alerte-critique">{erreur}</div>
      )}

      {/* Résultat Dijkstra */}
      {resultat && resultat.statut === "succes" && (
        <div className="card" style={{ borderLeft: "4px solid #27AE60" }}>
          <div className="card-header">
            <h3>✅ Résultat de Dijkstra</h3>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div>
              <p style={{ fontSize: 12, color: "#888" }}>Établissement cible</p>
              <p style={{ fontWeight: "bold", color: "#1A5276", fontSize: 16 }}>
                🏥 {resultat.etablissement_cible?.nom}
              </p>
            </div>
            <div>
              <p style={{ fontSize: 12, color: "#888" }}>Lits disponibles</p>
              <p style={{ fontWeight: "bold", color: "#27AE60", fontSize: 16 }}>
                {resultat.etablissement_cible?.lits_disponibles} lits libres
              </p>
            </div>
            <div>
              <p style={{ fontSize: 12, color: "#888" }}>Distance totale</p>
              <p style={{ fontWeight: "bold", fontSize: 16 }}>
                📍 {resultat.distance_km} km
              </p>
            </div>
            <div>
              <p style={{ fontSize: 12, color: "#888" }}>Temps estimé</p>
              <p style={{ fontWeight: "bold", fontSize: 16 }}>
                ⏱ {resultat.temps_minutes} minutes
              </p>
            </div>
          </div>

          {/* Chemin */}
          <div style={{ marginTop: 16, padding: 12, background: "#f8f9fa", borderRadius: 6 }}>
            <p style={{ fontSize: 12, color: "#888", marginBottom: 8 }}>Chemin optimal :</p>
            <p style={{ fontWeight: "bold", color: "#534AB7" }}>
              {Array.isArray(resultat.chemin)
                ? resultat.chemin.join(" → ")
                : resultat.chemin}
            </p>
          </div>

          {/* Métadonnées */}
          <div style={{ marginTop: 12, fontSize: 11, color: "#888" }}>
            Calculé en {resultat.duree_calcul_ms} ms |
            Complexité : {resultat.complexite}
          </div>
        </div>
      )}

      {resultat?.statut === "info" && (
        <div className="alerte alerte-succes">
          ✅ {resultat.message}
        </div>
      )}
    </div>
  );
}

export default Orientation;
