import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

st.set_page_config(
    page_title="Tableau de bord — Priorisation des élèves à risque",
    layout="wide"
)

st.title(" Tableau de bord — Priorisation des élèves à risque")

st.markdown("""
Ce tableau de bord permet d’analyser les performances scolaires et d’identifier les élèves prioritaires selon leur **complexité d’accompagnement** et leur **niveau de risque**.
""")


st.markdown("---")

# A. Chargement + Préparation des données

@st.cache_data
def load_data():
    df = pd.read_csv("exercice_data.csv", encoding="latin1")

    # Nettoyage 
    df_clean = df.drop(columns=["StudentID", "FirstName", "FamilyName"], errors="ignore")

    # Conversion yes/no -> 1/0
    yes_no_cols = ["schoolsup", "famsup", "paid", "activities",
                   "nursery", "higher", "internet", "romantic"]
    for col in yes_no_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].map({"yes": 1, "no": 0})


    # RiskScore
    max_abs = max(df_clean["absences"].max(), 1)
    max_fail = max(df_clean["failures"].max(), 1)

    df_clean["RiskScore"] = (
        (df_clean["absences"] / max_abs) * 3 +
        (df_clean["failures"] / max_fail) * 3 +
        ((5 - df_clean["studytime"]) / 4) * 2 +
        ((df_clean["Walc"] + df_clean["Dalc"]) / 10) * 2 +
        (df_clean["goout"] / 5) * 2 +
        ((3 - df_clean["health"]) / 5) * 2
    )

    def classify_risk(score):
        if score >= 6:
            return "High Risk"
        elif score >= 3:
            return "Medium Risk"
        else:
            return "Low Risk"
    df_clean["RiskCategory"] = df_clean["RiskScore"].apply(classify_risk)

    
    # Complexity Score
    df_clean["complexity_score"] = (
        df_clean["absences"] * 0.4 +
        df_clean["Dalc"] * 0.2 +
        df_clean["Walc"] * 0.2 +
        (5 - df_clean["studytime"]) * 0.2
    )

    # Élève haut risque
    med_complexity = df_clean["complexity_score"].median()
    df_clean["high_risk"] = ((df_clean["FinalGrade"] < 10) &
                             (df_clean["complexity_score"] > med_complexity)).astype(int)

    return df_clean


df = load_data()


# B. SIDEBAR – FILTRES

st.sidebar.markdown("## Filtres du Dashboard")

df_filtered = df.copy()


# 1. Sexe
sex_filter = st.sidebar.multiselect(
    "Sexe :", options=df["sex"].unique(), default=df["sex"].unique()
)
df_filtered = df_filtered[df_filtered["sex"].isin(sex_filter)]


# 2. Âge
age_min, age_max = st.sidebar.slider(
    "Âge :", min_value=int(df["age"].min()),
    max_value=int(df["age"].max()),
    value=(int(df["age"].min()), int(df["age"].max()))
)
df_filtered = df_filtered[(df_filtered["age"] >= age_min) & (df_filtered["age"] <= age_max)]


# 3. Catégorie de risque
risk_filter = st.sidebar.multiselect(
    "Catégorie de risque :", options=df["RiskCategory"].unique(),
    default=df["RiskCategory"].unique()
)
df_filtered = df_filtered[df_filtered["RiskCategory"].isin(risk_filter)]


# 4. Adresse
address_filter = st.sidebar.multiselect(
    "Type d’habitation :", options=df["address"].unique(),
    default=df["address"].unique()
)
df_filtered = df_filtered[df_filtered["address"].isin(address_filter)]


# C. KPIs
st.subheader("Indicateurs Clés")

col1, col2, col3, col4, col5,  = st.columns(5)

with col1:
    st.metric("Moyenne FinalGrade", round(df_filtered["FinalGrade"].mean(), 2))

with col2:
    st.metric("Absences moyennes", round(df_filtered["absences"].mean(), 2))

with col3:
    low_study_pct = (df_filtered["studytime"] <= 2).mean() * 100
    st.metric("Faible temps d’étude (%)", f"{low_study_pct:.1f} %")

with col4:
    st.metric("Nombre d'élèves", len(df_filtered))

with col5:
    st.metric("Élèves à haut risque", df_filtered["high_risk"].sum())

st.markdown("---")


# D. VISUALISATIONS

# ----------------- SCATTERPLOT -----------------
st.subheader("Priorisation des élèves : Complexité vs Performance Finale")

fig3, ax3 = plt.subplots(figsize=(8, 6))
sizes = df_filtered["studytime"] * 40
# Scatterplot
scatter = ax3.scatter(
    df_filtered["complexity_score"],
    df_filtered["FinalGrade"],
    c=df_filtered["absences"],
    s=sizes,
    cmap="viridis",
    alpha=0.75,
    edgecolors="black",
    linewidth=0.5
)
# Lignes de séparation (zones de décision)
ax3.axhline(10, color='red', linestyle='--', alpha=0.6)
ax3.axvline(5, color='red', linestyle='--', alpha=0.6)

# Titres et labels
ax3.set_title("Nuage de points : Priorisation des élèves selon Complexité et Note Finale")
ax3.set_xlabel("Score de Complexité")
ax3.set_ylabel("Note Finale")

# Colorbar
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label("Absences")

st.pyplot(fig3)

# ----------------- HISTOGRAMME -----------------
st.subheader("Distribution des notes finales(vue d’ensemble)")
fig1, ax1 = plt.subplots(figsize=(7, 4))
ax1.hist(df_filtered["FinalGrade"], bins=15, color="purple", alpha=0.7)
ax1.set_xlabel("FinalGrade")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# -----------------  Absences vs FinalGrade  -----------------
st.subheader("Impact de l’absentéisme sur la performance scolaire")

abs_mean = df.groupby("absences")["FinalGrade"].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))

bars = ax.bar(abs_mean["absences"], abs_mean["FinalGrade"], color="purple", edgecolor="black")

# Rotation des labels
ax.set_xticks(abs_mean["absences"])
ax.set_xticklabels(abs_mean["absences"], rotation=90, fontsize=8)

ax.set_xlabel("Absences")
ax.set_ylabel("Note finale moyenne")
ax.set_title("Absences vs FinalGrade - Moyenne des notes")
ax.grid(axis='y', linestyle='--', alpha=0.6)

st.pyplot(fig)

# ----------------- BARPLOTS -----------------
st.subheader("Facteurs influençant la note finale")
colA, colB,colD, colE =st.columns(4)

# --------- FAILURES vs FinalGrade ---------
with colA:
    st.write("Influence des échecs antérieurs sur la note finale")

    figC, axC = plt.subplots(figsize=(4, 3))
    fail_mean = df_filtered.groupby("failures")["FinalGrade"].mean()

    bars = axC.bar(fail_mean.index.astype(str), fail_mean.values, color="#e74c3c", edgecolor="black")
    for bar in bars:
        axC.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f"{bar.get_height():.1f}", ha="center", fontsize=9)

    axC.set_xlabel("Failures")
    axC.set_ylabel("FinalGrade Moyenne")
    axC.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(figC)

# --------- STUDYTIME vs FinalGrade ---------
with colB:
    st.write("Lien entre temps d’étude et réussite scolaire")

    figD, axD = plt.subplots(figsize=(4, 3))
    study_mean = df_filtered.groupby("studytime")["FinalGrade"].mean()

    bars2 = axD.bar(study_mean.index.astype(str), study_mean.values, color="skyblue", edgecolor="black")
    for bar in bars2:
        axD.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                 f"{bar.get_height():.1f}", ha="center", fontsize=9)

    axD.set_xlabel("Studytime")
    axD.set_ylabel("FinalGrade Moyenne")
    axD.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(figD)

# ------------------ Dalc (alcool en semaine) ------------------
with colD:
    st.write("Consommation d’alcool (semaine) et performance scolaire")

    figDalc, axDalc = plt.subplots(figsize=(4, 3))
    dalc_mean = df_filtered.groupby("Dalc")["FinalGrade"].mean()

    bars_dalc = axDalc.bar(
        dalc_mean.index.astype(str),
        dalc_mean.values,
        color="#f39c12",
        edgecolor="black"
    )

    for bar in bars_dalc:
        height = bar.get_height()
        axDalc.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            f"{height:.1f}",
            ha="center",
            fontsize=9
        )

    axDalc.set_xlabel("Dalc (alcool semaine)")
    axDalc.set_ylabel("Note finale moyenne")
    axDalc.set_title("Dalc vs FinalGrade")
    axDalc.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(figDalc)


# ------------------ Walc (alcool week-end) ------------------
with colE:
    st.write(" Consommation d’alcool (week-end) et performance scolaire")

    figWalc, axWalc = plt.subplots(figsize=(4, 3))
    walc_mean = df_filtered.groupby("Walc")["FinalGrade"].mean()

    bars_walc = axWalc.bar(
        walc_mean.index.astype(str),
        walc_mean.values,
        color="#c0392b",
        edgecolor="black"
    )

    for bar in bars_walc:
        height = bar.get_height()
        axWalc.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            f"{height:.1f}",
            ha="center",
            fontsize=9
        )

    axWalc.set_xlabel("Walc (alcool week-end)")
    axWalc.set_ylabel("Note finale moyenne")
    axWalc.set_title("Walc vs FinalGrade")
    axWalc.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(figWalc)



# E. TABLEAU DES ÉLÈVES PRIORITAIRES
st.subheader("Élèves prioritaires")

df_filtered["priority_score"] = (
    (20 - df_filtered["FinalGrade"]) * 0.5 +
    df_filtered["complexity_score"] * 0.5
)

df_priority = df_filtered.sort_values("priority_score", ascending=False)

st.dataframe(df_priority.head(20)[[ "sex","age",
    "FinalGrade", "complexity_score", "priority_score",
    "absences", "studytime", "failures", "RiskCategory"
]])
