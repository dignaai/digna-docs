# digna Data Anomalies – Détection basée sur l'IA des problèmes de qualité des données

**Observabilité pilotée par l'IA pour une confiance des données en continu**

digna Data Anomalies fait partie de la **digna Data Observability Platform** — une solution modulaire qui améliore la **qualité des données** en analysant en continu le comportement des jeux de données au fil du temps.

Il apprend automatiquement ce à quoi ressemble le « normal » pour vos données et vous alerte lorsque le comportement change — sans définir de seuils statiques ni écrire la moindre règle.  
Le module s'exécute directement dans votre base de données, de sorte que les données ne quittent jamais votre environnement.

---

## Objectif de digna Data Anomalies

Le module **digna Data Anomalies** fournit une **observabilité des données** continue en calculant et en suivant des métriques statistiques prédéfinies telles que :

- Volume de données et nombre d'enregistrements  
- Taux de valeurs manquantes  
- Distributions de valeurs et histogrammes  
- Plages numériques et moyennes  
- Unicité des colonnes et longueur des textes  

Ces métriques sont collectées automatiquement pour chaque jeu de données.  
En les utilisant, digna construit des modèles qui représentent le comportement typique de chaque métrique — apprenant les schémas quotidiens, hebdomadaires ou saisonniers.  
Une fois entraîné, le module prédit les valeurs attendues pour les nouvelles données et détecte les écarts qui peuvent indiquer des problèmes de qualité, des pannes de processus ou des changements en amont.

---

## Principales capacités

- Apprend automatiquement le comportement attendu des données grâce à l'IA — sans configuration de seuils.  
- Détecte les baisses soudaines, les pics ou les dérives dans le volume de données et les distributions.  
- Identifie les colonnes inversées ou les mappages incorrects entre attributs.  
- Met en évidence des valeurs catégorielles inattendues (par ex., de nouvelles régions ou codes).  
- Prend en charge tous les types de colonnes : numériques, catégorielles ou non spécifiées.  
- Fonctionne entièrement dans l'environnement du client — aucun déplacement de données.  
- S'intègre avec **digna Data Analytics** pour l'analyse des tendances à long terme.

---

## Comment ça marche

### Étape 1 – Calcul des métriques
digna calcule un ensemble de métriques de profil pour chaque table et colonne.  
Ces métriques décrivent la structure et le comportement statistique de vos données et sont stockées pour analyse ultérieure.

### Étape 2 – Entraînement du modèle
À partir des valeurs historiques des métriques, digna entraîne des modèles compacts d'apprentissage automatique (signature models) qui capturent la plage normale de chaque métrique.

### Étape 3 – Seuils automatiques
En utilisant *inférence conforme*, digna calcule des intervalles de confiance adaptatifs (seuils automatiques) qui évoluent avec vos données.  
Si de nouvelles valeurs de métriques se situent en dehors de la plage prédite, elles sont signalées comme anomalies.

Cette boucle de rétroaction continue garantit que la surveillance reste pertinente même lorsque les volumes ou les schémas de données évoluent naturellement.

---

## Scénarios d'exemple

### Baisse inattendue du volume d'enregistrements
Un jeu de données contient typiquement environ 500 000 enregistrements par jour.  
Lorsqu'une nouvelle livraison ne comprend que 50 000 enregistrements, digna signale une anomalie et montre à quel point la valeur dévie de sa plage apprise.

### Colonnes inversées détectées
La longueur moyenne de chaîne de `last_name` correspond soudainement à celle de `first_name`.  
digna reconnaît la déviation dans les motifs de métriques et signale un possible échange de colonnes.

### Catégorie inattendue détectée
Une colonne listant des villes autrichiennes contient soudainement “Zurich”.  
Sur la base des distributions historiques, digna marque la nouvelle valeur comme inattendue et alerte l'utilisateur.

---

## Intégration avec d'autres modules

- **digna Data Analytics** — agrège l'historique des anomalies et les métriques de volatilité pour révéler les tendances à long terme.  
- **digna Data Validation** — applique des règles métier explicites pour des contrôles de qualité déterministes.  
- **digna Data Timeliness** — surveille les temps d'arrivée des données et corrèle les retards avec les occurrences d'anomalies.  
- **digna Data Schema Tracker** — détecte les changements structurels pouvant expliquer de nouvelles anomalies.

---

## Cas d'utilisation typiques

- Détection de chargements de données manquants ou en double.  
- Identification de colonnes inversées ou tronquées.  
- Détection de dérive de distribution pour des caractéristiques numériques ou catégorielles.  
- Recherche de valeurs ou codes de référence inattendus.  
- Surveillance des pipelines d'ingestion continus pour détecter des irrégularités.  
- Suivi de la **qualité et de l'observabilité des données** à travers les domaines.

---

## Avantages

- Détection immédiate des comportements de données anormaux.  
- Élimine l'ajustement manuel des seuils.  
- Réduit l'effort opérationnel pour les grands environnements de données.  
- Renforce la confiance dans les systèmes d'analyse et de reporting.  
- Renforce la **qualité des données** et l'**observabilité des données** de bout en bout.

---

## Modules digna apparentés

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — métriques de tendance et de volatilité.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — vérification des données basée sur des règles.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — surveillance des calendriers de livraison des données.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — détection des changements de schéma.

---

## Résumé

Le module **digna Data Anomalies** constitue le cœur de la **digna Data Observability Platform** pilotée par l'IA.  
En surveillant en continu les métriques clés, en apprenant les schémas et en identifiant les écarts, il aide les organisations à garantir que la **qualité des données** reste fiable, stable et explicable — sans configuration manuelle.