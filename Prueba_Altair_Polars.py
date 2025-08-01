import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import polars as pl
    import numpy as np
    return alt, mo, np, pl


@app.cell
def _():
    with open("entorno_marimo/Docs/bombas.txt", "r") as fin, open("entorno_marimo/Docs/bombas_clean.txt", "w") as fout:
        for line in fin:
            if line.endswith(",\n"):
                fout.write(line[:-2] + "\n")
            elif line.endswith(","):
                fout.write(line[:-1] + "\n")
            else:
                fout.write(line)

    with open("entorno_marimo/Docs/bombas2.txt", "r") as fin, open("entorno_marimo/Docs/bombas2_clean.txt", "w") as fout:
        for line in fin:
            if line.endswith(",\n"):
                fout.write(line[:-2] + "\n")
            elif line.endswith(","):
                fout.write(line[:-1] + "\n")
            else:
                fout.write(line)
    return


@app.cell
def _(
    BBar,
    amplitud,
    fig_BVDer,
    fig_BVIzq,
    fig_T1_T4,
    fig_T2_T3,
    fig_seno,
    mo,
):
    vistaIzq = mo.vstack([fig_BVIzq, fig_T1_T4])
    vistaDer = mo.vstack([fig_BVDer, fig_T2_T3])
    vistaCuadrado = mo.hstack([vistaIzq, vistaDer], justify = "space-around", align = "center")
    senoInteractivo = mo.hstack([fig_seno,amplitud], justify = "space-around", align = "center")

    tabs = mo.ui.tabs({
        "Simulación 1": [vistaCuadrado],
        "Comparación" : BBar,
        "Senos" : senoInteractivo
    })
    tabs
    return


@app.cell
def _(pl):
    def truncar (database: pl.DataFrame, x: float):

        fila = x*1+0-1
        fila = int(fila)
        return database.head(fila)

    return (truncar,)


@app.cell
def _(pl, truncar):
    tanques_df = pl.read_csv(
        "entorno_marimo/Docs/bombas_clean.txt",
        separator =";",
        infer_schema_length=1000
        )

    tanques2_df = pl.read_csv(
        "entorno_marimo/Docs/bombas2_clean.txt",
        separator = ";",
        infer_schema_length=1000
    )

    tanques_df = truncar(tanques_df, 634)
    tanques2_df = truncar(tanques2_df, 634)
    print(tanques_df)
    print(tanques2_df)
    return tanques2_df, tanques_df


@app.cell
def _(alt, pl):
    def createFig(database: pl.DataFrame, ejex: str, ejey: str, clr: str):

        fig = alt.Chart(database).mark_line().encode(
        x=alt.X(ejex),
        y=alt.Y(ejey),
        color=alt.value(clr)
        )

        return fig
    return (createFig,)


@app.cell
def _(createFig, tanques_df):
    fig_BIzq = createFig(tanques_df, "Time", "leftPump", 'blue')
    fig_VIzq = createFig(tanques_df, "Time", "leftValve", 'red')

    fig_BVIzq = fig_BIzq+fig_VIzq
    return (fig_BVIzq,)


@app.cell
def _(createFig, tanques_df):
    fig_T1 = createFig(tanques_df, "Time", "T1Level", 'blue')
    fig_T4 = createFig(tanques_df, "Time", "T4Level", 'red')

    fig_T1_T4 = fig_T1+fig_T4
    return (fig_T1_T4,)


@app.cell
def _(createFig, tanques_df):
    fig_BDer = createFig(tanques_df, "Time", "rightPump", 'blue')
    fig_VDer = createFig(tanques_df, "Time", "rightValve", 'red')

    fig_BVDer = fig_BDer+fig_VDer
    return (fig_BVDer,)


@app.cell
def _(createFig, tanques_df):
    fig_T2 = createFig(tanques_df, "Time", "T2Level", 'blue')
    fig_T3 = createFig(tanques_df, "Time", "T3Level", 'red')

    fig_T2_T3 = fig_T2+fig_T3
    return (fig_T2_T3,)


@app.cell
def data_explorer(mo, tanques_df):
    explorador = mo.ui.data_explorer(tanques_df)
    return


@app.cell
def _(mo):
    amplitud = mo.ui.slider(start=0, stop=10, label="Amplitud", value=5)
    return (amplitud,)


@app.cell
def _(np, pl):
    def crearSeno(amplitud: int):
        x = np.linspace(0, 6*np.pi)
        y = amplitud * np.sin(x)

        return pl.DataFrame({
            'x':x,
            'seno':y,
            'amplitud':[amplitud]*len(x)
        })
    return (crearSeno,)


@app.cell
def _(amplitud, crearSeno, createFig):
    Amp = amplitud.value
    seno_df = crearSeno(Amp)

    fig_seno = createFig(seno_df, "x", "seno", 'red')

    return (fig_seno,)


@app.cell
def _(tanques2_df, tanques_df):
    tanques_merged_df = tanques_df.join(tanques2_df, on = "Time", how = "inner", suffix = "_2")

    print(tanques_merged_df)
    return (tanques_merged_df,)


@app.cell
def _(alt, pl, tanques_merged_df):
    max_BIz = tanques_merged_df["leftPump"].max()
    max_BIz_2 = tanques_merged_df["leftPump_2"].max()

    dataBBar = pl.DataFrame({
        "Etiqueta" : ["Valor maximo bomba 1", "Valor maximo bomba 2"],
        "Valor" : [max_BIz, max_BIz_2]
    })

    BBar = alt.Chart(dataBBar).mark_bar(color = 'blue', size = 50).encode(
        x="Etiqueta",
        y="Valor"   
    )

    return (BBar,)


if __name__ == "__main__":
    app.run()
