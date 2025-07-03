import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""#🔌Consumo de electricidad """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM 'cs_electric.csv'
        """
    )
    return


@app.cell
def _():
    import pandas as pd
    import plotly.express as px

    # Cargar el CSV
    df = pd.read_csv("cs_electric.csv", sep=';', encoding='utf-8')

    # Asegurar tipo numérico
    df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"] = pd.to_numeric(
        df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce"
    )

    # Convertir columna de fecha a datetime
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    # Extraer año
    df["AÑO"] = df["FECHA"].dt.year

    # Agrupar por año y sumar consumo
    df_agrupado = df.groupby("AÑO")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum().reset_index()

    # Graficar
    fig = px.bar(
        df_agrupado,
        x="AÑO",
        y="CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)",
        text_auto=".2s",
        labels={
            "AÑO": "FECHA",
            "CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)": "Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"
        },
        title="Consumo anual de electricidad de la Administración de Castilla y León",
        color_discrete_sequence=["mediumseagreen"] 
    )

    fig.update_layout(
        title_text="CONSUMO DE ELECTRICIDAD",
        yaxis_title="Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)",
        xaxis_title="FECHA",
    
        height=500
    )

    fig.show()
    fig

    return df, pd, px


@app.cell
def _(df, pd, px):
    import matplotlib.pyplot as plt

    # Asegurar que los valores son numéricos
    df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"] = pd.to_numeric(
        df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce"
    )

    # Agrupar por organismo
    df_organismos = df.groupby("ORGANISMO / CONSEJERÍA")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum().reset_index()

    # Ordenar de mayor a menor (opcional para visual más clara)
    df_organismos = df_organismos.sort_values(by="CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)", ascending=False)

    # Crear gráfico de pastel
    fig1 = px.pie(
        df_organismos,
        names="ORGANISMO / CONSEJERÍA",
        values="CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)",
        title="Consumo de electricidad por Organismos de la Administración de Castilla y León",
        hole=0,  # 0 = tarta clásica, >0 = dona
    )

    # Mostrar % y valor absoluto en tooltip
    fig1.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Consumo: %{value:,.0f} kWh<br>Porcentaje: %{percent}"
    )
    fig1.update_layout(height=500)
    fig1.show()
    fig1

    return


@app.cell
def _(df, pd):

    import folium
    from folium.plugins import HeatMap


    # Asegurar que las columnas relevantes sean numéricas
    df["LATITUD"] = pd.to_numeric(df["COORDENADA Y LATITUD"], errors="coerce")
    df["LONGITUD"] = pd.to_numeric(df["COORDENADA X LONGITUD"], errors="coerce")
    df["CONSUMO"] = pd.to_numeric(df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce")

    # Filtrar filas válidas
    filas = df.dropna(subset=["LATITUD", "LONGITUD", "CONSUMO"])

    # Crear mapa centrado en Castilla y León
    m = folium.Map(location=[41.65, -4.75], zoom_start=7)

    # Añadir capa de calor (lat, lon, peso)
    heat_data = filas[["LATITUD", "LONGITUD", "CONSUMO"]].values.tolist()
    HeatMap(heat_data, radius=15, blur=20, max_zoom=10).add_to(m)

    # Mostrar el mapa en notebook (Jupyter / Marimo)
    m

    return


@app.cell
def _(df, pd):
    import plotly.graph_objects as go

    # Asegurar tipos
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df["CONSUMO"] = pd.to_numeric(df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce")
    df["GD_20"] = pd.to_numeric(df["G.D. en Base 20"], errors="coerce")
    df["GD_26"] = pd.to_numeric(df["G.D. en Base 26"], errors="coerce")

    # Agrupamos por mes por seguridad
    mes = df.groupby("FECHA")[["CONSUMO", "GD_20", "G.D. en Base 26"]].sum().reset_index()

    # Crear figura con dos ejes Y
    fig2 = go.Figure()

    # Línea verde (consumo eléctrico)
    fig2.add_trace(go.Scatter(
        x=mes["FECHA"], y=mes["CONSUMO"],
        mode='lines',
        name="Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)",
        line=dict(color="green"),
        yaxis="y1"
    ))

    # Línea naranja (GD Base 20)
    fig2.add_trace(go.Scatter(
        x=mes["FECHA"], y=mes["GD_20"],
        mode='lines',
        name="Suma G.D. en Base 20",
        line=dict(color="orange"),
        yaxis="y2"
    ))

    # Línea azul (GD Base 26)
    fig2.add_trace(go.Scatter(
        x=mes["FECHA"], y=mes["G.D. en Base 26"],
        mode='lines',
        name="Suma G.D. en Base 26",
        line=dict(color="blue"),
        yaxis="y2"
    ))

    # Configurar ejes
    fig2.update_layout(
        title="Evolución mensual del consumo eléctrico",
        xaxis_title="FECHA",
    
        yaxis=dict(
        title=dict(text="Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)", font=dict(color="green")),
        tickfont=dict(color="green"),
        side="left"
    ),
    yaxis2=dict(
        title=dict(text="Suma G.D. en Base 20 / 26", font=dict(color="orange")),
        tickfont=dict(color="orange"),
        overlaying="y",
        side="right"
    ),
         legend=dict(
            x=1.05,     # Más allá del borde derecho
            y=1,        # Arriba del todo
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0)',  # Fondo transparente
            borderwidth=0
        )
    )

    fig2.show()
    fig2
    return


@app.cell
def _(df, pd, px):

    # Asegurar tipos correctos
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df["CONSUMO"] = pd.to_numeric(df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce")

    # Extraer mes y año
    df["AÑO"] = df["FECHA"].dt.year
    df["MES"] = df["FECHA"].dt.month

    # Agrupar por año y mes
    ano_mes = df.groupby(["AÑO", "MES"])["CONSUMO"].sum().reset_index()

    # Gráfico de líneas
    fig3 = px.line(
        ano_mes,
        x="MES",
        y="CONSUMO",
        color="AÑO",
        markers=True,
        labels={
            "MES": "Mes",
            "CONSUMO": "kWh/mes",
            "AÑO": "Año"
        },
        title="Comparativa mensual del consumo eléctrico por años"
    )

    # Ajustar diseño
    fig3.update_layout(
        height=500,
        legend=dict(
            x=1.05, y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    fig3.show()
    fig3
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM 'cs_energia.csv'
        """
    )
    return


@app.cell
def _(df, mo, pd):

    # Aseguramos que los datos estén en el formato adecuado
    df["CUPS ELECTRICIDAD"] = pd.to_numeric(df["CUPS ELECTRICIDAD"], errors="coerce")
    df["CONSUMO"] = pd.to_numeric(df["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce")
    df["TIPO_PUNTO"] = df["TIPO DE PUNTO DE MEDIDA"].fillna("(sin punto de medida)")

    # Agrupar por tipo de punto
    tabla = df.groupby("TIPO_PUNTO").agg(
        CUPS_E=("CUPS ELECTRICIDAD", "sum"),
        CONSUMO_ELEC=("CONSUMO", "sum")
    ).reset_index()

    # Totales
    total_cups = tabla["CUPS_E"].sum()
    total_consumo = tabla["CONSUMO_ELEC"].sum()

    # Porcentajes
    tabla["% CUPS"] = tabla["CUPS_E"] / total_cups * 100
    tabla["% CONSUMO"] = tabla["CONSUMO_ELEC"] / total_consumo * 100

    # Fila de total general
    fila_total = pd.DataFrame([{
        "TIPO_PUNTO": "Total general",
        "CUPS_E": total_cups,
        "CONSUMO_ELEC": total_consumo,
        "% CUPS": None,
        "% CONSUMO": None
    }])

    tabla_final = pd.concat([tabla, fila_total], ignore_index=True)

    # Formato visual
    tabla_final["CUPS_E"] = tabla_final["CUPS_E"].apply(lambda x: f"{int(x):,}".replace(",", ".") if pd.notna(x) else "")
    tabla_final["CONSUMO_ELEC"] = tabla_final["CONSUMO_ELEC"].apply(lambda x: f"{int(x):,}".replace(",", ".") if pd.notna(x) else "")
    tabla_final["% CUPS"] = tabla_final["% CUPS"].apply(lambda x: f"{x:.2f} %" if pd.notna(x) else "")
    tabla_final["% CONSUMO"] = tabla_final["% CONSUMO"].apply(lambda x: f"{x:.2f} %" if pd.notna(x) else "")

    # Renombrar columnas para mostrar
    tabla_final.columns = [
        "Puntos de medida",
        "Nº de CUPS Electricidad",
        "% de CUPS",
        "Consumo electricidad (kWh)",
        "% consumo"
    ]

    mo.md("### Puntos de medida eléctricos")
    tabla_final
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
