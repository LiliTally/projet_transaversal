-- ============================================================
--  PROJET  : Smart Santé 2035
--  FICHIER : database/schema.sql
--  RÔLE    : Structure des tables PostgreSQL.
--            À exécuter une seule fois pour créer la base.
--  USAGE   : psql -U postgres -d smartsante_db -f schema.sql
--  NIVEAU  : Licence 2 Informatique – GPI
-- ============================================================

-- Créer la base de données si elle n'existe pas
-- (à exécuter séparément : CREATE DATABASE smartsante_db;)

-- ── Table des patients ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS patients (
    id_patient          VARCHAR(20)    PRIMARY KEY,
    nom                 VARCHAR(100)   NOT NULL,
    prenom              VARCHAR(100)   NOT NULL,
    age                 INTEGER        NOT NULL CHECK (age >= 0 AND age <= 130),
    score_triage        DECIMAL(5,2)   NOT NULL CHECK (score_triage >= 0 AND score_triage <= 100),
    niveau_priorite     INTEGER        NOT NULL CHECK (niveau_priorite BETWEEN 1 AND 5),
    couleur_priorite    VARCHAR(10)    NOT NULL,
    timestamp_admission BIGINT         NOT NULL,
    statut              VARCHAR(20)    DEFAULT 'EN_ATTENTE',
    created_at          TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

-- ── Table des constantes vitales ─────────────────────────────
CREATE TABLE IF NOT EXISTS constantes_vitales (
    id_constantes           VARCHAR(20)  PRIMARY KEY,
    patient_id              VARCHAR(20)  REFERENCES patients(id_patient) ON DELETE CASCADE,
    frequence_cardiaque     INTEGER      NOT NULL,
    saturation_o2           DECIMAL(5,2) NOT NULL,
    temperature             DECIMAL(4,1) NOT NULL,
    frequence_respiratoire  INTEGER      NOT NULL,
    tension_arterielle      VARCHAR(10)  NOT NULL,
    score_vital_calcule     DECIMAL(5,2),
    timestamp_mesure        BIGINT       NOT NULL
);

-- ── Table des établissements de santé ─────────────────────────
CREATE TABLE IF NOT EXISTS etablissements (
    id_etab           VARCHAR(20)   PRIMARY KEY,
    nom               VARCHAR(200)  NOT NULL,
    niveau_soins      INTEGER       NOT NULL CHECK (niveau_soins BETWEEN 1 AND 5),
    latitude          DECIMAL(10,7) NOT NULL,
    longitude         DECIMAL(10,7) NOT NULL,
    capacite_totale   INTEGER       NOT NULL CHECK (capacite_totale >= 0),
    lits_disponibles  INTEGER       NOT NULL CHECK (lits_disponibles >= 0),
    est_operationnel  BOOLEAN       DEFAULT TRUE,
    updated_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ── Table des arcs (routes entre établissements) ──────────────
CREATE TABLE IF NOT EXISTS arcs_hospitaliers (
    id_arc          SERIAL        PRIMARY KEY,
    id_source       VARCHAR(20)   REFERENCES etablissements(id_etab),
    id_destination  VARCHAR(20)   REFERENCES etablissements(id_etab),
    distance_km     DECIMAL(8,2)  NOT NULL CHECK (distance_km > 0),
    temps_min       INTEGER       NOT NULL CHECK (temps_min > 0),
    etat_route      VARCHAR(20)   NOT NULL DEFAULT 'goudron',
    ambulance_dispo BOOLEAN       DEFAULT FALSE
);

-- ── Table des orientations ────────────────────────────────────
CREATE TABLE IF NOT EXISTS orientations (
    id_orientation    SERIAL        PRIMARY KEY,
    patient_id        VARCHAR(20)   REFERENCES patients(id_patient),
    etab_source_id    VARCHAR(20)   REFERENCES etablissements(id_etab),
    etab_cible_id     VARCHAR(20)   REFERENCES etablissements(id_etab),
    chemin_json       TEXT,
    distance_km       DECIMAL(8,2),
    temps_minutes     INTEGER,
    duree_calcul_ms   DECIMAL(8,2),
    created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ── Index pour accélérer les requêtes fréquentes ─────────────
CREATE INDEX IF NOT EXISTS idx_patients_niveau
    ON patients(niveau_priorite);

CREATE INDEX IF NOT EXISTS idx_patients_statut
    ON patients(statut);

CREATE INDEX IF NOT EXISTS idx_etablissements_niveau
    ON etablissements(niveau_soins);

CREATE INDEX IF NOT EXISTS idx_etablissements_lits
    ON etablissements(lits_disponibles);
