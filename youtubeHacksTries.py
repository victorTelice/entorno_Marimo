import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    return alt, mo


@app.cell
def _(mo):
    from motalk import WebkitSpeechToTextWidget

    speech_widget=mo.ui.anywidget(WebkitSpeechToTextWidget())
    speech_widget
    return


@app.cell
def _(mo):
    from mopaint import Paint
    from mohtml import img, div, tailwind_css

    tailwind_css()
    widget = mo.ui.anywidget(Paint(height=550))
    widget
    return


@app.cell
def _(mo):
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
      # Widget front-end JavaScript code
        _esm = """
        function render({ model, el }) {
          let getCount = () => model.get("count");
          let button = document.createElement("button");
          button.innerHTML = `count is ${getCount()}`;
          button.addEventListener("click", () => {
            model.set("count", getCount() + 1);
            model.save_changes();
          });
          model.on("change:count", () => {
            button.innerHTML = `count is ${getCount()}`;
          });
          el.appendChild(button);
        }
        export default { render };
      """
        _css = """
        button {
          padding: 5px !important;
          border-radius: 5px !important;
          background-color: #f0f0f0 !important;

          &:hover {
            background-color: lightblue !important;
            color: white !important;
          }
        }
      """

      # Stateful property that can be accessed by JavaScript & Python
        count = traitlets.Int(0).tag(sync=True)

    widget2 = mo.ui.anywidget(CounterWidget())
    widget2
    #breakpoint()

    return (widget2,)


@app.cell
def _(widget2):
    # In another cell, you can access the widget's value
    widget2.value

    # You can also access the widget's specific properties
    widget2.count
    return


@app.cell
def _(mo):
    mo.accordion(
        {"Tip": "Use accordions to let users reveal and hide content."}
    )
    return


@app.cell
def _(mo):
    mo.carousel([
        mo.md("# Introduction"),
        "By the marimo team",
        mo.md("## What is marimo?"),
        mo.md("![marimo moss ball](https://marimo.app/logotype-wide.svg)"),
        mo.md("## Questions?"),
    ])
    return


@app.cell
def _(alt, mo):


    from vega_datasets import data

    chart = (
        alt.Chart(data.cars())
        .mark_point()
        .encode(
            x="Horsepower",
            y="Miles_per_Gallon",
            color="Origin",
        )
    )

    chart = mo.ui.altair_chart(chart)
    chart
    return


@app.cell
def _(mo):


    def click_boton(event):
        print("Button presioned!")

    button_event=mo.ui.button(label="Press me!", kind="danger", on_click=click_boton)

    button_event

    return


if __name__ == "__main__":
    app.run()
