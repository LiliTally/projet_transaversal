-- ============================================================
--  PROJET  : Smart Santé 2035
--  FICHIER : database/data_init.sql
--  RÔLE    : Données initiales pour la base de données.
--            Insère les établissements de santé et les routes.
--  USAGE   : psql -U postgres -d smartsante_db -f data_init.sql
--  NIVEAU  : Licence 2 Informatique – GPI
-- ============================================================

-- ── Établissements de santé ───────────────────────────────────
INSERT INTO etablissements
    (id_etab, nom, niveau_soins, latitude, longitude, capacite_totale, lits_disponibles)
VALUES
    ('CSB-01',   'CSB Manakambahiny',            2, -18.9100, 47.5300, 20,  15),
    ('CSB-02',   'CSB Anosibe',                  2, -18.9300, 47.5400, 18,  10),
    ('HOP-DIS',  'Hôpital de District Anta.',    3, -18.9200, 47.5100, 80,  12),
    ('HOP-REF',  'Hôpital Référence Analakely',  4, -18.9000, 47.5200, 200, 35),
    ('CHUR-ANT', 'CHUR Antananarivo',             5, -18.8900, 47.5000, 500, 60),
    ('HOP-SAT',  'Hôpital Saturé (exemple)',      3, -18.9100, 47.5500, 60,   0)
ON CONFLICT (id_etab) DO NOTHING;

-- ── Routes entre établissements (arcs du graphe) ─────────────
INSERT INTO arcs_hospitaliers
    (id_source, id_destination, distance_km, temps_min, etat_route, ambulance_dispo)
VALUES
    ('CSB-01',  'HOP-DIS',   8.5,  25, 'goudron', TRUE),
    ('CSB-01',  'HOP-SAT',   3.0,  10, 'goudron', FALSE),
    ('CSB-01',  'HOP-REF',  15.0,  40, 'piste',   FALSE),
    ('CSB-02',  'HOP-DIS',   6.0,  20, 'goudron', TRUE),
    ('HOP-DIS', 'HOP-REF',   7.0,  20, 'goudron', TRUE),
    ('HOP-DIS', 'CHUR-ANT', 12.0,  30, 'goudron', TRUE),
    ('HOP-REF', 'CHUR-ANT',  5.0,  15, 'goudron', TRUE),
    ('HOP-SAT', 'HOP-DIS',   6.0,  18, 'goudron', FALSE)
ON CONFLICT DO NOTHING;
