import marimo

__generated_with = "0.14.9"
app = marimo.App(
    width="medium",
    layout_file="layouts/altair_polars.slides.json",
)


@app.cell
def interfaz(mo, tab1, tab5):
    mo.ui.tabs({"Consumo Energía": tab1 , "Datos": tab5})
    return


@app.cell
def importaciones():
    import marimo as mo
    from marimo import ui
    import polars as pl
    import altair as alt
    import pyarrow as pa
    import pandas as pd
    import vegafusion as vf
    from vega_datasets import data
    import folium
    from folium import plugins
    from folium.plugins import HeatMap
    return HeatMap, alt, folium, mo, pl, plugins, ui


@app.cell
def contenido_pestanhas(
    Grafica_Barra_Lateral,
    Grafica_Barras_Verticales,
    Grafica_Circular,
    Mapa,
    Tabla_Consumo_Anual,
    Tabla_Consumo_Centros,
    Tabla_Sumas_Centro,
    concatenado,
    dataframe_stats,
    dataframes,
    energía_df,
    grupo_estadisticas,
    grupo_stats,
    mo,
    organismos_ener,
    seleccion_tabla,
    stats,
    superficie_ener,
):
    tab1 = (mo.vstack([
        grupo_estadisticas(stats(grupo_stats)),
        Grafica_Barra_Lateral(dataframe_stats),
        Mapa(energía_df, tipo_mapa=1),
        Grafica_Barras_Verticales(organismos_ener),
        Tabla_Sumas_Centro(concatenado,ancho=600),
        Tabla_Consumo_Anual(),
        Grafica_Circular(superficie_ener),
        Tabla_Consumo_Centros()

    ]),


        )
    tab5 = mo.vstack([seleccion_tabla,dataframes[seleccion_tabla.value]])
    return tab1, tab5


@app.cell
def obtencion_df(depuradoDF, pl):
    # Lee CSV completo de forma rápida
    energía_df = depuradoDF(pl.read_parquet("energia.parquet"))
    electricidad_df = depuradoDF(pl.read_parquet("electricidad.parquet"))
    gas_df = depuradoDF(pl.read_parquet("gas.parquet"))
    gasoil_df = depuradoDF(pl.read_parquet("gasoil.parquet"))

    return electricidad_df, energía_df, gas_df, gasoil_df


@app.cell
def _(pl):
    def depuradoDF(source):
        tirar_columnas_elec = [c for c, dt in source.schema.items() if dt == pl.Binary]
        elec_arreglado = source.drop(tirar_columnas_elec)
        return elec_arreglado
    return (depuradoDF,)


@app.cell
def carga_dataframes(electricidad_df, energía_df, gas_df, gasoil_df):
    dataframes ={
    "Energía": energía_df,
    "Electricidad": electricidad_df, 
    "Gas": gas_df,
    "Gasoil": gasoil_df,
    }

    return (dataframes,)


@app.cell
def seleccion_dataframes(dataframes, ui):
    seleccion_tabla=ui.radio(label="Selecciona la tabla a mostrar", options=dataframes.keys(), value='Energía')
    return (seleccion_tabla,)


@app.cell
def estadisticas(mo):
    def stats(estadisticas):
        ener   = mo.stat(
            value=estadisticas[0], 
            caption="Nª de Centros de consumo\n(Edificios e instalaciones)", 
            bordered=True
        )
        elec = mo.stat(
            value=estadisticas[1], 
            caption="Nº Suministros electricidad\n(CUPsE)", 
            bordered=True
        )
        gas = mo.stat(
            value=estadisticas[2], 
            caption="Nº Suministros gas natural canalizadoºn(CUPs GN)", 
            bordered=True
        )
        gasoil= mo.stat(
            value=estadisticas[3], 
            caption="Nº de centros con gasóleo\n(GSL - Solo Sanidad y Educación)",  
            bordered=True
        )

        return ener, elec, gas, gasoil

    def grupo_estadisticas(estadisticas):
        return mo.hstack(
            estadisticas,
            justify="space-around",
            align="center",
            gap=2.0,
            wrap=True,
            widths="equal"
        )
    return grupo_estadisticas, stats


@app.cell
def calculo_estadisticas(electricidad_df, energía_df, gas_df, gasoil_df):
    estadistica_centros=len(energía_df['centro_de_consumo'].value_counts())
    estadistica_electricidad=len(electricidad_df['cups_electricidad'].value_counts())
    estadistica_gas=len(gas_df['cups_gas_natural'].value_counts())
    estadistica_gasoil=len(gasoil_df['centro_de_consumo'].value_counts())
    grupo_stats = [estadistica_centros,estadistica_electricidad,estadistica_gas,estadistica_gasoil]

    return (
        estadistica_electricidad,
        estadistica_gas,
        estadistica_gasoil,
        grupo_stats,
    )


@app.cell
def _(alt, mo):
    def Grafica_Barra_Lateral(source):   

        barra_lateral=alt.Chart(source).mark_bar(color="red").encode(
            x=alt.X("Valores:Q", axis=None),
            y=alt.Y("Labels:N")
        )

        # Agregar etiquetas dentro de las barras (las categorías)
        etiquetas = alt.Chart(source).mark_text(
            align='left',
            baseline='middle',
            dx=5,
            color='black',
            fontSize=14
        ).encode(
            x="Valores:Q",
            y="Labels:N",
            text="Valores"
        )

        # Combinar gráfico de barras con etiquetas
        grafica = (barra_lateral + etiquetas).properties(
            width=400,
            height=150
        )
        plot= mo.ui.altair_chart(grafica)
        return plot

    return (Grafica_Barra_Lateral,)


@app.cell
def dataframe_estadisticas(
    estadistica_electricidad,
    estadistica_gas,
    estadistica_gasoil,
    pl,
):
    dataframe_stats = pl.DataFrame({
            "Labels": ["Electricidad", "Gas", "Gasoil"],
            "Valores": [estadistica_electricidad,estadistica_gas,estadistica_gasoil]
    })
    return (dataframe_stats,)


@app.cell
def _(alt, mo):
    def Grafica_Barras_Verticales(source, ancho=800):

        grafica = (
            alt.Chart(source)
            .mark_bar()
            .encode(
                x=alt.X('organismo_consejeria:N', sort='-y'),
                y=alt.Y('len:Q',
                        title='Consumo mensual total (kWh)')
            )
            .properties(
                width=ancho,      
                height=400,       
                title="Consumo por organismo o consejería"
            )
        )
        plot = mo.ui.altair_chart(grafica)
        return plot

    return (Grafica_Barras_Verticales,)


@app.cell
def _(alt, mo):
    def Grafica_Circular(source):
        grafica=alt.Chart(source).mark_arc().encode(
            theta="superficie_construida",
            color="organismo_consejeria"
        )

        plot = mo.ui.altair_chart(grafica)
        return plot
    return (Grafica_Circular,)


@app.cell
def datos_graficas(energía_df, pl):
    organismos_ener=energía_df.group_by("organismo_consejeria").len()
    superficie_ener = energía_df.group_by('organismo_consejeria').agg(pl.col('superficie_construida').sum())
    return organismos_ener, superficie_ener


@app.cell
def _(electricidad_df, gas_df, gasoil_df, mo, pl):
    def Tabla_Consumo_Anual():
        df1=electricidad_df.group_by("ano").agg(pl.col("consumo_mensual_energia_activa_total_kwh").sum())
        df2=gas_df.group_by("ano").agg(pl.col("consumo_mensual_total_gas_natural_kwh").sum())
        df3=gas_df.group_by("ano").agg(pl.col("g_d_en_base_20").sum())
        df4=gas_df.group_by("ano").agg(pl.col("g_d_en_base_26").sum())
        df5=gasoil_df.group_by("ano").agg(pl.col("consumo_mensual_total_gsl_m3_gasoleo_c").sum())
    
        tabla=mo.ui.table(pl.concat([df1,df2,df3,df4,df5],how='align'))

        return tabla

    return (Tabla_Consumo_Anual,)


@app.cell
def _(electricidad_df, energía_df, gas_df, gasoil_df, mo, pl):
    def Tabla_Consumo_Centros():

        df0=energía_df.group_by("tipo_de_centro_a_nivel_de_administracion_autonomica").len()
        df1=electricidad_df.group_by("tipo_de_centro_a_nivel_de_administracion_autonomica").agg(pl.col("consumo_mensual_energia_activa_total_kwh").sum())
        df2=gas_df.group_by("tipo_de_centro_a_nivel_de_administracion_autonomica").agg(pl.col("consumo_mensual_total_gas_natural_kwh").sum())

        df3=gasoil_df.group_by("tipo_de_centro_a_nivel_de_administracion_autonomica").agg(pl.col("consumo_mensual_total_gsl_m3_gasoleo_c").sum())
    
        tabla=mo.ui.table(pl.concat([df0,df1,df2,df3],how='align'))

        return tabla

    return (Tabla_Consumo_Centros,)


@app.cell
def _(HeatMap, folium, pl, plugins):
    def Mapa(source, tipo_mapa):    
        energia_renombrada = source.rename({
            'coordenada_x_longitud': 'longitud',
            'coordenada_y_latitud': 'latitud'
        })
    
        # Convertir coordenadas a numérico y eliminar filas no válidas
        energia_renombrada = energia_renombrada.with_columns([
            pl.col('longitud').cast(pl.Float64, strict=False),
            pl.col('latitud').cast(pl.Float64, strict=False)
        ]).drop_nulls(['longitud', 'latitud'])
    
        # Filtrar coordenadas dentro del rango geográfico de Castilla y León
        energia_renombrada = energia_renombrada.filter(
            (pl.col('longitud') >= -10) & (pl.col('longitud') <= 5) &
            (pl.col('latitud') >= 35) & (pl.col('latitud') <= 45)
        )
    
        # Eliminar duplicados
        coordenadas_unicas = energia_renombrada.select(['latitud', 'longitud']).unique()
    
        # Crear el mapa centrado en Castilla y León
        mapa = folium.Map(location=[41.65, -4.72], zoom_start=8)

        if tipo_mapa == 0 :

            plugins.MarkerCluster(coordenadas_unicas.transpose()).add_to(mapa)

        elif tipo_mapa == 1 :

            HeatMap(coordenadas_unicas.transpose()).add_to(mapa)

            print("Hola mundo")
    
    
    

        return mapa
    

    return (Mapa,)


@app.cell
def calculo_tabla_sumas(energía_df, pl):
     # Agrupar y sumar la columna 'cups_e'
    cups_e = (
        energía_df
        .group_by("tipo_de_centro_a_nivel_de_administracion_autonomica")
        .agg(pl.col("cups_e").sum())
        .drop_nulls()
        .sort("tipo_de_centro_a_nivel_de_administracion_autonomica")
        .rename({"cups_e": "suma"})
        .with_columns(tipo=0)
    )

    # Agrupar y sumar la columna 'cups_gn'
    cups_gn = (
        energía_df
        .group_by("tipo_de_centro_a_nivel_de_administracion_autonomica")
        .agg(pl.col("cups_gn").sum())
        .drop_nulls()
        .sort("tipo_de_centro_a_nivel_de_administracion_autonomica")
        .rename({"cups_gn": "suma"})
        .with_columns(tipo=1)
    )

    # Agrupar y sumar la columna 'gsl'
    gsl = (
        energía_df
        .group_by("tipo_de_centro_a_nivel_de_administracion_autonomica")
        .agg(pl.col("gsl").sum())
        .drop_nulls()
        .sort("tipo_de_centro_a_nivel_de_administracion_autonomica")
        .rename({"gsl": "suma"})
        .with_columns(tipo=2)
    )

    # Concatenar los DataFrames verticalmente
    concatenado = pl.concat([cups_e, cups_gn, gsl], how="vertical")

    # Convertir la columna 'tipo' a string
    concatenado = concatenado.with_columns(concatenado["tipo"].cast(pl.Utf8))

    concatenado = concatenado.with_columns([pl.col("tipo").str.replace(pattern="0",value="cups_e")])
    concatenado = concatenado.with_columns([pl.col("tipo").str.replace(pattern="1",value="cups_gn")])
    concatenado = concatenado.with_columns([pl.col("tipo").str.replace(pattern="2",value="gsl")])

    return (concatenado,)


@app.cell
def _(alt, mo):
    def Tabla_Sumas_Centro(source,ancho):
        grafica = alt.Chart(source).mark_bar().encode(
            x="suma:Q",
            y="tipo_de_centro_a_nivel_de_administracion_autonomica",
            color="tipo",
        ).properties(width=ancho)

        plot = mo.ui.altair_chart(grafica)

        return plot
    return (Tabla_Sumas_Centro,)


if __name__ == "__main__":
    app.run()
