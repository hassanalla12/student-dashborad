# Student Prioritization Dashboard – Exercice Technique Ministère de l'Éducation

Ce projet présente une première version d’un outil permettant aux conseillers pédagogiques
de **prioriser les élèves nécessitant un accompagnement**, en se basant sur :

- leur **performance scolaire actuelle** (FinalGrade),  
- et la **complexité estimée d’un soutien pédagogique** (absences, failures, studytime, consommation d’alcool, etc.).

---

## 🚀 Fonctionnalités principales

- **KPIs globaux** : indicateurs synthétiques sur les élèves  
- **Analyse des facteurs majeurs** : absences, échecs, temps d’étude, alcool  
- **Visualisation centrale** :  
  ➜ Scatterplot *Complexity Score vs FinalGrade* permettant d'identifier
     immédiatement les élèves prioritaires  
- **Classement automatique des élèves à risque**  
- **Interface simple et intuitive** (Streamlit)  
- **Code facile à maintenir, à améliorer et à déployer**

---

## 🛠️ Installation locale

Pour exécuter l'application en local :

```bash
pip install -r requirements.txt
streamlit run dashboard.py
