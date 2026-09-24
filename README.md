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

- NAV reconstruction and reconciliation
- share-class returns
- cumulative performance
- flows
- portfolio and manager aggregation
- drawdowns
- exposure aggregation
- reusable risk metrics
- duplicate and invalid-input validation

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

By default the demo uses SQLite for zero-configuration reproducibility. Set `DATABASE_URL` to a PostgreSQL connection string for production-style deployment.

All demo data are synthetic and do not contain proprietary investment information.
