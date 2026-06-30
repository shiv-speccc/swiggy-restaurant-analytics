# Swiggy Restaurant Analytics Dashboard

An interactive business analytics dashboard built with **Dash (Plotly)**, analyzing Swiggy's restaurant
listings dataset across 9 Indian cities — covering market coverage, pricing, ratings, cuisine trends,
and delivery time performance.

## Project Structure
```
swiggy-dashboard/
├── app.py              # Main Dash application
├── requirements.txt    # Python dependencies
├── data/
│   └── swiggy.csv      # Dataset (~8,680 restaurants)
└── README.md
```

## Features
- **KPI cards**: total restaurants, cities covered, avg rating, avg price for two, avg delivery time, cuisines tracked
- **Filters**: city (multi-select), cuisine (multi-select), price range slider, minimum rating slider — all linked across every chart
- **Charts**:
  - Restaurants by city
  - Average rating by city
  - Top 10 cuisines by restaurant count
  - Price vs. rating scatter (bubble size = number of ratings)
  - Delivery time distribution
  - Top 10 areas by restaurant count
- **Data table**: sortable/filterable list of top-rated restaurants matching the current filters

## How to Run in VS Code

1. **Open the folder** `swiggy-dashboard` in VS Code (`File > Open Folder`).

2. **Create a virtual environment** (recommended — use the integrated terminal, `` Ctrl+` ``):
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

5. Open your browser to **http://127.0.0.1:8050** — the dashboard will load there. It auto-reloads
   on save since debug mode is on.

> Note: this project doesn't need conda/scipy, so the Smart App Control / DLL issue you've hit before
> with scipy-based projects shouldn't come up here. If `pip install` ever gets blocked, fall back to a
> conda env the same way you did for your other projects (`conda create -n swiggy python=3.11`).

## Publishing to GitHub (web UI, since Git isn't installed locally)
1. Create a new repo on GitHub (e.g. `swiggy-restaurant-analytics`).
2. Click **Add file > Upload files**, drag in `app.py`, `requirements.txt`, `README.md`, and the `data/` folder.
3. Commit directly to `main`.

## Deploying (optional)
This app is structured for easy deployment to **Render** or **Railway** (both support Dash via `gunicorn`):
- The Flask server is exposed as `server = app.server` in `app.py`, which is what these platforms expect.
- Start command: `gunicorn app:server`
- Add `gunicorn` to `requirements.txt` before deploying.

## Dataset
Source: *Swiggy Restaurants Dataset* (Kaggle, by Abhijit Dahatonde). Columns: restaurant name, area, city,
price for two, average rating, total ratings, food/cuisine type, address, and delivery time — covering
Bangalore, Mumbai, Chennai, Pune, Hyderabad, Kolkata, Ahmedabad, Delhi, and Surat.
