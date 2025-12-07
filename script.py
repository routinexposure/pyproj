import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from collections import Counter

russian_letters = list("абвгдежзийклмнопрстуфхцчшщъыьэюяё")

with open("war_and_peace.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()

letters = [ch for ch in text if ch in russian_letters]
counts = Counter(letters)
values_sorted = [counts[ch] for ch in russian_letters]


app = dash.Dash(__name__)
app.title = "Анализ букв — Война и Мир"


app.layout = html.Div(
    style={"padding": "20px", "font-family": "Arial"},
    children=[
        html.H1("Анализ букв в книге «Война и Мир»", style={"text-align": "center"}),

        html.Div([
            html.Label("Тип графика:"),
            dcc.Dropdown(
                id="chart-type",
                value="bar",
                options=[
                    {"label": "Столбцы", "value": "bar"},
                    {"label": "Линия", "value": "line"},
                    {"label": "Площадь", "value": "area"},
                ],
                style={"width": "250px"}
            ),
        ], style={"display": "inline-block", "margin-right": "50px"}),

        html.Div([
            html.Label("Тема интерфейса:"),
            dcc.Dropdown(
                id="theme",
                value="plotly_white",
                options=[
                    {"label": "Светлая", "value": "plotly_white"},
                    {"label": "Тёмная", "value": "plotly_dark"}
                ],
                style={"width": "250px"}
            ),
        ], style={"display": "inline-block"}),

        dcc.Graph(id="graph", style={"margin-top": "30px"})
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("chart-type", "value"),
    Input("theme", "value"),
)
def update_graph(chart_type, theme):

    fig = go.Figure()

    if chart_type == "bar":
        fig.add_trace(go.Bar(
            x=russian_letters,
            y=values_sorted,
            hovertemplate="Буква: %{x}<br>Количество: %{y}<extra></extra>",
            marker=dict(line=dict(width=1))
        ))

    elif chart_type == "line":
        fig.add_trace(go.Scatter(
            x=russian_letters,
            y=values_sorted,
            mode="lines+markers",
            hovertemplate="Буква: %{x}<br>Количество: %{y}<extra></extra>",
            line=dict(width=3)
        ))

    elif chart_type == "area":
        fig.add_trace(go.Scatter(
            x=russian_letters,
            y=values_sorted,
            fill="tozeroy",
            hovertemplate="Буква: %{x}<br>Количество: %{y}<extra></extra>",
            line=dict(width=2)
        ))

    fig.update_layout(
        template=theme,
        title="Частота букв в русском тексте",
        xaxis_title="Буква",
        yaxis_title="Количество",
        transition_duration=500,
        width=1200,
        height=600
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)

