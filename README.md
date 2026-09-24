# Production-Style Investment Analytics Platform

A small internal-fintech style platform for ingesting investment data, storing it in a relational model, reconciling NAVs, calculating performance and exposures, and serving portfolio analytics through Streamlit.

## Stack

- Python
- PostgreSQL-compatible SQLAlchemy models
- Pandas / NumPy
- Pydantic validation
- PyTest
- Streamlit
- structured logging and config

## Data model

- managers
- funds
- share_classes
- nav_history
- flows
- positions
- strategy_assignments
- exposures

## Processing

- NAV ingestion and reconciliation
- share-class returns
- cumulative performance
- portfolio and manager aggregation
- drawdowns
- exposure aggregation
- attribution-style contribution analysis
- reusable risk metrics
- duplicate and invalid-input validation

## Validation status

The current demo pipeline passes **6 automated tests** and successfully builds the synthetic relational dataset end to end.

The bootstrap workflow inserts monthly NAV history across multiple share classes, exercises the service/repository layer, and creates a working analytics database suitable for the Streamlit front end.

All demo data are synthetic. No proprietary investment information is included.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
pytest -q
python scripts/bootstrap_demo.py
streamlit run dashboard/app.py
```

By default the demo uses SQLite for zero-configuration reproducibility. Set `DATABASE_URL` to a PostgreSQL connection string for a production-style deployment.

## Scope

This project is designed as an internal investment-data and analytics platform rather than as a single standalone model. The emphasis is on reproducible ingestion, normalized data structures, validation, reconciliation, reusable analytics, and an operator-facing dashboard.
