import streamlit as st
import pandas as pd

# --- Basiskonfiguration ------------------------------------------------------
st.set_page_config(
    page_title="EAM Maturity Assessment",
    page_icon="🧱",
    layout="wide"
)

# --- Helper -------------------------------------------------------------------
def maturity_label(score: float) -> str:
    if score < 1.5:
        return "Level 1 – Ad-hoc / Chaotisch"
    elif score < 2.5:
        return "Level 2 – Wiederholbar"
    elif score < 3.5:
        return "Level 3 – Definiert"
    elif score < 4.5:
        return "Level 4 – Gesteuert / Gemessen"
    else:
        return "Level 5 – Optimiert / Kontinuierlich verbessert"


# Konfiguration der Dimensionen & Fragen
DIMENSIONS = {
    "Strategie & Governance": [
        "EAM ist klar in der Unternehmensstrategie verankert.",
        "Es gibt verbindliche Richtlinien / Referenzarchitekturen.",
        "Architektur-Entscheidungen werden aktiv gesteuert (Boards, Gremien).",
    ],
    "Methoden & Standards": [
        "Es existiert ein dokumentiertes EAM-Vorgehensmodell.",
        "Architektur-Standards werden in Projekten verbindlich angewendet.",
        "EAM-Artefakte (z.B. Capability Maps) sind konsistent und aktuell.",
    ],
    "Tooling & Repository": [
        "Es gibt ein zentrales Architektur-Repository (z.B. EA-Tool).",
        "Architekturdaten werden aktiv gepflegt (Owner, Prozesse).",
        "Schnittstellen zu CMDB / Portfolio / Projekttools existieren.",
    ],
    "EAM im Projekt- & Lösungsdesign": [
        "Solution-Architekten nutzen EAM-Artefakte in Projekten.",
        "Es gibt verbindliche Architecture-Reviews / -Checkpoints.",
        "EAM ist in Projekt- und Change-Prozesse integriert.",
    ],
    "Data & AI im EAM": [
        "Architekturdaten werden für Auswertungen und Reports genutzt.",
        "Es gibt erste AI-Unterstützung (z.B. Analyse, Vorschläge, Clustering).",
        "Datenqualität des Architektur-Repository ist ausreichend für Analysen.",
    ],
    "Organisation & Skills": [
        "Rollen & Verantwortlichkeiten für EAM sind klar definiert.",
        "EAM hat ausreichende Kapazität & Budget.",
        "Mitarbeitende kennen Nutzen & Prinzipien von EAM.",
    ],
}

# --- Sidebar ------------------------------------------------------------------
st.sidebar.title("EAM Maturity Assessment")
st.sidebar.markdown(
    """
Dieses Tool erfasst den **Reifegrad deines Enterprise Architecture Managements**
anhand mehrerer Dimensionen.

Bewerte jede Aussage von **1 (trifft überhaupt nicht zu)** bis
**5 (trifft voll zu)**.
"""
)

with st.sidebar.expander("Hinweise zur Interpretation"):
    st.markdown(
        """
- **Level 1–2**: Eher ad-hoc, stark personenabhängig  
- **Level 3**: Definierte Prozesse, sichtbare Struktur  
- **Level 4–5**: Messbare Steuerung, kontinuierliche Verbesserung, hoher Business-Impact
"""
    )

# Optional: Metadaten zum Assessment
st.sidebar.subheader("Assessment-Infos")
assessment_name = st.sidebar.text_input("Name des Assessments", "Pilot EAM Assessment")
participant = st.sidebar.text_input("Teilnehmer / Bereich", "")

# --- Hauptinhalt -------------------------------------------------------------
st.title("🧱 EAM Maturity Assessment")

st.markdown(
    """
Dieses Formular hilft dir, den aktuellen **Reifegrad deiner EAM-Fähigkeiten**
strukturiert einzuschätzen.

Beantworte die Aussagen möglichst **realistisch** – das ist ein Werkzeug zur
Selbstreflexion, kein Marketing-Pitch 😉.
"""
)

# Formular für Bewertung
with st.form("eam_assessment_form"):
    st.markdown("### Bewertungen")

    scores = {}
    for dim, questions in DIMENSIONS.items():
        st.markdown(f"#### {dim}")
        dim_scores = []
        for q in questions:
            value = st.slider(
                q,
                min_value=1,
                max_value=5,
                value=3,
                step=1,
                help="1 = trifft überhaupt nicht zu, 5 = trifft voll zu",
                key=f"{dim}-{q}",
            )
            dim_scores.append(value)
        scores[dim] = dim_scores

    submitted = st.form_submit_button("Auswertung anzeigen")

# --- Auswertung --------------------------------------------------------------
if submitted:
    # Durchschnitt pro Dimension
    dim_results = {}
    for dim, values in scores.items():
        dim_results[dim] = sum(values) / len(values)

    overall_score = sum(dim_results.values()) / len(dim_results)
    overall_label = maturity_label(overall_score)

    st.markdown("---")
    st.header("Ergebnis")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(
            label="Gesamt-Reifegrad (Ø über alle Dimensionen)",
            value=f"{overall_score:.2f}",
            delta=overall_label,
        )

        st.markdown("**Verbale Einordnung:**")
        st.markdown(f"- {overall_label}")

        if participant:
            st.markdown(f"**Teilnehmer / Bereich:** {participant}")
        if assessment_name:
            st.markdown(f"**Assessment:** {assessment_name}")

    with col2:
        st.markdown("**Reifegrad je Dimension (Durchschnitt):**")
        df = pd.DataFrame(
            {
                "Dimension": list(dim_results.keys()),
                "Score": list(dim_results.values()),
            }
        ).set_index("Dimension")

        st.bar_chart(df)

    # Textuelle Hinweise je nach Score
    st.markdown("### Interpretation & nächste Schritte")

    if overall_score < 2:
        st.warning(
            "Dein EAM befindet sich in einem **sehr frühen Reifegrad**. "
            "Fokus: Grundlagen schaffen – Rollen, Governance, erste Artefakte und ein leichtgewichtiges Operating-Modell etablieren."
        )
    elif overall_score < 3:
        st.info(
            "Dein EAM ist **im Aufbau**. Ihr habt erste Strukturen, aber noch viel Potenzial, "
            "um verbindliche Prozesse, Tooling und Governance zu stärken."
        )
    elif overall_score < 4:
        st.success(
            "Dein EAM ist **solide aufgestellt**. Der nächste Schritt ist stärkere Messbarkeit, "
            "Integration in Entscheidungsprozesse und mehr Automatisierung/AI."
        )
    else:
        st.success(
            "Sehr hoher Reifegrad – Fokus auf **kontinuierliche Verbesserung**, datengetriebene Steuerung "
            "und Skalierung des Nutzens (z.B. durch AI-gestützte Analysen)."
        )

    # Tabelle mit Detailergebnissen
    st.markdown("### Detailübersicht")
    detail_rows = []
    for dim, values in scores.items():
        for i, q in enumerate(DIMENSIONS[dim]):
            detail_rows.append(
                {
                    "Dimension": dim,
                    "Frage": q,
                    "Bewertung": values[i],
                }
            )
    detail_df = pd.DataFrame(detail_rows)
    st.dataframe(detail_df, use_container_width=True)

    # Download als CSV
    st.markdown("### Export")
    csv = detail_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Ergebnisse als CSV herunterladen",
        data=csv,
        file_name="eam_maturity_results.csv",
        mime="text/csv",
    )

else:
    st.info("Bitte fülle das Formular aus und klicke auf **„Auswertung anzeigen“**.")
