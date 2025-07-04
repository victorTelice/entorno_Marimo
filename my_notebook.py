# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    #Este archivo esta generado con el argumento '--sandbox' y ya incluye una serie de paquetes y configuraciones prefijadas. 
    ### Mi objetivo era que me hiciese un docker seguro como ponia en la documentacion pero creo que no ha funcionado.
    """
    )
    return


if __name__ == "__main__":
    app.run()
