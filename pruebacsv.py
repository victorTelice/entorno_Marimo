import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    centros = mo.sql(
        f"""
        SELECT * FROM 'centros-de-consumo-energetico-de-la-administracion-autonoma-de-castilla-y-leon.csv'
        """
    )
    return


@app.cell
def _(mo):
    import pandas as pd
    df = pd.read_csv('centros-de-consumo-energetico-de-la-administracion-autonoma-de-castilla-y-leon.csv', sep=';')
    visual=mo.ui.data_explorer(df)
    visual
    num=len(df)
    df["CUPs E"] = pd.to_numeric(df["CUPs E"], errors="coerce")
    num_suministros = df["CUPs E"].sum()
    df["CUPs GN"] = pd.to_numeric(df["CUPs GN"], errors="coerce")
    num_suministros_gas=df["CUPs GN"].sum()
    df["GSL"] = pd.to_numeric(df["GSL"], errors="coerce")
    num_suministros_gasol=df["GSL"].sum()

    return (
        df,
        num,
        num_suministros,
        num_suministros_gas,
        num_suministros_gasol,
        pd,
    )


@app.cell
def _(mo, num, num_suministros, num_suministros_gas, num_suministros_gasol):
    mo.md(f"""Centros de consumo energético\n\nNum centros: {num}\n\nNum Suministros electricos: {num_suministros}\n\nNum Suministros gas natural: {num_suministros_gas}\n\nNum Suministros gasoleo: {num_suministros_gasol}""")
    return


@app.cell
def _(df, pd):
    import plotly.express as px
    resumen = pd.DataFrame({
        "Tipo": ["Electricidad", "Gas", "Gasóleo"],
        "Suministros": [
            df["CUPs E"].sum(),
            df["CUPs GN"].sum(),
            df["GSL"].sum()
        ]
    })
    fig = px.bar(
        resumen,
        x="Suministros",
        y="Tipo",
        orientation="h",
        text="Suministros",
        color="Tipo",
        color_discrete_sequence=["#b70e28", "#b70e28", "#b70e28"]
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="start",
        marker_line_color="white",
        marker_line_width=1.5,
        textfont=dict(color="white", size=14)
    )

    fig.update_layout(
        title="Número de suministros energéticos",
        xaxis=dict(showgrid=False),
        yaxis=dict(categoryorder="total ascending"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        bargap=0.3,
        height=300
    )

    fig.show()
    return (px,)


@app.cell
def _(df, pd):
    import folium
    from folium.plugins import MarkerCluster


    # Asegúrate de que las coordenadas estén bien
    df["COORDENADA X LONGITUD"] = pd.to_numeric(df["COORDENADA X LONGITUD"], errors='coerce')
    df["COORDENADA Y LATITUD"] = pd.to_numeric(df["COORDENADA Y LATITUD"], errors='coerce')
    #df.dropna(subset=["COORDENADA X LONGITUD", "COORDENADA Y LATITUD"])
    df2 = df.dropna(subset=["COORDENADA X LONGITUD", "COORDENADA Y LATITUD"])
    # Crear el mapa centrado en Castilla y León
    m = folium.Map(location=[41.65, -4.72], zoom_start=7)

    # Crear un cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Añadir cada centro de consumo al cluster
    for idx, row in df2.iterrows():
        folium.Marker(
            location=[row["COORDENADA Y LATITUD"], row["COORDENADA X LONGITUD"]],
            popup=row["CENTRO DE CONSUMO"]
        ).add_to(marker_cluster)

    # Mostrar el mapa
    m

    return


@app.cell
def _(df, px):
    centros_por_tipo = df["TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"].value_counts().reset_index()
    centros_por_tipo.columns = ["TIPO_CENTRO", "Recuento"]

    fig2 = px.bar(
        centros_por_tipo,
        x="TIPO_CENTRO",
        y="Recuento",
        title="N° Centros de Consumo Administración Autonómica",
        labels={"TIPO_CENTRO": "TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"},
        color_discrete_sequence=["#f47d42"],  # color parecido al de la imagen
    )
    fig2.update_layout(
        xaxis_tickangle=-45,
        legend_title_text="",  # Oculta "Recuento"
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
    )
    fig2.show()
    return


@app.cell
def _(df):
    agrupado = df.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")[["CUPs E", "CUPs GN", "GSL"]].sum().reset_index()
    agrupado.rename(columns={
        "TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA": "Tipo Centro",
        "CUPs E": "Suma CUPs E",
        "CUPs GN": "Suma CUPs GN",
        "GSL": "Suma GSL"
    }, inplace=True)
    df_long = agrupado.melt(
        id_vars="Tipo Centro",
        value_vars=["Suma CUPs E", "Suma CUPs GN", "Suma GSL"],
        var_name="Tipo Suministro",
        value_name="Cantidad"
    )
    return (df_long,)


@app.cell
def _(df_long, px):

    fig3 = px.bar(
        df_long,
        x="Cantidad",
        y="Tipo Centro",
        color="Tipo Suministro",
        orientation="h",
        title="Nº Suministros energéticos por tipo de centro",
        color_discrete_sequence=["#98B4D4", "#F79A83", "#7BB09E"]  # Colores similares
    )

    fig3.update_layout(barmode="stack")
    fig3.show()
    return


@app.cell
def _(df, pd):

    import matplotlib.pyplot as plt

    # Agrupar y ordenar la superficie construida por tipo de centro
    df['SUPERFICIE CONSTRUIDA'] = pd.to_numeric(df['SUPERFICIE CONSTRUIDA'], errors='coerce')
    df_grouped = df.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA").sum(numeric_only=True)
    df_superficie = df_grouped["SUPERFICIE CONSTRUIDA"].sort_values(ascending=False)

    # Función para mostrar % y valor absoluto
    def autopct_func(pct):
        total = df_superficie.sum()
        valor = int(round(pct * total / 100.0))
        return f"{pct:.1f}%\n({valor:,} m²)"

    # Crear gráfico de tarta
    plt.figure(figsize=(10, 8))
    plt.pie(
        df_superficie,
        labels=df_superficie.index,
        autopct=autopct_func,
        startangle=90,
        counterclock=False
    )
    plt.title("Superficie de centros de consumo por tipo de centro (m²)")
    plt.axis("equal")  # Mantiene forma circular
    plt.tight_layout()
    plt.show()

    return


if __name__ == "__main__":
    app.run()
