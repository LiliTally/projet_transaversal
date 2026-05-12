// ============================================================
//  PROJET  : Smart Santé 2035
//  FICHIER : src/api/axiosConfig.js
//  RÔLE    : Configuration d'Axios pour appeler l'API Flask.
//            Toutes les requêtes HTTP passent par ici.
//  NIVEAU  : Licence 2 Informatique – GPI
// ============================================================

import axios from "axios";

// URL de base de l'API Flask (back-end Python)
// En développement : http://localhost:5000
// En production : l'URL du serveur déployé
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

// Créer une instance Axios avec la configuration de base
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 secondes maximum d'attente
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// ── Intercepteur de requêtes ──────────────────────────────────
// Ajoute automatiquement le token JWT à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => Promise.reject(error)
);

// ── Intercepteur de réponses ──────────────────────────────────
// Gère les erreurs globalement (ex: token expiré → redirection login)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
