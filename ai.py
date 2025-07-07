import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import polars as pl
    import numpy as np
    import altair as alt
    import pandas as pd

    # Define the number of random dates
    n_dates = 10

    # Generate random dates within a specific range
    start_date = pd.Timestamp('2022-01-01')
    end_date = pd.Timestamp('2022-12-31')
    random_dates = pd.date_range(start=start_date, end=end_date, freq='D').to_series().sample(n_dates).reset_index(drop=True)

    # Create a Polars DataFrame with random dates
    df = pl.DataFrame({"random_dates": random_dates})

    # Create a count of occurrences for visualization
    visual_data = df.group_by("random_dates").agg(pl.len().alias("count"))

    # Convert the Polars DataFrame to a pandas DataFrame for Altair
    visual_data_pd = visual_data.to_pandas()

    # Create an Altair chart
    chart = alt.Chart(visual_data_pd).mark_bar().encode(
        x='random_dates:T',
        y='count:Q',
        tooltip=['random_dates:T', 'count:Q']
    ).properties(
        title='Random Dates Count'
    )

    chart  # Display the chart

    return


if __name__ == "__main__":
    app.run()
