import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    import folium
    from folium.plugins import HeatMap

    import io

    return HeatMap, folium, io, mdates, mo, pd, plt


@app.cell
def _(figura_circular, io):

    buf = io.BytesIO()
    figura_circular.savefig(buf, format="png")
    buf.seek(0)
    img_bytes = buf.read()

    return


@app.cell
def pestanhas(
    centros_consumo_energetico,
    consumo_electricidad,
    consumo_energetico,
    consumo_gas,
    consumo_gasoil,
    figura1,
    figura_circular,
    figura_circular_electricidad,
    grafica_electricidad_anual,
    grafica_electricidad_mensual,
    grafica_electricidad_tarifas,
    grafica_sumas,
    mapa,
    mapa_calor,
    numero_suministros_energeticos,
    tabla_año,
    tabla_consumos_centros,
):
    tab1 = centros_consumo_energetico, numero_suministros_energeticos, mapa, figura1, grafica_sumas, tabla_año, figura_circular, tabla_consumos_centros

    tab2 = grafica_electricidad_anual, figura_circular_electricidad, grafica_electricidad_tarifas, mapa_calor, grafica_electricidad_mensual

    tab3 = consumo_gasoil, consumo_electricidad, consumo_energetico, consumo_gas
    return tab1, tab2, tab3


@app.cell
def usuario(mo, tab1, tab2, tab3):

    # cell: b
    mo.ui.tabs({
        "Consumo Energético": tab1,
        "Consumo_Electricidad": tab2,
        "Conjunto_de_Datos": tab3
    })

    return


@app.cell
def map(folium, pd, plt):
    # Cargar el archivo CSV
    consumo_energetico = pd.read_csv(
        "centros-de-consumo-energetico-de-la-administracion-autonoma-de-castilla-y-leon.csv",
        sep=';', encoding='utf-8', engine='python'
    )


    # Verificar que la columna de tipo de centro a nivel de administración autonómica existe
    columna_tipo = "TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA"
    if columna_tipo in consumo_energetico.columns:
        # Contar la cantidad de centros por tipo
        conteo_por_tipo1 = consumo_energetico[columna_tipo].value_counts()

        # Crear la figura y el eje
        figura1, axis = plt.subplots(figsize=(10, 6))
        barras1 = axis.bar(conteo_por_tipo1.index, conteo_por_tipo1.values, color='red')

        # Títulos y etiquetas
        axis.set_title('Cantidad de centros por Tipo de administración autonómica')
        axis.set_xlabel('Tipo de centro')
        axis.set_ylabel('Cantidad')
        axis.set_xticks(range(len(conteo_por_tipo1)))
        axis.set_xticklabels(conteo_por_tipo1.index, rotation=45, ha='right')



    # Eliminar bordes superiores y derechos
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)

        # Devolver la figura para que Marimo la renderice correctamente

    else:
        print(f"La columna '{columna_tipo}' no se encuentra en el archivo.")

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

    return consumo_energetico, figura1, mapa


@app.cell
def _(pd):
    consumo_gas = pd.read_csv('consumo-de-gas-en-centros-de-la-administracion-autonomica-de-castilla-y-leon.csv', sep=";")
    return (consumo_gas,)


@app.cell
def _(consumo_gas):
    municipios_gas_natural=consumo_gas['CUPS GAS NATURAL'].value_counts()

    dato_gas=len(municipios_gas_natural)
    return (dato_gas,)


@app.cell
def _(consumo_energetico):
    numero_centros_consumo = consumo_energetico['CENTRO DE CONSUMO'].value_counts()
    dato_centros=len(numero_centros_consumo)
    return (dato_centros,)


@app.cell
def _(pd):
    consumo_electricidad = pd.read_csv('consumo-de-electricidad-en-centros-de-la-administracion-autonomica-de-castilla-y.csv', sep=";")
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
def _(consumo_gasoil):
    numero_centros_gasoil=consumo_gasoil['CENTRO DE CONSUMO'].value_counts()
    dato_gasoil=len(numero_centros_gasoil)
    return (dato_gasoil,)


@app.cell
def consumo1(dato_centros, dato_electricidad, dato_gas, dato_gasoil, mo):
    centro=mo.stat(value=dato_centros,caption="Total de centros")
    electricidad=mo.stat(value=dato_electricidad,caption="Nº suministros electricidad")
    gas=mo.stat(value=dato_gas,caption="Nº CUPs GN")
    gasoleo=mo.stat(value=dato_gasoil,caption="Nº centros con gasóleo")

    info =[centro,electricidad,gas,gasoleo]
    centros_consumo_energetico=mo.hstack(info,justify="space-around", gap="2rem")
    return (centros_consumo_energetico,)


@app.cell
def consumo2(dato_electricidad, dato_gas, dato_gasoil, plt):
    datos=[dato_electricidad,dato_gas, dato_gasoil]
    etiquetas=["Electricidad","Gas","Gasoil"]


    fig, ax = plt.subplots()
    bars = ax.barh(etiquetas, datos, color='red')



    for bar, etiqueta in zip(bars, etiquetas):
        ax.text(bar.get_x() + 10, bar.get_y() + bar.get_height()/2, etiqueta,
                va='center', ha='left', color='white', fontsize=10)

    # Añadir valores al extremo derecho dentro de la barra
    for bar in bars:
        ax.text(bar.get_width() - 10, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width():.0f}', va='center', ha='right', color='white', fontsize=10)



    ax.axis('off')

    plt.xlabel("Cantidad de valores únicos")
    numero_suministros_energeticos=plt.title("Nº de suministros energéticos")


    return (numero_suministros_energeticos,)


@app.cell
def _(consumo_energetico, plt):

    # Agrupar por tipo de centro y sumar las columnas numéricas
    suma_por_tipo = consumo_energetico.groupby('TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA')[['CUPs E', 'CUPs GN', 'GSL']].sum()

    # Ordenar por la suma de 'CUPs E' de mayor a menor
    suma_por_tipo_ordenado = suma_por_tipo.sort_values(by='CUPs E', ascending=True)

    # Crear gráfico de barras horizontales apiladas
    plt.figure(figsize=(10, 6))
    suma_por_tipo_ordenado.plot(kind='barh', stacked=True, colormap='Set1')
    plt.title('Nº Suministros energéticos por tipo de centro')
    plt.xlabel('Cantidad total')
    plt.ylabel('TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA')
    grafica_sumas=plt.legend(title='Tipo de suministro')


    return (grafica_sumas,)


@app.cell
def _(consumo_electricidad, consumo_gas, consumo_gasoil, pd):

    consumo_electricidad.columns = consumo_electricidad.columns.str.strip()

    # Procesar electricidad: agrupar por año y sumar consumo
    consumo_electricidad['AÑO'] = pd.to_numeric(consumo_electricidad['AÑO'], errors='coerce')
    consumo_electricidad['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'] = pd.to_numeric(
        consumo_electricidad['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'], errors='coerce'
    )
    electricidad_agg = consumo_electricidad.groupby('AÑO')['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'].sum().reset_index()
    electricidad_agg.rename(columns={'CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)': 'Electricidad (kWh)'}, inplace=True)

    consumo_gas.columns = consumo_gas.columns.str.strip()

    # Procesar gas: agrupar por año y sumar consumo de gas y derivados
    consumo_gas['AÑO'] = pd.to_numeric(consumo_gas['AÑO'], errors='coerce')
    consumo_gas['CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)'] = pd.to_numeric(consumo_gas['CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)'], errors='coerce')
    consumo_gas['G.D. en Base 20'] = pd.to_numeric(consumo_gas['G.D. en Base 20'], errors='coerce')
    consumo_gas['G.D. en Base 26'] = pd.to_numeric(consumo_gas['G.D. en Base 26'], errors='coerce')

    gas_agg = consumo_gas.groupby('AÑO').agg({
        'CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)': 'sum',
        'G.D. en Base 20': 'sum',
        'G.D. en Base 26': 'sum'
    }).reset_index()

    gas_agg.rename(columns={
        'CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)': 'Gas (kWh)',
        'G.D. en Base 20': 'GD20',
        'G.D. en Base 26': 'GD26'
    }, inplace=True)

    consumo_gasoil.columns = consumo_gasoil.columns.str.strip()

    # Corregir el nombre de la columna de gasóleo C
    gasoil_col = [col for col in consumo_gasoil.columns if 'Gasóleo C' in col][0]

    # Procesar gasoil: agrupar por año y sumar consumo
    consumo_gasoil['AÑO'] = pd.to_numeric(consumo_gasoil['AÑO'], errors='coerce')
    consumo_gasoil[gasoil_col] = pd.to_numeric(consumo_gasoil[gasoil_col], errors='coerce')
    consumo_gasoil['G.D. en Base 20'] = pd.to_numeric(consumo_gasoil['G.D. en Base 20'], errors='coerce')
    consumo_gasoil['G.D. en Base 26'] = pd.to_numeric(consumo_gasoil['G.D. en Base 26'], errors='coerce')

    gasoil_agg = consumo_gasoil.groupby('AÑO').agg({
        gasoil_col: 'sum',
        'G.D. en Base 20': 'sum',
        'G.D. en Base 26': 'sum'
    }).reset_index()

    gasoil_agg.rename(columns={
        gasoil_col: 'Gasóleo C',
        'G.D. en Base 20': 'GD20_gasoil',
        'G.D. en Base 26': 'GD26_gasoil'
    }, inplace=True)

    # Combinar los datos
    consumo_total = pd.merge(electricidad_agg, gas_agg, on='AÑO', how='outer')
    consumo_total = pd.merge(consumo_total, gasoil_agg, on='AÑO', how='outer')

    # Sumar GD20 y GD26 de gas y gasoil
    consumo_total['GD20'] = consumo_total[['GD20', 'GD20_gasoil']].sum(axis=1)
    consumo_total['GD26'] = consumo_total[['GD26', 'GD26_gasoil']].sum(axis=1)

    # Eliminar columnas intermedias
    consumo_total.drop(columns=['GD20_gasoil', 'GD26_gasoil'], inplace=True)

    # Rellenar valores nulos con 0
    consumo_total.fillna(0, inplace=True)

    # Mostrar la tabla final
    tabla_año=consumo_total.sort_values('AÑO').reset_index(drop=True)


    return (tabla_año,)


@app.cell
def resumen(
    consumo_electricidad,
    consumo_energetico,
    consumo_gas,
    consumo_gasoil,
    pd,
):

    centros_por_tipo = consumo_energetico['TIPO DE CENTRO DE CONSUMO'].value_counts().reset_index()
    centros_por_tipo.columns = ['TIPO DE CENTRO DE CONSUMO', 'CANTIDAD DE CENTROS']


    # Agrupar por tipo de centro y sumar consumo
    elec_resumen = consumo_electricidad.groupby("TIPO DE CENTRO DE CONSUMO")["CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)"].sum().reset_index()
    elec_resumen.columns = ["TIPO DE CENTRO DE CONSUMO", "ELECTRICIDAD (kWh)"]

    gas_resumen = consumo_gas.groupby("TIPO DE CENTRO DE CONSUMO")["CONSUMO MENSUAL TOTAL GAS NATURAL (kWh)"].sum().reset_index()
    gas_resumen.columns = ["TIPO DE CENTRO DE CONSUMO", "GAS (kWh)"]

    gasoil_resumen = consumo_gasoil.groupby("TIPO DE CENTRO DE CONSUMO")["CONSUMO MENSUAL TOTAL GSL (M3)\nGasóleo C"].sum().reset_index()
    gasoil_resumen.columns = ["TIPO DE CENTRO DE CONSUMO", "GASÓLEO C (m3)"]


    # Unir los tres resúmenes
    merged = pd.merge(elec_resumen, gas_resumen, on="TIPO DE CENTRO DE CONSUMO", how="outer")
    merged = pd.merge(merged, gasoil_resumen, on="TIPO DE CENTRO DE CONSUMO", how="outer")
    merged = pd.merge(merged, centros_por_tipo, on="TIPO DE CENTRO DE CONSUMO", how="left")

    # Rellenar valores faltantes con 0
    merged.fillna(0, inplace=True)

    merged["CANTIDAD DE CENTROS"] = merged["CANTIDAD DE CENTROS"].astype(int)

    # Agregar fila de totales
    totals = merged[["ELECTRICIDAD (kWh)", "GAS (kWh)", "GASÓLEO C (m3)", "CANTIDAD DE CENTROS"]].sum()
    totals_row = pd.DataFrame([["TOTAL", *totals]], columns=merged.columns)
    tabla_consumos_centros = pd.concat([merged, totals_row], ignore_index=True)
    return (tabla_consumos_centros,)


@app.cell
def _(consumo_energetico, plt):

    # Agrupar por 'CENTRO DE CONSUMO' y sumar la 'SUPERFICIE CONSTRUIDA'
    grafica_circular = consumo_energetico.groupby('TIPO DE CENTRO A NIVEL DE ADMINISTRACIÓN AUTONÓMICA')['SUPERFICIE CONSTRUIDA'].sum().dropna()

    # Eliminar valores nulos y convertir a numérico
    grafica_circular = grafica_circular.dropna()
    grafica_circular = grafica_circular.astype(float)

    # Ordenar de mayor a menor
    grafica_circular = grafica_circular.sort_values(ascending=False)

    # Calcular porcentajes
    percentages = grafica_circular / grafica_circular.sum() * 100


    # Crear etiquetas para la leyenda
    labels = [f"{name} ({pct:.1f}%)" for name, pct in zip(grafica_circular.index, percentages)]

    # Crear gráfico circular sin etiquetas
    figura_circular, axis2 = plt.subplots(figsize=(8, 8))
    wedges, _ = axis2.pie(grafica_circular, startangle=90)

    # Añadir leyenda con etiquetas personalizadas
    dibujado= axis2.legend(wedges, labels, title="Tipo de Centro", loc="center left", bbox_to_anchor=(1, 0.5))
    return figura_circular, wedges


@app.cell
def electricidad1(consumo_electricidad, plt):

    consumo_anual = consumo_electricidad.groupby('AÑO')['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'].sum()

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    grafica_electricidad_anual=consumo_anual.plot(kind='bar', color='skyblue')
    plt.title('Consumo Anual de Energía Activa')
    plt.xlabel('Año')
    plt.ylabel('Energía Activa Consumida (kWh)')
    plt.xticks(rotation=45)
    plt.savefig("consumo_anual_energia.png")



    return (grafica_electricidad_anual,)


@app.cell
def electricidad2(consumo_electricidad, plt, wedges):
    consumo_organismos_electricidad = consumo_electricidad.groupby('ORGANISMO / CONSEJERÍA')['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'].sum()

    labels3 = [f"{name}" for name in consumo_organismos_electricidad.index]

    figura_circular_electricidad, axis3 = plt.subplots(figsize=(8, 8))

    wedges2, _ = axis3.pie(consumo_organismos_electricidad, startangle=90)
    dibujado2= axis3.legend(wedges, labels3, title="Tipo de Organismo", loc="center left", bbox_to_anchor=(1, 0.5))

    return (figura_circular_electricidad,)


@app.cell
def electricidad3(consumo_electricidad, plt):
    consumo_electricidad_tarifas = consumo_electricidad.groupby('TARIFA ELÉCTRICA')['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'].sum()

    # Plotting the bar chart
    plt.figure(figsize=(10, 6))
    grafica_electricidad_tarifas=consumo_electricidad_tarifas.plot(kind='pie', color='skyblue')
    plt.title('Consumo Anual de Energía Activa')
    plt.xlabel('Año')
    plt.ylabel('Energía Activa Consumida (kWh)')
    plt.xticks(rotation=45)
    plt.savefig("consumo_anual_energia.png")
    return (grafica_electricidad_tarifas,)


@app.cell
def heat_map_electricidad(HeatMap, consumo_electricidad, folium, pd):
    # Filtrar filas con valores válidos en coordenadas y consumo
    coordenadas_heatmap = consumo_electricidad[
        ['COORDENADA Y LATITUD', 'COORDENADA X LONGITUD', 'CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)']].copy()


    # Convertir columnas a tipo numérico
    coordenadas_heatmap.loc[:,'lat'] = pd.to_numeric(coordenadas_heatmap['COORDENADA Y LATITUD'], errors='coerce')
    coordenadas_heatmap.loc[:,'lon'] = pd.to_numeric(coordenadas_heatmap['COORDENADA X LONGITUD'], errors='coerce')
    coordenadas_heatmap.loc[:,'consumo'] = pd.to_numeric(coordenadas_heatmap['CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)'], errors='coerce')

    # Eliminar filas con valores no numéricos
    coordenadas_heatmap = coordenadas_heatmap.dropna(subset=['lat', 'lon', 'consumo'])

    # Crear el mapa centrado en Castilla y León
    mapa_calor = folium.Map(location=[41.65, -4.72], zoom_start=7)

    # Crear lista de puntos para el mapa de calor
    datos_calor = [[row['lat'], row['lon'], row['consumo']] for index, row in coordenadas_heatmap.iterrows()]

    # Añadir capa de mapa de calor
    resultado_mapa_calor=HeatMap(datos_calor, radius=10, max_zoom=13).add_to(mapa_calor)
    return (mapa_calor,)


@app.cell
def electricidad4(consumo_electricidad, mdates, pd, plt):

    # Renombrar columnas con codificación incorrecta
    consumo_electricidad.rename(columns={
        'AÑO': 'AÑO',
        'CONSUMO MENSUAL ENERGÍA ACTIVA TOTAL (kWh)': 'CONSUMO',
        'G.D. en Base 20': 'GD20',
        'G.D. en Base 26': 'GD26'

    }, inplace=True)

    # Diccionario para convertir nombres de meses a números
    meses = {
        'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4, 'MAYO': 5, 'JUNIO': 6,
        'JULIO': 7, 'AGOSTO': 8, 'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12
    }

    # Convertir columna MES a número
    consumo_electricidad['MES_NUM'] = consumo_electricidad['MES'].str.upper().map(meses)

    # Crear columna de fecha usando año, mes y día
    consumo_electricidad['FECHA'] = pd.to_datetime(dict(year=consumo_electricidad['AÑO'], month=consumo_electricidad['MES_NUM'], day=1), errors='coerce')

    # Ordenar por fecha
    consumo_electricidad.sort_values('FECHA', inplace=True)

    consumo_electricidad_mensual=consumo_electricidad.groupby('FECHA')[['CONSUMO','GD20','GD26']].sum().reset_index()

    # Crear figura y ejes
    grafica_electricidad_mensual, axis4 = plt.subplots(figsize=(14, 6))

    # Primer eje Y: Consumo
    axis4.set_xlabel('Fecha')
    axis4.set_ylabel('Consumo (kWh)', color='green')
    axis4.plot(consumo_electricidad_mensual['FECHA'], consumo_electricidad_mensual['CONSUMO'], color='green', label='Consumo (kWh)')
    axis4.tick_params(axis='y', labelcolor='green')

    # Segundo eje Y: G.D. en Base 20
    axis4_1 = axis4.twinx()
    axis4_1.set_ylabel('G.D. Base 20', color='blue')
    axis4_1.plot(consumo_electricidad_mensual['FECHA'], consumo_electricidad_mensual['GD20'], color='blue', label='G.D. Base 20')
    axis4_1.tick_params(axis='y', labelcolor='blue')

    # Tercer eje Y: G.D. en Base 26
    axis4_2 = axis4.twinx()
    axis4_2.spines['right'].set_position(('outward', 60))
    axis4_2.set_ylabel('G.D. Base 26', color='red')
    axis4_2.plot(consumo_electricidad_mensual['FECHA'], consumo_electricidad_mensual['GD26'], color='red', label='G.D. Base 26')
    axis4_2.tick_params(axis='y', labelcolor='red')

    # Formatear eje X
    axis4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    axis4.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    grafica_electricidad_mensual.autofmt_xdate()

    # Título y leyenda
    resultado_grafica_electricidad_3D=plt.title('Consumo mensual y G.D. en Base 20 y 26 (con líneas conectadas)')
    return (grafica_electricidad_mensual,)


@app.cell
def _(consumo_electricidad, mo):
    mo.ui.data_explorer(consumo_electricidad)
    return


if __name__ == "__main__":
    app.run()
