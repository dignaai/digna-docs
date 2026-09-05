# Data Anomalies – Automated Detection
<h1 style="display:none;">Module piloté par l'IA pour la qualité et l'observabilité des données – digna Data Anomalies</h1>

---

## Purpose

Le module **Data Anomalies** identifie automatiquement les irrégularités dans vos jeux de données — sans besoin d'écrire des règles.  
Il surveille en continu **la qualité de la livraison des données**, apprend ce qu'est la “normale” et détecte les écarts en temps réel.

En utilisant une détection basée sur l'IA, digna repère les *erreurs silencieuses de données* telles que les enregistrements manquants, dupliqués ou corrompus pouvant fausser les rapports, les modèles ML et les tableaux de bord.

---

## Technical Overview

### Metrics analyzed

digna profile en continu les aspects suivants de vos données :

- **Volume d'enregistrements** – nombre total de lignes, quotidien ou par lot  
- **Valeurs manquantes** – détection des champs nuls ou vides  
- **Distributions et histogrammes** – surveillance des changements de forme des données  
- **Plages de valeurs** – identification automatique des valeurs hors plage ou extrêmes  
- **Unicité** – vérification des clés dupliquées ou des entrées répétées  

### Intelligent anomaly detection

- Utilise **l'apprentissage historique** pour définir dynamiquement des bornes attendues  
- Détecte les écarts au niveau du **volume, des distributions de valeurs ou des relations logiques**  
- Emploie l'IA pour adapter automatiquement les seuils selon l'heure de la journée ou les schémas saisonniers  
- Différencie les **fluctuations statistiques** des véritables anomalies  
- Produit des métriques détaillées et des scores de confiance par jeu de données et par colonne  

---

## Detection Scenarios

Ci‑dessous des exemples de problèmes réels détectés automatiquement par le module **Data Anomalies** :

| Scenario | Description |
|-----------|--------------|
| **Baisse ou pic de volume** | Moitié des transactions quotidiennes manquantes, chargements de lots dupliqués ou pics de données soudains |
| **Valeurs manquantes ou nulles** | Extractions terminées mais colonnes critiques laissées vides |
| **Dérives de distribution** | Le montant moyen d'achat ou le nombre de transactions par région change de façon inattendue |
| **Échange de colonnes** | Des colonnes comme *first_name* et *last_name* inversées accidentellement pendant l'ETL |
| **Valeurs catégorielles inattendues** | p.ex., « Zurich » apparaît dans la liste des villes autrichiennes |
| **Perte soudaine d'unicité** | Des identifiants auparavant uniques commencent à se dupliquer à cause d'erreurs de jointure en amont |

---

## Architecture and Execution

- **Exécution dans la base de données :** Toute la logique de détection d'anomalies s'exécute *à l'intérieur du moteur de base de données* (Teradata, Snowflake, Databricks, PostgreSQL, etc.)  
- **Aucun déplacement de données :** digna lit uniquement des métriques, ne transfère jamais les données brutes à l'extérieur  
- **Mises à jour incrémentielles :** Seuls les segments de données nouveaux sont analysés à chaque exécution pour des raisons d'efficacité  
- **Fréquence d'inspection configurable :** Horaire, quotidienne ou déclenchée par des processus en amont  
- **Stockage des résultats :** Les métriques et les indicateurs d'anomalie sont écrits dans le schéma d'observabilité de digna pour visualisation et alerting  

---

## Benefits

| Area | Benefit |
|------|----------|
| **Automatisation** | Élimine des centaines de définitions SQL ou de règles manuelles |
| **Précision** | Détecte des problèmes que des seuils statiques manquent souvent |
| **Scalabilité** | Surveille efficacement des millions d'enregistrements par table |
| **Intégration** | Fonctionne de manière fluide avec *digna Data Analytics* pour l'analyse des tendances |
| **Conformité** | Assure un contrôle continu sur la **qualité et l'observabilité des données** |
| **Transparence** | Fournit des scores de confiance, des horodatages et des codes de raison pour chaque anomalie |

---

## How digna Learns “Normal”

1. **Phase de profilage :** digna collecte des métriques à partir des jeux de données historiques.  
2. **Phase d'apprentissage :** Les modèles IA identifient les motifs récurrents (saisonniers, hebdomadaires, quotidiens).  
3. **Phase de surveillance :** Les futurs jeux de données sont comparés aux seuils appris dynamiquement.  
4. **Phase d'alerte :** Les écarts au‑delà des bornes de confiance statistiques sont signalés comme anomalies.  

Tous les modèles sont explicables, déterministes et optimisés pour les volumes de données d'entreprise.

---

## Example Use Cases

- Surveillance de la qualité des données dans les **systèmes de transactions bancaires**  
- Détection des échecs de chargement dans les jobs **ETL** ou les entrepôts de données  
- Identification d'activités client anormales dans les **enregistrements télécom**  
- Observation de la cohérence des données cliniques dans les pipelines d'**analytique santé**  
- Prévention des tableaux de bord cassés dans les environnements **BI et reporting**

---

## Frequently Asked Questions

**Data Anomalies nécessite‑t‑il des règles prédéfinies ?**  
Non — le module apprend automatiquement à partir du comportement des données.

**Puis‑je toujours définir des seuils spécifiques si nécessaire ?**  
Oui. digna permet de combiner la détection basée sur l'IA et la détection par règles (via *Data Validation*).

**Comment les faux positifs sont‑ils minimisés ?**  
Le module utilise un apprentissage adaptatif et des scores de confiance statistiques pour ignorer les variations saisonnières normales.

**Où s'effectue le calcul ?**  
Tout le traitement s'exécute au sein de votre base de données — digna n'extrait jamais les données brutes.

**Est‑ce adapté aux données sensibles ou réglementées ?**  
Oui. digna s'exécute entièrement sur site ou dans un cloud privé et respecte les normes de conformité européennes.

---