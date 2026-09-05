# Journal des modifications – Version 2026.04  

Avec la version 2026.04, digna renforce significativement ses capacités en analytique et en validation des données.  
Cette version introduit une analyse avancée des séries temporelles, des composants de validation réutilisables et une standardisation centralisée des valeurs.

---

## Nouvelles fonctionnalités  

### Analytics Chart – Analyse des séries temporelles sans science des données  
- Nouveau **Analytics Chart** pour l'analyse interactive des séries temporelles  
- Méthodes analytiques intégrées :
    - Régressions linéaire, quadratique et cubique  
    - Régression par segments avec points de rupture configurables  
    - Techniques de lissage  
    - Analyse des quantiles  
- Identification automatique des tendances, de la saisonnalité et des changements de motifs  
- Analyse des résidus pour une compréhension approfondie des écarts  
- Les séries temporelles sont calculées automatiquement pour chaque jeu de données  

**Impact :** Permet aux utilisateurs de comprendre le comportement complexe des données au fil du temps sans expertise en science des données ni outils externes.

---

### Énumérations – Définition centralisée des valeurs autorisées  
- Définissez des jeux réutilisables de valeurs autorisées (ex. : pays, états, codes d'état)  
- Validez les valeurs de colonnes par rapport à des énumérations prédéfinies dans **digna Data Validation**  
- Réutilisez les énumérations entre projets et sources de données  
- Utilisez les énumérations partout via `#ENUM:MY_ENUM#`  
- Toutes les vérifications sont exécutées **directement dans la base de données source**  

**Impact :** Assure des valeurs de données cohérentes et standardisées dans toute l'organisation.

---

### Modèles de règles de validation – Logique réutilisable de qualité des données  
- Définissez des règles de validation réutilisables (ex. : vérifications d'espaces, NOT NULL, vérifications de format)  
- Appliquez les modèles à plusieurs jeux de données  
- Garantissez une logique de règle cohérente entre les projets  
- Réduisez les duplications et la configuration manuelle  
- Toutes les vérifications sont exécutées **directement dans la base de données source**  

**Impact :** Permet une validation des données scalable et haute performance sans déplacement des données.

---

### Conditions de pertinence au niveau des statistiques  
- Définissez des conditions de pertinence au **niveau des colonnes pour chaque statistique**  
- Étend le concept des conditions de pertinence pour les anomalies  
- Contrôlez quand une statistique doit être considérée comme pertinente  
- Réduisez le bruit en excluant les situations non critiques  

**Impact :** Améliore la qualité du signal en ne se concentrant que sur les écarts significatifs.

---

## Capacités étendues d'analyse de données et de validation  

Avec cette version, digna étend à la fois la **compréhension des données** et la **standardisation de la validation des données** :

- Interprétation avancée des **séries temporelles** sans connaissances en science des données  
- Définition centralisée des **valeurs autorisées via des énumérations**  
- Logique de **validation réutilisable via des modèles**  
- Contrôle granulaire de la **pertinence des statistiques et des alertes**  

Ensemble, ces capacités permettent aux organisations non seulement de détecter les problèmes, mais aussi de **comprendre, standardiser et contrôler la qualité des données**.

---

## Bénéficiaires de cette version  

- **Ingénieurs de données :** Logique de validation réutilisable et meilleur contrôle du comportement de surveillance  
- **Équipes Qualité des données & Gouvernance :** Règles standardisées et validation cohérente des données entre les systèmes  
- **Équipes Analytics & BI :** Meilleure compréhension des tendances et des écarts  
- **Propriétaires de plateforme :** Adoption accrue via une analytique simplifiée et une validation scalable  

---

## Mises à jour CLI  
- Aucun changement  

---