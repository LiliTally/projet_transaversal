// ============================================================
//  FICHIER : src/pages/FileTriage.jsx
//  RÔLE    : Affiche la file de triage (tas binaire) en temps réel.
//            Permet d'extraire le prochain patient à traiter.
// ============================================================

import React, { useState, useEffect } from "react";
import { consulterProchain, traiterProchain } from "../api/patientApi";
import BadgePriorite from "../components/BadgePriorite";

function FileTriage() {
  const [prochain, setProchain]       = useState(null);
  const [message, setMessage]         = useState(null);
  const [chargement, setChargement]   = useState(false);

  useEffect(() => { charger(); }, []);

  const charger = async () => {
    try {
      const data = await consulterProchain();
      setProchain(data);
    } catch (err) {
      setProchain(null);
    }
  };

  const traiter = async () => {
    setChargement(true);
    try {
      // Appel API Flask : POST /triage/traiter → O(log n)
      const data = await traiterProchain();
      setMessage({
        type: "succes",
        texte: `✅ Patient traité : ${data.prenom} ${data.nom} | ${data.patients_restants} restants | ${data.complexite}`,
      });
      charger();
    } catch (err) {
      setMessage({ type: "erreur", texte: "Erreur lors du traitement." });
    } finally {
      setChargement(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ color: "#1A5276", fontSize: 22, marginBottom: 4 }}>
          🚨 File de Triage
        </h1>
        <p style={{ color: "#555", fontSize: 13 }}>
          Gestion de la file de priorité par tas binaire (Binary Max-Heap).
          Le patient le plus grave est toujours traité en premier.
        </p>
      </div>

      {/* Explication algorithmique */}
      <div className="card" style={{ borderLeft: "4px solid #1A5276", marginBottom: 16 }}>
        <p style={{ fontSize: 13, color: "#555" }}>
          <strong>Algorithme :</strong> Tas binaire (Binary Max-Heap)<br/>
          🔹 Insertion : <code>O(log n)</code> — sift-up<br/>
          🔹 Extraction du plus urgent : <code>O(log n)</code> — sift-down<br/>
          🔹 Consultation du plus urgent : <code>O(1)</code> — racine du tas<br/>
          🔹 Avantage vs FIFO : garantit que l'urgence médicale passe toujours en premier
        </p>
      </div>

      {message && (
        <div className={`alerte alerte-${message.type === "succes" ? "succes" : "critique"}`}
             style={{ marginBottom: 16 }}>
          {message.texte}
        </div>
      )}

      {/* Prochain patient */}
      <div className="card">
        <div className="card-header">
          <h3>👁 Prochain patient à traiter — O(1)</h3>
          <button className="btn btn-secondary" onClick={charger}>🔄 Actualiser</button>
        </div>

        {prochain && prochain.statut === "succes" ? (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <h4 style={{ color: "#1A5276" }}>
                  {prochain.prenom} {prochain.nom}
                </h4>
                <p style={{ fontSize: 13, color: "#555", marginTop: 4 }}>
                  Score : <strong>{prochain.score_triage}</strong> |
                  ID : <code>{prochain.id_patient}</code>
                </p>
                <p style={{ fontSize: 11, color: "#888", marginTop: 4 }}>
                  {prochain.complexite}
                </p>
              </div>
              <BadgePriorite niveau={prochain.niveau_priorite} couleur={prochain.couleur} />
            </div>
            <div style={{ marginTop: 16 }}>
              <button className="btn btn-danger" onClick={traiter} disabled={chargement}>
                {chargement ? "⏳..." : "🏥 Traiter ce patient — O(log n)"}
              </button>
            </div>
          </div>
        ) : (
          <div className="alerte alerte-info">
            ✅ File de triage vide — aucun patient en attente.
          </div>
        )}
      </div>

      {/* Légende niveaux */}
      <div className="card">
        <div className="card-header"><h3>📋 Niveaux de priorité médicale</h3></div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {[
            { niveau: 1, couleur: "ROUGE",  desc: "Critique – Traiter immédiatement (0 min)" },
            { niveau: 2, couleur: "ORANGE", desc: "Très urgent – Traiter dans 15 min" },
            { niveau: 3, couleur: "JAUNE",  desc: "Urgent – Traiter dans 30 min" },
            { niveau: 4, couleur: "VERT",   desc: "Non urgent – Traiter dans 1h" },
            { niveau: 5, couleur: "BLEU",   desc: "Peut attendre – 2 heures" },
          ].map(item => (
            <div key={item.niveau} style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <BadgePriorite niveau={item.niveau} couleur={item.couleur} />
              <span style={{ fontSize: 13, color: "#555" }}>{item.desc}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default FileTriage;
