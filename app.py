import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stSlider > div {
            background-color: #1e1e1e;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.title("SBCL Cancer Resonance Interface")
st.subheader("Symbolic Therapeutic Alignment Tool")

# Sidebar sliders
with st.sidebar:
    st.header("Symbolic Parameters")
    delivery = st.slider("Delivery Efficiency", 0.0, 1.0, 0.5, 0.01)
    recognition = st.slider("Target Recognition", 0.0, 1.0, 0.5, 0.01)
    flexibility = st.slider("Molecular Flexibility", 0.0, 1.0, 0.5, 0.01)

# Compute Scores
def compute_scores(delivery, recognition, flexibility):
    entropy = round(50 + recognition * 30 - flexibility * 10, 1)
    selectivity = round(60 + recognition * 30, 1)
    coherence = round(70 + delivery * 15 - flexibility * 5, 1)
    phase_lock = round((entropy + selectivity + coherence) / 3, 1)
    return {
        "entropy_alignment": min(entropy, 100),
        "selectivity": min(selectivity, 100),
        "field_coherence": min(coherence, 100),
        "phase_lock": min(phase_lock, 100)
    }

scores = compute_scores(delivery, recognition, flexibility)

# Display updated scores
with st.container():
    st.markdown("### Real-Time Scoring Metrics")
    st.metric("Entropy Alignment", f"{scores['entropy_alignment']}%")
    st.metric("Target Selectivity", f"{scores['selectivity']}%")
    st.metric("Field Coherence", f"{scores['field_coherence']}%")
    st.metric("Phase Lock", f"{scores['phase_lock']}%")

# Dynamic Waveform Generator
x = np.linspace(0, 10, 1000)
waves = [
    np.sin(x + i + recognition * 3) * (1 - 0.4 * flexibility) * (1 + delivery * 0.5)
    for i in np.linspace(0, 2 * np.pi, 7)
]

# Generate Plot
fig = go.Figure()

colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494']

for i, y in enumerate(waves):
    fig.add_trace(go.Scatter(x=x, y=y + i * 1.5, mode='lines', line=dict(color=colors[i % len(colors)], width=2)))

fig.update_layout(
    title="Symbolic Resonance Field",
    xaxis_title="Phase Domain",
    yaxis_title="Amplitude",
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(color="white"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

