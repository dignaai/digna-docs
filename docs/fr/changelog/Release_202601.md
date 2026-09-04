---
title: digna Release 2026.01 | Sources de données logiques, connexions globales et Data Validation avancée
description: Découvrez les nouveautés de digna Release 2026.01. Cette version introduit des connexions globales de base de données, des sources de données logiques, des conditions de pertinence d'anomalie, des exportations CSV et une Data Validation avancée incluant des vérifications d'intégrité référentielle.
keywords: digna Release 2026.01, digna journal des modifications, digna datasource, connexions de base de données digna, digna Data Anomalies, digna Data Validation, validation d'intégrité référentielle, règles de qualité des données, observabilité des données, export CSV digna
image: /assets/logo_square.png
---

# Journal des modifications – Release 2026.01  

Avec la Release 2026.01, digna introduit des améliorations majeures pour la modélisation des sources de données, la gestion des connexions et l'ergonomie des inspections.  
Cette version renforce la flexibilité dans tous les modules et étend significativement la couverture en matière de **qualité et de validation des données**.

---

## Nouvelles fonctionnalités  

### Connexions globales de base de données  
- Les connexions aux bases de données sont désormais configurées au **niveau global**.  
- Les connexions globales peuvent être réutilisées dans **tous les projets**, simplifiant la configuration et la maintenance.  
- **Impact:** Réduit la charge opérationnelle et garantit une connectivité cohérente entre les environnements.

### Plusieurs connexions source par projet  
- Les projets peuvent désormais référencer **plusieurs configurations de connexion source**.  
- Permet des configurations plus flexibles pour des paysages de données projet complexes.  
- **Impact:** Prend en charge des architectures d'entreprise réalistes avec des sources de données hétérogènes.

### Sources de données logiques  
- Les sources de données représentent désormais une **couche logique** au sein d'un projet.  
- Chaque source de données peut être basée sur :
    - une **table de base de données**
    - une **vue de base de données**
    - une **requête SQL personnalisée**  
- Cette séparation améliore la réutilisation, la clarté et la modélisation des inspections à travers les modules.  
- **Impact:** Découple les inspections et les règles de qualité des données du stockage physique, améliorant la maintenabilité et la réutilisation.

### Condition de pertinence des anomalies  
- Une **Condition de pertinence des anomalies** peut désormais être définie pour contrôler l'évaluation du statut d'anomalie au niveau du jeu de données.  
- Les statistiques sont calculées indépendamment du fait que la condition soit définie ou remplie.  
- Si la condition **n'est pas remplie**, **digna Data Anomalies** ne fournit pas de statut d'anomalie (vert / jaune / rouge).  
- **Exemple :** Exclure le jeu de données de l'évaluation des anomalies lorsque le nombre d'enregistrements est inférieur à 10.  
- **Impact:** Garantit que les anomalies sont évaluées uniquement dans des contextes métier pertinents.

### Configuration des notifications par module  
- Les notifications peuvent désormais être configurées **par module** directement dans digna.  
- Permet un contrôle indépendant du comportement d'alerte pour **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation**, et d'autres modules.  
- **Impact:** Permet des stratégies d'alerte précises alignées sur les responsabilités des équipes et la criticité.

### Export des résultats d'inspection (CSV)  
- Les utilisateurs peuvent désormais **télécharger les résultats d'inspection au format CSV**.  
- Permet l'analyse hors ligne, le reporting et l'intégration avec des outils externes.  
- **Impact:** Simplifie les audits, le reporting et l'analyse qualité des données en aval.

---

## Capacités étendues de validation des données  

Avec cette version, **digna Data Validation** prend désormais en charge un ensemble complet de règles de qualité des données :

- **Règles de validation au niveau des lignes**  
- **Vérifications d'unicité multi-colonnes**  
- **Validation de l'intégrité référentielle entre sources de données**

Ensemble, ces contrôles permettent d'appliquer des **règles de qualité structurelles et relationnelles** sur des paysages de données complexes.

### Vérifications d'unicité pour plusieurs colonnes
- Introduction des **vérifications d'unicité** pour un **ensemble configurable de colonnes**.  
- Permet la validation de clés composées et de contraintes d'unicité au niveau métier.  
- **Impact:** Détecte des entités métier en double qui ne peuvent pas être identifiées par des contrôles sur une seule colonne.

### Vérifications d'intégrité référentielle
- Introduction des **vérifications d'intégrité référentielle** pour valider les relations entre sources de données.  
- Garantit que les **valeurs de clés étrangères** dans une source de données existent dans une source de données cible référencée.  
- Aide à détecter tôt les enregistrements orphelins, les relations cassées et les problèmes de cohérence des données.  
- Conçu pour fonctionner avec des **sources de données logiques**, y compris les vues et les requêtes SQL personnalisées.  
- **Cas d'utilisation :** intégrité des entrepôts de données, reporting réglementaire, cohérence des données de référence et analytique en aval fiable.

---

## Bénéficiaires de cette version  

- **Ingénieurs de données :** Modélisation des sources de données plus flexible et connexions de base de données réutilisables  
- **Équipes Qualité des données & Gouvernance :** Couverture de validation étendue incluant les règles d'intégrité relationnelle  
- **Équipes Analytics & BI :** Entrées plus propres et résultats d'inspection exportables  
- **Responsables de la plateforme :** Complexité de configuration réduite et maintenabilité opérationnelle améliorée

---

## Mises à jour CLI  
- Aucune modification

---