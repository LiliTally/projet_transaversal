// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/pages/Admission.jsx
//  RÔLE    : Formulaire d'admission d'un nouveau patient.
//            Envoie les données à l'API Flask et affiche
//            le niveau de priorité calculé.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import React, { useState } from "react";
import { admettrePatient } from "../api/patientApi";
import BadgePriorite from "../components/BadgePriorite";

// Valeurs initiales du formulaire
const FORM_VIDE = {
  nom: "", prenom: "", age: "",
  fc: "", spo2: "", temperature: "", fr: "", tension: "120/80",
  score_symptomes: 50, score_antecedents: 30,
};

function Admission() {
  const [form, setForm]           = useState(FORM_VIDE);
  const [resultat, setResultat]   = useState(null);
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur]       = useState(null);

  // ── Gestion des champs du formulaire ──────────────────────
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ── Soumission du formulaire ───────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    setChargement(true);
    setErreur(null);
    setResultat(null);

    try {
      // Appel API Flask : POST /patients/admission
      const data = await admettrePatient({
        nom              : form.nom,
        prenom           : form.prenom,
        age              : parseInt(form.age),
        fc               : parseInt(form.fc),
        spo2             : parseFloat(form.spo2),
        temperature      : parseFloat(form.temperature),
        fr               : parseInt(form.fr),
        tension          : form.tension,
        score_symptomes  : parseInt(form.score_symptomes),
        score_antecedents: parseInt(form.score_antecedents),
      });

      setResultat(data);
      setForm(FORM_VIDE);   // Réinitialiser le formulaire

    } catch (err) {
      setErreur(err.response?.data?.erreur || "Erreur de connexion au serveur.");
    } finally {
      setChargement(false);
    }
  };

  // ── Rendu ──────────────────────────────────────────────────
  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ color: "#1A5276", fontSize: 22, marginBottom: 4 }}>
          ➕ Admettre un patient
        </h1>
        <p style={{ color: "#555", fontSize: 13 }}>
          Saisissez les données cliniques du patient.
          Le score de triage sera calculé automatiquement par le système MTI.
        </p>
      </div>

      {/* Résultat après soumission */}
      {resultat && (
        <div className="alerte alerte-succes" style={{ marginBottom: 16 }}>
          <div>
            <strong>✅ Patient admis avec succès !</strong>
            <p style={{ marginTop: 4 }}>
              ID : <code>{resultat.id_patient}</code> |
              Score : <strong>{resultat.score_triage}</strong> |{" "}
              <BadgePriorite niveau={resultat.niveau_priorite} couleur={resultat.couleur} />
            </p>
            {resultat.alerte_requise && (
              <p style={{ color: "#C0392B", fontWeight: "bold", marginTop: 4 }}>
                🚨 ALERTE CRITIQUE envoyée au médecin de garde !
              </p>
            )}
            <p style={{ fontSize: 12, marginTop: 4 }}>
              Patients en attente : {resultat.patients_en_attente}
            </p>
          </div>
        </div>
      )}

      {erreur && (
        <div className="alerte alerte-critique" style={{ marginBottom: 16 }}>
          ⚠ {erreur}
        </div>
      )}

      {/* Formulaire d'admission */}
      <div className="card">
        <div className="card-header">
          <h3>📋 Informations du patient</h3>
        </div>

        <form onSubmit={handleSubmit}>
          {/* Données démographiques */}
          <p style={{ fontWeight: "bold", color: "#1F618D", marginBottom: 10 }}>
            👤 Données démographiques
          </p>
          <div className="form-row">
            <div className="form-group">
              <label>Nom *</label>
              <input name="nom" value={form.nom} onChange={handleChange}
                     placeholder="Ex: Rakoto" required />
            </div>
            <div className="form-group">
              <label>Prénom *</label>
              <input name="prenom" value={form.prenom} onChange={handleChange}
                     placeholder="Ex: Jean" required />
            </div>
          </div>
          <div className="form-group" style={{ maxWidth: 200 }}>
            <label>Âge (années) *</label>
            <input name="age" type="number" value={form.age} onChange={handleChange}
                   placeholder="Ex: 45" min="0" max="130" required />
          </div>

          {/* Constantes vitales */}
          <p style={{ fontWeight: "bold", color: "#1F618D", margin: "16px 0 10px" }}>
            ❤ Constantes vitales
          </p>
          <div className="form-row">
            <div className="form-group">
              <label>Fréquence cardiaque (bpm) * <small style={{color:"#888"}}>(normal: 60-100)</small></label>
              <input name="fc" type="number" value={form.fc} onChange={handleChange}
                     placeholder="Ex: 85" min="0" max="300" required />
            </div>
            <div className="form-group">
              <label>Saturation O₂ (%) * <small style={{color:"#888"}}>(normal: 95-100)</small></label>
              <input name="spo2" type="number" step="0.1" value={form.spo2} onChange={handleChange}
                     placeholder="Ex: 97.5" min="0" max="100" required />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Température (°C) * <small style={{color:"#888"}}>(normal: 36.5-37.5)</small></label>
              <input name="temperature" type="number" step="0.1" value={form.temperature}
                     onChange={handleChange} placeholder="Ex: 37.2" required />
            </div>
            <div className="form-group">
              <label>Fréq. respiratoire (/min) * <small style={{color:"#888"}}>(normal: 12-20)</small></label>
              <input name="fr" type="number" value={form.fr} onChange={handleChange}
                     placeholder="Ex: 16" required />
            </div>
          </div>
          <div className="form-group" style={{ maxWidth: 200 }}>
            <label>Tension artérielle *</label>
            <input name="tension" value={form.tension} onChange={handleChange}
                   placeholder="Ex: 120/80" required />
          </div>

          {/* Scores complémentaires */}
          <p style={{ fontWeight: "bold", color: "#1F618D", margin: "16px 0 10px" }}>
            📝 Évaluation clinique
          </p>
          <div className="form-row">
            <div className="form-group">
              <label>Score symptômes (0-100) : {form.score_symptomes}</label>
              <input name="score_symptomes" type="range" min="0" max="100"
                     value={form.score_symptomes} onChange={handleChange} />
            </div>
            <div className="form-group">
              <label>Score antécédents (0-100) : {form.score_antecedents}</label>
              <input name="score_antecedents" type="range" min="0" max="100"
                     value={form.score_antecedents} onChange={handleChange} />
            </div>
          </div>

          {/* Boutons */}
          <div style={{ display: "flex", gap: 12, marginTop: 20 }}>
            <button type="submit" className="btn btn-primary" disabled={chargement}>
              {chargement ? "⏳ Calcul en cours..." : "✅ Admettre et calculer le triage"}
            </button>
            <button type="button" className="btn btn-secondary"
                    onClick={() => { setForm(FORM_VIDE); setResultat(null); }}>
              🔄 Réinitialiser
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Admission;
