// ============================================================
//  FICHIER : src/pages/Rapports.jsx
//  RÔLE    : Page des rapports statistiques et analytiques.
//            Affiche les indicateurs de performance du système.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import React, { useState } from "react";
import { lancerDemo } from "../api/patientApi";

function Rapports() {
  const [demo, setDemo]           = useState(null);
  const [chargement, setChargement] = useState(false);

  const chargerStats = async () => {
    setChargement(true);
    try {
      const data = await lancerDemo();
      setDemo(data);
    } catch (err) {
      console.error("Erreur chargement stats", err);
    } finally {
      setChargement(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ color: "#1A5276", fontSize: 22, marginBottom: 4 }}>
          📈 Rapports et statistiques
        </h1>
        <p style={{ color: "#555", fontSize: 13 }}>
          Indicateurs de performance du système de triage et d'orientation.
        </p>
      </div>

      {/* Complexités algorithmiques */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-header">
          <h3>⚙ Analyse de complexité algorithmique</h3>
        </div>
        <table>
          <thead>
            <tr>
              <th>Opération</th>
              <th>Structure</th>
              <th>Complexité</th>
              <th>Contexte Madagascar</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Insertion patient dans la file</td>
              <td>Tas binaire</td>
              <td><code>O(log n)</code></td>
              <td>n=500 → 9 comparaisons max</td>
            </tr>
            <tr>
              <td>Extraction patient le plus urgent</td>
              <td>Tas binaire</td>
              <td><code>O(log n)</code></td>
              <td>n=500 → 9 opérations max</td>
            </tr>
            <tr>
              <td>Consulter le plus urgent</td>
              <td>Tas binaire</td>
              <td><code>O(1)</code></td>
              <td>Accès direct à la racine</td>
            </tr>
            <tr>
              <td>Orientation hospitalière</td>
              <td>Graphe + Dijkstra</td>
              <td><code>O((V+E) log V)</code></td>
              <td>V=3000, E=15000 → 207 000 ops</td>
            </tr>
            <tr>
              <td>Recherche dossier patient</td>
              <td>Table de hachage</td>
              <td><code>O(1)</code> moy.</td>
              <td>Accès instantané par ID</td>
            </tr>
            <tr>
              <td>Construction initiale du tas</td>
              <td>Floyd (tas binaire)</td>
              <td><code>O(n)</code></td>
              <td>Plus rapide que n insertions</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Comparaison FIFO vs HEAP */}
      <div className="card" style={{ marginBottom: 16 }}>
        <div className="card-header">
          <h3>🆚 Comparaison FIFO vs Tas Binaire</h3>
        </div>
        <table>
          <thead>
            <tr>
              <th>Critère</th>
              <th>File FIFO</th>
              <th>Tas Binaire ✅</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Insertion</td>
              <td><code>O(1)</code></td>
              <td><code>O(log n)</code></td>
            </tr>
            <tr>
              <td>Extraction du plus urgent</td>
              <td><code>O(n)</code> — parcours total</td>
              <td><code>O(log n)</code> ✅</td>
            </tr>
            <tr>
              <td>Consultation sans extraction</td>
              <td><code>O(n)</code></td>
              <td><code>O(1)</code> ✅</td>
            </tr>
            <tr>
              <td>Garantie médicale</td>
              <td style={{ color: "#C0392B" }}>❌ Aucune — ordre d'arrivée</td>
              <td style={{ color: "#27AE60" }}>✅ Toujours le plus grave en premier</td>
            </tr>
            <tr>
              <td>Risque d'erreur médicale</td>
              <td style={{ color: "#C0392B" }}>❌ Élevé — cas critiques peuvent attendre</td>
              <td style={{ color: "#27AE60" }}>✅ Minimisé</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Démonstration en direct */}
      <div className="card">
        <div className="card-header">
          <h3>▶ Rapport en temps réel</h3>
          <button className="btn btn-primary" onClick={chargerStats} disabled={chargement}>
            {chargement ? "⏳..." : "🔄 Générer"}
          </button>
        </div>

        {demo ? (
          <div>
            {demo.resultats?.map((r, i) => (
              <div key={i} style={{ padding: 14, background: "#f8f9fa", borderRadius: 6, marginBottom: 10 }}>
                <p style={{ fontWeight: "bold", color: "#1A5276", marginBottom: 6 }}>
                  {r.algorithme}
                </p>
                <p style={{ fontSize: 12, color: "#555" }}>
                  Complexité : <code>{r.complexite}</code>
                </p>
                {r.avantage && (
                  <p style={{ fontSize: 12, color: "#27AE60", marginTop: 4 }}>✅ {r.avantage}</p>
                )}
                {r.ordre_traitement && (
                  <div style={{ marginTop: 8 }}>
                    <p style={{ fontSize: 12, fontWeight: "bold", marginBottom: 4 }}>
                      Ordre de traitement (le plus grave en premier) :
                    </p>
                    {r.ordre_traitement.map((p, j) => (
                      <p key={j} style={{ fontSize: 12, color: "#333", marginLeft: 12 }}>
                        {j + 1}. {p.nom} — Score: {p.score} — {p.couleur}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p style={{ fontSize: 13, color: "#888" }}>
            Cliquez sur "Générer" pour afficher les statistiques en temps réel.
          </p>
        )}
      </div>
    </div>
  );
}

export default Rapports;
