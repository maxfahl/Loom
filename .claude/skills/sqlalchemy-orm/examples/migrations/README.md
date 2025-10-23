# Alembic Migrations Example

This directory contains example Alembic migration scripts.

To use Alembic, you would typically:

1.  Initialize Alembic in your project root:
    ```bash
    alembic init alembic
    ```
2.  Configure `alembic.ini` and `alembic/env.py` to point to your database and models.
3.  Generate a new migration script:
    ```bash
    alembic revision --autogenerate -m "Description of migration"
    ```
4.  Apply migrations to your database:
    ```bash
    alembic upgrade head
    ```

Refer to the `alembic_setup.sh` script in the `scripts/` directory for automated setup.
