import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Load the parsed data
with open("output/output4.json", "r") as f:
    parsed = json.load(f)
data = parsed["data"]

# Extract data
freq = data["Freq"]
zmod = data["Zmod"]
zphz = data["Zphz"]
zreal = data["Zreal"]
zimag = data["Zimag"]

# Bode Plot: Magnitude + Phase in Subplots
fig_bode = make_subplots(rows=2, cols=1, shared_xaxes=True,
                         subplot_titles=("Magnitude |Z|", "Phase ∠Z"),
                         vertical_spacing=0.1)

# Add magnitude trace
fig_bode.add_trace(go.Scatter(x=freq, y=zmod, mode='lines+markers', name='|Z|'),
                   row=1, col=1)

# Add phase trace
fig_bode.add_trace(go.Scatter(x=freq, y=zphz, mode='lines+markers', name='Phase (°)'),
                   row=2, col=1)

# Layout updates
fig_bode.update_layout(
    title="Bode Plot",
    height=600,
    showlegend=False
)

# X-axis: log scale
fig_bode.update_xaxes(type="log", title="Frequency (Hz)", row=2, col=1)

# Y-axes
fig_bode.update_yaxes(title="|Z| (Ω)", type="log", row=1, col=1)
fig_bode.update_yaxes(title="Phase (°)", row=2, col=1)

# Nyquist Plot
fig_nyquist = go.Figure()
fig_nyquist.add_trace(go.Scatter(x=zreal, y=[-z for z in zimag],
                                 mode='lines+markers', name='Nyquist'))

fig_nyquist.update_layout(
    title="Nyquist Plot",
    xaxis_title="Zreal (Ω)",
    yaxis_title="-Zimag (Ω)",
    yaxis=dict(scaleanchor="x", scaleratio=1)
)

# Show plots
fig_bode.show()
fig_nyquist.show()
