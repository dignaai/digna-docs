# Changelog – Release 2024.12

La version 2024.12 apporte un nouvel ensemble de fonctionnalités et d'améliorations qui rendent digna plus automatisé, flexible et prêt pour l'entreprise.  
Cette version améliore la planification, le reporting, la gestion des requêtes et la précision de la détection d'anomalies.  

---

## Nouvelles fonctionnalités

### Built-in Scheduler
Les inspections ne dépendent plus uniquement de la ligne de commande ou des appels API.  
Avec le **nouveau digna Scheduler**, les inspections peuvent être exécutées automatiquement à des moments définis.  

- Prend en charge les **expressions Cron** pour les planifications récurrentes (quotidiennes, hebdomadaires ou intervalles personnalisés).  
- Offre un contrôle précis via les **offsets**, les **dates de début** et les **dates de fin**.  
- Permet aux équipes de garantir que toutes les sources de données critiques sont inspectées de façon cohérente et sans effort manuel.  

---

### Rapports au format PDF
Les équipes peuvent désormais partager facilement les résultats avec les parties prenantes grâce aux **exports PDF**.  

- Les graphiques, métriques et résultats d'anomalies peuvent être exportés dans un format PDF professionnel.  
- Les rapports combinent les **visualisations** et les **données sous-jacentes** pour servir à la fois les utilisateurs techniques et métier.  
- Élimine le besoin d'outils externes pour la création de rapports.  

---

### Nouveau type de colonne : `CUSTOM`
Pour offrir plus de flexibilité, digna introduit un nouveau **type de colonne `CUSTOM`**.  

- Les utilisateurs peuvent définir précisément quelles **statistiques et métriques** sont appliquées à des attributs spécifiques.  
- Idéal pour des cas particuliers qui ne rentrent pas dans des catégories standard telles que NUMERICAL ou CATEGORICAL.  
- Aide à maintenir des analyses ciblées et des résultats pertinents pour le contexte métier.  

---

### Nouveaux placeholders dans les requêtes snapshot
Les requêtes snapshot sont désormais plus simples et moins sujettes aux erreurs grâce aux **placeholders dynamiques**.  

- Des tokens comme `#date+n#` ou `#date-n#` ajustent automatiquement les dates dans les requêtes.  
- Exemple :  
  - `#date+1#` → demain  
  - `#date-2#` → il y a deux jours  
- Élimine les calculs manuels de dates et assure la cohérence entre les équipes.  

---

### Optimisation des seuils
Les seuils d'anomalie sont désormais plus intelligents et sensibles au contexte.  

- Pour des métriques telles que **NULL COUNT**, les seuils inférieurs sont automatiquement plafonnés à **0**.  
- Évite des seuils invalides ou dépourvus de sens.  
- Se traduit par moins de faux positifs et une détection d'anomalies plus fiable.  

---

## Améliorations générales
- Composants **UI** affinés dans les vues de configuration de projet et d'attribut.  
- **Performance du tableau de bord** améliorée pour de grands volumes de données.  
- **Journalisation et messages d'erreur** renforcés pour faciliter le dépannage.  

---

## Résumé
La Release 2024.12 renforce digna en tant que plateforme pour la **qualité des données, la détection d'anomalies et l'observabilité**.  
Avec l'automatisation via la planification, des rapports PDF partageables, des colonnes personnalisables, des requêtes snapshot simplifiées et des seuils plus intelligents, digna devient encore plus précieux pour les utilisateurs techniques comme pour les parties prenantes métier.