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
    visual=mo.ui.data_explorer(df);
    visual
    return


if __name__ == "__main__":
    app.run()
