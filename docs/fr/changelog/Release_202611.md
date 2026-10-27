---
title: digna Release 2026.11 | Data Reconciliation (Beta), digna Agentic (Beta) et digna Engine
description: Découvrez les nouveautés de la Release 2026.11 de digna. Cette version introduit trois ajouts majeurs - digna Data Reconciliation (Beta), digna Agentic (Beta) avec le digna MCP Server, et le digna Engine, qui permet des contrôles d'intégrité référentielle entre différentes technologies de bases de données.
keywords: digna Release 2026.11, changelog digna, digna Data Reconciliation, rapprochement des données, validation ETL, rapprochement source-cible, digna Agentic, digna MCP Server, agents IA qualité des données, digna Engine, intégrité référentielle entre connexions, attributs de requête, profilage des données, observabilité des données
image: /assets/logo_square.png
---

# Changelog – Release 2026.11  

La Release 2026.11 s'articule autour de trois ajouts majeurs :

- **digna Data Reconciliation (Beta)** : vérifie que les données restent cohérentes lorsqu'elles circulent entre les systèmes  
- **digna Agentic (Beta)** : ouvre digna aux agents IA via le digna MCP Server  
- **digna Engine** : profile, en option, les données au sein de digna et permet des contrôles d'intégrité référentielle entre différentes technologies de bases de données  

---

## Nouvelles fonctionnalités  

### digna Data Reconciliation (Beta) – Cohérence de la source à la cible  
Les données transitent souvent par plusieurs systèmes avant d'arriver dans un rapport. digna Data Reconciliation (Beta) compare une source de données **cible** avec les **sources** à partir desquelles elle a été construite, et alerte lorsqu'elles ne concordent plus.

- Configurée sous forme de règles nommées dans le nouvel onglet **Data Reconciliation** de la source de données cible  
- Toute source de données du projet pour laquelle Data Reconciliation est activé peut servir de source  
- Les cas d'usage incluent les procédures de rapprochement standard et la validation des résultats des processus ETL  
- Deux types de règles : **Exact** et **AI**  

**Règles Exact – Le rapprochement comme règle de qualité des données** : vous définissez précisément ce qui doit correspondre entre une source et une cible, comme pour une règle de qualité des données.

  - Comparer une source de données d'origine avec une source de données cible  
  - Associer un contrôle cible à un contrôle source par statistique et par attribut, par ex. le nombre de lignes ou la somme d'une colonne de montants  
  - Autoriser un écart avec une tolérance **Absolute** (par ex. ± 10) ou **Relative** (par ex. ± 0,5 % de la source)  
  - La chronologie affiche l'écart de chaque jour par rapport à la tolérance  

**Règles AI – Le rapprochement comme observabilité des données** : digna apprend comment une cible suit ses sources, de la même manière que digna observe les données dans les autres modules, et alerte lorsque cette relation se rompt.

  - Combiner les contrôles de plusieurs sources de données d'origine avec les contrôles d'une cible  
  - Inutile de connaître ou de formaliser la logique qui les relie (jointures, filtres, agrégations)  
  - Un modèle apprend à partir de l'historique comment la cible suit ses sources le même jour  
  - Chaque contrôle cible est prédit à partir des valeurs sources du jour, et digna alerte lorsque la cible sort de la bande formée par les erreurs passées propres à la règle  
  - Chaque règle dispose de ses propres **Model settings** : **Sensitivity**, **Memory** et **Model Complexity**  

Les contrôles de rapprochement apparaissent sur le Dashboard avec une chronologie par règle. Ils comptent dans le statut global de l'inspection et déclenchent des notifications.

**Impact :** Couvre les deux facettes du rapprochement. Les règles Exact imposent des contrôles connus entre source et cible, et les règles AI surveillent des flux complexes comme les processus ETL : les données perdues ou modifiées en cours de route sont ainsi détectées sans SQL de rapprochement écrit à la main.

---

### digna Agentic (Beta) – digna pour les agents IA  
Première version de digna Agentic (Beta). Les agents IA peuvent désormais travailler avec digna, répondre à des questions métier sur vos données et vous aider à améliorer votre configuration.

**digna MCP Server** : permet à Claude et à d'autres agents IA de travailler avec digna via le Model Context Protocol.

  - Gérer les projets, les sources de données, les règles, les plannings d'inspection et les abonnements  
  - Lire les statuts d'inspection jusqu'au contrôle individuel, pour analyser les alertes  

**Descriptions des sources de données et des attributs** : décrivez en langage courant ce que contient une source de données ou un attribut.

  - Les agents IA utilisent ces descriptions pour interpréter vos données  
  - Posez des questions métier sur vos données : les agents IA y répondent à partir de ce que digna surveille  
  - Si la configuration actuelle de digna ne permet pas de répondre à une question, l'agent IA propose, si possible, des modifications de la source de données et de ses attributs, par ex. l'ajout d'un nouveau dataset  

**Impact :** Permet de poser des questions métier sur vos données en langage courant, et permet aux agents IA d'aider à configurer digna et à analyser les problèmes de qualité des données.

---

### digna Engine – Profilez là où vous le souhaitez  
Par défaut, digna profile les données là où elles se trouvent, dans la base de données source. Le digna Engine ajoute une option : digna exporte les données depuis la source et les profile au sein du digna Engine.

- Facultatif, non obligatoire : le profilage dans la base de données source reste disponible  
- Choisi pour chaque connexion de base de données comme emplacement de profilage (**Profiling Location**) : **Source Database** ou **digna Engine**  
- Disponible pour toutes les technologies source prises en charge  

**Intégrité référentielle entre connexions** : certains contrôles nécessitent l'export des données. Le digna Engine étend **digna Data Validation** à ces cas.

  - **Contrôles d'intégrité référentielle** entre sources de données situées sur des **connexions de base de données différentes**, y compris avec des technologies de bases de données différentes (par ex. Oracle et PostgreSQL)  
  - Fonctionne avec les deux emplacements de profilage : avec Source Database, seules les colonnes clés sont exportées vers le digna Engine  
  - Le tableau de bord indique lorsqu'un contrôle s'exécute sur deux connexions  

**Impact :** Permet de choisir où les données sont profilées, et d'imposer des relations entre des systèmes reposant sur des technologies de bases de données différentes.

---

## Améliorations du profilage  

Cette version donne également aux utilisateurs davantage de contrôle sur ce qui est profilé et sur la manière de le faire.

### Attributs de requête – Colonnes définies par l'utilisateur  
- Définir des colonnes artificielles : une expression SQL portant sur une ou plusieurs colonnes de la source de données  
- Chaque attribut de requête possède son propre nom  
- Profilé et contrôlé comme n'importe quel autre attribut  

### Catégorie de colonne DATE  
- Nouvelle catégorie **Date** pour les attributs  
- Métriques relatives à la date inspectée  

### Profilage à la demande  
- Profiler n'importe quel attribut sur l'instantané complet d'une date, sans lancer d'inspection  
- Aide à définir le type de colonne de l'attribut : **Numerical**, **Categorical**, **Date** ou **Unspecified**  

---

## Qui bénéficie de cette version  

- **Data Engineers :** validation des résultats ETL avec digna Data Reconciliation (Beta)  
- **Équipes Finance, Risques et Contrôle de gestion :** procédures de rapprochement standard sous forme de règles Exact dans digna Data Reconciliation (Beta)  
- **Équipes Qualité des données et Gouvernance :** intégrité référentielle entre technologies de bases de données avec le digna Engine  
- **Utilisateurs métier :** réponses des agents IA aux questions métier sur les données avec digna Agentic (Beta)  
- **Équipes IA et Automatisation :** agents IA travaillant avec digna via digna Agentic (Beta)  

---

## Mises à jour de la CLI  
- Aucun changement  
