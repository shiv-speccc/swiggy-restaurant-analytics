"""
Swiggy Restaurant Analytics Dashboard
Run with: python app.py
Then open http://127.0.0.1:8050 in your browser
"""

import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

# ----------------------------------------------------------------------
# 1. LOAD & PREP DATA
# ----------------------------------------------------------------------
df = pd.read_csv("data/swiggy.csv")
df.columns = [c.strip() for c in df.columns]

df["Food type"] = df["Food type"].fillna("")
cuisine_long = (
    df.assign(Cuisine=df["Food type"].str.split(","))
    .explode("Cuisine")
)
cuisine_long["Cuisine"] = cuisine_long["Cuisine"].str.strip()
cuisine_long = cuisine_long[cuisine_long["Cuisine"] != ""]

CITIES = sorted(df["City"].unique())
CUISINES = sorted(cuisine_long["Cuisine"].unique())

PRICE_MIN, PRICE_MAX = int(df["Price"].min()), int(df["Price"].max())
RATING_MIN, RATING_MAX = float(df["Avg ratings"].min()), float(df["Avg ratings"].max())

# ----------------------------------------------------------------------
# 2. APP SETUP
# ----------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Swiggy Restaurant Analytics",
)
server = app.server

SWIGGY_ORANGE = "#fc8019"

# ----------------------------------------------------------------------
# 3. REUSABLE COMPONENTS
# ----------------------------------------------------------------------
def kpi_card(title, value_id, icon=""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icon, style={"fontSize": "26px"}),
                html.H3(id=value_id, className="card-title mb-0", style={"fontWeight": "700"}),
                html.P(title, className="text-muted mb-0", style={"fontSize": "13px"}),
            ]
        ),
        className="shadow-sm text-center h-100",
        style={"borderTop": f"4px solid {SWIGGY_ORANGE}"},
    )


def chart_card(title, graph_id, width):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6(title, className="mb-2", style={"fontWeight": "600"}),
                    dcc.Graph(id=graph_id, config={"displayModeBar": False}),
                ]
            ),
            className="shadow-sm h-100",
        ),
        md=width,
        className="mb-4",
    )


# ----------------------------------------------------------------------
# 4. LAYOUT
# ----------------------------------------------------------------------
filters = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Filters", style={"fontWeight": "700", "color": SWIGGY_ORANGE}),
            html.Label("City", className="mt-2 fw-semibold"),
            dcc.Dropdown(
                id="city-filter",
                options=[{"label": c, "value": c} for c in CITIES],
                multi=True,
                placeholder="All cities",
            ),
            html.Label("Cuisine", className="mt-3 fw-semibold"),
            dcc.Dropdown(
                id="cuisine-filter",
                options=[{"label": c, "value": c} for c in CUISINES],
                multi=True,
                placeholder="All cuisines",
            ),
            html.Label("Price for Two (₹)", className="mt-3 fw-semibold"),
            dcc.RangeSlider(
                id="price-filter",
                min=PRICE_MIN,
                max=PRICE_MAX,
                value=[PRICE_MIN, PRICE_MAX],
                tooltip={"placement": "bottom", "always_visible": False},
                marks=None,
            ),
            html.Label("Minimum Rating", className="mt-3 fw-semibold"),
            dcc.Slider(
                id="rating-filter",
                min=RATING_MIN,
                max=RATING_MAX,
                step=0.1,
                value=RATING_MIN,
                marks={i: str(i) for i in range(int(RATING_MIN), int(RATING_MAX) + 1)},
                tooltip={"placement": "bottom", "always_visible": False},
            ),
        ]
    ),
    className="shadow-sm h-100",
)

kpi_row = dbc.Row(
    [
        dbc.Col(kpi_card("Restaurants", "kpi-total", "🍽️"), md=2),
        dbc.Col(kpi_card("Cities Covered", "kpi-cities", "🏙️"), md=2),
        dbc.Col(kpi_card("Avg Rating", "kpi-rating", "⭐"), md=2),
        dbc.Col(kpi_card("Avg Price for Two", "kpi-price", "💰"), md=2),
        dbc.Col(kpi_card("Avg Delivery Time", "kpi-delivery", "🛵"), md=2),
        dbc.Col(kpi_card("Cuisines Tracked", "kpi-cuisines", "🍜"), md=2),
    ],
    className="mb-4 g-3",
)

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("🟠 Swiggy Restaurant Analytics", style={"fontWeight": "800"}),
                        html.P(
                            "Business intelligence dashboard — market coverage, pricing, ratings & delivery performance",
                            className="text-muted",
                        ),
                    ]
                )
            ),
            className="mt-4 mb-3",
        ),
        kpi_row,
        dbc.Row(
            [
                dbc.Col(filters, md=3),
                dbc.Col(
                    dbc.Row(
                        [
                            chart_card("Restaurants by City", "fig-city-count", 6),
                            chart_card("Average Rating by City", "fig-city-rating", 6),
                            chart_card("Top 10 Cuisines by Restaurant Count", "fig-top-cuisines", 6),
                            chart_card("Price vs. Rating", "fig-price-rating", 6),
                            chart_card("Delivery Time Distribution", "fig-delivery-dist", 6),
                            chart_card("Top 10 Areas by Restaurant Count", "fig-top-areas", 6),
                        ]
                    ),
                    md=9,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6("Top Rated Restaurants (filtered)", style={"fontWeight": "600"}),
                            dash_table.DataTable(
                                id="restaurant-table",
                                columns=[
                                    {"name": i, "id": i}
                                    for i in [
                                        "Restaurant",
                                        "City",
                                        "Area",
                                        "Food type",
                                        "Price",
                                        "Avg ratings",
                                        "Total ratings",
                                        "Delivery time",
                                    ]
                                ],
                                page_size=10,
                                sort_action="native",
                                filter_action="native",
                                style_table={"overflowX": "auto"},
                                style_cell={"fontSize": "13px", "padding": "6px"},
                                style_header={
                                    "backgroundColor": SWIGGY_ORANGE,
                                    "color": "white",
                                    "fontWeight": "600",
                                },
                            ),
                        ]
                    ),
                    className="shadow-sm",
                ),
                className="mb-5",
            )
        ),
    ],
    fluid=True,
    style={"backgroundColor": "#f8f9fa"},
)


# ----------------------------------------------------------------------
# 5. FILTER HELPER
# ----------------------------------------------------------------------
def filter_data(cities, cuisines, price_range, min_rating):
    dff = df.copy()
    if cities:
        dff = dff[dff["City"].isin(cities)]
    if cuisines:
        pattern = "|".join([c.replace("+", r"\+") for c in cuisines])
        dff = dff[dff["Food type"].str.contains(pattern, case=False, na=False, regex=True)]
    dff = dff[(dff["Price"] >= price_range[0]) & (dff["Price"] <= price_range[1])]
    dff = dff[dff["Avg ratings"] >= min_rating]
    return dff


# ----------------------------------------------------------------------
# 6. CALLBACKS
# ----------------------------------------------------------------------
@app.callback(
    Output("kpi-total", "children"),
    Output("kpi-cities", "children"),
    Output("kpi-rating", "children"),
    Output("kpi-price", "children"),
    Output("kpi-delivery", "children"),
    Output("kpi-cuisines", "children"),
    Output("fig-city-count", "figure"),
    Output("fig-city-rating", "figure"),
    Output("fig-top-cuisines", "figure"),
    Output("fig-price-rating", "figure"),
    Output("fig-delivery-dist", "figure"),
    Output("fig-top-areas", "figure"),
    Output("restaurant-table", "data"),
    Input("city-filter", "value"),
    Input("cuisine-filter", "value"),
    Input("price-filter", "value"),
    Input("rating-filter", "value"),
)
def update_dashboard(cities, cuisines, price_range, min_rating):
    dff = filter_data(cities, cuisines, price_range, min_rating)

    total = len(dff)
    n_cities = dff["City"].nunique()
    avg_rating = round(dff["Avg ratings"].mean(), 2) if total else 0
    avg_price = round(dff["Price"].mean(), 0) if total else 0
    avg_delivery = round(dff["Delivery time"].mean(), 1) if total else 0

    dff_long = (
        dff.assign(Cuisine=dff["Food type"].str.split(","))
        .explode("Cuisine")
    )
    dff_long["Cuisine"] = dff_long["Cuisine"].str.strip()
    dff_long = dff_long[dff_long["Cuisine"] != ""]
    n_cuisines = dff_long["Cuisine"].nunique()

    city_counts = dff["City"].value_counts().reset_index()
    city_counts.columns = ["City", "Count"]
    fig_city_count = px.bar(
        city_counts, x="City", y="Count", color_discrete_sequence=[SWIGGY_ORANGE]
    )
    fig_city_count.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)

    city_rating = dff.groupby("City")["Avg ratings"].mean().reset_index().sort_values("Avg ratings")
    fig_city_rating = px.bar(
        city_rating, x="Avg ratings", y="City", orientation="h",
        color_discrete_sequence=["#2c3e50"],
    )
    fig_city_rating.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)

    top_cuisines = dff_long["Cuisine"].value_counts().head(10).reset_index()
    top_cuisines.columns = ["Cuisine", "Count"]
    fig_top_cuisines = px.bar(
        top_cuisines.sort_values("Count"), x="Count", y="Cuisine", orientation="h",
        color_discrete_sequence=[SWIGGY_ORANGE],
    )
    fig_top_cuisines.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)

    fig_price_rating = px.scatter(
        dff, x="Price", y="Avg ratings", color="City", size="Total ratings",
        hover_name="Restaurant", opacity=0.7,
    )
    fig_price_rating.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)

    fig_delivery_dist = px.histogram(
        dff, x="Delivery time", nbins=20, color_discrete_sequence=["#2c3e50"]
    )
    fig_delivery_dist.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)

    top_areas = dff["Area"].value_counts().head(10).reset_index()
    top_areas.columns = ["Area", "Count"]
    fig_top_areas = px.bar(
        top_areas.sort_values("Count"), x="Count", y="Area", orientation="h",
        color_discrete_sequence=[SWIGGY_ORANGE],
    )
    fig_top_areas.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)

    table_data = (
        dff.sort_values("Avg ratings", ascending=False)
        .head(200)[
            ["Restaurant", "City", "Area", "Food type", "Price", "Avg ratings", "Total ratings", "Delivery time"]
        ]
        .to_dict("records")
    )

    return (
        f"{total:,}",
        n_cities,
        avg_rating,
        f"₹{avg_price:,.0f}",
        f"{avg_delivery} min",
        n_cuisines,
        fig_city_count,
        fig_city_rating,
        fig_top_cuisines,
        fig_price_rating,
        fig_delivery_dist,
        fig_top_areas,
        table_data,
    )


# ----------------------------------------------------------------------
# 7. RUN
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
