// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/pages/Dashboard.jsx
//  RÔLE    : Tableau de bord principal – vue en temps réel
//            des statistiques du système de triage.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import React, { useState, useEffect } from "react";
import { consulterProchain, lancerDemo } from "../api/patientApi";
import BadgePriorite from "../components/BadgePriorite";

function Dashboard() {
  // ── État du composant ──────────────────────────────────────
  const [prochain, setProchain]     = useState(null);
  const [stats, setStats]           = useState(null);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur]         = useState(null);
  const [demo, setDemo]             = useState(null);

  // ── Chargement initial des données ────────────────────────
  useEffect(() => {
    chargerDonnees();
    // Rafraîchir toutes les 30 secondes
    const intervalle = setInterval(chargerDonnees, 30000);
    return () => clearInterval(intervalle);
  }, []);

  const chargerDonnees = async () => {
    try {
      setChargement(true);
      // Appel API Flask : GET /triage/prochain
      const data = await consulterProchain();
      setProchain(data);
      setErreur(null);
    } catch (err) {
      setErreur("Impossible de contacter le serveur Flask.");
    } finally {
      setChargement(false);
    }
  };

  const lancerDemonstration = async () => {
    try {
      const data = await lancerDemo();
      setDemo(data);
    } catch (err) {
      setErreur("Erreur lors de la démonstration.");
    }
  };

  // ── Rendu ──────────────────────────────────────────────────
  return (
    <div>
      {/* En-tête */}
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ color: "#1A5276", fontSize: 22, marginBottom: 4 }}>
          📊 Tableau de bord – Smart Santé 2035
        </h1>
        <p style={{ color: "#555", fontSize: 13 }}>
          Système Intelligent de Triage et d'Orientation Hospitalière – Madagascar
        </p>
      </div>

      {/* Alerte si erreur */}
      {erreur && (
        <div className="alerte alerte-critique">
          ⚠ {erreur} — Vérifiez que le serveur Flask tourne sur le port 5000.
        </div>
      )}

      {/* Statistiques rapides */}
      <div className="stats-grid">
        <div className="stat-card rouge">
          <div className="stat-number" style={{ color: "#C0392B" }}>
            {prochain?.niveau_priorite === 1 ? "1" : "0"}
          </div>
          <div className="stat-label">🔴 Patients critiques</div>
        </div>

        <div className="stat-card orange">
          <div className="stat-number" style={{ color: "#E67E22" }}>
            {prochain?.patients_en_attente || 0}
          </div>
          <div className="stat-label">File d'attente totale</div>
        </div>

        <div className="stat-card vert">
          <div className="stat-number" style={{ color: "#27AE60" }}>5</div>
          <div className="stat-label">Établissements actifs</div>
        </div>

        <div className="stat-card">
          <div className="stat-number">O(1)</div>
          <div className="stat-label">Accès prochain patient</div>
        </div>
      </div>

      {/* Prochain patient à traiter */}
      <div className="card">
        <div className="card-header">
          <h3>🚨 Prochain patient à traiter</h3>
          <button className="btn btn-secondary" onClick={chargerDonnees}>
            🔄 Actualiser
          </button>
        </div>

        {chargement ? (
          <div className="loading">Chargement en cours...</div>
        ) : prochain && prochain.statut === "succes" ? (
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            <div style={{ flex: 1 }}>
              <h4 style={{ color: "#1A5276", marginBottom: 6 }}>
                {prochain.prenom} {prochain.nom}
              </h4>
              <p style={{ fontSize: 13, color: "#555" }}>
                Score de triage : <strong>{prochain.score_triage}</strong>
              </p>
              <p style={{ fontSize: 12, color: "#888", marginTop: 4 }}>
                {prochain.complexite}
              </p>
            </div>
            <BadgePriorite
              niveau={prochain.niveau_priorite}
              couleur={prochain.couleur}
            />
          </div>
        ) : (
          <div className="alerte alerte-info">
            ✅ Aucun patient en attente pour le moment.
          </div>
        )}
      </div>

      {/* Section Démonstration */}
      <div className="card">
        <div className="card-header">
          <h3>⚙ Démonstration algorithmique</h3>
          <button className="btn btn-primary" onClick={lancerDemonstration}>
            ▶ Lancer la démo
          </button>
        </div>

        {demo ? (
          <div>
            {demo.resultats?.map((r, i) => (
              <div key={i} style={{ marginBottom: 12, padding: 12, background: "#f8f9fa", borderRadius: 6 }}>
                <p style={{ fontWeight: "bold", color: "#1A5276", marginBottom: 4 }}>
                  {r.algorithme}
                </p>
                <p style={{ fontSize: 12, color: "#555" }}>
                  Complexité : <code>{r.complexite}</code>
                </p>
                {r.avantage && (
                  <p style={{ fontSize: 12, color: "#27AE60", marginTop: 4 }}>
                    ✅ {r.avantage}
                  </p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p style={{ fontSize: 13, color: "#888" }}>
            Cliquez sur "Lancer la démo" pour tester les 3 algorithmes :
            tas binaire, Dijkstra et table de hachage.
          </p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
