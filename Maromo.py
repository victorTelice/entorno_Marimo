import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.graph_objects as go
    return go, mo, pd


@app.cell
def _(mo, pd):
    df = pd.read_csv('entorno_marimo/Docs/consumo.csv', sep=';')

    df['CUPs E'] = pd.to_numeric(df['CUPs E'], errors='coerce')
    df['CUPs GN'] = pd.to_numeric(df['CUPs GN'], errors='coerce')
    df['GSL'] = pd.to_numeric(df['GSL'], errors='coerce')

    centros_consumo = len(df['TIPO DE CENTRO DE CONSUMO'])
    suministros_elec = df['CUPs E'].sum()
    suministros_gas = df['CUPs GN'].sum()
    suministros_gsl = df['GSL'].sum()

    def stat_create(val, cap):

        return mo.stat(
            value = val,
            caption = cap
        ).style({ "text-align": "center"})

    info_centros = stat_create(centros_consumo, "Nº de centros de consumo")
    info_sum_elec = stat_create(suministros_elec, "Nº de suministros electricidad")
    info_sum_gas = stat_create(suministros_gas, "Nº de suministros gas natural canalizado")
    info_sum_gsl = stat_create(suministros_gsl, "Nº de centros con gasóleo")

    mo.hstack([info_centros, info_sum_elec, info_sum_gas, info_sum_gsl], justify = "space-around", gap = "2rem")
    return suministros_elec, suministros_gas, suministros_gsl


@app.cell
def _():
    import plotly.graph_objects as go
    return (go,)


@app.cell
def _(go, suministros_elec, suministros_gas, suministros_gsl):
    categorias = ['Gasóleo', 'Gas', 'Electricidad']
    valores = [suministros_gsl, suministros_gas, suministros_elec]  
    textos = [suministros_gsl, suministros_gas, suministros_elec]

    fig = go.Figure(
        data=[
            go.Bar(
                y=categorias,
                x=valores,
                orientation='h',
                text=textos,              
                textposition='inside',    
                marker_color=['#df2d07', '#df2d07', '#df2d07'],
                hovertext=textos,
                hoverinfo="text"
            )
        ]
    )

    # Personalizar el diseño
    fig.update_layout(
        title="Número de suministros energéticos",
        xaxis=dict(showticklabels=False, visible=False),
        yaxis=dict(title=""),
        height=250,
        plot_bgcolor='white',
        margin=dict(l=120, r=30, t=50, b=30)
    )

    fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
