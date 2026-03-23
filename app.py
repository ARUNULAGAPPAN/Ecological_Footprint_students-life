import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import html
import re

st.set_page_config(page_title="Gryfindors | Eco-Footprint", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    :root {
        --primary: #7C3AED;
        --primary-dark: #5B21B6;
        --primary-soft: #EDE9FE;
        --bg-1: #C4B5FD;
        --bg-2: #DDD6FE;
        --bg-3: #F5F3FF;
        --surface: #FFFFFF;
        --text-main: #111827;
        --text-muted: #4B5563;
        --border: #D1D5DB;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main) !important;
    }

    .stApp {
        background: linear-gradient(160deg, var(--bg-1) 0%, var(--bg-2) 35%, var(--bg-3) 75%, #FFFFFF 100%);
    }

    p, span, div, label, .stMarkdown, .stMarkdown * {
        color: var(--text-main);
    }

    /* Headings */
    h1, h2, h3 {
        color: var(--text-main) !important;
        font-weight: 800 !important;
    }

    h1 {
        letter-spacing: -0.02em;
    }

    /* Modern Card UI */
    .metric-card {
        background: var(--surface);
        color: var(--text-main);
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid var(--primary);
        border: 1px solid var(--border);
        box-shadow: 0 10px 24px rgba(17, 24, 39, 0.08);
        margin-bottom: 20px;
        text-align: center;
    }

    .metric-card h4 { color: var(--text-muted) !important; margin-bottom: 8px; font-size: 0.84rem; text-transform: uppercase; }
    .metric-card h2 { color: var(--text-main) !important; margin: 0; font-size: 2rem; }

    .tip-card {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px 16px;
        box-shadow: 0 8px 16px rgba(17, 24, 39, 0.06);
        margin-top: 10px;
    }

    .tip-title {
        color: var(--primary-dark) !important;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .college-kpi-card {
        background: #FFFFFF;
        border: 2px solid #A78BFA;
        border-left: 8px solid var(--primary);
        border-radius: 14px;
        padding: 24px 18px;
        box-shadow: 0 10px 24px rgba(109, 40, 217, 0.12);
        text-align: center;
        margin-bottom: 12px;
    }

    .college-kpi-card h4 {
        margin: 0 0 10px 0;
        color: #4C1D95 !important;
        font-size: 0.88rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        font-weight: 700;
    }

    .college-kpi-card h2 {
        margin: 0;
        color: #111827 !important;
        font-size: 2rem;
        font-weight: 800;
    }

    .recommendation-list {
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px 14px;
    }

    .recommendation-list li {
        color: #111827 !important;
        margin: 8px 0;
    }

    .leaderboard-wrap {
        background: #FFFFFF;
        border: 1px solid #C4B5FD;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 8px 18px rgba(109, 40, 217, 0.12);
    }

    .leaderboard-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
    }

    .leaderboard-table thead th {
        background: #6D28D9;
        color: #FFFFFF !important;
        text-align: left;
        padding: 12px 14px;
        font-weight: 700;
    }

    .leaderboard-table tbody td {
        color: #111827 !important;
        padding: 11px 14px;
        border-top: 1px solid #EDE9FE;
    }

    .leaderboard-table tbody tr:nth-child(odd) {
        background: #FAF5FF;
    }

    .leaderboard-table tbody tr:nth-child(even) {
        background: #FFFFFF;
    }

    .score-pill {
        background: #EDE9FE;
        color: #5B21B6 !important;
        padding: 4px 10px;
        border-radius: 999px;
        font-weight: 700;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary)) !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100%;
        box-shadow: 0 8px 18px rgba(124, 58, 237, 0.28) !important;
    }

    .stButton>button:hover {
        filter: brightness(1.05);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: var(--text-main);
        border: 1px solid var(--border);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-soft) !important;
        color: var(--primary-dark) !important;
        border-color: #C4B5FD !important;
    }

    .stSelectbox label, .stTextInput label, .stRadio label, .stSlider label {
        color: var(--text-main) !important;
        font-weight: 600 !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background: #FFFFFF !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        color: #111827 !important;
        background: #FFFFFF !important;
    }

    [data-baseweb="select"] input,
    [data-baseweb="select"] div {
        color: #111827 !important;
        background: #FFFFFF !important;
    }

    /* Dropdown menu options (Transport, Diet) */
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] ul,
    div[role="listbox"] {
        background: #FFFFFF !important;
    }

    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    div[role="option"] {
        background: #FFFFFF !important;
        color: #6D28D9 !important;
        font-weight: 700 !important;
    }

    div[data-baseweb="popover"] li *,
    div[data-baseweb="menu"] li *,
    div[role="option"] * {
        color: #6D28D9 !important;
        opacity: 1 !important;
    }

    div[data-baseweb="popover"] li[aria-selected="true"],
    div[data-baseweb="menu"] li[aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background: #EDE9FE !important;
        color: #5B21B6 !important;
    }

    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover,
    div[role="option"]:hover {
        background: #F5F3FF !important;
        color: #5B21B6 !important;
    }

    .stSelectSlider {
        color: #111827 !important;
    }

    .stSubheader, .stCaption, .stInfo, .stMarkdown p, .stMarkdown li, .stWrite {
        color: #111827 !important;
    }

    /* Enforce readable black text across app sections */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] li,
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4 {
        color: #111827 !important;
    }

    /* File uploader visibility fixes */
    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF !important;
        border: 2px dashed #A78BFA !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #111827 !important;
    }

    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #5B21B6, #7C3AED) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    [data-testid="stFileUploader"] button:hover {
        filter: brightness(1.06);
    }

    [data-testid="stDataFrame"] * {
        color: #111827 !important;
    }

    .dev-footer {
        margin-top: 28px;
        padding: 14px 12px;
        border-top: 2px solid #A78BFA;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
    }

    .dev-footer-title {
        text-align: center;
        color: #4C1D95 !important;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: 0.03em;
    }

    .dev-footer-names {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
        color: #111827 !important;
        font-family: Algerian, "Times New Roman", serif;
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def _normalize_text(value):
    return re.sub(r"\s+", " ", str(value).strip().lower())


def _resolve_column(columns, keyword_groups):
    normalized = {col: _normalize_text(col) for col in columns}
    for keys in keyword_groups:
        for original, norm_col in normalized.items():
            if all(k in norm_col for k in keys):
                return original
    return None


def _extract_first_number(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None


def process_csv_data(df):
    """Calculates TotalScore based on user's specific Google Form Columns"""

    transport_col = _resolve_column(
        df.columns,
        [["primary", "mode", "transport"], ["transport", "college"], ["transport"]],
    )
    laptop_col = _resolve_column(
        df.columns,
        [["laptop", "computer", "daily"], ["laptop", "hours"], ["computer", "hours"], ["digital", "usage"]],
    )
    ac_col = _resolve_column(
        df.columns,
        [["air", "conditioning"], ["use", "ac"], ["ac", "regularly"]],
    )
    diet_col = _resolve_column(
        df.columns,
        [["primary", "diet"], ["diet"]],
    )
    bottles_col = _resolve_column(
        df.columns,
        [["plastic", "bottles", "week"], ["bottles", "week"], ["plastic", "bottles"]],
    )
    reusable_col = _resolve_column(
        df.columns,
        [["reusable", "water", "bottle"], ["reusable", "bottle"]],
    )
    
    def calculate_row(row):
        score = 0

        t_mode = _normalize_text(row.get(transport_col, "Walking"))
        if any(word in t_mode for word in ["walk", "bicycle", "cycle"]):
            score += 5
        elif "bus" in t_mode:
            score += 12
        elif any(word in t_mode for word in ["bike", "motor"]):
            score += 22
        elif "car" in t_mode:
            score += 35
        else:
            score += 20

        e_hrs = _normalize_text(row.get(laptop_col, "0-2"))
        if "0-2" in e_hrs or "0 to 2" in e_hrs:
            score += 5
        elif "2-5" in e_hrs or "2 to 5" in e_hrs:
            score += 12
        elif "5-8" in e_hrs or "5 to 8" in e_hrs:
            score += 20
        elif "8+" in e_hrs or "more" in e_hrs:
            score += 28
        else:
            hours = _extract_first_number(e_hrs)
            if hours is None:
                score += 12
            elif hours <= 2:
                score += 5
            elif hours <= 5:
                score += 12
            elif hours <= 8:
                score += 20
            else:
                score += 28

        ac = _normalize_text(row.get(ac_col, "No"))
        if "yes" in ac or "daily" in ac:
            score += 20
        elif "occasion" in ac or "sometimes" in ac:
            score += 10

        diet = _normalize_text(row.get(diet_col, "Mixed"))
        if "vegetarian" in diet or "vegan" in diet:
            score += 10
        elif "mixed" in diet:
            score += 20
        elif "non" in diet or "meat" in diet:
            score += 30
        else:
            score += 20

        bottles = _normalize_text(row.get(bottles_col, "0-1"))
        if "0-1" in bottles or "0 to 1" in bottles:
            score += 5
        elif "2-4" in bottles or "2 to 4" in bottles:
            score += 15
        else:
            bottle_count = _extract_first_number(bottles)
            if bottle_count is None:
                score += 15
            elif bottle_count <= 1:
                score += 5
            elif bottle_count <= 4:
                score += 15
            else:
                score += 25

        reusable = _normalize_text(row.get(reusable_col, "Yes"))
        if "no" in reusable:
            score += 10
        
        return score

    df['TotalScore'] = df.apply(calculate_row, axis=1)
    return df


def get_personalized_tips(transport, laptop_hours, diet, total_score):
    tips = []

    if transport in ["Car", "Bike"]:
        tips.append("Shift 2-3 days/week to bus, bicycle, or carpool to cut transport emissions quickly.")
    if laptop_hours in ["5-8", "8+"]:
        tips.append("Use power-saving mode, lower screen brightness, and shut down devices overnight.")
    if diet == "Non-vegetarian":
        tips.append("Try 2 vegetarian days each week to reduce food-related ecological impact.")
    if diet == "Mixed":
        tips.append("Increase plant-based meals and reduce packaged food to lower waste and footprint.")

    if total_score >= 70:
        tips.append("Start with one high-impact habit this month (transport or energy) for visible score reduction.")
    elif total_score < 45:
        tips.append("Your baseline is strong. Maintain these habits and help peers adopt low-impact choices.")

    if not tips:
        tips.append("Keep your current low-impact habits consistent and track improvements weekly.")

    return tips[:4]


def get_campus_tips(df):
    tips = []

    transport_col = 'What is your primary mode of transport to college?'
    laptop_col = 'How many hours do you use a laptop/computer daily?'
    diet_col = 'What is your primary diet?'
    reusable_col = 'Do you carry a reusable water bottle?'

    if transport_col in df.columns:
        top_transport = df[transport_col].astype(str).value_counts().idxmax()
        if 'Car' in top_transport or 'Bike' in top_transport:
            tips.append("Campus trend: transport is a major contributor. Promote bus passes, cycle days, and carpool groups.")

    if laptop_col in df.columns:
        high_energy = df[laptop_col].astype(str).str.contains('5-8|8+', regex=True).mean()
        if high_energy >= 0.4:
            tips.append("Campus trend: high digital usage. Run energy-awareness campaigns for device efficiency.")

    if diet_col in df.columns:
        nonveg_share = df[diet_col].astype(str).str.contains('Non', case=False).mean()
        if nonveg_share >= 0.35:
            tips.append("Campus trend: food footprint is significant. Encourage plant-forward options in canteens.")

    if reusable_col in df.columns:
        no_reusable_share = df[reusable_col].astype(str).str.contains('No', case=False).mean()
        if no_reusable_share >= 0.3:
            tips.append("Campus trend: plastic reduction opportunity. Add refill stations and reusable bottle drives.")

    if not tips:
        tips.append("Overall campus pattern is balanced. Focus on awareness sessions and monthly footprint tracking.")

    avg_score = float(df['TotalScore'].mean()) if 'TotalScore' in df.columns else 0
    high_impact_share = float((df['TotalScore'] >= 45).mean()) if 'TotalScore' in df.columns else 0

    if avg_score >= 45:
        tips.append("Campus average is on the higher side. Start a 30-day challenge focused on transport and energy habits.")
    if high_impact_share >= 0.35:
        tips.append("A notable share of students are in moderate/high impact range. Run department-wise mentoring and monthly audits.")

    deduped = []
    for tip in tips:
        if tip not in deduped:
            deduped.append(tip)

    if len(deduped) < 2:
        deduped.append("Introduce a weekly eco-scoreboard to track progress and increase participation.")

    return deduped[:5]

st.title("Gryfindors: Eco-Footprint Dashboard")
st.markdown("### College Sustainability Analysis Engine")

tab1, tab2 = st.tabs(["Live Demo Calculator", "College Data Analysis"])

with tab1:
    col_in, col_res = st.columns([1, 1.5], gap="large")
    
    with col_in:
        st.subheader("Personal Factors")
        name = st.text_input("Student Name", "Volunteer")
        t = st.selectbox("Transport", ["Walking/Bicycle", "Public Bus", "Bike", "Car"])
        e = st.select_slider("Laptop Hours", ["0-2", "2-5", "5-8", "8+"])
        d = st.selectbox("Diet", ["Vegetarian", "Mixed", "Non-vegetarian"])
        
        if st.button("Calculate My Impact"):
            t_s = {"Walking/Bicycle": 5, "Public Bus": 12, "Bike": 20, "Car": 35}[t]
            e_s = {"0-2": 6, "2-5": 12, "5-8": 20, "8+": 28}[e]
            f_s = {"Vegetarian": 10, "Mixed": 20, "Non-vegetarian": 30}[d]
            total = t_s + e_s + f_s

            st.session_state.demo_res = {
                "name": name,
                "total": total,
                "labels": ["Transport", "Energy", "Food"],
                "vals": [t_s, e_s, f_s],
                "tips": get_personalized_tips(t, e, d, total),
            }

    with col_res:
        if 'demo_res' in st.session_state:
            res = st.session_state.demo_res
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card'><h4>TOTAL SCORE</h4><h2>{res['total']}</h2></div>", unsafe_allow_html=True)
            status = "LOW" if res['total'] < 45 else "MODERATE" if res['total'] < 70 else "HIGH"
            status_color = "#059669" if status == "LOW" else "#B45309" if status == "MODERATE" else "#DC2626"
            c2.markdown(f"<div class='metric-card'><h4>IMPACT LEVEL</h4><h2 style='color:{status_color}'>{status}</h2></div>", unsafe_allow_html=True)

            fig_demo = go.Figure(data=[
                go.Bar(
                    x=res['labels'],
                    y=res['vals'],
                    marker_color=['#8B5CF6', '#7C3AED', '#6D28D9'],
                    text=res['vals'],
                    textposition='outside',
                    hovertemplate="%{x}: %{y} points<extra></extra>",
                )
            ])
            fig_demo.update_layout(
                title="Impact Breakdown (Lower is Better)",
                yaxis_title="Score Contribution",
                xaxis_title="Lifestyle Category",
                font_family="Inter",
                font_color="#111827",
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=50, b=20),
            )
            st.plotly_chart(fig_demo, use_container_width=True)

            st.caption("Explanation: each bar shows contribution to your footprint score. Lower category scores indicate more sustainable habits.")
            st.markdown("<div class='tip-card'><div class='tip-title'>Personalized Tips to Reduce Footprint</div></div>", unsafe_allow_html=True)
            for tip in res['tips']:
                st.write(f"- {tip}")
        else:
            st.markdown("<div class='tip-card'><div class='tip-title'>Live Demo Calculator</div>Enter your factors and click <b>Calculate My Impact</b> to see score, level, graph, and tips.</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Upload Survey Data")
    uploaded_file = st.file_uploader("Drop your 'Ecological Sheet' CSV here", type="csv")

    if uploaded_file is not None:
        raw_df = pd.read_csv(uploaded_file)
        df = process_csv_data(raw_df)

        m1, m2, m3 = st.columns(3)
        avg_s = df['TotalScore'].mean()
        m1.markdown(f"<div class='college-kpi-card'><h4>CAMPUS AVG</h4><h2>{avg_s:.1f}</h2></div>", unsafe_allow_html=True)
        m2.markdown(f"<div class='college-kpi-card'><h4>RESPONDENTS</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='college-kpi-card'><h4>MAX IMPACT</h4><h2>{df['TotalScore'].max()}</h2></div>", unsafe_allow_html=True)

        st.markdown("---")

        c_left, c_right = st.columns(2)
        
        with c_left:
            fig_hist = px.histogram(df, x="TotalScore", title="<b>Footprint Distribution</b>",
                                   color_discrete_sequence=['#7C3AED'], template="plotly_white")
            fig_hist.add_vline(
                x=df['TotalScore'].mean(),
                line_dash="dash",
                line_color="#111827",
                annotation_text="Campus Average",
                annotation_position="top right"
            )
            fig_hist.update_layout(
                font_family="Inter",
                font_color="#111827",
                bargap=0.1,
                xaxis_title="Total Footprint Score",
                yaxis_title="Number of Students",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.caption("Explanation: this chart shows how student footprint scores are distributed across the campus.")
            
        with c_right:
            avg_year = df.groupby('What is your year of study?')['TotalScore'].mean().reset_index()
            fig_year = px.bar(avg_year, x='What is your year of study?', y='TotalScore',
                             title="<b>Avg Footprint by Study Year</b>",
                             color_discrete_sequence=['#6D28D9'], template="plotly_white", text_auto='.2f')
            fig_year.update_layout(
                font_family="Inter",
                font_color="#111827",
                xaxis_title="Year of Study",
                yaxis_title="Average Score",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_year, use_container_width=True)
            st.caption("Explanation: compares average ecological footprint between study years to identify focus groups.")

        st.subheader("Campus Personalization Tips")
        campus_tips = get_campus_tips(df)
        tips_html = "".join([f"<li>{tip}</li>" for tip in campus_tips])
        st.markdown(
            f"""
            <div class='tip-card'>
                <div class='tip-title'>Data-Driven Recommendations</div>
                <ol class='recommendation-list'>{tips_html}</ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("Sustainability Leaderboard")
        st.write("Top students with the lowest environmental impact.")
        name_col = 'Name' if 'Name' in df.columns else df.columns[0]
        leaderboard = df[[name_col, 'What is your year of study?', 'TotalScore']].sort_values(by="TotalScore").head(10).copy()
        leaderboard.columns = ['Student', 'Year of Study', 'Total Score']
        leaderboard.insert(0, 'Rank', range(1, len(leaderboard) + 1))

        rows_html = ""
        for _, row in leaderboard.iterrows():
            rows_html += (
                f"<tr>"
                f"<td>{int(row['Rank'])}</td>"
                f"<td>{html.escape(str(row['Student']))}</td>"
                f"<td>{html.escape(str(row['Year of Study']))}</td>"
                f"<td><span class='score-pill'>{float(row['Total Score']):.1f}</span></td>"
                f"</tr>"
            )

        st.markdown(
            f"""
            <div class='leaderboard-wrap'>
                <table class='leaderboard-table'>
                    <thead>
                        <tr>
                            <th style='width:80px;'>Rank</th>
                            <th>Student</th>
                            <th style='width:220px;'>Year of Study</th>
                            <th style='width:160px;'>Total Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.info("Please upload your college survey CSV to unlock the analytics dashboard.")
        st.image("https://img.icons8.com/illustrations/official/256/upload-to-cloud.png", width=100)

st.markdown(
    """
    <div class='dev-footer'>
        <div class='dev-footer-title'>Development Team</div>
        <div class='dev-footer-names'>
            <span>Arun Ulagappan S</span>
            <span>•</span>
            <span>Syndhavi S</span>
            <span>•</span>
            <span>Manjushree R G</span>
            <span>•</span>
            <span>Priyadharshini S</span>
            <span>•</span>
            <span>Dharshini Priya A</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)