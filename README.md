# Investment Data & NAV Analytics Platform

A Python and Streamlit demo that ingests monthly fund data, checks NAV arithmetic and turns a relational database into share-class performance and exposure views.

## Demo dataset

The seeded bootstrap creates 24 monthly observations per share class from January 2024 through December 2025: **2 managers, 2 funds, 2 share classes, 48 NAV records and 96 exposure records**. The NAV check compares reported total NAV with NAV per share multiplied by units.

This is an independent personal rebuild using synthetic data. It contains no Valmar Capital code or data.

## Run the local demo

```bash
pip install -r requirements.txt
export PYTHONPATH=src
DATABASE_URL=sqlite:///investment_analytics_demo.db python scripts/bootstrap_demo.py
DATABASE_URL=sqlite:///investment_analytics_demo.db streamlit run dashboard/app.py
```

Use a dedicated demo database. The bootstrap drops and recreates the schema before seeding it. See the [data model and service layout](docs/architecture.md) for details.
