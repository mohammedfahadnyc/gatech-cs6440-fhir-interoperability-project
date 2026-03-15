# Database Snapshot Directory

Place the checked-in PostgreSQL snapshot in this folder as:

```text
001_snapshot.sql
```

When a developer starts PostgreSQL with a fresh Docker volume, the official Postgres image automatically imports SQL files from this directory.

Typical flow:

1. Run the backend and add or update data.
2. Export the current database state with `backend/scripts/export_db_snapshot.sh`.
3. Commit the updated `001_snapshot.sql`.
4. Fresh clones can initialize PostgreSQL from that snapshot.
