# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">Module Data Timeliness piloté par IA pour la qualité des données et l'observabilité – digna</h1>

---

## Objectif

Le module **Data Timeliness** garantit que **les données arrivent à l'heure** — à chaque fois.  
Il surveille en continu les calendriers de livraison et détecte automatiquement lorsque des jeux de données, tables ou fichiers sont **retardés, manquants ou incomplets**.  

En combinant l'apprentissage par IA et des horaires définis par l'utilisateur, *digna* permet aux organisations d'éviter les erreurs en aval et de respecter des objectifs stricts de **SLA (accord de niveau de service)** pour la **qualité des données** et l'**observabilité des pipelines de données**.

---

## Vue technique

### Modes de surveillance doubles
- **Modèles d'arrivée appris par l'IA**  
  digna apprend automatiquement le rythme naturel de vos livraisons de données — quotidiennes, horaires ou déclenchées par des événements — en analysant les horodatages historiques et les temps d'achèvement.  
  Il s'adapte aux changements de calendriers métier, aux week-ends ou aux pics de fin de mois.

- **Horaires définis par l'utilisateur**  
  Les utilisateurs peuvent définir explicitement les heures de livraison attendues (ex. : *tous les jours de la semaine avant 7h30*).  
  digna compare l'heure d'arrivée réelle au planning prévu et déclenche des alertes lorsque les données sont en retard ou manquantes.

### Mécanisme de détection
- Évalue les **horodatages de métadonnées**, les **comptages d'enregistrements** et la **fraîcheur des tables**  
- Détecte les **jobs ETL bloqués**, les **extractions échouées** et les **arrivées de fichiers partielles**  
- S'intègre avec *Data Anomalies* et *Data Validation* pour des insights combinés

---

## Scénarios de détection

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Flux de données marché quotidien retardé de deux heures, entraînant des rapports hors SLA |
| **Missing load** | Une table ou partition planifiée non mise à jour pour la date courante |
| **Chained dependency delay** | Le retard d'un job en amont impacte le rafraîchissement du pipeline en aval |
| **Weekend pattern shift** | Le modèle IA s'adapte automatiquement lorsqu'aucune donnée n'est attendue le dimanche |

---

## Architecture et exécution

- **Exécution in-database :** digna exécute les vérifications de timeliness directement dans votre base de données ou entrepôt de données.  
- **Accès metadata léger :** lit les horodatages de jobs, les comptages d'enregistrements et les informations de partition — aucune extraction de données requise.  
- **Fréquence configurable :** planifiez la surveillance par jeu de données, schéma ou pipeline.  
- **Alertes inter-modules :** les résultats peuvent déclencher des avertissements visuels dans *Inspection Hub* ou des notifications par e-mail, Slack ou API.  

---

## Cas d'utilisation exemple

- **Flux de marché financier :** détecter les retards dans les mises à jour des prix ou des données de trading.  
- **Chargements d'entrepôt de données :** surveiller lorsque les jobs ETL nocturnes se terminent plus tard que prévu.  
- **Partage de données entre équipes :** s'assurer que les livraisons départementales ont lieu avant les coupures quotidiennes.  
- **Reporting réglementaire :** confirmer que les soumissions incluent le dernier instantané de données disponible.  

---

## Avantages

| Area | Benefit |
|------|----------|
| **Business Continuity** | Évite les perturbations opérationnelles dues à des données retardées ou manquantes |
| **Data Quality** | Améliore la fiabilité et la cohérence des pipelines de données |
| **Compliance** | Assure le respect des SLA et la transparence pour les audits |
| **Automation** | L'IA supprime le suivi manuel des plannings |
| **Integration** | Fonctionne parfaitement avec *Data Analytics* pour visualiser les tendances de timeliness au fil du temps |

---

## Comment digna apprend les temps de livraison attendus

1. **Analyse historique :** digna observe les heures de chargement et les durées précédentes.  
2. **Modélisation IA :** le machine learning crée une baseline dynamique pour l'arrivée attendue.  
3. **Surveillance :** chaque nouvelle livraison est comparée à la baseline.  
4. **Alerte :** les écarts déclenchent des alertes avec des métriques contextuelles et des scores de confiance.  

Cette approche d'apprentissage continu s'adapte aux processus évolutifs tout en maintenant un faible taux de faux positifs.

---

## Questions fréquentes

**Puis-je définir mes propres horaires de livraison ?**  
Oui. digna prend en charge à la fois les plannings fixes définis par l'utilisateur et les modèles appris par l'IA.

**Peut-il s'intégrer à mon outil ETL ou d'orchestration ?**  
Oui. digna s'intègre à des outils tels que Airflow, dbt, Informatica ou des planificateurs personnalisés.

**Où se déroule le calcul ?**  
Toutes les analyses s'exécutent dans votre base de données ou votre entrepôt cloud — aucun service externe n'est utilisé.

**Que se passe-t-il lorsque les données sont en retard ?**  
digna déclenche des alertes dans le tableau de bord, dans Inspection Hub et via API/webhooks pour notifier immédiatement les équipes opérationnelles.

---


**digna Data Timeliness** aide à garantir la **confiance dans les données**, en combinant la **détection pilotée par IA**, l'**exécution sur site (on-premises)** et l'**observabilité des données** — le tout dans votre environnement contrôlé.