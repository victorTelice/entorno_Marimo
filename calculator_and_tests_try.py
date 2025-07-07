import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import pytest
    return mo, pl, pytest


@app.cell
def _(mo):
    mo.md(r"""##Code snippet of a basic calculator function with marimo properties 🧮""")
    return


@app.cell
def _():
    '''''
    def funcionCalculador2(num:float, num2:float, operador:str) -> float:
        if operador == '+':
            resultado=num + num2
            return resultado
        elif operador == '-':
            resultado=num - num2
            return resultado
        elif operador == '*':
            resultado=num * num2
            return resultado
        elif operador == '/':
            if num2 == 0:
                raise ValueError("No se puede dividir entre cero.")
            else:
                resultado= num1/num2
                return resultado
        elif operador == '**':
            resultado = num ** num2
            return resultado
        else:
            raise ValueError(f"Operador no válido: {operador}")

        print(resultado)
    '''''
    return


@app.function
##Calculator function
#Parameters:
#num: float the firts operator
#num2:float the second operator
#operador:str
#Result: float the result of the operation

def funcionCalculadora(num:float, num2: float, operador:str) -> float:
    resultado=0

    if operador == "+":
        resultado=num+num2
    elif operador =="-":
        resultado=num-num2
    elif operador =="*":
        resultado=num*num2
    elif operador == "/":
        if num==0:
            raise ValueError("No se puede dividir por 0")
        else:
            resultado=num/num2
   # else:
      #  raise ValueError(f"Operador no válido: {operador}")

    return resultado


@app.cell
def _(mo):
    #ui parameters

    a = mo.ui.slider(1,100)

    b = mo.ui.slider(1,100)

    sign=mo.ui.text(placeholder= "Write the operator:", label="Operator (+, -, *, /, **)")

    mo.vstack([
        mo.md("num1:"),
        a,
        mo.md(""),
        mo.md("num2:"),
        b,
        mo.md(""),
        sign,
    ])


    return a, b, sign


@app.cell
def _():
    #res = funcionCalculadora(a.value, b.value, sign.value.strip())
    return


@app.cell
def _():
    '''''
    # %%
    # / output: true
    def funcion():
        try:
            op = sign.value.strip()
            mo.md("aqui llega")
            mo.md("vamos a hacer una calculadora sencilla usando sliders")
            res = funcionCalculadora(a.value, b.value, op)
            # breakpoint()
            mo.md(f"### ✅ Resultado: {a.value} {op} {b.value} = **{res}**")
        except Exception as e:
            # breakpoint()
            print(f"{e}")
            mo.md("aqui tambien")
            mo.md(f"❌ **Error:** {e}")
    '''''
    return


@app.cell
def _(a, b, mo, sign):
    #example with try-except
    try:   
        op = sign.value.strip()
        #mo.md("aqui llega")
        #mo.md("vamos a hacer una calculadora sencilla usando sliders")
        res = funcionCalculadora(a.value, b.value, op)
        print("jjj")
        mo.md(f"### ✅ Resultado: {a.value} {op} {b.value} = **{res}**")
    except Exception as e:
        print(f"{e}")
        #mo.md("aqui tambien")
        #mo.md(f"❌ **Error:** {e}")
    return


@app.cell
def _(a, b, mo, sign):
    #Cell run control with stop
    mo.stop(not a.value or not b.value or not sign.value) #until these conditions became true the program won´t continue

    op2 = sign.value.strip()
    print("aqui llega")
    print("vamos a hacer una calculadora sencilla usando sliders")
    res2 = funcionCalculadora(a.value, b.value, op2)
    print(f"resultado: {res2}")
    mo.md(f"### ✅ Resultado: {a.value} {op2} {b.value} = **{res2}**")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ##Code examples with batch 😲
    This allows the form to be displayed interactively, and the values entered by the user are automatically integrated into the generated content.
    """
    )
    return


@app.cell
def _(mo):
    user_info = mo.md(
        '''
        - What's your name?: {name}
        - When were you born?: {birthday}
        '''
    ).batch(name=mo.ui.text(), birthday=mo.ui.date())
    user_info
    return


@app.cell
def _(mo):
    el = mo.md("{start} → {end}").batch(
        start=mo.ui.date(label="Start Date"),
        end=mo.ui.date(label="End Date")
    )
    el
    return


@app.cell
def _(mo):
    markdown = mo.md(
        '''
        - What's your name?: {name}
        - When were you born?: {birthday}
        '''
    )
    batch = mo.ui.batch(
        markdown, {"name": mo.ui.text(), "birthday": mo.ui.date()}
    )

    batch
    return


@app.cell
def _(mo):
    mo.md(r"""##Custom filters using Polars 👈""")
    return


@app.cell
def _(mo, pl):


    df = pl.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "David"],
        "age": [25, 30, 35, 40],
        "city": ["New York", "London", "Paris", "Tokyo"]
    })

    age_filter = mo.ui.slider.from_series(df["age"], label="Max age")
    city_filter = mo.ui.dropdown.from_series(df["city"], label="City")

    mo.hstack([age_filter, city_filter])

    return age_filter, city_filter, df


@app.cell
def _(age_filter, city_filter, df, mo, pl):
    # Cell 2
    filtered_df = df.filter((pl.col("age") <= age_filter.value) & (pl.col("city") == city_filter.value))
    mo.ui.table(filtered_df)
    return


@app.cell
def _(mo):
    mo.md(r"""##Testing notebooks""")
    return


@app.cell
def _(pytest):

    class Tests:
        @staticmethod
        def test1_calculator():
            assert funcionCalculadora(10, 7,"-")==3, "This test passes"
    

        @staticmethod
        def test2_calculator():
            assert funcionCalculadora(3, 2, "*")==8, "This test fails"

    @pytest.mark.parametrize(
        "x,y,op,solution",
        [
            (10,7, "-",3),
            (3,2, "*",6),
            (5,1, "+",6),
            (8,4, "/",2),
        
        ]
    )
        

    def test_parameterized(x, y, op, solution):
        assert funcionCalculadora(x, y, op) == solution
    return


@app.cell
def _():
    return


@app.function
def inc(x):
    return x + 1


@app.cell
def _(pytest):
    class TestBlock:
        @staticmethod
        def test_fails():
            assert inc(3) == 5, "This test fails"

        @staticmethod
        def test_sanity():
            assert inc(3) == 4, "This test passes"

    @pytest.mark.parametrize(("x", "y"), [(3, 4), (4, 5)])
    def test_param(x, y):
        assert inc(x) == y
    return


if __name__ == "__main__":
    app.run()
