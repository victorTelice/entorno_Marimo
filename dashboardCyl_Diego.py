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
def _():

    import pandas as pd
    df_electric = pd.read_csv('cs_electric.csv' ,sep=';')
    df_energia=pd.read_csv('cs_energia.csv', sep=';')
    df_gas=pd.read_csv('cs_gas.csv', sep=';')
    df_gasoil = pd.read_csv(
        'cs_gasoil.csv',
        delimiter=';',
        encoding='utf-8',
    )
    #mo.ui.data_explorer(df_electric)

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
def _(df_energia, plt):
    #Primero se agrupan los datos en funcion del tipo de centro y el total de CUPS GN , GSL y CUPS E
    df_agrupado2 = df_energia.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA") [["CUPs E", "GSL","CUPs GN" ]].sum().sort_values("CUPs E", ascending=True)
    df_agrupado2.head()

    #ahora hacemos el grafico
    fig3, ax3 = plt.subplots(figsize=(10, 6))

    df_agrupado2.plot(kind="barh", stacked=True, ax=ax3, color=["coral", "mediumseagreen", "steelblue"])

    handles, labels =ax3.get_legend_handles_labels()
    ax3.legend(handles=handles, labels=labels, loc="lower right")

    #le añadimos las lineas de guia
    for x in range(0, 701, 100):
        ax3.axvline(x=x, color="gray", linestyle="--", linewidth=0.5, zorder=0)

    #Etiquetas
    ax3.set_xlabel("Número de suministros")
    ax3.set_ylabel("Tipo de centro a nivel de administración autonómica")

    plt.tight_layout()


    return (fig3,)


@app.cell
def _(df_energia, plt):
    ##grafico circular
    #Agrupar por tipo de centro y sumar la superficie
    df_superficie = df_energia.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")["SUPERFICIE CONSTRUIDA"].sum()



    # Ordenar de mayor a menor para mostrar mejor el gráfico
    df_superficie = df_superficie.sort_values(ascending=False)


    # Gráfico de pastel
    fig_pastel, ax4 = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts =ax4.pie(
        df_superficie,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 9},
        wedgeprops={"edgecolor": "white"},
        pctdistance=0.9,  # aleja los porcentajes
    
    )

    legend=ax4.legend(wedges, df_superficie.index, title="Tipo de centro", loc="center left", bbox_to_anchor=(1, 0.5))

    legend.get_title().set_fontweight('bold')




    plt.tight_layout()
    #plt.show()

    return fig_pastel, wedges


@app.cell
def _(df_electric, df_gas, df_gasoil, pd):
    ##primera tabla
    '''''
    print("tabla energia:")
    print(df_energia.columns)
    print("tabla electricidad:")
    print(df_electric.columns)
    print("tabla gas:")
    print(df_gas.columns)
    print("tabla gasoil:")
    print(df_gasoil.columns)
    '''''



    # Asegurarse de que los consumos son numéricos
    df_electric["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"] = pd.to_numeric(df_electric["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], errors="coerce")
    df_gas["CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)"] = pd.to_numeric(df_gas["CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)"], errors="coerce")
    df_gasoil["CONSUMO MENSUAL TOTAL GSL (M3)\nGasóleo C"] = pd.to_numeric(df_gasoil["CONSUMO MENSUAL TOTAL GSL (M3)\nGasóleo C"], errors="coerce")
    df_gasoil["G.D. en Base 20"] = pd.to_numeric(df_gasoil["G.D. en Base 20"], errors="coerce")
    df_gasoil["G.D. en Base 26"] = pd.to_numeric(df_gasoil["G.D. en Base 26"], errors="coerce")

    # Agrupar y sumar por año
    elec_anual = df_electric.groupby("AÑO")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum()
    gas_anual = df_gas.groupby("AÑO")["CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)"].sum()
    gasoil_anual = df_gasoil.groupby("AÑO")["CONSUMO MENSUAL TOTAL GSL (M3)\nGasóleo C"].sum()
    gd20_anual = df_gasoil.groupby("AÑO")["G.D. en Base 20"].sum()
    gd26_anual = df_gasoil.groupby("AÑO")["G.D. en Base 26"].sum()

    # Combinarlo todo en un solo DataFrame
    tabla = pd.concat(
        [elec_anual, gas_anual, gasoil_anual, gd20_anual, gd26_anual], axis=1
    ).fillna(0)

    # Renombrar columnas
    tabla.columns = [
        "Consumo Electricidad (kWh/año)",
        "Consumo Gas (kWh/año)",
        "Consumo Gasóleo C (kWh/año)",
        "Calefacción (GD20)",
        "Calefacción (GD26)"
    ]

    # Añadir fila de total general
    totales = pd.DataFrame(tabla.sum()).T
    totales.index = ["Total general"]
    tabla_final_evAnual = pd.concat([tabla, totales])

    # Mostrar en tabla bonita
    #import IPython.display as d





    # Formatear con separador de miles
    #tabla_formateada = tabla_final.applymap(lambda x: f"{int(round(x)):,}".replace(",", "."))
    return elec_anual, tabla_final_evAnual


@app.cell
def _(df_electric, df_energia, df_gas, df_gasoil, pd):
    ##tabla 2
    # Filtrar año 2024
    elec_2024 = df_electric[df_electric["AÑO"] == 2024]
    gas_2024 = df_gas[df_gas["AÑO"] == 2024]
    gasoil_2024 = df_gasoil[df_gasoil["AÑO"] == 2024]

    # Agrupar por tipo de centro
    consumo_elec = elec_2024.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum()
    consumo_gas = gas_2024.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")["CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)"].sum()
    consumo_gasoil = gasoil_2024.groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")["CONSUMO MENSUAL TOTAL GSL (M3)\nGasóleo C"].sum()

    # Nº de centros por tipo (de tabla energía, ya que contiene 1 fila por centro)
    centros_2024 = df_energia[df_energia["ID OPTE CENTRO DE CONSUMO"].isin(df_electric[df_electric["AÑO"] == 2024]["ID OPTE CENTRO DE CONSUMO"].unique())].groupby("TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA")["ID OPTE CENTRO DE CONSUMO"].nunique()

    # Unir todo
    tabla_2024 = pd.concat([centros_2024, consumo_elec, consumo_gas, consumo_gasoil], axis=1).fillna(0)
    tabla_2024.columns = ["Nº de centros", "Consumo Electricidad (kWh/año)", "Consumo Gas (kWh/año)", "Consumo Gasóleo C (kWh/año)"]

    # Añadir fila de total
    totals = pd.DataFrame(tabla_2024.sum()).T
    totals.index = ["Total"]
    tabla_2024_final = pd.concat([tabla_2024, totals])

    #d.display(tabla_2024_final)

    return (tabla_2024_final,)


@app.cell
def _(mo):
    mo.md(
        r"""
    <br>
    ##dataset de consumo energético:
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
def _(df_gas, plt):
    ##gráfico comparativa mensual consumo gas por año

    # Diccionario que vincula nombres de meses con su número
    meses_orden = {
        "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
        "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
        "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
    }


    # Asigna número de mes si lo tienes como texto
    df_gas["MES_NUM"] = df_gas["MES"].map(meses_orden)

    # Agrupa por AÑO y MES_NUM
    monthly_gas = df_gas.groupby(["AÑO", "MES_NUM"])["CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)"].sum().reset_index()

    # Pivot para que haya una columna por año
    pivot = monthly_gas.pivot(index="MES_NUM", columns="AÑO", values="CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)")
    pivot = pivot.sort_index()

    # Gráfico
    fig1_gas=plt.figure(figsize=(12, 6))
    for year in pivot.columns:
        plt.plot(pivot.index, pivot[year], marker="o", label=year)

    plt.xticks(ticks=range(1, 13), labels=range(1, 13))  # Eje X: 1 a 12
    plt.xlabel("Mes (número)")
    plt.ylabel("kWh/mes")
    plt.title("Comparativa mensual del consumo de gas por años")
    plt.legend(title="Año")
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    return (fig1_gas,)


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
def _(elec_anual, plt):
    ##grafico 1 consumo de electricidad


    fig_consumo_anual_elec, ax_elec = plt.subplots(figsize=(10, 6))
    ax_elec.bar(elec_anual.index.astype(str), elec_anual.values, color="mediumseagreen")

    ax_elec.set_title("Consumo anual de electricidad de la Administración de Castilla y León")
    ax_elec.set_ylabel("Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)")
    ax_elec.set_xlabel("FECHA")

    plt.tight_layout()
    #plt.show()
    return (fig_consumo_anual_elec,)


@app.cell
def _(df_electric, plt, wedges):
    ##grafico 2
    organismos= df_electric.groupby("ORGANISMO / CONSEJERÍA")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum()
    organismos= organismos.sort_values(ascending=False)

    fig_pastel_elec, ax_pastel_elec = plt.subplots(figsize=(8, 8))
    ax_pastel_elec.pie(organismos, autopct="%1.1f%%", startangle=90, wedgeprops={'edgecolor': 'white'})

    legend2=ax_pastel_elec.legend(wedges, organismos.index, title="Organismos", loc="center left", bbox_to_anchor=(1, 0.5))

    legend2.get_title().set_fontweight('bold')

    plt.tight_layout()
    #plt.show()
    return (fig_pastel_elec,)


@app.cell
def _(df_electric, plt, wedges):
    ##grafico 3
    tarifas = df_electric.groupby("TARIFA ELÉCTRICA")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum()
    tarifas=tarifas.sort_values(ascending=False)

    fig2_pastelelec, ax2_elecpastel = plt.subplots(figsize=(8, 8))
    ax2_elecpastel.pie(tarifas,  autopct="%1.1f%%", startangle=90, wedgeprops={'edgecolor': 'white'})

    legend3=ax2_elecpastel.legend(wedges, tarifas.index, title="Tarifas", loc="center left", bbox_to_anchor=(1, 0.5))

    legend3.get_title().set_fontweight('bold')

    plt.tight_layout()
    #plt.show()

    return (fig2_pastelelec,)


@app.cell
def _(df_electric, plt):
    ##grafico 4

    monthly = df_electric.groupby(["FECHA"])[
        ["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)", "G.D. en Base 20", "G.D. en Base 26"]
    ].sum().reset_index()



    #print(monthly)
    fig4_elec, ax4_elec = plt.subplots(figsize=(12, 6))

    ax4_elec.plot(monthly["FECHA"], monthly["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"], label="Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)", color="mediumseagreen")
    ax2_elec = ax4_elec.twinx()
    ax2_elec.plot(monthly["FECHA"], monthly["G.D. en Base 20"], label="Suma G.D. en Base 20", color="orangered")
    ax2_elec.plot(monthly["FECHA"], monthly["G.D. en Base 26"], label="Suma G.D. en Base 26", color="royalblue")

    ax4_elec.set_ylabel("Suma CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)")
    ax2_elec.set_ylabel("Suma G.D. en Base 20 / 26")
    ax4_elec.set_title("Evolución mensual del consumo eléctrico")

    fig4_elec.legend(loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3)
    plt.tight_layout()
    #plt.show()

    return (fig4_elec,)


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
def _(
    fig,
    fig1_gas,
    fig2,
    fig2_pastelelec,
    fig3,
    fig4_elec,
    fig_consumo_anual_elec,
    fig_pastel,
    fig_pastel_elec,
    mapa,
    mo,
    num_centros,
    num_electricidad,
    num_gas,
    num_gasoil,
    tabla_2024_final,
    tabla_final_evAnual,
):


    #objeto de pestaña de energia
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
            mo.md("**Nº Suministros energéticos por tipo de centro**"),
            fig3,
            mo.md("**Evolución anual de consumos energéticos con severidad climática en centros de la Administración autonómica**"),
            tabla_final_evAnual,
            mo.md("**Superficie de centros de consumo por tipo de centro (m2)**"),
            fig_pastel,
            mo.md("**Evolución del consumo energético por tipo de centro en 2024**"),
            tabla_2024_final


        ]
    )

    #objeto de pestaña gas 
    _gas = mo.vstack(
        [
            mo.md("**CONSUMO DE GAS**"),
            mo.md("**Comparativa mensual del consumo de gas por años**"),
            fig1_gas,


        ]
    )

    #objeto de pestaña electricidad
    _electric = mo.vstack(
        [
            mo.md("**CONSUMO DE ELECTRICIDAD**"),
        
            mo.md("**Consumo anual de electricidad de la Administración de Castilla y León**"),
            fig_consumo_anual_elec,
            mo.md("**Consumo de electricidad por Organismos de la Administración de Castilla y León**"),
            fig_pastel_elec,
            mo.md("**Consumo de electricidad por tipo de tarifa eléctrica de la Administración de Castilla y León**"),
            fig2_pastelelec,
            mo.md("Evolución mensual del consumo eléctrico"),
            fig4_elec,
        ]
    )

    #objeto de pestaña gasoil
    _gasoil=mo.vstack(
        [
            mo.md("**CONSUMO DE GASOIL**"),
            mo.md("Y esto sería más de lo mismo, introducir las gráficas, tablas y demás")
        ]
    )

    #llamamos al ui
    mo.ui.tabs(
        {
            "⚡Centros de consumo": _energia,
            "💡Consumo de electricidad": _electric,
            "🚭Consumo de gas": _gas,
            "🚗Consumo de gasoil":_gasoil
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
