import dash
from dash import dcc, html, Input, Output, State
import base64
import io
import json
import tempfile
from parser.eis_parser import EISParser
from parser.utils import detect_experiment_type
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = "HZB EIS Parser"

app.layout = html.Div([
    html.H2("HZB Gamry EIS Parser"),

    dcc.Upload(
        id='upload-data',
        children=html.Div(['📁 Drag & Drop or Click to Upload a .DTA File']),
        style={
            'width': '100%', 'height': '80px', 'lineHeight': '80px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
        multiple=False
    ),

    html.Div([
        html.Label("DOE Version:"),
        dcc.Input(id='doe-version', type='text', placeholder='e.g. v1.0', style={'marginRight': '20px'}),

        html.Label("Battery ID:"),
        dcc.Input(id='battery-id', type='text', placeholder='Battery_12345', style={'marginRight': '20px'}),

        html.Label("DOE Section:"),
        dcc.Input(id='doe-section', type='number', placeholder='e.g. 2'),
    ], style={'marginBottom': '20px'}),

    html.Button("Convert and Visualize", id='process-btn', n_clicks=0),

    html.H4("Converted JSON Output:"),
    html.Pre(id='json-output', style={'whiteSpace': 'pre-wrap', 'maxHeight': '300px', 'overflowY': 'scroll'}),

    html.Div([
        dcc.Graph(id='nyquist-plot'),
        dcc.Graph(id='bode-plot')
    ])
])

@app.callback(
    Output('json-output', 'children'),
    Output('nyquist-plot', 'figure'),
    Output('bode-plot', 'figure'),
    Input('process-btn', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('doe-version', 'value'),
    State('battery-id', 'value'),
    State('doe-section', 'value'),
)
def process_and_plot(n_clicks, contents, filename, doe_version, battery_id, doe_section):
    if not contents or n_clicks == 0:
        return dash.no_update, go.Figure(), go.Figure()

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Save uploaded content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".DTA", mode='wb') as temp_file:
        temp_file.write(decoded)
        temp_filepath = temp_file.name

    # Detect experiment type and parse
    experiment_type = detect_experiment_type(temp_filepath)
    if experiment_type != "PWR800_HYBRIDEIS":
        return f"Unsupported experiment type: {experiment_type}", go.Figure(), go.Figure()

    extra_metadata = {
        "doe_version": doe_version,
        "battery_id": battery_id,
        "doe_section": doe_section
    }

    try:
        parser = EISParser(temp_filepath, extra_metadata=extra_metadata)
        parser.parse()

        parsed = {
            "instrument_type": "Gamry",
            "experiment_class": "EIS",
            "metadata": parser.metadata,
            "doe_version": parser.extra_metadata.get("doe_version"),
            "battery_id": parser.extra_metadata.get("battery_id"),
            "doe_section": parser.extra_metadata.get("doe_section"),
            "data": parser.data
        }

        from plotly.subplots import make_subplots

        # Generate Nyquist Plot
        Zreal = parsed['data'].get('Zreal', [])
        Zimag = parsed['data'].get('Zimag', [])
        fig_nyquist = go.Figure()
        fig_nyquist.add_trace(go.Scatter(x=Zreal, y=[-z for z in Zimag], mode='lines+markers', name='Nyquist'))
        fig_nyquist.update_layout(
            title="Nyquist Plot",
            xaxis_title="Zreal (Ω)",
            yaxis_title="-Zimag (Ω)",
            yaxis=dict(scaleanchor="x", scaleratio=1)
        )

        # Generate Bode Plot as Subplots (|Z| and Phase)
        freq = parsed['data'].get('Freq', [])
        zmod = parsed['data'].get('Zmod', [])
        zphz = parsed['data'].get('Zphz', [])

        fig_bode = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                subplot_titles=("Magnitude |Z|", "Phase ∠Z"),
                                vertical_spacing=0.1)

        fig_bode.add_trace(go.Scatter(x=freq, y=zmod, mode='lines+markers', name='|Z|'), row=1, col=1)
        fig_bode.add_trace(go.Scatter(x=freq, y=zphz, mode='lines+markers', name='Phase (°)'), row=2, col=1)

        fig_bode.update_layout(
            title="Bode Plot",
            height=600,
            showlegend=False
        )

        fig_bode.update_xaxes(type="log", title="Frequency (Hz)", row=2, col=1)
        fig_bode.update_yaxes(title="|Z| (Ω)", type="log", row=1, col=1)
        fig_bode.update_yaxes(title="Phase (°)", row=2, col=1)


        return json.dumps(parsed, indent=2), fig_nyquist, fig_bode

    except Exception as e:
        return f"❌ Error: {str(e)}", go.Figure(), go.Figure()

if __name__ == '__main__':
    app.run(debug=True)
