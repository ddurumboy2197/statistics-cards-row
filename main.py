import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Ma'lumotlar manbasidan ma'lumot olish
df = pd.DataFrame({
    'Kategoriya': ['Savdo', 'Savdo', 'Savdo', 'Savdo', 'Savdo', 'Savdo', 'Savdo', 'Savdo', 'Savdo', 'Savdo'],
    'Qabul qilingan': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    'Yetkazib berilgan': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
})

# Grafikni chizish
fig = px.bar(df, x='Kategoriya', y='Qabul qilingan', title='Qabul qilingan savdo')
fig.update_layout(xaxis_title='Kategoriya', yaxis_title='Qabul qilingan')

# Dash uchun grafikni yaratish
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1('Statistika kartalari qatori'),
    html.Div([
        html.Div([
            html.H2('Qabul qilingan savdo'),
            dcc.Graph(id='qabul-qilingan', figure=fig)
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H2('Yetkazib berilgan savdo'),
            dcc.Graph(id='yetkazib-berilgan')
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),
    html.Div([
        html.Div([
            html.H2('Jami savdo'),
            html.Div(id='jami-savdo')
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.H2('O'rtacha savdo'),
            html.Div(id='ortacha-savdo')
        ], style={'width': '49%', 'display': 'inline-block'})
    ])
])

# Jami savdo va o'rtacha savdo hisoblash
@app.callback(
    [Output('jami-savdo', 'children'),
     Output('ortacha-savdo', 'children')],
    [Input('qabul-qilingan', 'figure')]
)
def update_jami_savdo(figure):
    jami_savdo = df['Qabul qilingan'].sum()
    ortacha_savdo = jami_savdo / len(df)
    return f'Jami savdo: {jami_savdo}', f'O\'rtacha savdo: {ortacha_savdo}'

# Yetkazib berilgan savdo grafikini yaratish
@app.callback(
    Output('yetkazib-berilgan', 'figure'),
    [Input('qabul-qilingan', 'figure')]
)
def update_yetkazib_berilgan(figure):
    df_yetkazib_berilgan = df.copy()
    df_yetkazib_berilgan['Qabul qilingan'] = df_yetkazib_berilgan['Yetkazib berilgan']
    fig_yetkazib_berilgan = px.bar(df_yetkazib_berilgan, x='Kategoriya', y='Qabul qilingan', title='Yetkazib berilgan savdo')
    fig_yetkazib_berilgan.update_layout(xaxis_title='Kategoriya', yaxis_title='Yetkazib berilgan')
    return fig_yetkazib_berilgan

if __name__ == '__main__':
    app.run_server(debug=True)
