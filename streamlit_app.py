import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------------------
# Basic Page Config
# -------------------------------------------------------------------
st.set_page_config(
    page_title="EAM Maturity Assessment",
    page_icon="🧱",
    layout="wide"
)

# -------------------------------------------------------------------
# Config: Dimensionen, Fragen, Kurzbeschreibungen
# -------------------------------------------------------------------
DIMENSIONS = [
    {
        "id": "strategy",
        "name": "Strategische Verankerung & Governance",
        "description": "Wie stark ist EAM in Strategie, Entscheidungsprozessen und Governance verankert?",
        "questions": [
            "Es gibt ein klares, schriftlich fixiertes Mandat für EAM (z.B. vom CIO/Board).",
            "EAM-Ziele sind explizit mit der Unternehmensstrategie verknüpft.",
            "Architekturentscheidungen werden in festen Gremien getroffen (Architecture Board, Governance Runden).",
            "EAM-Prinzipien (z.B. Cloud first, Clean Core, Standardisierung) sind definiert und werden angewendet."
        ],
    },
    {
        "id": "method",
        "name": "Methoden, Modelle & Referenzarchitekturen",
        "description": "Reifegrad von Vorgehensmodell, Artefakten und Standards.",
        "questions": [
            "Es existiert ein dokumentiertes EAM-Vorgehensmodell (z.B. Phasen, Deliverables, Rollen).",
            "Es gibt belastbare Referenzarchitekturen (z.B. ERP Cloud RefArch, Integrationsarchitektur).",
            "Business Capabilities, Domänenmodelle und Zielbilder werden aktiv genutzt.",
            "EAM-Vorgaben sind in Projektstandards (Templates, Checklisten, Qualitätsschranken) verankert."
        ],
    },
    {
        "id": "tooling",
        "name": "Tooling & Architektur-Repository",
        "description": "Wie gut sind Daten, Werkzeuge und Integrationen rund um EAM aufgestellt?",
        "questions": [
            "Es existiert ein zentrales Architektur-Repository / EA-Tool.",
            "Architekturobjekte (Anwendungen, Schnittstellen, Capabilities, Technologien) sind weitgehend vollständig gepflegt.",
            "Es gibt Schnittstellen zu anderen Systemen (CMDB, Projektportfolio, CI/CD, ITSM).",
            "Architekturdaten werden regelmäßig aktualisiert (definierte Owner & Prozesse)."
        ],
    },
    {
        "id": "projects",
        "name": "EAM in Projekten & Lösungsarchitektur",
        "description": "Wie stark ist EAM im Projektalltag verankert?",
        "questions": [
            "Für Projekte gibt es verpflichtende Architektur-Checkpoints (z.B. Solution Design Review).",
            "Solution-Architekten nutzen aktiv EAM-Artefakte (z.B. Capability Maps, Referenzarchitekturen).",
            "Architekturvorgaben fließen in Ausschreibungen, Provider-Briefings und technische Designs ein.",
            "Es gibt klare Kriterien, wann Projekte EAM involvieren müssen (z.B. Budget, Kritikalität, Domäne)."
        ],
    },
    {
        "id": "data_ai",
        "name": "Datenbasis & AI-Unterstützung im EAM",
        "description": "Wie daten- und AI-getrieben arbeitet das EAM?",
        "questions": [
            "Es existieren Standard-Reports/Dashboards auf Basis von Architekturdaten (Landscape, Risiken, Redundanzen).",
            "Architekturdaten werden für Entscheidungen genutzt (z.B. für Roadmaps, Decommissioning, Cloud-Migration).",
            "AI wird bereits getestet oder eingesetzt (z.B. automatisierte Analysen, Clustering, Impact-Analysen).",
            "Die Datenqualität im EA-Repository ist ausreichend, um sinnvolle AI-Use-Cases zu ermöglichen."
        ],
    },
    {
        "id": "org_skills",
        "name": "Organisation, Rollen & Skills",
        "description": "Struktur, Kapazität und Kompetenzen des EAM.",
        "questions": [
            "Rollen für EAM (Enterprise-, Domain-, Solution-Architekten) sind definiert und beschrieben.",
            "Es existiert ein dediziertes EAM-Team mit klarer Verantwortlichkeit.",
            "Stakeholder kennen Nutzen und Arbeitsweise des EAM (Kommunikation, Schulungen).",
            "Es existiert ein Skill- und Entwicklungsplan für Architekt:innen (Methodik, Cloud, Security, Data, AI)."
        ],
    },
    {
        "id": "value",
        "name": "Business Value & Steuerung",
        "description": "Wie messbar trägt EAM zum Geschäftserfolg bei?",
        "questions": [
            "Es gibt Kennzahlen/OKRs für EAM (z.B. Technologiestandardisierung, Reduktion Redundanzen).",
            "EAM wird aktiv genutzt, um Investitionen zu priorisieren (z.B. Roadmaps, Portfolioentscheidungen).",
            "Erfolge von EAM werden sichtbar gemacht (z.B. Case Studies, Management-Reports).",
            "Business-Vertreter sehen EAM überwiegend als Enabler, nicht als Bremse."
        ],
    },
]

# -------------------------------------------------------------------
# Helper: Maturity Berechnung & Texte
# -------------------------------------------------------------------
def maturity_label(score: float) -> str:
    if score < 1.5:
        return "EA Level 1 – Ad-hoc / Chaotisch"
    elif score < 2.5:
        return "EA Level 2 – Wiederholbar (Basic Setup)"
    elif score < 3.5:
        return "EA Level 3 – Definiert (Strukturiert etabliert)"
    elif score < 4.5:
        return "EA Level 4 – Gesteuert & Gemessen"
    else:
        return "EA Level 5 – Optimiert & Wertgetrieben"


def cmmi_level(score: float):
    """Einfache Mapping-Logik von EA-Maturity auf CMMI-Level."""
    if score < 1.5:
        lvl = 1
        desc = "CMMI Level 1 – Initial (unstrukturiert, stark personenabhängig)"
    elif score < 2.5:
        lvl = 2
        desc = "CMMI Level 2 – Managed (grundlegende Planung und Wiederholbarkeit)"
    elif score < 3.5:
        lvl = 3
        desc = "CMMI Level 3 – Defined (standardisierte und dokumentierte Prozesse)"
    elif score < 4.5:
        lvl = 4
        desc = "CMMI Level 4 – Quantitatively Managed (kennzahlenbasiert gesteuert)"
    else:
        lvl = 5
        desc = "CMMI Level 5 – Optimizing (kontinuierliche Verbesserung, Innovation)"
    return lvl, desc


def recommendations_for_dimension(dim_name: str, score: float):
    """Grobe Handlungsempfehlungen je Dimension und Score-Range."""
    recs = []

    if dim_name == "Strategische Verankerung & Governance":
        if score < 2:
            recs = [
                "Formuliere ein klares Mandat für EAM (Sponsor auf CIO-/Vorstandsebene).",
                "Etabliere ein Architecture Board mit klaren Entscheidungsrechten.",
                "Definiere 5–7 verbindliche Architekturprinzipien (z.B. Cloud first, Standard vor Individuallösung).",
            ]
        elif score < 3.5:
            recs = [
                "Schärfe die Kopplung von EAM-Zielen an Business- und Digitalstrategie.",
                "Standardisiere Entscheidungsprozesse (Templates, Kriterien, Entscheidungspfade).",
                "Verankere Governance z.B. in Projektsteerings und Portfoliogremien.",
            ]
        else:
            recs = [
                "Baue KPI-basierte Steuerung von Architekturentscheidungen weiter aus.",
                "Nutze EAM aktiver als Sparringspartner bei strategischen Investitionen.",
                "Skaliere Governance auf Domänen/Business Units mit klaren Delegationsmodellen.",
            ]

    elif dim_name == "Methoden, Modelle & Referenzarchitekturen":
        if score < 2:
            recs = [
                "Starte mit einem schlanken EAM-Vorgehensmodell (Phasen, wesentliche Deliverables).",
                "Definiere eine erste ERP-/Integrationsreferenzarchitektur als Leitplanke.",
                "Erstelle eine Business Capability Map als zentrales Kommunikationsartefakt.",
            ]
        elif score < 3.5:
            recs = [
                "Standardisiere zentrale Artefakte (Vorlagen für Zielbilder, Solution Designs, Roadmaps).",
                "Verankere EAM-Artefakte verbindlich in Projektmethodik (z.B. Stage-Gate, Agile DoR/DoD).",
                "Pflege Referenzarchitekturen kontinuierlich und verknüpfe sie mit realen Systemen.",
            ]
        else:
            recs = [
                "Nutze Referenzarchitekturen aktiv für Sourcing-/Partnerauswahl.",
                "Etabliere Varianten (z.B. Multi-Region-ERP, Resilienz-Blueprints) und Szenarioplanung.",
                "Nutze AI, um Inkonsistenzen in Modellen und Architekturen zu identifizieren.",
            ]

    elif dim_name == "Tooling & Architektur-Repository":
        if score < 2:
            recs = [
                "Wähle ein zentrales EA-Tool oder initial ein strukturiertes Repository (z.B. CMDB-Erweiterung).",
                "Definiere ein Minimaldatenmodell (Anwendungen, Schnittstellen, Plattformen, Business Capabilities).",
                "Setze erste Importmechanismen (z.B. aus CMDB oder Cloud-Umgebungen).",
            ]
        elif score < 3.5:
            recs = [
                "Schärfe Datenpflegeprozesse mit klaren Ownern je Objekt-Typ.",
                "Automatisiere Datenimporte (CI/CD, Cloud-Discovery, CMDB).",
                "Baue Standard-Dashboards für Management und Projekte auf.",
            ]
        else:
            recs = [
                "Erweitere das Datenmodell um Risiko-, Kosten- und Resilienzparameter.",
                "Setze AI-gestützte Konsistenzprüfungen (z.B. Redundanzen, Schatten-IT).",
                "Nutze das Repository als Single Source für Impact-Analysen und Roadmaps.",
            ]

    elif dim_name == "EAM in Projekten & Lösungsarchitektur":
        if score < 2:
            recs = [
                "Definiere verbindliche Trigger, wann EAM involviert wird (Budget, Kritikalität, Domainschnitt).",
                "Etabliere mind. einen Architektur-Checkpoint pro Projekt (Early Architecture Review).",
                "Erstelle eine schlanke Solution-Design-Vorlage.",
            ]
        elif score < 3.5:
            recs = [
                "Verknüpfe Projektportfolioprozesse mit EAM (z.B. Business Case + Architekturzusage).",
                "Baue ein Community-of-Practice für Solution-Architekten auf.",
                "Stärke EAM als Sparringspartner statt reines Kontrollgremium.",
            ]
        else:
            recs = [
                "Verankere AI-Unterstützung in Projektarbeit (z.B. automatisierte Impact-Analysen).",
                "Nutze Lessons Learned, um Standard-Bausteine für neue Projekte abzuleiten.",
                "Führe KPIs für Architekturbeteiligung und -qualität in Projekten ein.",
            ]

    elif dim_name == "Datenbasis & AI-Unterstützung im EAM":
        if score < 2:
            recs = [
                "Identifiziere 2–3 Kern-Reports, die das Management wirklich braucht (z.B. ERP-Landschaft, Risiko-Hotspots).",
                "Verbessere Datenqualität im Repository (Vollständigkeit, Eindeutigkeit, Dubletten).",
                "Starte mit ersten Analysen in Excel/BI auf Basis der vorhandenen Architekturdaten.",
            ]
        elif score < 3.5:
            recs = [
                "Etabliere Standard-Dashboards (z.B. Tech-Debt, Cloud-Migrationsstatus, Redundanzen).",
                "Bewerte Architekturdaten explizit hinsichtlich AI-Fitness (Vollständigkeit, Struktur, Semantik).",
                "Teste einfache AI-Use-Cases (z.B. Clustering ähnlicher Anwendungen, Impact-Analysen).",
            ]
        else:
            recs = [
                "Implementiere AI-gestützte Empfehlungen (z.B. Konsolidierungsvorschläge, Risiko-Prognosen).",
                "Nutze Natural Language Interfaces, um Architekturdaten abzufragen (z.B. Chat über Landscape).",
                "Verbinde EAM-AI-Use-Cases mit anderen Analytics-/Data-Science-Initiativen.",
            ]

    elif dim_name == "Organisation, Rollen & Skills":
        if score < 2:
            recs = [
                "Definiere klare Rollen inkl. Mandat (Enterprise-, Domain-, Solution-Architekt:in).",
                "Benütze ein Operating Model (z.B. EAM als zentrale Funktion plus Domänenarchitekten).",
                "Bestimme erste Schlüsselpersonen und formiere ein Kernteam.",
            ]
        elif score < 3.5:
            recs = [
                "Erstelle einen Skill-Matrix und Trainingsplan für Architekt:innen.",
                "Etabliere regelmäßige Formate (Architektur-Community, Brown Bag Sessions).",
                "Schärfe die Zusammenarbeit mit Security, Data, Cloud und PMO/Portfolio.",
            ]
        else:
            recs = [
                "Positioniere Architekt:innen als Trusted Advisor im Business.",
                "Nutze Karrierepfade und Zertifizierungen zur Bindung von Architekt:innen.",
                "Baue ein aktives internes Architekturnetzwerk mit Mentoring-Strukturen auf.",
            ]

    elif dim_name == "Business Value & Steuerung":
        if score < 2:
            recs = [
                "Definiere 3–5 einfache KPIs, die EAM-Mehrwert sichtbar machen (z.B. Anzahl Technologien, System-Redundanzen).",
                "Verknüpfe erste Architekturentscheidungen mit Business-Effekten (z.B. Kosten, Time-to-Market, Resilienz).",
                "Kommuniziere konkrete EAM-Erfolge (z.B. vermiedene Risiken oder Doppelentwicklungen).",
            ]
        elif score < 3.5:
            recs = [
                "Etabliere ein KPI-Dashboard für das Management (z.B. Architekturkonformität, Tech-Debt-Trends).",
                "Nutze Roadmaps, um Business-Fähigkeiten und IT-Investitionen zu verbinden.",
                "Integriere EAM stärker in strategische Planungszyklen (Budget-/Portfolio-Runden).",
            ]
        else:
            recs = [
                "Verknüpfe EAM-KPIs mit Unternehmenskennzahlen (z.B. EBIT, NPS, Lieferfähigkeit).",
                "Nutze AI-gestützte Simulationen für Szenarien (z.B. Ausfall kritischer Systeme, Cloud-Migrationen).",
                "Skaliere EAM als Enabler für Transformationsprogramme (ERP 2.0, Data & AI, Platform-Strategie).",
            ]

    return recs


# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------
st.sidebar.title("EAM Maturity Assessment 🧱")
st.sidebar.markdown(
    """
Bewerte jede Aussage auf einer Skala von **1 bis 5**:

- **1**: trifft überhaupt nicht zu  
- **3**: teilweise / uneinheitlich  
- **5**: trifft voll zu, gelebte Praxis
"""
)

with st.sidebar.expander("Maturity-Skala (EA-spezifisch)"):
    st.markdown(
        """
- **EA Level 1** – Ad-hoc, personengetrieben  
- **EA Level 2** – Wiederholbar, erste Strukturen  
- **EA Level 3** – Definiert, standardisiert  
- **EA Level 4** – Gesteuert & gemessen  
- **EA Level 5** – Optimiert, wert- & datengetrieben
"""
    )

st.sidebar.subheader("Assessment-Infos")
assessment_name = st.sidebar.text_input("Name des Assessments", "Pilot EAM Assessment")
participant = st.sidebar.text_input("Teilnehmer / Bereich", "")

# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------
st.title("🧱 EAM Maturity Assessment – Prototyp")
st.markdown(
    """
Dieses Tool hilft dir, den **Reifegrad deines Enterprise Architecture Managements** 
strukturiert zu bewerten – inkl. **EA-Maturity-Level**, **CMMI-Vergleich** und 
konkreten **Handlungsvorschlägen** je Dimension.
"""
)

st.markdown("---")

# -------------------------------------------------------------------
# Formular
# -------------------------------------------------------------------
with st.form("eam_assessment_form"):
    st.markdown("### 1. Bewertung der Dimensionen")

    scores = {}
    detail_scores = []

    for dim in DIMENSIONS:
        st.markdown(f"#### {dim['name']}")
        st.caption(dim["description"])

        cols = st.columns(2)
        dim_values = []

        for i, question in enumerate(dim["questions"]):
            col = cols[i % 2]
            with col:
                value = st.slider(
                    f"{question}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"{dim['id']}_{i}",
                )
            dim_values.append(value)
            detail_scores.append(
                {
                    "Dimension": dim["name"],
                    "Frage": question,
                    "Bewertung": value,
                }
            )

        scores[dim["name"]] = dim_values
        st.markdown("")

    submitted = st.form_submit_button("🚀 Auswertung anzeigen")

# -------------------------------------------------------------------
# Auswertung
# -------------------------------------------------------------------
if not submitted:
    st.info("Bitte fülle das Assessment aus und klicke auf **„🚀 Auswertung anzeigen“**.")
else:
    # Durchschnitt je Dimension
    dim_results = {
        dim_name: sum(values) / len(values)
        for dim_name, values in scores.items()
    }

    overall_score = sum(dim_results.values()) / len(dim_results)
    overall_label = maturity_label(overall_score)
    cmmi_lvl, cmmi_desc = cmmi_level(overall_score)

    st.markdown("---")
    st.header("2. Ergebnisse")

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.subheader("Gesamt-Reifegrad")

        st.metric(
            label="Durchschnitt über alle Dimensionen (EA-Maturity)",
            value=f"{overall_score:.2f}",
        )

        st.markdown(f"**EA-Maturity-Level:** {overall_label}")
        st.progress(min(max(overall_score / 5, 0.0), 1.0))

        st.markdown("**CMMI-Einordnung (abgeleitet):**")
        st.markdown(f"- {cmmi_desc}")

        st.markdown(
            f"""
**Interpretation (High-Level):**

- Aus Sicht **Enterprise Architecture** liegst du bei: **{overall_label}**  
- Aus Sicht eines **CMMI Assessments** würdest du grob in **Level {cmmi_lvl}** fallen  
"""
        )

    with col_side:
        st.subheader("Meta-Infos")
        st.markdown(f"**Assessment:** {assessment_name}")
        if participant:
            st.markdown(f"**Teilnehmer / Bereich:** {participant}")
        st.markdown(f"**Anzahl Dimensionen:** {len(DIMENSIONS)}")
        st.markdown(f"**Fragen insgesamt:** {len(detail_scores)}")

    # -------------------------------------------------------------------
    # Visualisierung: Radar / Spider Chart
    # -------------------------------------------------------------------
    st.markdown("### 3. Profil je Dimension")

    dim_df = pd.DataFrame(
        {
            "Dimension": list(dim_results.keys()),
            "Score": list(dim_results.values()),
        }
    )

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("**Balken-Chart (Scores je Dimension)**")
        st.bar_chart(dim_df.set_index("Dimension"))

    with col_chart2:
        st.markdown("**Radar-Chart (EA-Profil)**")
        fig = px.line_polar(
            dim_df,
            r="Score",
            theta="Dimension",
            line_close=True,
            range_r=[0, 5],
        )
        fig.update_traces(fill="toself")
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------------
    # Detailtabelle & Export
    # -------------------------------------------------------------------
    st.markdown("### 4. Detailergebnisse & Export")

    detail_df = pd.DataFrame(detail_scores)
    st.dataframe(detail_df, use_container_width=True)

    csv = detail_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Ergebnisse als CSV herunterladen",
        data=csv,
        file_name="eam_maturity_results.csv",
        mime="text/csv",
    )

    # -------------------------------------------------------------------
    # Handlungsvorschläge je Dimension
    # -------------------------------------------------------------------
    st.markdown("### 5. Handlungsvorschläge je Dimension")

    for dim in DIMENSIONS:
        dim_name = dim["name"]
        score = dim_results[dim_name]
        recs = recommendations_for_dimension(dim_name, score)

        with st.expander(f"{dim_name} – Score: {score:.2f}"):
            st.markdown(f"**Aktueller Reifegrad (EA-Sicht):** {score:.2f}")
            lvl_txt = maturity_label(score)
            st.markdown(f"**Interpretation:** {lvl_txt}")

            cmmi_dim_lvl, cmmi_dim_desc = cmmi_level(score)
            st.markdown(f"**CMMI-Näherung:** {cmmi_dim_desc}")

            if recs:
                st.markdown("**Konkrete nächste Schritte (Vorschlag):**")
                for r in recs:
                    st.markdown(f"- {r}")
            else:
                st.markdown(
                    "Aktuell liegen hier bereits sehr gute Werte vor – Fokus auf Feintuning und kontinuierliche Verbesserung."
                )

    # -------------------------------------------------------------------
    # Gesamt-Next Steps
    # -------------------------------------------------------------------
    st.markdown("### 6. Gesamtbewertung & Next Steps")

    if overall_score < 2:
        st.warning(
            "Dein EAM befindet sich in einem **frühen Aufbauzustand (EA Level 1–2)**. "
            "Fokus: Grundlagen legen – Mandat, Rollen, einfaches Vorgehensmodell und ein erstes Repository aufbauen."
        )
    elif overall_score < 3.5:
        st.info(
            "Dein EAM ist **solide im Aufbau (EA Level 2–3)**. "
            "Fokus: Standardisierung, verbindliche Governance, bessere Integration in Projekte und erste KPI-Steuerung."
        )
    else:
        st.success(
            "Dein EAM ist bereits **weit entwickelt (EA Level 3–5)**. "
            "Fokus: Kennzahlenbasierte Steuerung, AI-gestützte Analysen, Business Value kontinuierlich sichtbar machen."
        )

    st.markdown(
        """
**Typischer 3-Schritte-Plan:**

1. **Transparenz & Datenbasis**  
   Landscape, kritische Systeme, Projekte und Roadmaps im Repository konsolidieren, Datenqualität erhöhen.

2. **Governance & Integration**  
   EAM verbindlich in Portfolio- und Projektprozesse einbinden, Architektur-Checkpoints und Referenzarchitekturen nutzen.

3. **AI & Value**  
   Architekturdaten für Auswertungen, Szenarien und AI-Use-Cases nutzen (Impact-Analysen, Konsolidierungsvorschläge, Risiko-Hotspots).
"""
    )
