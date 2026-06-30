# 🟠 Swiggy Restaurant Market Analytics Dashboard

A business intelligence dashboard built to analyze Swiggy's restaurant marketplace — covering market
coverage, pricing strategy, cuisine demand, and delivery performance across 9 Indian cities. Built to
mirror the kind of internal analytics tooling a food-delivery platform's strategy/ops team would use to
track marketplace health and identify expansion or pricing opportunities.

**🔗 Live demo:** https://web-production-532f4.up.railway.app

---

## Business Context

Swiggy operates a two-sided marketplace where restaurant supply, pricing, and delivery performance
directly drive customer retention and order volume. This dashboard answers the kind of questions a
marketplace analytics or strategy team would ask:

- Which cities are under- or over-saturated with restaurant supply?
- How does pricing vary by city, and where is there room to attract premium or budget partners?
- Which cuisines dominate demand, and where are the gaps?
- Are delivery times within an acceptable SLA range, and where do they degrade?
- Which restaurants/areas are top performers worth highlighting or studying for best practices?

## Dataset

**Source:** Swiggy Restaurants Dataset (Kaggle, by Abhijit Dahatonde)
**Size:** ~8,680 restaurant listings across 9 cities — Bangalore, Mumbai, Chennai, Pune, Hyderabad,
Kolkata, Ahmedabad, Delhi, and Surat
**Fields:** restaurant name, area, city, price for two, average rating, total ratings, cuisine/food type,
address, delivery time

> Note: this is a public snapshot dataset (not live Swiggy data), used here to demonstrate dashboard
> engineering and analytical approach rather than real-time business reporting.

## Key Features

| Feature | Description |
|---|---|
| **KPI Summary** | Total restaurants, cities covered, average rating, average price for two, average delivery time, cuisines tracked |
| **Cross-linked Filters** | City (multi-select), cuisine (multi-select), price range, minimum rating — every chart and the data table update together |
| **City Analysis** | Restaurant count and average rating by city, to spot supply concentration and quality gaps |
| **Cuisine Analysis** | Top 10 cuisines by restaurant count, surfacing demand patterns |
| **Pricing Analysis** | Price-vs-rating scatter plot (bubble size = number of ratings) to spot value-for-money outliers |
| **Delivery Performance** | Delivery time distribution to flag SLA risk areas |
| **Area-level Breakdown** | Top 10 areas by restaurant count, for hyperlocal market density |
| **Restaurant Explorer** | Sortable, filterable table of top-rated restaurants matching current filters |

## Tech Stack

- **Dash (Plotly)** — chosen over Streamlit for this project specifically because it mirrors how
  production-grade BI tools handle multi-chart cross-filtering and granular callback-driven interactivity
- **Plotly Express** — interactive charting (zoom, hover, pan)
- **Pandas** — data prep and transformation (including cuisine de-duplication via explode on
  comma-separated fields)
- **Dash Bootstrap Components** — responsive layout and KPI card styling
- **Gunicorn** — production WSGI server for deployment

## Project Structure
```
swiggy-dashboard/
├── app.py              # Main Dash application (layout + callbacks)
├── requirements.txt    # Python dependencies
├── Procfile             # Start command for deployment (Render/Railway)
├── data/
│   └── swiggy.csv      # Dataset (~8,680 restaurants)
└── README.md
```

## Running Locally (VS Code)

1. **Open the folder** in VS Code: `File > Open Folder` → select `swiggy-dashboard`
2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the app**:
   ```bash
   python app.py
   ```
5. Open **http://127.0.0.1:8050** in your browser. Auto-reloads on save (debug mode is on).

> If `pip install` fails with a `metadata-generation-failed` error on pandas, it usually means your
> Python version is newer than the pinned package has a prebuilt wheel for. Fix: run
> `pip install --upgrade pandas dash dash-bootstrap-components plotly` to grab the latest compatible
> versions, since `requirements.txt` uses `>=` ranges rather than hard pins.

## Deployment

Deployed on **Railway** (Render also works — both support Dash via Gunicorn).

- Flask server exposed as `server = app.server` in `app.py`, which is what these platforms expect
- Start command (in `Procfile`): `web: gunicorn app:server`

**To deploy your own copy:**
1. Push this repo to GitHub
2. On Railway: **New Project → Deploy from GitHub repo** → select your repo
3. Railway auto-detects Python + the `Procfile` and builds automatically
4. Once deployed, go to **Settings → Networking → Generate Domain** for a public URL

## Possible Extensions

- City-level "expansion opportunity score" combining restaurant density, average rating, and pricing
  headroom
- A dedicated restaurant deep-dive page (search one restaurant, view its full profile)
- Time-based trend simulation if a dated/historical version of the dataset becomes available

---

**Author:** Shivarchan C ([GitHub](https://github.com/shiv-speccc) ·
[LinkedIn](https://www.linkedin.com/in/shivarchan-coomaran-b47b14293))
