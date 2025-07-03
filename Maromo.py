import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
        import marimo as mo
    import pandas as pd
    import folium
    import plotly.graph_objects as go
    import plotly.express as px
    from folium.plugins import MarkerCluster
    """,
    name="_"
)


@app.cell
def _(pd):
    df = pd.read_csv('entorno_marimo/Docs/consumo.csv', sep=';')

    dfce = pd.read_csv('entorno_marimo/Docs/consumo_electricidad.csv', sep=';')

    dfcg = pd.read_csv('entorno_marimo/Docs/consumo_gas.csv', sep=';')

    dfcgsl = pd.read_csv('entorno_marimo/Docs/consumo_gsl.csv', sep=';')

    return df, dfce, dfcg, dfcgsl


@app.cell
def _(df, mo, pd):
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
def _(MarkerCluster, df, folium):
    df_clean = df.dropna(subset=['COORDENADA Y LATITUD', 'COORDENADA X LONGITUD'])

    # Crear mapa centrado en España
    m = folium.Map(
        location=[40.4637, -3.7492],  # Centro de España
        zoom_start=6,
        tiles='cartodbpositron'
    )

    # Crear un clúster de marcadores
    marker_cluster = MarkerCluster().add_to(m)

    # Añadir cada punto al clúster
    for _, row in df_clean.iterrows():
        folium.CircleMarker(
            location=[row['COORDENADA Y LATITUD'], row['COORDENADA X LONGITUD']],
            radius=9,  # tamaño del círculo
            color='#b22222',
            fill=True,
            fill_color='#e74c3c',
            fill_opacity=0.8,
            popup=row['CENTRO DE CONSUMO'],
            tooltip=row['CENTRO DE CONSUMO']
        ).add_to(marker_cluster)

    m
    return


@app.cell
def _(df, px):
    num_tipo_centros = df['TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA'].value_counts()

    num_tipo_centros_df = num_tipo_centros.reset_index()
    num_tipo_centros_df.columns = ['Tipo de Centro', 'Cantidad']

    fig2 = px.bar(
        num_tipo_centros_df,
        x='Tipo de Centro',
        y='Cantidad',
        color_discrete_sequence=['#df2d07'], 
        title='Nº Centros de Consumo Administración Autonómica'
    )

    fig2.update_layout(showlegend = False,
                      xaxis_title = None,
                      yaxis_title = None)
    fig2.update_traces(hovertemplate='%{x}<br>%{y}<extra></extra>')

    fig2
    return


@app.cell
def _(df, pd, px):
    agrupado = df.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")[["GSL", "CUPs GN", "CUPs E"]].sum().reset_index()

    agrupado = agrupado.rename(columns={
        "CUPs E": "Suma CUPs E",
        "CUPs GN": "Suma CUPs GN",
        "GSL": "Suma GSL"
    })

    agrupado["TOTAL"] = agrupado[["Suma GSL", "Suma CUPs GN", "Suma CUPs E"]].sum(axis=1)
    agrupado = agrupado.sort_values("TOTAL", ascending=True)

    melted = agrupado.melt(
        id_vars=["TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"],
        value_vars=["Suma CUPs E", "Suma CUPs GN", "Suma GSL"],  # <-- Aquí el orden que quieres en la barra
        var_name="Suministro",
        value_name="Cantidad"
    )

    orden_suministros = ["Suma CUPs E", "Suma CUPs GN", "Suma GSL"]
    melted["Suministro"] = pd.Categorical(melted["Suministro"], categories=orden_suministros, ordered=True)

    melted["TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"] = pd.Categorical(
        melted["TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"],
        categories=agrupado["TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"],
        ordered=True
    )

    fig3 = px.bar(
        melted,
        y="TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA",
        x="Cantidad",
        color="Suministro",
        orientation="h",
        barmode="stack",
        color_discrete_map={
            "Suma CUPs GN": "#ff926b",
            "Suma GSL": "#93d6c3",
            "Suma CUPs E": "#b1bce6"
        },
        title="Nº Suministros energéticos por tipo de centro"
    )

    fig3.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title=None,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig3.update_traces(hovertemplate='%{x}<br>%{y}<extra></extra>')

    fig3
    return


@app.cell
def _(dfce, dfcg, dfcgsl, pd):
    consumo_anual_electricidad = dfce.groupby('AÑO')['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'].sum().reset_index()
    consumo_anual_gas = dfcg.groupby('AÑO')['CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)'].sum().reset_index()
    consumo_anual_gls = dfcgsl.groupby('AÑO')['CONSUMO MENSUAL TOTAL GSL (M3) Gasóleo C'].sum().reset_index()
    consumo_anual_gd20 = dfcgsl.groupby('AÑO')['G.D. en Base 20'].sum().reset_index()
    consumo_anual_gd26 = dfcgsl.groupby('AÑO')['G.D. en Base 26'].sum().reset_index()

    consumo_anual_electricidad = consumo_anual_electricidad.rename(
        columns={'CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)': 'Consumo Electricidad (kWh/año)'}
    )
    consumo_anual_gas = consumo_anual_gas.rename(
        columns={'CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)': 'Consumo Gas (kWh/año)'}
    )
    consumo_anual_gls = consumo_anual_gls.rename(
        columns={'CONSUMO MENSUAL TOTAL GSL (M3) Gasóleo C': 'Consumo Gasóleo C (kWh/año)'}
    )
    consumo_anual_gd20 = consumo_anual_gd20.rename(
        columns={'G.D. en Base 20': 'Calefacción (GD20)'}
    )
    consumo_anual_gd26 = consumo_anual_gd26.rename(
        columns={'G.D. en Base 26': 'Calefacción (GD26)'}
    )

    tabla = consumo_anual_electricidad.merge(consumo_anual_gas, on='AÑO', how='outer')
    tabla = tabla.merge(consumo_anual_gls, on='AÑO', how='outer')
    tabla = tabla.merge(consumo_anual_gd20, on='AÑO', how='outer')
    tabla = tabla.merge(consumo_anual_gd26, on='AÑO', how='outer')

    tabla = tabla.sort_values('AÑO')
    tabla = tabla.fillna(0)

    totales = tabla[['Consumo Electricidad (kWh/año)', 
                     'Consumo Gas (kWh/año)', 
                     'Consumo Gasóleo C (kWh/año)',
                     'Calefacción (GD20)',
                     'Calefacción (GD26)']].sum()
    totales['AÑO'] = 'Total general'

    tabla_final = pd.concat([
        tabla,
        pd.DataFrame([totales])
    ], ignore_index=True)

    tabla_final
    return


@app.cell
def _(df, px):
    df_pie = df.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")["SUPERFICIE CONSTRUIDA"].sum().reset_index()

    fig4 = px.pie(
        df_pie,
        names="TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA",
        values="SUPERFICIE CONSTRUIDA",
        title="Superficie de centros de consumo por tipo de centro (m2)",
    )

    fig4.update_traces(
        textposition='outside',
        textinfo='label',
        textfont_size=18,        
        pull=[0.03]*len(df_pie),  
    )

    fig4.update_layout(
        showlegend=False,
        width=900,               
        height=700,              
        margin=dict(t=80, b=20, l=20, r=20),
        title_x=0.05,             
        font=dict(size=16)
    )

    fig4.update_traces(
        hovertemplate='%{percent}',  
        textposition='outside',
        textinfo='label',
    )

    fig4
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
