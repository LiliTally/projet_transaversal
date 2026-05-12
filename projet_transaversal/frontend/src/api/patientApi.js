// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/api/patientApi.js
//  RÔLE    : Fonctions d'appel à l'API Flask pour les patients.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import api from "./axiosConfig";

// ── Admettre un patient ───────────────────────────────────────
export const admettrePatient = async (donnees) => {
  // POST /patients/admission
  const response = await api.post("/patients/admission", donnees);
  return response.data;
};

// ── Obtenir un patient par son ID ─────────────────────────────
export const obtenirPatient = async (idPatient) => {
  // GET /patients/:id
  const response = await api.get(`/patients/${idPatient}`);
  return response.data;
};

// ── Consulter le prochain patient (O(1) - racine du tas) ──────
export const consulterProchain = async () => {
  // GET /triage/prochain
  const response = await api.get("/triage/prochain");
  return response.data;
};

// ── Traiter le prochain patient (O(log n) - extraire max) ─────
export const traiterProchain = async () => {
  // POST /triage/traiter
  const response = await api.post("/triage/traiter");
  return response.data;
};

// ── Calculer l'orientation Dijkstra ───────────────────────────
export const calculerOrientation = async (idPatient, idSource) => {
  // GET /orientation/:idPatient/:idSource
  const response = await api.get(`/orientation/${idPatient}/${idSource}`);
  return response.data;
};

// ── Mettre à jour les lits d'un établissement ─────────────────
export const mettreAJourLits = async (idEtab, litsDisponibles) => {
  // PUT /etablissements/:id/lits
  const response = await api.put(`/etablissements/${idEtab}/lits`, {
    lits_disponibles: litsDisponibles,
  });
  return response.data;
};

// ── Lancer la démonstration complète ─────────────────────────
export const lancerDemo = async () => {
  // GET /demo
  const response = await api.get("/demo");
  return response.data;
};
