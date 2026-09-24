# Architecture

The platform uses a layered architecture so persistence, validation, analytics, and presentation remain separate.

## Persistence layer

SQLAlchemy models define managers, funds, share classes, NAV history, flows, positions, strategy assignments, and exposures.

SQLite is the default local backend for zero-configuration reproducibility. The same ORM layer is PostgreSQL-compatible through `DATABASE_URL`.

## Validation layer

Pydantic schemas validate incoming records before persistence. Database constraints and duplicate checks provide a second line of defense against invalid or inconsistent records.

## Service and repository layer

Repository objects isolate database access from analytics logic. Service functions coordinate ingestion and reconciliation workflows, including estimated versus final NAV checks.

## Analytics layer

Reusable functions calculate:

- periodic NAV returns
- cumulative performance
- drawdowns
- annualized metrics
- flow-adjusted returns
- manager and portfolio aggregation
- exposure aggregation
- contribution-style attribution

## Dashboard

The Streamlit interface reads from the platform output and exposes portfolio overview, performance, manager analysis, attribution, exposures, and risk views.

## Validation

The current demo pipeline passes six automated tests and successfully builds the synthetic database end to end. The bootstrap script creates monthly NAV records for multiple share classes through the same service layer used by the application.

## Data discipline

All included demo records are synthetic. The repository intentionally contains no proprietary fund, investor, or portfolio data.
