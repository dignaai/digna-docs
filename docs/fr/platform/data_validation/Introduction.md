---
title: Data Validation – contrôles basés sur des règles pour conformité et auditabilité | Documentation digna
description: Découvrez comment digna Data Validation applique des contrôles déterministes basés sur des règles avec seuils, plages et listes de référence. Assurez la conformité, l'auditabilité et le reporting réglementaire dans la finance, la santé et d'autres secteurs sensibles aux données.
image: /assets/logo_square.png
keywords:
  - validation des données
  - contrôles de données basés sur des règles
  - qualité des données
  - qualité des données
  - observabilité des données
  - seuils et plages
  - validation par listes de référence
  - auditabilité
  - surveillance de la conformité
  - digna data validation
lang: fr
robots: index, follow
og_title: Data Validation – contrôles basés sur des règles pour conformité et auditabilité | Documentation digna
og_description: digna Data Validation applique des contrôles déterministes basés sur des règles avec seuils, plages et listes de référence. Conçu pour les secteurs régulés, il garantit conformité, transparence et auditabilité.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">Module Data Validation piloté par l'IA pour la qualité et l'observabilité des données – digna</h1>

---

## Objectif

Le **Data Validation** module garantit la **qualité des données** via des contrôles précis basés sur des règles.  
Il permet aux organisations de définir une logique de validation métier et technique déterministe, assurant que les données respectent les normes de conformité, les SLA contractuels et les exigences réglementaires.

En combinant l'*exécution des règles dans la base de données*, des *traces d'audit complètes* et l'*intégration avec les autres modules digna*, le **Data Validation** garantit une **qualité des données et une observabilité** cohérentes et traçables dans des environnements d'entreprise complexes.

---

## Aperçu technique

### Types de validation pris en charge

- **Vérifications d'égalité**  
  Confirmer que les valeurs correspondent aux résultats attendus (par ex. codes de référence, indicateurs booléens, correspondances catégorielles).

- **Seuils & Plages**  
  Valider des mesures numériques ou des KPI par rapport à des limites définies — statiques ou dérivées dynamiquement.

- **Listes de référence & lookups**  
  Vérifier si les valeurs de champ existent dans des jeux de données maîtres approuvés (par ex. codes TVA, listes ISO de pays, catalogues produits).

- **Cohérence entre colonnes**  
  Garantir la correction relationnelle (par ex. la devise correspond à la région, la catégorie de risque correspond au type d'actif).

- **Règles de gestion des valeurs nulles**  
  Détecter des valeurs nulles ou vides inattendues dans des colonnes critiques.

### Exécution et journalisation

- **Traitement en base de données** – Toutes les règles de validation s'exécutent directement dans votre base de données (Teradata, Snowflake, Databricks, PostgreSQL, etc.).  
- **Aucune extraction de données** – digna ne transfère jamais les données brutes en dehors de votre environnement.  
- **Traçabilité complète** – Chaque résultat de règle est journalisé avec horodatage, jeu de données responsable, nombre d'enregistrements et statut réussite/échec.  
- **Audit**