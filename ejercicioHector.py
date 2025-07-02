import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import folium
    return folium, mo, pd, plt


@app.cell
def _(mo):
    mo.md(r"""#Tabla del consumo de gas""")
    return


@app.cell
def _(mo):
    consumo_gas = mo.sql(
        f"""
        SELECT * FROM 'consumo-de-gas-en-centros-de-la-administracion-autonomica-de-castilla-y-leon.csv'
        """
    )
    return (consumo_gas,)


@app.cell
def _(consumo_gas):
    municipios_gas_natural=consumo_gas['CUPS GAS NATURAL'].value_counts()

    dato_gas=len(municipios_gas_natural)
    return (dato_gas,)


@app.cell
def _(folium, pd):
    # Cargar el archivo CSV
    consumo_energetico = pd.read_csv(
        "centros-de-consumo-energetico-de-la-administracion-autonoma-de-castilla-y-leon.csv",
        sep=';', encoding='utf-8', engine='python'
    )

    # Renombrar columnas para facilitar el acceso
    consumo_energetico = consumo_energetico.rename({
        'COORDENADA X LONGITUD': 'longitud',
        'COORDENADA Y LATITUD': 'latitud'
    }, axis=1)

    # Eliminar filas con coordenadas no válidas
    consumo_energetico['longitud'] = pd.to_numeric(consumo_energetico['longitud'], errors='coerce')
    consumo_energetico['latitud'] = pd.to_numeric(consumo_energetico['latitud'], errors='coerce')

    # Filtrar coordenadas dentro del rango geográfico de Castilla y León
    consumo_energetico = consumo_energetico[
        (consumo_energetico['longitud'] >= -10) & (consumo_energetico['longitud'] <= 5) &
        (consumo_energetico['latitud'] >= 35) & (consumo_energetico['latitud'] <= 45)
    ]

    # Eliminar duplicados
    coordenadas_unicas = consumo_energetico[['latitud', 'longitud']].drop_duplicates()

    # Crear el mapa centrado en Castilla y León
    mapa = folium.Map(location=[41.65, -4.72], zoom_start=7)

    # Añadir marcadores
    for _, row in coordenadas_unicas.iterrows():
        folium.Marker(location=[row['latitud'], row['longitud']]).add_to(mapa)

    # Guardar el mapa como archivo HTML
    mapa.save("mapa_centros_consumo.html")

    return consumo_energetico, mapa


@app.cell
def _(mo):
    mo.md(r"""#Tabla del consumo energético""")
    return


@app.cell
def _(consumo_energetico):
    consumo_energetico
    return


@app.cell
def _(consumo_energetico):
    numero_centros_consumo = consumo_energetico['CENTRO DE CONSUMO'].value_counts()
    dato_centros=len(numero_centros_consumo)
    return (dato_centros,)


@app.cell
def _(mo):
    mo.md(r"""#Tabla del consumo de electricidad""")
    return


@app.cell
def _(mo):
    consumo_electricidad = mo.sql(
        f"""
        SELECT * FROM 'consumo-de-electricidad-en-centros-de-la-administracion-autonomica-de-castilla-y.csv'
        """
    )
    return (consumo_electricidad,)


@app.cell
def _(consumo_electricidad):
    numero_cups_electricidad=consumo_electricidad['CUPS ELECTRICIDAD'].value_counts()
    dato_electricidad=len(numero_cups_electricidad)
    return (dato_electricidad,)


@app.cell
def _(pd):
    consumo_gasoil= pd.read_csv(
        "consumo-de-gasoil-en-centros-de-educacion-y-sanidad-de-la-administracion-autonom.csv",
        sep=';',  # Delimitador usado en el archivo
        encoding='utf-8',  # Codificación estándar
        engine='python'  # Motor flexible para parsing
    )

    return (consumo_gasoil,)


@app.cell
def _(mo):
    mo.md(r"""#Tabla del consumo de gasoil""")
    return


@app.cell
def _(consumo_gasoil):
    consumo_gasoil
    return


@app.cell
def _(consumo_gasoil):
    numero_centros_gasoil=consumo_gasoil['CENTRO DE CONSUMO'].value_counts()
    dato_gasoil=len(numero_centros_gasoil)
    return (dato_gasoil,)


@app.cell
def _(mo):
    mo.md(r"""#RESUMEN DE DATOS""")
    return


@app.cell
def _(dato_centros, dato_electricidad, dato_gas, dato_gasoil, mo):
    centro=mo.stat(value=dato_centros,caption="Total de centros")
    electricidad=mo.stat(value=dato_electricidad,caption="Nº suministros electricidad")
    gas=mo.stat(value=dato_gas,caption="Nº CUPs GN")
    gasoleo=mo.stat(value=dato_gasoil,caption="Nº centros con gasóleo")

    info =[centro,electricidad,gas,gasoleo]
    mo.hstack(info,justify="space-around", gap="2rem")
    return


@app.cell
def _(dato_centros, dato_electricidad, dato_gas, dato_gasoil, plt):
    datos=[dato_centros,dato_electricidad,dato_gas, dato_gasoil]
    etiquetas=["Centros","Electricidad","Gas","Gasoil"]

    plt.figure(figsize=(10, 6))
    plt.barh(etiquetas, datos, color='skyblue')
    plt.xlabel("Cantidad de valores únicos")
    plt.title("Nº de suministros energéticos")
    plt.tight_layout()
    plt.show()

    return


@app.cell
def _(consumo_energetico):
    # Renombrar columnas para facilitar el acceso

    modificacion_consumo_energetico = consumo_energetico.rename({
        'COORDENADA X LONGITUD': 'longitud',
        'COORDENADA Y LATITUD': 'latitud'
    })


    return


@app.cell
def _(mo):
    mo.md(r"""##Número de centros de consumo de la Administración autonómica (mapa)""")
    return


@app.cell
def _(mapa):
    mapa
    return


@app.cell
def _(consumo_energetico, plt):
    # Contar la cantidad de centros por tipo
    conteo_por_tipo = consumo_energetico['TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA'].value_counts()

    # Crear la gráfica de barras verticales
    plt.figure(figsize=(10, 6))
    conteo_por_tipo.plot(kind='bar', color='red')
    plt.title('Cantidad de centros por Tipo de administración autonómica')
    plt.xlabel('Tipo de centro')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return


@app.cell
def _(consumo_energetico, plt):

    # Agrupar por tipo de centro y sumar las columnas numéricas
    suma_por_tipo = consumo_energetico.groupby('TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA')[['CUPs E', 'CUPs GN', 'GSL']].sum()

    # Ordenar por la suma de 'CUPs E' de mayor a menor
    suma_por_tipo_ordenado = suma_por_tipo.sort_values(by='CUPs E', ascending=True)

    # Crear gráfico de barras horizontales apiladas
    plt.figure(figsize=(10, 6))
    suma_por_tipo_ordenado.plot(kind='barh', stacked=True, colormap='Set2')
    plt.title('Nº Suministros energéticos por tipo de centro')
    plt.xlabel('Cantidad total')
    plt.ylabel('TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA')
    plt.legend(title='Tipo de suministro')
    plt.tight_layout()
    plt.show()

    return


if __name__ == "__main__":
    app.run()
