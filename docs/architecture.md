# Architecture

The platform is split into configuration, relational persistence, input validation, repository, service, calculation, reconciliation, and presentation layers.

SQLAlchemy defines PostgreSQL-compatible relational models while SQLite provides a zero-configuration test and demo environment. Pydantic validates incoming NAV, flow, and position payloads before persistence. Repository methods isolate SQL access, while the service layer provides application-level ingestion workflows.

Analytics functions are side-effect free and independently testable. Reconciliation compares estimated and final NAVs in basis points and flags missing records as failures. Composite uniqueness constraints protect share-class/date NAV history from duplicate records.

The Streamlit frontend reads from the same relational model rather than a separate spreadsheet export. Demo data are synthetic and deliberately separated from any proprietary investment data.
