# Database Snapshot Directory

This directory is reserved for optional local PostgreSQL initialization snapshots.

The public portfolio copy intentionally does not include a database snapshot because snapshots can contain seeded demo records and account data. For local development, the backend can seed an empty database at startup when `AUTO_SEED=true`.

If you create a private development snapshot, place it here as:

```text
001_snapshot.sql
```

Do not commit snapshots that contain credentials, real patient information, or private demo records.
