# Student Prioritization Dashboard – Exercice Technique (Ministère de l'Éducation)

Ce projet présente une première version d’un outil permettant aux conseillers pédagogiques
de **prioriser les élèves nécessitant un accompagnement**, en se basant sur :

- leur **performance scolaire actuelle** (FinalGrade),
- et la **complexité estimée d’un soutien pédagogique** (absences, failures, studytime, alcool…).

L’objectif est de proposer une solution simple, intuitive et facilement déployable.

---

## Fonctionnalités principales

- **KPIs globaux** : performance moyenne, absences, temps d’étude faible, élèves à risque
- **Analyse des facteurs majeurs** : absences, échecs, temps d’étude, alcool
- **Visualisation centrale** :
  ➜ Scatterplot *Complexity Score vs FinalGrade* permettant d’identifier rapidement les élèves prioritaires
- **Classement automatique** des élèves à accompagner en priorité
- **Interface simple et intuitive** (Streamlit)
- **Code facile à adapter, maintenir et déployer**

---

## Installation locale

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Déploiement Streamlit Cloud

Cette application est conçue pour être déployée rapidement sur Streamlit Cloud.

1. Importer ce repository dans votre compte Streamlit  
2. Sélectionner le fichier principal : `dashboard.py`  
3. Lancer le déploiement  

---

## Structure du projet

```
dashboard.py        → Code principal de l'application Streamlit
requirements.txt    → Dépendances nécessaires au fonctionnement
README.md           → Présentation du projet et explication des critères
```

---

## Explication des critères, KPIs et limitations

Les KPIs et le score de priorisation ont été définis en combinant des indicateurs fortement liés à la performance scolaire : absences, temps d’étude, nombre d’échecs et note finale.  
Le *complexity score* regroupe ces facteurs avec des pondérations simples, permettant d'estimer rapidement la difficulté d’accompagnement d’un élève.  
Le *priority score* combine ce niveau de complexité et la performance actuelle pour identifier les élèves à aider en premier.

Une limite de cette méthode est que les pondérations utilisées sont définies manuellement et non optimisées statistiquement ; certains indicateurs peuvent aussi être sous-déclarés (ex : alcool).  

Une amélioration future consisterait à affiner les pondérations à partir de retours du personnel pédagogique ou à intégrer un modèle prédictif plus avancé pour prioriser les élèves de manière plus robuste.

---

## Auteur

Projet réalisé dans le cadre de l’exercice technique du Ministère de l'Éducation.
