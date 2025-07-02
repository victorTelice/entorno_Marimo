import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    📊Prueba para copiar un dashboard de datos energéticos de Castilla y León 📊
    <br>
    """
    )
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    ''''''
    import pandas as pd
    df_electric = pd.read_csv('cs_electric.csv' ,sep=';')
    df_energia=pd.read_csv('cs_energia.csv', sep=';')
    df_gas=pd.read_csv('cs_gas.csv', sep=';')
    df_gasoil = pd.read_csv(
        'cs_gasoil.csv',
        delimiter=';',
        encoding='utf-8',
    )
    mo.ui.data_explorer(df_electric)
    ''''''
    return df_electric, df_energia, df_gas, df_gasoil, pd


@app.cell
def _(mo):
    mo.md(r"""<span style="color:red; font-size:30px;font-weight:bold;">DATAHUB energético de la Administración autónoma de Castilla y León</span>""")
    return


@app.cell
def _(df_energia, pd):
    ##Codigo que realiza el mapa
    import folium

    #Asegurar que las columnas clave están en formato numérico
    df_energia["COORDENADA Y LATITUD"] = pd.to_numeric(df_energia["COORDENADA Y LATITUD"], errors='coerce')
    df_energia["COORDENADA X LONGITUD"] = pd.to_numeric(df_energia["COORDENADA X LONGITUD"], errors='coerce')

    df_agrupado = df_energia.groupby("MUNICIPIO DIRECCIÓN").agg({
        "COORDENADA Y LATITUD": "mean",
        "COORDENADA X LONGITUD": "mean"
    }).reset_index()

    df_agrupado["num_centros"] = df_energia.groupby("MUNICIPIO DIRECCIÓN").size().values
    df_agrupado = df_agrupado.dropna(subset=["COORDENADA Y LATITUD", "COORDENADA X LONGITUD"])

    #Crear el mapa centrado en Castilla-Y León
    mapa = folium.Map(location=[41.6, -4.7], zoom_start=7)

    #Añadir los círculos proporcionales
    for _, row in df_agrupado.iterrows():
        folium.CircleMarker(
            location=[row["COORDENADA Y LATITUD"], row["COORDENADA X LONGITUD"]],
            radius=max(row["num_centros"] ** 0.5,3),  # escala visual (ajustable)
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.6,
            popup=f"{row["MUNICIPIO DIRECCIÓN"]}: {row['num_centros']} centros",
            tooltip=f"{row["MUNICIPIO DIRECCIÓN"]}: {row['num_centros']} centros"
        ).add_to(mapa)

    #Mostrar o guardar el mapa
    mapa.save("mapa_centros.html")  # puedes abrirlo en el navegador

    html_code = mapa._repr_html_()  # obtiene el HTML del mapa
    #mapa

    return (mapa,)


@app.cell
def _(df_energia):
    import matplotlib.pyplot as plt

    # Indicadores
    num_centros = len(df_energia)
    num_electricidad = df_energia["CUPs E"].sum()
    num_gas = df_energia["CUPs GN"].sum()
    num_gasoil = df_energia["GSL"].sum()


    # Gráfico de barras 1
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Electricidad', 'Gas Natural', 'Gasóleo'],
           [num_electricidad, num_gas, num_gasoil],
           color=['blue', 'green', 'red'])
    ax.set_title('Número de suministros por tipo de energía')
    ax.set_ylabel('Cantidad')
    fig.tight_layout()

    return fig, num_centros, num_electricidad, num_gas, num_gasoil, plt


@app.cell
def _(df_energia, plt):
    # Agrupar por tipo de centro y contar
    conteo = df_energia["TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"].value_counts().sort_values(ascending=False)

    # Gráfico de barras 2
    plt.figure(figsize=(12, 6))
    bars = plt.bar(conteo.index, conteo.values, color='coral')

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.bar(conteo.index, conteo.values, color='coral')
    ax2.set_ylabel("Recuento")
    ax2.set_xlabel("Tipo de centro")
    ax2.tick_params(axis='x', rotation=45)
    fig2.tight_layout()
    return (fig2,)


@app.cell
def _(mo):
    mo.md(
        r"""
    <br>
    #dataset de consumo energético:
    <br>
    """
    )
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
def _(mo):
    mo.md(
        r"""
    <br>
    ##dataset de consumo de gas:
    <br>
    """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        SELECT * FROM 'cs_gas.csv'
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    <br>
    ##dataset de consumo de electricidad:
    <br>
    """
    )
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
def _(mo):
    mo.md(
        r"""
    <br>
    ##Pestañas con las tablas 
    <br>
    """
    )
    return


@app.cell
def _(df_electric, df_energia, df_gas, df_gasoil, mo):

    # Crear pestañas
    tabs = mo.ui.tabs({
        "Energía": mo.md(df_energia.head().to_markdown()),
        "Electricidad": mo.md(df_electric.head().to_markdown()),
        "Gas": mo.md(df_gas.head().to_markdown()),
        "Gasoil": mo.md(df_gasoil.head().to_markdown()),
    })

    tabs

    return


@app.cell
def _(mo):
    mo.md(
        r"""
    <br>
    <br>
    #A PARTIR DE AQUÍ SON LAS PESTAÑAS CON LOS GRÁFICOS 🧑‍🎨
    """
    )
    return


@app.cell
def _(fig, fig2, mapa, mo, num_centros, num_electricidad, num_gas, num_gasoil):



    _energia = mo.vstack(
        [

            mo.md("**CENTROS DE CONSUMO ENERGÉTICO**"),
            mo.hstack(
                [
                    mo.md(f"- N° de centros: **{num_centros}**"),
                    mo.md(f"- Electricidad: **{num_electricidad}**"),
                    mo.md(f"- Gas Natural: **{num_gas}**"),
                    mo.md(f"- Gasóleo: **{num_gasoil}**"),
                ]
            ),
            mo.md("**Número de suministros energéticos**"),
            fig,
            mo.md("**Número de centros de consumo de la Administración autonómica (mapa)**"),
            mapa,
            mo.md(" **Nº Centros de Consumo Administración Autonómica** "),
            fig2,
      

        ]
    )

    _gas = mo.vstack(
        [
            mo.md("**Consumo Gas**"),


        ]
    )

    _electric = mo.vstack(
        [
            mo.md("**Consumo Electricidad**")
        ]
    )

    _gasoil=mo.vstack(
        [
            mo.md("**Consumo Gasoil**")
        ]
    )

    mo.ui.tabs(
        {
            "⚡Energía": _energia,
            "🚭 Gas": _gas,
            "💡 Electricidad": _electric,
            "🚗 Gasoil":_gasoil
        }
    )
    return


@app.cell
def _():


    #df = pd.read_csv( 'cs_gasoil.csv', sep=';', encoding='utf-8' )
    #df

    return


if __name__ == "__main__":
    app.run()
