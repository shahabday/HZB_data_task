import plotly.graph_objects as go
import json

# Load the parsed data
with open("output2.json", "r") as f:
    parsed = json.load(f)
data = parsed["data"]

# Bode Plot
fig_bode = go.Figure()
fig_bode.add_trace(go.Scatter(x=data["Freq"],
                               y=data["Zreal"],
                                 mode='lines+markers', name='Zreal'))
fig_bode.add_trace(go.Scatter(x=data["Freq"],
                               y=data["Zimag"],
                                 mode='lines+markers', name='Zimag'))

fig_bode.update_layout(
    title="Bode Plot",
    xaxis=dict(title="Frequency (Hz)", type="log"),
    yaxis=dict(title="Impedance (Ω)"),
    legend=dict(x=0.01, y=0.99)
)

# Nyquist Plot
fig_nyquist = go.Figure()
fig_nyquist.add_trace(go.Scatter(x=data["Zreal"], y= [ -z for z  in data["Zimag"]],
                                 mode='lines+markers', name='Nyquist'))

fig_nyquist.update_layout(
    title="Nyquist Plot",
    xaxis_title="Zreal (Ω)",
    yaxis_title="-Zimag (Ω)",
    yaxis=dict(scaleanchor="x", scaleratio=1)  # Equal aspect ratio
)

fig_bode.show()
fig_nyquist.show()
