import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Credit Assessment: JSPL",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (Styling) ---
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    .stMetric {background-color: #f8f9fa; border-left: 5px solid #004b8d; padding: 10px; border-radius: 5px;}
    .decision-card {
        padding: 20px; border-radius: 10px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: INPUTS ---
st.sidebar.header("⚙️ Evaluation Parameters")

# Defaults set to generate Score 4.55 (REJECT)
s_fin = st.sidebar.slider("Financial Strength (25%)", 0, 10, 8)
s_ind = st.sidebar.slider("Industry/Models (20%)", 0, 10, 6)
s_mgt = st.sidebar.slider("Mgmt & Forensic (15%)", 0, 10, 7)
s_col = st.sidebar.slider("Collateral (25%)", 0, 10, 0)  # Critical Miss
s_str = st.sidebar.slider("Strategic Fit (15%)", 0, 10, 2)

# Calculation
score = (s_fin * 0.25) + (s_ind * 0.20) + (s_mgt * 0.15) + (s_col * 0.25) + (s_str * 0.15)

# Logic
if score >= 7.5:
    status, color, bg, icon, msg = "APPROVED", "#28a745", "#e8f5e9", "✅", "Proposal meets all risk acceptance criteria."
elif score >= 5.0:
    status, color, bg, icon, msg = "REVIEW", "#ffc107", "#fff3e0", "⚠️", "Marginal score; requires additional Collateral."
else:
    status, color, bg, icon, msg = "REJECT", "#dc3545", "#ffebee", "⛔", "<b>Rationale:</b> High Risk due to Unsecured structure & Strategic Mismatch."

if st.sidebar.button("🔄 Reset Dashboard"):
    st.cache_data.clear()
    st.rerun()

# --- 4. HEADER: LOGOS & TITLE ---
# Using reliable Wikimedia PNG links
c1, c2, c3 = st.columns([1, 4, 1])

with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bandhan_Bank_Logo.svg/1200px-Bandhan_Bank_Logo.svg.png", use_container_width=True)

with c2:
    st.markdown("<h1 style='text-align: center; color: #004b8d;'>Credit Evaluation Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Borrower: Jindal Steel & Power | Proposal: ₹1,415 Cr Unsecured</h4>", unsafe_allow_html=True)

with c3:
    # Use the 'Jindal Steel and Power' logo specific link
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Jindal_Steel_and_Power_Logo.svg/1200px-Jindal_Steel_and_Power_Logo.svg.png", use_container_width=True)

st.markdown("---")

# --- 5. SPLIT LAYOUT (Small Gauge Left | Decision Right) ---
col_L, col_R = st.columns([1, 2])

# LEFT: Compact Riskometer
with col_L:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "<b>AI CREDIT SCORE</b>", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 5], 'color': "#ffebee"},
                {'range': [5, 7.5], 'color': "#fff3e0"},
                {'range': [7.5, 10], 'color': "#e8f5e9"}
            ],
            'threshold': {'line': {'color': "black", 'width': 3}, 'thickness': 0.75, 'value': 7.5}
        }
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

# RIGHT: Decision Card
with col_R:
    st.markdown(f"""
    <div class="decision-card" style="background-color: {bg}; border: 2px solid {color}; margin-top: 20px;">
        <h2 style="color: {color}; margin: 0; font-weight: 800;">{icon} {status}</h2>
        <h1 style="font-size: 3em; margin: 5px 0;">{score:.2f} <span style="font-size: 0.4em; color: gray;">/ 10</span></h1>
        <hr style="border-top: 1px solid {color}; opacity: 0.5;">
        <p style="font-size: 1.2rem; color: #333; margin: 0;">{msg}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 6. METRICS SECTION ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Net Debt / EBITDA", "1.48x", "Worsening", delta_color="inverse")
m2.metric("Altman Z-Score", "2.92", "Grey Zone", delta_color="off")
m3.metric("Ohlson O-Score", "< 1%", "Safe", delta_color="normal")
m4.metric("Strategic Fit", "Low", "Mismatch", delta_color="inverse")

# --- 7. GRAPHS (2x2 Grid) ---
st.subheader("📊 Detailed Analysis")

row1_1, row1_2 = st.columns(2)

# GRAPH 1: Financial Trend
with row1_1:
    st.markdown("**1. Financial Trend: Rising Debt Levels**")
    df_trend = pd.DataFrame({'Year': ['FY23', 'FY24', 'FY25'], 'Debt': [9500, 10200, 14156], 'EBITDA': [11000, 12500, 9500]})
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=df_trend['Year'], y=df_trend['EBITDA'], name='EBITDA', marker_color='#004b8d', opacity=0.6))
    fig_trend.add_trace(go.Scatter(x=df_trend['Year'], y=df_trend['Debt'], name='Net Debt', line=dict(color='red', width=3)))
    fig_trend.update_layout(height=300, margin=dict(t=20,b=20,l=20,r=20), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_trend, use_container_width=True)

# GRAPH 2: Peer Comparison
with row1_2:
    st.markdown("**2. Peer Leverage Comparison (Debt/EBITDA)**")
    df_peer = pd.DataFrame({'Company': ['JSPL', 'Tata Steel', 'JSW Steel'], 'Leverage': [1.48, 2.5, 2.8]})
    fig_peer = px.bar(df_peer, x='Company', y='Leverage', color='Company', text='Leverage',
                      color_discrete_map={'JSPL':'#28a745', 'Tata Steel':'gray', 'JSW Steel':'gray'})
    fig_peer.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_peer, use_container_width=True)

row2_1, row2_2 = st.columns(2)

# GRAPH 3: Risk Radar
with row2_1:
    st.markdown("**3. Risk Gap Analysis (Ideal vs Actual)**")
    cats = ['Financial', 'Industry', 'Mgmt', 'Collateral', 'Strategy']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=[s_fin, s_ind, s_mgt, s_col, s_str], theta=cats, fill='toself', name='Actual', line_color=color))
    fig_radar.add_trace(go.Scatterpolar(r=[8, 8, 8, 10, 8], theta=cats, name='Ideal', line_color='green', line_dash='dot'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=300, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig_radar, use_container_width=True)

# GRAPH 4: Strategic Fit Donut
with row2_2:
    st.markdown("**4. Bandhan Bank Strategy vs Proposal**")
    labels = ['Secured (Target)', 'Unsecured (This Loan)']
    fig_donut = go.Figure(data=[go.Pie(labels=labels, values=[60, 40], hole=.6, marker_colors=['#004b8d', '#dc3545'])])
    fig_donut.update_layout(height=300, showlegend=True, margin=dict(t=20,b=20,l=20,r=20))
    st.plotly_chart(fig_donut, use_container_width=True)
