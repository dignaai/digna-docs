---
title: Planification avancée avec Crontab
description: Apprenez à planifier un job dans digna en utilisant des expressions crontab pour des horaires avancés.
---

# Planification avancée avec Crontab

Ce guide montre comment planifier des jobs dans *digna* en utilisant des **crontab expressions**.  
Contrairement aux modèles standard (quotidien, hebdomadaire, mensuel), crontab vous donne toute la flexibilité pour définir des horaires personnalisés.

---

## Démo interactive

<!--ARCADE EMBED START--><div style="position: relative; padding-bottom: calc(45.27777777777778% + 41px); height: 0; width: 100%;"><iframe src="https://demo.arcade.software/KsvddSRGi6uWSOsNhsP7?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true" title="Schedule a Data Job with a Custom Run Time" frameborder="0" loading="lazy" webkitallowfullscreen mozallowfullscreen allowfullscreen allow="clipboard-write" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; color-scheme: light;" ></iframe></div><!--ARCADE EMBED END-->

---

## Ce que vous apprendrez

- Comment ouvrir la section **Scheduling** dans le tableau de bord  
- Comment créer un nouveau job en utilisant une **crontab expression**  
- Comment définir un planning qui s'exécute uniquement les **week-ends à 10:00**  

---

## Exemple : Planning de week-end

Pour programmer un job pour qu'il s'exécute chaque **samedi et dimanche à 10:00**, utilisez l'expression suivante :


- `0` → minute (à l'heure)  
- `10` → hour (10 h)  
- `*` → every day of the month (chaque jour du mois)  
- `*` → every month (tous les mois)  
- `sat,sun` → only on Saturdays and Sundays (uniquement le samedi et le dimanche)  

---

## Pourquoi utiliser crontab ?

- Créer des plannings au-delà des modèles standard quotidiens, hebdomadaires ou mensuels  
- Définir des heures d'exécution précises (jours, heures ou intervalles spécifiques)  
- Utile pour les jobs du week-end, les vérifications en dehors des heures normales, ou la surveillance fréquente  

---