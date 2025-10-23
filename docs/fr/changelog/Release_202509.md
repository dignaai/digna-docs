---
title: digna Version 2025.09 | Architecture modulaire, cinq nouveaux modules, MFA via OIDC
description: Découvrez les nouveautés de digna Version 2025.09. Cette version introduit une architecture modulaire, cinq nouveaux modules, MFA via OIDC, et des notifications par module.
keywords: digna Version 2025.09, digna journal des modifications, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna conception modulaire, digna OIDC MFA
image: /assets/logo_square.png
---

# Journal des modifications – Version 2025.09  

Avec la Version 2025.09, digna introduit une nouvelle **architecture modulaire** et lance **cinq modules spécialisés** pour la qualité et l'observabilité des données.  
Cette version renforce également l'authentification et améliore la gestion des notifications sur toute la plateforme.  

---

## 🚀 Nouvelles fonctionnalités  

### Architecture modulaire  
- digna adopte désormais une **architecture modulaire**.  
- Les clients peuvent activer uniquement les modules dont ils ont besoin et en ajouter d'autres au fur et à mesure de l'évolution de leurs besoins.  
- Les fonctionnalités précédentes font désormais partie de **digna Data Anomalies**.  

### Nouveaux modules  
- **digna Data Anomalies** – Détection pilotée par IA des anomalies dans les volumes de données, les distributions et les valeurs manquantes.  
- **digna Data Analytics** – Évaluation en séries temporelles des métriques d'observabilité pour détecter les tendances à long terme et la volatilité.  
- **digna Data Timeliness** – Surveillance des délais d'arrivée attendus des données, basée à la fois sur l'IA et sur des règles.  
- **digna Data Validation** – Vérifications basées sur des règles au niveau des enregistrements pour garantir la conformité aux règles métier.  
- **digna Data Schema Tracker** – Détection des changements de schéma (modifications DDL) dans les bases de données surveillées.  

### MFA via OIDC  
- Prise en charge de l'**authentification multifacteur (MFA)** avec OIDC Single Sign-On.  
- Offre une sécurité de niveau entreprise pour toutes les connexions utilisateur.  

### Notifications par module  
- Les notifications sont désormais envoyées **par module**, ce qui facilite la séparation des alertes provenant de Data Anomalies, Data Analytics et des autres modules.  

---

## 🛠 Mises à jour de la CLI  

- **Nouvelle commande : `inspect-cancel`** – Annule les inspections par ID de requête ou termine toutes les requêtes actives.  
- **Nouvelle commande : `check-config`** – Valide les fichiers de configuration avant le démarrage.  
- **Nouvelle commande : `remove-orphans`** – Nettoie les entrées de référentiel orphelines.  
- **Commande `inspect` améliorée** – Nouvelle option `--bypass-backend` (`-bb`) et codes de retour standardisés (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Documentation  
- Nouveaux guides:  
  - Guide d'intégration Single Sign-On