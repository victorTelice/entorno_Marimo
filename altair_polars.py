import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


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
    return alt, mo, pd, pl, ui


@app.cell
def contenido_pestanhas(
    Grafica_Barra_Lateral,
    Grafica_Barras_Verticales,
    Grafica_Circular,
    Tabla_Consumo_Anual,
    dataframe_stats,
    dataframes,
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
        Grafica_Barras_Verticales(organismos_ener),
        Tabla_Consumo_Anual(),
        Grafica_Circular(superficie_ener)

    ]),
    

        )
    tab5 = mo.vstack([seleccion_tabla,dataframes[seleccion_tabla.value]])
    return tab1, tab5


@app.cell
def obtencion_df(depuradoDF, pd, pl):
    # Lee CSV completo de forma rápida
    energía_df = depuradoDF(pl.read_parquet("energia.parquet"))
    electricidad_df = depuradoDF(pl.read_parquet("electricidad.parquet"))
    gas_df = depuradoDF(pl.read_parquet("gas.parquet"))
    gasoil_df = depuradoDF(pl.read_parquet("gasoil.parquet"))


    electricidad_df_pandas = pd.read_csv("electricidad.csv", sep=';')



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

        # Eliminar columnas binarias
    

        # Chart con ancho personalizado
        grafica = (
            alt.Chart(source)
            .mark_bar()
            .encode(
                x=alt.X('organismo_consejeria:N', sort='-y'),
                y=alt.Y('len:Q',
                        title='Consumo mensual total (kWh)')
            )
            .properties(
                width=ancho,      # aquí defines el ancho
                height=400,       # opcional: también puedes ajustar alto
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
def _(gas_df, mo):
    mo.ui.table(data=gas_df)
    return


@app.cell
def _(electricidad_df, gas_df, gasoil_df, mo, pl):
    def Tabla_Consumo_Anual():
        df1=electricidad_df.group_by("ano").agg(pl.col("consumo_mensual_energia_activa_total_kwh").sum()).sort("ano")
        df2=gas_df.group_by("ano").agg(pl.col("consumo_mensual_total_gas_natural_kwh").sum()).sort("ano").drop("ano")
        df3=gas_df.group_by("ano").agg(pl.col("g_d_en_base_20").sum()).sort("ano").drop("ano")
        df4=gas_df.group_by("ano").agg(pl.col("g_d_en_base_26").sum()).sort("ano").drop("ano")
        df5=gasoil_df.group_by("ano").agg(pl.col("consumo_mensual_total_gsl_m3_gasoleo_c").sum()).sort("ano").drop("ano")
    
        tabla=mo.ui.table(pl.concat([df1,df2,df3,df4,df5],how='horizontal')) 

        return tabla

    return (Tabla_Consumo_Anual,)


if __name__ == "__main__":
    app.run()
