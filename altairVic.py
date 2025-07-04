import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt

    return alt, mo


@app.cell
def _(mo):
    mo.md(r"""#Gráficas Equipos Premier con Altair""")
    return


@app.cell
def _():
    import pandas as pd

    # Equipos y temporadas
    equipos = ["Liverpool", "Manchester City", "Arsenal"]
    temporadas = [2019, 2020, 2021]
    jornadas = list(range(1, 39))  # 38 jornadas

    # Crear puntos por partido aleatorios
    import random
    data = []
    for year in temporadas:
        for team in equipos:
            total = 0
            for jornada in jornadas:
                puntos = random.choice([0, 1, 3])  # simulación realista
                data.append({
                    "year": year,
                    "match_day": jornada,
                    "team_name": team,
                    "points": puntos
                })

    # DataFrame con puntos por partido
    points_by_match = pd.DataFrame(data)

    # Agrupar por temporada y equipo
    points = points_by_match.groupby(["year", "team_name"])["points"].sum().reset_index()
    points.rename(columns={"points": "total_points"}, inplace=True)
    return equipos, pd, points, points_by_match


@app.cell
def _(equipos, mo):

    # Dropdown interactivo con marimo
    equipo_dropdown = mo.ui.dropdown(options=equipos, label="Selecciona un equipo")

    return (equipo_dropdown,)


@app.cell
def _(bar_season_chart, equipo_dropdown, line_season_chart, mo):
    selected_team = equipo_dropdown.value

    mo.vstack([
        equipo_dropdown,
        mo.ui.tabs(
            {
                "::lucide:chart-column-big:: Por temporada": bar_season_chart(selected_team),
                "::lucide:chart-spline:: Progresión por jornada": line_season_chart(selected_team),
            }
        )
    ])
    return (selected_team,)


@app.cell
def _(dot_season_chart, selected_team):
    dot_season_chart(selected_team)
    return


@app.cell
def _(alt, mo, points, points_by_match):
    # 1. BARRAS POR TEMPORADA
    def bar_season_chart(equipo):
        df_filtrado = points[points["team_name"] == equipo]
        chart = (
            alt.Chart(df_filtrado)
            .mark_bar()
            .encode(
                x=alt.X("year:O", title="Temporada"),
                y=alt.Y("total_points:Q", title="Puntos"),
                color=alt.Color("team_name:N", title="Equipo")
            )
        )

        return mo.ui.altair_chart(
            chart,
            chart_selection="point",
            legend_selection=False,
            label=f"Puntos por Temporada: {equipo}",
        )

    # 2. PUNTOS POR PARTIDO (DOT CHART opcional)
    def dot_season_chart(equipo):
        df_filtrado = points_by_match[points_by_match["team_name"] == equipo]
        chart = (
            alt.Chart(df_filtrado)
            .mark_circle()
            .encode(
                x=alt.X("match_day:N", title="Jornada"),
                y=alt.Y("year:O", title="Temporada"),
                size="points:Q",
                color=alt.Color("team_name:N", title="Equipo")
            )
        )

        return mo.ui.altair_chart(
            chart,
            chart_selection="point",
            legend_selection=False,
            label="Progresión por Partido",
        )
    return bar_season_chart, dot_season_chart


@app.cell
def _(alt, mo, points_by_match):
    # 3. LINEA ACUMULADA DE PUNTOS POR TEMPORADA
    def line_season_chart(equipo):
        df_filtrado = points_by_match[points_by_match["team_name"] == equipo]

        chart = (
            alt.Chart(df_filtrado)
            .transform_window(
                frame=[None, 0],
                sort=[{"field": "match_day"}],
                groupby=["year", "team_name"],
                cumulative_points="sum(points)",
                index="rank()"
            )
            .mark_line()
            .encode(
                x=alt.X("index:N", title="Jornada"),
                y=alt.Y("cumulative_points:Q", title="Puntos acumulados"),
                color=alt.Color("year:N", title="Temporada")
            )
        )

        return mo.ui.altair_chart(chart, label=f"Progresión por jornada: {equipo}")

    return (line_season_chart,)


@app.cell
def _(mo):
    mo.md(r"""#Gráficos dinámicos""")
    return


@app.cell
def _(mo):
    import numpy as np
    import polars as pl


    # Crear un slider
    slider = mo.ui.slider(start=5, stop=50, step=1, value=10, label="Tamaño de la serie")

    return np, slider


@app.cell
def _(alt, mo, np, pd, slider):

    # Generar datos y gráfico de forma tradicional
    size = slider.value
    dinData = np.random.randint(0, 10, size)
    df = pd.DataFrame({"x": range(size), "y": np.cumsum(dinData)})

    # Crear gráfico con Altair
    chart = alt.Chart(df).mark_line().encode(
        x="x",
        y="y"
    ).properties(title=f"Gráfico de suma acumulada (n = {size})")

    # Mostrar todo junto
    mo.vstack([
        slider,
        mo.ui.altair_chart(chart)
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""#Flow diagrams y widgets""")
    return


@app.cell
def _(np):

    import matplotlib.pyplot as plt
    plt.style.use("_mpl-gallery")

    np.random.seed(21)
    x = 4 + np.random.normal(0, 2, 24)
    y = 4 + np.random.normal(0, 2, len(x))
    sizes = np.random.uniform(15, 80, len(x))
    opacity = np.random.uniform(0, 1, len(x))
    return opacity, plt, sizes, x, y


@app.cell
def _(mo):
    from ipyreactflow import ColorPicker

    widget = mo.ui.anywidget(ColorPicker())
    widget
    return (widget,)


@app.cell
def _(np, opacity, plt, sizes, widget, x, y):
    fig, ax = plt.subplots()
    if widget.target_node == "green":
        c = "limegreen"
    if widget.target_node == "blue":
        c = "deepskyblue"
    ax.scatter(x, y, s=sizes * 30, color=c or None, alpha=opacity * 1)

    fig.set_size_inches(3, 3)
    ax.set(
        xlim=(0, 8), xticks=np.arange(1, 8), ylim=(0, 8), yticks=np.arange(1, 8)
    )
    plt.gca()
    return


@app.cell
def _(mo):
    mo.md(r"""#Dibujando un ScatterChart""")
    return


@app.cell
def _(mo):
    from drawdata import ScatterWidget
    widget2 = mo.ui.anywidget(ScatterWidget(height=350))
    widget2
    return


@app.cell
def _(mo):
    mo.md(r"""#Gráficas completas""")
    return


@app.cell
def _(mo):
    n_items = mo.ui.slider(start=3, stop=16, step=1, debounce=True)
    mo.md(
        f"""
        Choose a number of items $n$: {n_items}
        """
    )
    return (n_items,)


@app.cell
def _(mo, pymde):
    penalty_function = mo.ui.dropdown(
        options={
            "Linear": pymde.penalties.Linear,
            "Quadratic": pymde.penalties.Quadratic,
            "Cubic": pymde.penalties.Cubic,
        },
        value="Cubic",
    )
    mo.md(
        f"""
        Choose a penalty function: {penalty_function}
        """
    )
    return (penalty_function,)


@app.cell
def _(complete_graph, mo, n_items, penalty_function):
    plot = complete_graph(n_items.value, penalty_function.value)

    mo.md(
        f"""
        Here is a plot of $K_n$ with $n={n_items.value}$, i.e., a complete graph on 
        ${n_items.value}$ nodes. This graph has

        \[
        (n)(n-1)/2 = {n_items.value*(n_items.value-1)//2}
        \]

        edges. The plot was obtained using a 
        {penalty_function.value.__name__.lower()} penalty function.

        {mo.as_html(plot)}
        """
    )
    return


@app.cell
def _(pymde):
    import functools

    @functools.cache
    def complete_graph(n_items, penalty_function):
        edges = pymde.all_edges(n_items)
        mde = pymde.MDE(
            n_items,
            embedding_dim=2,
            edges=edges,
            distortion_function=penalty_function(weights=1.0),
            constraint=pymde.Standardized(),
        )
        mde.embed(max_iter=25, verbose=True)
        return mde.plot(edges=edges)

    return (complete_graph,)


@app.cell
def _():
    import pymde
    return (pymde,)


if __name__ == "__main__":
    app.run()
