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
# Labels & Config
# -------------------------------------------------------------------
LABELS = {
    1: "1 – Ad-hoc / Chaotisch",
    2: "2 – Basic / Wiederholbar",
    3: "3 – Definiert",
    4: "4 – Gesteuert / Gemessen",
    5: "5 – Optimiert / Wertgetrieben",
}

BUSINESS_GOALS = [
    "Kostenreduktion / Effizienz",
    "Resilienz & Betriebssicherheit",
    "Time-to-Market / Veränderungsgeschwindigkeit",
    "Regulatorik & Compliance",
    "Data & AI Enablement",
    "Standardisierung & Komplexitätsreduktion",
]

PAIN_POINTS = [
    "Keine Transparenz über Applikationslandschaft",
    "Schatten-IT & ungeplante Lösungen",
    "Komplexe & fragile ERP-Landschaft",
    "Fehlende Steuerbarkeit von Transformationen",
    "Zu viele Technologien / Varianten",
    "EAM wird als Bremse wahrgenommen",
]

TIME_HORIZONS = [
    "0–6 Monate",
    "6–12 Monate",
    "12–24 Monate",
]

# -------------------------------------------------------------------
# Dimensionen inkl. Fragen
# -------------------------------------------------------------------
DIMENSIONS = [
    {
        "id": "strategy",
        "name": "Strategische Verankerung & Governance",
        "description": "Wie stark ist EAM in Strategie, Entscheidungsprozessen und Governance verankert?",
        "questions": [
            "Es gibt ein klares, schriftlich fixiertes Mandat für EAM (z.B. vom CIO/Board).",
            "EAM-Ziele sind explizit mit der Unternehmensstrategie verknüpft.",
            "Architekturentscheidungen werden in festen Gremien getroffen (Architecture Board, Governance-Runden).",
            "EAM-Prinzipien (z.B. Cloud first, Clean Core, Standardisierung) sind definiert und werden angewendet.",
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
            "EAM-Vorgaben sind in Projektstandards (Templates, Checklisten, Qualitätsschranken) verankert.",
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
            "Architekturdaten werden regelmäßig aktualisiert (definierte Owner & Prozesse).",
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
            "Es gibt klare Kriterien, wann Projekte EAM involvieren müssen (z.B. Budget, Kritikalität, Domäne).",
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
            "Die Datenqualität im EA-Repository ist ausreichend, um sinnvolle AI-Use-Cases zu ermöglichen.",
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
            "Es existiert ein Skill- und Entwicklungsplan für Architekt:innen (Methodik, Cloud, Security, Data, AI).",
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
            "Business-Vertreter sehen EAM überwiegend als Enabler, nicht als Bremse.",
        ],
    },
    {
        "id": "erp_core",
        "name": "ERP & Core Plattformen / Resilienz",
        "description": "Wie robust, zukunftssicher und steuerbar sind ERP- und Core-Plattform-Architekturen?",
        "questions": [
            "Es existiert ein klares Zielbild für ERP / Core Plattformen (z.B. ERP 2.0, Cloud-MFRD, Clean Core).",
            "Resilienzanforderungen (z.B. Multi-Region, Failover, Kriegsfall-Tauglichkeit) sind in der Architektur umgesetzt.",
            "Schnittstellen- und Integrationsarchitekturen (API, Event-Driven Architecture) sind definiert und dokumentiert.",
            "Master Data Management und Datenhoheit (Data Supremacy) sind über ERP- und Kernsysteme hinweg geregelt.",
        ],
    },
]

CORE_DIM_IDS = ["strategy", "method", "tooling", "projects", "org_skills", "value"]
DATA_ERP_DIM_IDS = ["data_ai", "erp_core"]

# -------------------------------------------------------------------
# Helper Functions
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


def traffic_light(score: float) -> str:
    if score < 2.5:
        return "🔴"
    elif score < 3.5:
        return "🟡"
    else:
        return "🟢"


def recommendations_for_dimension(dim_name: str, score: float):
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
                "Verankere Governance in Projektsteerings und Portfoliogremien.",
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
                "Standardisiere zentrale Artefakte (Zielbilder, Solution Designs, Roadmaps).",
                "Verankere EAM-Artefakte verbindlich in der Projektmethodik.",
                "Pflege Referenzarchitekturen kontinuierlich und verknüpfe sie mit realen Systemen.",
            ]
        else:
            recs = [
                "Nutze Referenzarchitekturen aktiv für Sourcing- und Partnerauswahl.",
                "Etabliere Varianten (z.B. Multi-Region-ERP, Resilienz-Blueprints) und Szenarioplanung.",
                "Nutze AI, um Inkonsistenzen in Modellen und Architekturen zu identifizieren.",
            ]

    elif dim_name == "Tooling & Architektur-Repository":
        if score < 2:
            recs = [
                "Wähle ein zentrales EA-Tool oder initial ein strukturiertes Repository.",
                "Definiere ein Minimaldatenmodell (Applikationen, Schnittstellen, Plattformen, Business Capabilities).",
                "Setze erste Importmechanismen aus CMDB oder Cloud-Umgebungen um.",
            ]
        elif score < 3.5:
            recs = [
                "Schärfe Datenpflegeprozesse mit klaren Ownern je Objekttyp.",
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
                "Definiere Trigger, wann EAM involviert wird (Budget, Kritikalität, Domainschnitt).",
                "Etabliere mindestens einen Architektur-Checkpoint pro Projekt.",
                "Erstelle eine schlanke Solution-Design-Vorlage.",
            ]
        elif score < 3.5:
            recs = [
                "Verknüpfe Projektportfolioprozesse mit EAM.",
                "Baue ein Community-of-Practice für Solution-Architekten auf.",
                "Stärke EAM als Sparringspartner statt reines Kontrollgremium.",
            ]
        else:
            recs = [
                "Verankere AI-Unterstützung in Projektarbeit (z.B. Impact-Analysen).",
                "Nutze Lessons Learned, um Standard-Bausteine für neue Projekte abzuleiten.",
                "Führe KPIs für Architekturbeteiligung und -qualität in Projekten ein.",
            ]

    elif dim_name == "Datenbasis & AI-Unterstützung im EAM":
        if score < 2:
            recs = [
                "Identifiziere 2–3 Kern-Reports, die das Management wirklich braucht.",
                "Verbessere Datenqualität im Repository (Vollständigkeit, Dubletten).",
                "Starte mit ersten Analysen in BI-Tools auf Basis vorhandener Architekturdaten.",
            ]
        elif score < 3.5:
            recs = [
                "Etabliere Standard-Dashboards (Tech-Debt, Cloud-Migration, Redundanzen).",
                "Bewerte Architekturdaten explizit hinsichtlich AI-Fitness.",
                "Teste einfache AI-Use-Cases (Clustering, Impact-Analysen).",
            ]
        else:
            recs = [
                "Implementiere AI-gestützte Empfehlungen (Konsolidierung, Risiko-Prognosen).",
                "Nutze Natural-Language-Interfaces für Architekturdaten.",
                "Verbinde EAM-AI-Use-Cases mit anderen Analytics-/Data-Science-Initiativen.",
            ]

    elif dim_name == "Organisation, Rollen & Skills":
        if score < 2:
            recs = [
                "Definiere klare Rollen inkl. Mandat (Enterprise-, Domain-, Solution-Architekt:in).",
                "Skizziere ein EAM-Operating-Model (zentral plus Domänenarchitekten).",
                "Identifiziere Schlüsselpersonen und formiere ein Kernteam.",
            ]
        elif score < 3.5:
            recs = [
                "Erstelle eine Skill-Matrix und einen Trainingsplan.",
                "Etabliere regelmäßige Architektur-Formate (Community, Brown Bags).",
                "Schärfe die Zusammenarbeit mit Security, Data, Cloud und PMO.",
            ]
        else:
            recs = [
                "Positioniere Architekt:innen als Trusted Advisor im Business.",
                "Nutze Karrierepfade und Zertifizierungen zur Bindung.",
                "Baue ein aktives internes Architekturnetzwerk mit Mentoring auf.",
            ]

    elif dim_name == "Business Value & Steuerung":
        if score < 2:
            recs = [
                "Definiere 3–5 KPIs, die EAM-Mehrwert sichtbar machen.",
                "Verknüpfe Architekturentscheidungen mit Business-Effekten (Kosten, Risiken, Time-to-Market).",
                "Kommuniziere konkrete EAM-Erfolge an Management und Fachbereiche.",
            ]
        elif score < 3.5:
            recs = [
                "Etabliere ein KPI-Dashboard für das Management.",
                "Nutze Roadmaps, um Business-Fähigkeiten und IT-Investitionen zu verbinden.",
                "Integriere EAM stärker in strategische Planungszyklen.",
            ]
        else:
            recs = [
                "Verknüpfe EAM-KPIs mit Unternehmenskennzahlen (EBIT, NPS, Lieferfähigkeit).",
                "Nutze AI-gestützte Szenario-Simulationen.",
                "Skaliere EAM als Enabler für Transformationsprogramme.",
            ]

    elif dim_name == "ERP & Core Plattformen / Resilienz":
        if score < 2:
            recs = [
                "Erstelle ein klares Zielbild für ERP & Core Plattformen (z.B. ERP 2.0, Cloud-Strategie, Clean Core).",
                "Identifiziere kritische Prozesse und Systeme mit hohen Resilienzanforderungen.",
                "Definiere eine erste Multi-Region-/Resilienzarchitektur (z.B. MFRD-Blueprint).",
            ]
        elif score < 3.5:
            recs = [
                "Verankere Resilienzanforderungen (RTO/RPO, Kriegsfall-Szenarien) explizit in der Architektur.",
                "Stärke Event- und API-Architektur für lose Kopplung und Wiederanlauffähigkeit.",
                "Setze Master Data Governance über ERP- und Kernsysteme hinweg auf.",
            ]
        else:
            recs = [
                "Nutze Szenarioplanung für Ausfall-/Krisenszenarien (inkl. Übungen & Tests).",
                "Automatisiere Failover-Tests und Recovery-Playbooks.",
                "Nutze Architekturdaten, um Resilienz-Investitionen gezielt zu priorisieren.",
            ]

    return recs


def determine_archetype(overall_score, dim_results, pains, goals):
    """Einfaches Heuristik-Modell für Archetypen."""
    d = dim_results
    name = "Emerging EA Engine"
    desc = (
        "Ihr EAM befindet sich in einem wachstumsfähigen Zustand mit soliden Grundlagen. "
        "Die nächsten Schritte liegen in Standardisierung, besserer Projektintegration und klarer Wertkommunikation."
    )

    # Helper get score safely
    def s(dim_name, default=0):
        return d.get(dim_name, default)

    # Archetype 1: Firefighters
    if overall_score < 2.3 or "Komplexe & fragile ERP-Landschaft" in pains:
        name = "Architecture Firefighters"
        desc = (
            "Euer EAM agiert aktuell stark reaktiv: Es müssen laufend Brände gelöscht werden "
            "(Störungen, ungeplante Projekte, fragile ERP-Landschaft). Fokus: Transparenz schaffen, "
            "kritische Systeme absichern und ein minimales Governance-Framework etablieren."
        )
        return name, desc

    # Archetype 2: Method-heavy, low adoption
    if s("Methoden, Modelle & Referenzarchitekturen") >= 3.2 and s("EAM in Projekten & Lösungsarchitektur") < 3:
        name = "Methoden-stark, aber nicht gelebt"
        desc = (
            "Auf der methodischen Ebene seid ihr bereits gut aufgestellt (Modelle, Referenzarchitekturen, Vorgehen). "
            "Die Schwäche liegt in der Umsetzung: In Projekten und im Alltag werden diese Standards noch nicht "
            "konsequent genutzt. Fokus: Projektintegration, Kommunikation, Nutzenstory."
        )
        return name, desc

    # Archetype 3: Data-rich, low mandate
    if s("Tooling & Architektur-Repository") >= 3.2 and s("Strategische Verankerung & Governance") < 3:
        name = "Data-rich, low mandate"
        desc = (
            "Ihr verfügt bereits über gute Daten, Tools und teilweise auch Dashboards. "
            "Was fehlt, ist ein starkes Mandat und strategische Verankerung, damit diese Informationen "
            "auch wirksam in Entscheidungen einfließen."
        )
        return name, desc

    # Archetype 4: Value-focused transformer
    if s("Business Value & Steuerung") >= 3.5 and "Time-to-Market / Veränderungsgeschwindigkeit" in goals:
        name = "Value-driven Transformer"
        desc = (
            "Euer EAM ist stark auf Business Value ausgerichtet und gut an Transformationsthemen angebunden. "
            "Der Fokus liegt jetzt auf Skalierung – insbesondere über daten- und AI-getriebene Steuerung "
            "und stärkere Einbindung der Fachbereiche."
        )
        return name, desc

    # Archetype 5: Data & AI Ready (wenn Data/AI deutlich stärker)
    if s("Datenbasis & AI-Unterstützung im EAM") - overall_score >= 0.5:
        name = "Data & AI Ready, aber unterspannt"
        desc = (
            "Ihr habt bereits eine gute Datenbasis und erste Erfahrungen im Bereich Analytics/AI. "
            "Der nächste Schritt ist, diese Fähigkeiten stärker mit strategischer Steuerung und Governance "
            "zu verknüpfen, um Entscheidungen systematisch zu verbessern."
        )
        return name, desc

    return name, desc


def build_executive_summary(
    overall_score,
    overall_label,
    cmmi_lvl,
    dim_results,
    goals,
    pains,
    time_horizon,
):
    # Top 3 Stärken / Schwächen
    sorted_dims = sorted(dim_results.items(), key=lambda x: x[1], reverse=True)
    top3 = [f"{name} (Score {score:.2f})" for name, score in sorted_dims[:3]]
    bottom3 = [f"{name} (Score {score:.2f})" for name, score in sorted_dims[-3:]]

    goals_txt = ", ".join(goals) if goals else "noch nicht explizit priorisiert"
    pains_txt = ", ".join(pains) if pains else "nicht explizit angegeben"

    summary = f"""
Executive Summary – EAM Maturity Assessment
===========================================

Im aktuellen Assessment erreicht Ihre Organisation einen durchschnittlichen
**EAM-Reifegrad von {overall_score:.2f} – {overall_label}**.
Dies entspricht grob einem **CMMI-Level von {cmmi_lvl}**.

**Zentrale Geschäftsziele für EAM** (laut Assessment):
- {goals_txt}

**Aktuell wahrgenommene Pain Points**:
- {pains_txt}

**Stärkste Bereiche im EAM (Top 3):**
- {top3[0] if len(top3) > 0 else "-"}
- {top3[1] if len(top3) > 1 else "-"}
- {top3[2] if len(top3) > 2 else "-"}

**Größte Entwicklungsfelder (Bottom 3):**
- {bottom3[0] if len(bottom3) > 0 else "-"}
- {bottom3[1] if len(bottom3) > 1 else "-"}
- {bottom3[2] if len(bottom3) > 2 else "-"}

**Zeithorizont für Zielbild / Ambition:** {time_horizon}

Aus den Ergebnissen ergeben sich drei priorisierte Handlungsfelder:

1. **Transparenz & Datenbasis stärken**  
   Konsolidierung und Qualitätssteigerung der Architekturdaten (insb. kritische Systeme,
   ERP-Landschaft, Schnittstellen, Plattformen).

2. **Governance & Projektintegration schärfen**  
   Verbindliche Entscheidungspunkte, frühere Einbindung von EAM in Projekte und
   klare Architekturleitlinien für Vorhaben.

3. **Business Value & AI nutzen**  
   Daten- und AI-gestützte Analysen, um Investitionen, Risiken und Roadmaps
   fundierter und schneller zu steuern.

Die detaillierten Handlungsempfehlungen je Dimension finden Sie in den nachfolgenden Abschnitten.
"""
    return summary


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

# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------
st.title("🧱 EAM Maturity Assessment – Prototyp")
st.markdown(
    """
Dieses Tool hilft dir, den **Reifegrad deines Enterprise Architecture Managements** 
strukturiert zu bewerten – inkl. **EA-Maturity-Level**, **CMMI-Vergleich**, 
**Gap-Analyse (Ist vs. Ziel)** und konkreten **Handlungsvorschlägen**.
"""
)

st.markdown("---")

# -------------------------------------------------------------------
# Form: Wir sammeln alles in einem Multi-Tab-Formular
# -------------------------------------------------------------------
scores = {}
detail_scores = []
target_scores = {}

with st.form("eam_assessment_form"):
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "1️⃣ Kontext & Ziele",
            "2️⃣ EAM-Kerndimensionen",
            "3️⃣ Data, AI & ERP",
            "4️⃣ Review & Submit",
        ]
    )

    # ------------------ TAB 1: Kontext & Ziele ----------------------
    with tab1:
        st.subheader("Kontext & Ziele")
        st.markdown(
            """
Gib bitte ein paar Rahmendaten an – das hilft bei der Interpretation und der Ableitung
von Maßnahmen.
"""
        )

        assessment_name = st.text_input("Name des Assessments", "Pilot EAM Assessment")
        participant = st.text_input("Teilnehmer / Bereich", "")

        goals = st.multiselect(
            "Welche Ziele verfolgt ihr primär mit EAM?",
            BUSINESS_GOALS,
        )

        pains = st.multiselect(
            "Wo tut es heute am meisten weh?",
            PAIN_POINTS,
        )

        time_horizon = st.selectbox(
            "Zeithorizont für das gewünschte Zielbild",
            TIME_HORIZONS,
            index=1,
        )

        st.info(
            "Hinweis: Die Ziele und Pain Points werden später in der Executive Summary und den Handlungsempfehlungen genutzt."
        )

    # ------------------ TAB 2: Kern-Dimensionen ---------------------
    with tab2:
        st.subheader("EAM-Kerndimensionen")
        st.markdown(
            "Bewerte die folgenden Dimensionen. Nach den Fragen kannst du einen **Ziel-Reifegrad** für die nächsten 12–18 Monate angeben."
        )

        for dim in [d for d in DIMENSIONS if d["id"] in CORE_DIM_IDS]:
            st.markdown(f"#### {dim['name']}")
            st.caption(dim["description"])

            cols = st.columns(2)
            dim_values = []

            for i, question in enumerate(dim["questions"]):
                col = cols[i % 2]
                with col:
                    value = st.slider(
                        question,
                        min_value=1,
                        max_value=5,
                        value=3,
                        step=1,
                        format="%d",
                        key=f"{dim['id']}_{i}",
                        help="1 = ad-hoc, 3 = teilweise etabliert, 5 = gelebter Standard",
                    )
                    st.caption(f"Aktuelle Auswahl: **{LABELS[value]}**")
                dim_values.append(value)
                detail_scores.append(
                    {
                        "Dimension": dim["name"],
                        "Frage": question,
                        "Bewertung": value,
                    }
                )

            scores[dim["name"]] = dim_values

            target = st.slider(
                "Ziel-Reifegrad in 12–18 Monaten (EA-Sicht)",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                key=f"{dim['id']}_target",
            )
            st.caption(f"Ziel: **{LABELS[target]}**")
            target_scores[dim["name"]] = target

            st.markdown("")

    # ------------------ TAB 3: Data, AI & ERP -----------------------
    with tab3:
        st.subheader("Daten, AI & ERP / Core Plattformen")
        st.markdown(
            "Hier betrachten wir den datengetriebenen Teil des EAM sowie ERP & Core Plattformen mit Fokus auf Resilienz."
        )

        for dim in [d for d in DIMENSIONS if d["id"] in DATA_ERP_DIM_IDS]:
            st.markdown(f"#### {dim['name']}")
            st.caption(dim["description"])

            cols = st.columns(2)
            dim_values = []

            for i, question in enumerate(dim["questions"]):
                col = cols[i % 2]
                with col:
                    value = st.slider(
                        question,
                        min_value=1,
                        max_value=5,
                        value=3,
                        step=1,
                        format="%d",
                        key=f"{dim['id']}_{i}",
                        help="1 = ad-hoc, 3 = teilweise etabliert, 5 = gelebter Standard",
                    )
                    st.caption(f"Aktuelle Auswahl: **{LABELS[value]}**")
                dim_values.append(value)
                detail_scores.append(
                    {
                        "Dimension": dim["name"],
                        "Frage": question,
                        "Bewertung": value,
                    }
                )

            scores[dim["name"]] = dim_values

            target = st.slider(
                "Ziel-Reifegrad in 12–18 Monaten (EA-Sicht)",
                min_value=1,
                max_value=5,
                value=4,
                step=1,
                key=f"{dim['id']}_target",
            )
            st.caption(f"Ziel: **{LABELS[target]}**")
            target_scores[dim["name"]] = target

            st.markdown("")

    # ------------------ TAB 4: Review & Submit ----------------------
    with tab4:
        st.subheader("Review & Submit")
        st.markdown(
            """
Wenn du alle Fragen beantwortet hast, klicke auf **„🚀 Auswertung anzeigen“**.
Anschließend erhältst du:

- Gesamt-Reifegrad (EA-Maturity) und CMMI-Einordnung  
- Profil je Dimension inkl. Gap (Ist vs. Ziel)  
- Top 3 Stärken und Schwächen  
- Archetyp eures EAM-Setups  
- Executive Summary zur direkten Verwendung in Slides / Dokus  
- Roadmap (0–90 Tage, 6–12 Monate) und Workshop-Vorschlag
"""
        )

    submitted = st.form_submit_button("🚀 Auswertung anzeigen")

# -------------------------------------------------------------------
# Auswertung
# -------------------------------------------------------------------
if not submitted:
    st.info("Bitte fülle das Assessment aus und klicke auf **„🚀 Auswertung anzeigen“**.")
else:
    # Durchschnitt je Dimension (Ist)
    dim_results = {
        dim_name: sum(values) / len(values)
        for dim_name, values in scores.items()
    }

    overall_score = sum(dim_results.values()) / len(dim_results)
    overall_label = maturity_label(overall_score)
    cmmi_lvl, cmmi_desc = cmmi_level(overall_score)

    # Gap-Analyse: Ziel - Ist
    dim_gaps = {
        dim_name: target_scores.get(dim_name, 0) - dim_results.get(dim_name, 0)
        for dim_name in dim_results.keys()
    }

    st.markdown("---")
    st.header("2. Ergebnisse & Einordnung")

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

    with col_side:
        st.subheader("Meta-Infos")
        st.markdown(f"**Assessment:** {assessment_name}")
        if participant:
            st.markdown(f"**Teilnehmer / Bereich:** {participant}")
        st.markdown(f"**Anzahl Dimensionen:** {len(dim_results)}")
        st.markdown(f"**Zeithorizont Zielbild:** {time_horizon}")

    st.markdown("")

    # -------------------------------------------------------------------
    # Profil je Dimension
    # -------------------------------------------------------------------
    st.markdown("### 3. Profil & Gap-Analyse je Dimension")

    dim_df = pd.DataFrame(
        {
            "Dimension": list(dim_results.keys()),
            "Ist": list(dim_results.values()),
            "Ziel": [target_scores.get(d, None) for d in dim_results.keys()],
        }
    )
    dim_df["Gap (Ziel - Ist)"] = dim_df["Ziel"] - dim_df["Ist"]
    dim_df["Ampel"] = dim_df["Ist"].apply(traffic_light)

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("**Balken-Chart – Ist vs. Ziel je Dimension**")
        chart_df = dim_df.set_index("Dimension")[["Ist", "Ziel"]]
        st.bar_chart(chart_df)

    with col_chart2:
        st.markdown("**Radar-Chart – EA-Profil (Ist)**")
        radar_df = pd.DataFrame(
            {"Dimension": list(dim_results.keys()), "Score": list(dim_results.values())}
        )
        fig = px.line_polar(
            radar_df,
            r="Score",
            theta="Dimension",
            line_close=True,
            range_r=[0, 5],
        )
        fig.update_traces(fill="toself")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Detailtabelle (mit Ampel & Gap):**")
    st.dataframe(dim_df, use_container_width=True)

    # -------------------------------------------------------------------
    # Stärken / Schwächen & Archetyp
    # -------------------------------------------------------------------
    st.markdown("### 4. Stärken, Schwächen & Archetyp")

    sorted_dims = sorted(dim_results.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_dims[:3]
    bottom3 = sorted_dims[-3:]

    col_strengths, col_weaknesses = st.columns(2)

    with col_strengths:
        st.markdown("**Top 3 Stärken:**")
        for name, score in top3:
            st.markdown(f"- {traffic_light(score)} {name}: **{score:.2f}**")

    with col_weaknesses:
        st.markdown("**Top 3 Schwächen / Entwicklungsfelder:**")
        for name, score in bottom3:
            st.markdown(f"- {traffic_light(score)} {name}: **{score:.2f}**")

    archetype_name, archetype_desc = determine_archetype(
        overall_score, dim_results, pains, goals
    )

    st.markdown("**EAM-Archetyp (Heuristik):**")
    st.markdown(f"- **{archetype_name}**")
    st.markdown(f"{archetype_desc}")

    # -------------------------------------------------------------------
    # Detailergebnisse & Export
    # -------------------------------------------------------------------
    st.markdown("### 5. Detailergebnisse & Export")

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
    # Executive Summary
    # -------------------------------------------------------------------
    st.markdown("### 6. Executive Summary (auto-generiert)")

    exec_summary = build_executive_summary(
        overall_score,
        overall_label,
        cmmi_lvl,
        dim_results,
        goals,
        pains,
        time_horizon,
    )
    st.markdown(exec_summary)

    st.download_button(
        label="📄 Executive Summary als Text herunterladen",
        data=exec_summary.encode("utf-8"),
        file_name="eam_executive_summary.txt",
        mime="text/plain",
    )

    # -------------------------------------------------------------------
    # Handlungsvorschläge je Dimension
    # -------------------------------------------------------------------
    st.markdown("### 7. Handlungsvorschläge je Dimension")

    for dim in DIMENSIONS:
        dim_name = dim["name"]
        if dim_name not in dim_results:
            continue
        score = dim_results[dim_name]
        recs = recommendations_for_dimension(dim_name, score)

        with st.expander(f"{dim_name} – Score: {score:.2f} {traffic_light(score)}"):
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
    # Gesamt-Roadmap
    # -------------------------------------------------------------------
    st.markdown("### 8. Gesamtbewertung & Roadmap")

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

    st.markdown("#### Phase 1 – 0–90 Tage (Quick Wins & Foundation)")

    phase1_points = [
        "EAM-Mandat formal bestätigen und intern kommunizieren.",
        "Minimal-Operating-Model definieren (Rollen, Gremien, Kernartefakte).",
        "Architektur-Repository mit Kernobjekten befüllen (ERP, kritische Systeme, Hauptschnittstellen).",
        "1–2 Referenzarchitekturen definieren (z.B. ERP Cloud Target, Integrations-Blueprint).",
        "1–2 Standard-Reports für Management bereitstellen (z.B. ERP-Landschaft, Risiko-Hotspots).",
    ]

    if "Data & AI Enablement" in goals:
        phase1_points.append(
            "Architekturdaten im Hinblick auf AI-Fitness sichten (Struktur, Vollständigkeit, Semantik)."
        )

    for p in phase1_points:
        st.markdown(f"- {p}")

    st.markdown("#### Phase 2 – 6–12 Monate (Scaling & AI-Enablement)")

    phase2_points = [
        "EAM fest in Portfolio- und Projektprozesse integrieren (Checkpoints, Quality Gates).",
        "Datenqualität im Repository systematisch verbessern (Owner, Prozesse, Automatisierung).",
        "KPI-Set für EAM definieren (z.B. Standardisierung, Tech-Debt, Redundanzen, Risikoindikatoren).",
        "EAM-Roadmap erstellen (ERP 2.0, Resilienz, Data & AI, Security/Zero Trust).",
    ]

    if "Resilienz & Betriebssicherheit" in goals:
        phase2_points.append(
            "Resilienz-Blueprints (Multi-Region, Failover, Kriegsfall-Szenarien) definieren und testen."
        )
    if "Data & AI Enablement" in goals:
        phase2_points.append(
            "Erste AI-Use-Cases im EAM umsetzen (Impact-Analysen, Konsolidierungsvorschläge, Risiko-Hotspots)."
        )

    for p in phase2_points:
        st.markdown(f"- {p}")

    # -------------------------------------------------------------------
    # Workshop-Vorschlag
    # -------------------------------------------------------------------
    st.markdown("### 9. Empfohlenes Workshop-Format")

    st.markdown(
        """
**Vorschlag: EAM Maturity Workshop (2–3 Stunden)**  

1. **Kick-off & Zielsetzung (15 min)**  
   - Warum schauen wir auf EAM-Maturity?  
   - Welche Entscheidungen sollen dadurch vorbereitet werden?  

2. **Review der Assessment-Ergebnisse (30–45 min)**  
   - Vorstellung Gesamt-Score, Profil je Dimension  
   - Diskussion: Überraschungen, Aha-Momente  

3. **Fokusthemen identifizieren (30 min)**  
   - Top 3 Handlungsfelder wählen (per Voting)  
   - Tiefer eintauchen: Beispiele, konkrete Pain Points  

4. **Zielbild & Ambitionsniveau (30 min)**  
   - Wo wollen wir in 12–18 Monaten stehen?  
   - Ziel-Reifegrade je Dimension grob festlegen  

5. **Maßnahmen & Roadmap (30–45 min)**  
   - Quick Wins vs. strukturelle Maßnahmen  
   - Verantwortlichkeiten und nächste Schritte klären  
"""
    )
