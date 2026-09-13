---
title: digna Release 2026.06 | SDK Python, déploiement Docker et gestion avancée des validations
description: Découvrez les nouveautés de la Release 2026.06 de digna. Cette version introduit le nouveau SDK Python digna, le support officiel Docker, une expérience de tableau de bord repensée et des capacités d'import/export étendues pour les règles de validation.
keywords: digna Release 2026.06, SDK Python digna, prise en charge Docker digna, automatisation de la qualité des données, profilage des données, import-export des règles de validation, tableau de bord digna, plateforme d'observabilité des données, API Python, automatisation des métadonnées
image: /assets/logo_square.png
---

# Changelog – Release 2026.06  

Avec la Release 2026.06, digna franchit une étape majeure en matière d'automatisation, d'extensibilité et d'ergonomie de la plateforme.  
Cette version introduit le nouveau **digna Python SDK**, le support officiel **Docker**, une expérience de tableau de bord rafraîchie et une portabilité améliorée pour la gestion des règles de validation.

---

## Voir la présentation de la version

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — une présentation de cette version sur la chaîne YouTube de digna.*

---

## Nouvelles fonctionnalités  

### digna Python SDK – Automatisez tout avec Python  
- Installation via :
  ```bash
  pip install digna-sdk
  ```
- Gérer et automatiser digna de manière programmatique avec Python  
- Créer et configurer des projets via du code  
- Déclencher des inspections et des exécutions de monitoring  
- Gérer datasets, rules et configurations par programmation  
- Profiler des tables et extraire des insights de métadonnées  
- Exporter les résultats de profilage et de qualité des données vers des référentiels et systèmes externes  
- Intégrer avec des notebooks, des outils d'orchestration et des pipelines CI/CD  

**Impact :** Permet une approche infrastructure-as-code complète et une automatisation avancée des workflows de qualité et d'observabilité des données via Python.

---

### Support Docker – Déploiement et exploitation simplifiés  
- Image Docker officielle pour digna  
- Installation rapide et cohérente entre environnements  
- Onboarding simplifié pour les environnements de développement, de test et de production  
- Intégration aisée avec Kubernetes et les plateformes de conteneurs  
- Portabilité et reproductibilité améliorées des déploiements  

**Impact :** Facilite le déploiement et l'exploitation de digna dans des architectures cloud-native modernes.

---

### QueryMode – Stratégie d'exécution SQL flexible

Configurez la stratégie d'exécution des requêtes : mode **Single** ou **Combined**

**Single Mode** : Chaque statistique est calculée par une requête SQL dédiée

  - Idéal pour les sources de données volumineuses où la mémoire est limitée  
  - Évite l'épuisement des ressources lors de requêtes combinées (out of memory, limites de spool)  
  - Nombre de requêtes plus élevé mais empreinte mémoire par requête réduite

**Combined Mode** : Toutes les statistiques sont calculées dans une seule requête SQL

  - Réduit le nombre total de requêtes et la surcharge réseau  
  - Optimise les performances lorsque les sources de données tiennent en mémoire  
  - Plus efficace pour des exécutions fréquentes et parallèles

**Impact :** Offre aux utilisateurs un contrôle précis sur l'exécution des requêtes afin d'équilibrer performances, consommation de ressources et sécurité mémoire selon les caractéristiques de leurs sources de données.


---

### Modèle de prédiction configurable

Le modèle qui sous-tend la détection d'anomalies est désormais configurable. Sept paramètres pilotent l'ajustement de la prédiction :

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

Les valeurs par défaut conviennent à la grande majorité des séries, et chaque paramètre peut être rétabli à sa valeur par défaut à tout moment.

**Impact :** Donne aux utilisateurs la maîtrise du modèle de prédiction lui-même, en complément des réglages Sensitivity et Memory existants sur la bande de tolérance. Pour savoir quand recourir à l'un d'eux et comment le régler, contactez digna.

---

### Expérience de tableau de bord repensée  
- UI/UX modernisée et améliorée  
- Navigation et structure plus claires  
- Meilleure visibilité des résultats de monitoring et des insights de qualité des données  
- Lecture améliorée des alertes, statistiques et tableaux de bord  
- Accès plus rapide aux informations opérationnelles clés  

**Impact :** Améliore l'utilisabilité et la productivité quotidienne pour tous les utilisateurs.

---

### Import & Export étendus pour les règles de validation  
- Fonctionnalité d'import/export des règles de validation enrichie  
- Migration facilitée entre environnements et projets  
- Réutilisation simplifiée de jeux de règles standardisés  
- Meilleure gouvernance et gestion du cycle de vie des règles  
- Collaboration simplifiée entre équipes  

**Impact :** Permet une gouvernance de la qualité des données évolutive et cohérente à l'échelle de l'organisation.

---

## Améliorations de la plateforme  

- Intégration complète du SDK Python pour l'automatisation  
- Déploiement conteneurisé via Docker  
- UX améliorée grâce à un tableau de bord repensé  
- Portabilité étendue de la logique de validation  

---

## Qui bénéficie de cette version  

- Data Engineers : automatisation, utilisation du SDK, intégration aux pipelines  
- Platform Teams : déploiement simplifié via Docker  
- Data Governance Teams : gestion réutilisable des règles de validation  
- Analytics Teams : meilleure utilisabilité et visibilité des insights  

---

## Mises à jour de la CLI  
- Ajout du support d'intégration du SDK  
- Flux d'import/export améliorés  
- Améliorations générales de stabilité et de performance