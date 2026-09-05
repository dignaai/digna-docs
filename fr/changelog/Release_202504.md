# Changelog – Release 2025.04

Avec la Release 2025.04, digna fait un pas important pour rendre la qualité et l'observabilité des données plus faciles à gérer, plus transparentes pour les équipes et accessibles aux utilisateurs du monde entier.  
Cette version combine **de nouvelles fonctionnalités puissantes**, **des améliorations d'automatisation des flux de travail** et **des raffinements de l'expérience utilisateur**.  

---

## Nouvelles fonctionnalités

### Inspection Hub – Un nouveau centre de commande
L'**Inspection Hub** est désormais disponible comme lieu central pour gérer tous vos jobs d'inspection. Plutôt que de passer d'un module à l'autre ou de s'appuyer uniquement sur l'exécution en ligne de commande, vous pouvez maintenant surveiller et contrôler vos inspections depuis une interface unifiée.  

Principales capacités :  
- Inspections à la demande : Lancez de nouveaux jobs instantanément quand vous avez besoin de résultats récents.  
- Historique des inspections : Consultez une chronologie des inspections — ce qui a été exécuté, qui l'a déclenché et quand.  
- Suivi du statut : Les jobs sont clairement indiqués comme terminés, en cours ou en attente.  
- Informations sur l'initiateur : Vérifiez rapidement si une inspection a été déclenchée par un utilisateur, le planificateur ou le CLI.  
- Outils de nettoyage : Supprimez les jobs obsolètes ou inutiles pour garder votre espace de travail propre.  
- Journaux détaillés : Analysez chaque job pour voir sa durée, quelles sources ont été incluses et comment les seuils ont été appliqués.  

L'Inspection Hub offre aux équipes une **visibilité et un contrôle de bout en bout**, rendant la gestion des inspections plus simple pour les grands projets.  

---

### Prise en charge multilingue – digna parle votre langue
digna est désormais prêt pour les équipes internationales avec l'introduction de la **prise en charge multilingue**.  

Dans cette version, vous pouvez définir votre **langue d'interface préférée** directement dans les Préférences utilisateur. Les langues prises en charge incluent :  
- English (UK, US, CA, AU)  
- German (DE, AT, CH)  
- Polish (PL)  

Cela facilite l'utilisation de digna pour les organisations multilingues et assure une adoption plus fluide au sein des équipes travaillant dans différentes régions. D'autres langues seront ajoutées dans les prochaines versions.  

---

### Import & Export de sources de données – Configuration simplifiée
La cohérence entre les environnements est essentielle dans les déploiements d'entreprise. Avec la 2025.04, digna introduit l'**import/export de sources de données** via **dignacli**, l'outil en ligne de commande pour les utilisateurs avancés.  

Avantages :  
- Exportez une configuration de source de données une fois, puis réutilisez-la dans Development, Test et Production.  
- Éliminez la reconfiguration manuelle et évitez les erreurs coûteuses.  
- Prenez en charge les workflows automatisés et les pipelines CI/CD avec de simples commandes CLI (`export-ds` et `import-ds`).  
- Copiez rapidement des sources de données entre projets pour faciliter la collaboration.  

Cette fonctionnalité garantit que les équipes peuvent déployer en toute confiance, en sachant que les configurations sont cohérentes dans chaque environnement.  

---

### Module Analytics (v1) – De la détection à la compréhension
digna a commencé comme une plateforme de détection d'anomalies et de surveillance de la qualité des données. Avec la Release 2025.04, elle évolue encore avec la **première version de Module Analytics**.  

Module Analytics aide les utilisateurs à **comprendre leurs données** plutôt qu'à simplement réagir aux problèmes. Avec ce nouveau module, vous pouvez :  
- Suivre les tendances à long terme dans vos jeux de données.  
- Détecter et surveiller la volatilité pour comprendre les fluctuations.  
- Explorer le comportement des données au fil du temps pour un contexte plus approfondi.  

Par exemple, digna peut automatiquement mettre en évidence que « Le nombre de lignes a augmenté de 15,8 % depuis le début de l'année. »  
Pas de requêtes SQL, pas de vérifications manuelles — juste des **insights exploitables en un coup d'œil**.  

Ceci constitue la base du parcours de digna vers des analyses de données avancées, permettant aux équipes data de passer d'une surveillance réactive à proactive.  

---

### Améliorations du tableau de bord – Une expérience utilisateur plus fluide
Au-delà des fonctionnalités majeures, la Release 2025.04 inclut plusieurs **améliorations du tableau de bord** conçues pour rendre digna plus intuitif et agréable à utiliser :  
- Navigation plus rapide entre les projets et les inspections.  
- Mise en page plus claire pour les journaux d'inspection et les soumissions de jobs.  
- Ajustements de design subtils qui vous aident à trouver les insights plus rapidement.  

Ces améliorations sont directement basées sur les retours clients et démontrent notre engagement continu à faire de digna **une plateforme conçue pour un usage quotidien**.  

---

## Améliorations générales
- Optimisations de performance pour les jobs d'inspection sur de grands ensembles de données.  
- Amélioration de la gestion des erreurs dans dignacli pour fournir des retours plus clairs.  
- Améliorations de la stabilité pour les projets avec de nombreux jobs simultanés.  
- Raffinements de l'interface pour le filtrage des journaux de jobs et la gestion des projets.  

---

## Résumé
La Release 2025.04 porte sur le **contrôle, l'accessibilité et l'insight**.  

- Le nouvel **Inspection Hub** offre aux utilisateurs une visibilité complète sur les jobs d'inspection.  
- La **prise en charge multilingue** permet à digna d'être utilisé par des équipes du monde entier.  
- La fonctionnalité **d'import/export** simplifie la gestion des configurations entre environnements.  
- **Module Analytics (v1)** déplace l'accent de la détection vers la compréhension, avec le suivi des tendances et de la volatilité.  
- Les **améliorations du tableau de bord** affinent l'expérience utilisateur globale.  

Ensemble, ces mises à jour rendent digna plus puissant, convivial et prêt pour l'internationalisation que jamais.