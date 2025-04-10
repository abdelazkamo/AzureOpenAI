from typing import Tuple, List, Any
import aioodbc
import pyodbc
from .db import Database


class DB_Operations:
    def __init__(self):
        self.db = Database()  # Use the singleton instance

    async def init_db(self):
        """Ensure the database is initialized safely."""
        await self.db.init_db()

    async def execute_query(
        self,
        query: str,
        params: Tuple = (),
        should_fetch_data: bool = False,
        retries=3,
        transaction=None,
    ):
        for _ in range(retries):
            conn = transaction if transaction else await self.db.getconn()
            try:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params)

                    if should_fetch_data:
                        rows = await cursor.fetchall()
                        columns = [column[0] for column in cursor.description]
                        result = [dict(zip(columns, row)) for row in rows]
                        if not transaction:
                            await conn.commit()
                        return result

                    if not transaction:
                        await conn.commit()
                    return cursor.rowcount
            except (pyodbc.OperationalError, pyodbc.InterfaceError):
                await self.db.safe_reinitialize()  # Safe pool switch without breaking queries
            except Exception as e:
                raise e
            finally:
                if not transaction:
                    await self.db.putconn(conn)

    async def execute_bulk_insertion(
        self,
        records: List[Tuple[Any]],
        table_name: str,
        columns: List[str],
        retries=3,
        transaction=None,
    ):
        # Build the SQL placeholders for each record
        placeholders = ", ".join(["?" for _ in columns])
        column_names = ", ".join(columns)
        insert_query = (
            f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        )

        for _ in range(retries):
            conn = transaction if transaction else await self.db.getconn()
            try:
                async with conn.cursor() as cursor:
                    # Execute batch insert
                    for record in records:
                        await cursor.execute(insert_query, record)

                    if not transaction:
                        await conn.commit()
                    return
            except (pyodbc.OperationalError, pyodbc.InterfaceError):
                await self.db.safe_reinitialize()  # Safe pool switch without breaking queries
            except Exception as e:
                raise e
            finally:
                if not transaction:
                    await self.db.putconn(conn)

    # For better performance on large datasets, add a fast_bulk_insert method
    async def fast_bulk_insert(
        self,
        table_name: str,
        columns: List[str],
        values: List[Tuple[Any]],
        batch_size=1000,
        retries=3,
    ):
        column_str = ", ".join(columns)

        for _ in range(retries):
            conn = await self.db.getconn()
            try:
                async with conn.cursor() as cursor:
                    # Process in batches
                    for i in range(0, len(values), batch_size):
                        batch = values[i : i + batch_size]

                        # Create SQL with multiple value sets
                        value_placeholders = []
                        flat_params = []

                        for row in batch:
                            placeholders = (
                                "(" + ", ".join(["?" for _ in range(len(row))]) + ")"
                            )
                            value_placeholders.append(placeholders)
                            flat_params.extend(row)

                        query = f"INSERT INTO {table_name} ({column_str}) VALUES {', '.join(value_placeholders)}"
                        await cursor.execute(query, flat_params)

                await conn.commit()
                return
            except (pyodbc.OperationalError, pyodbc.InterfaceError):
                await self.db.safe_reinitialize()
            except Exception as e:
                raise e
            finally:
                await self.db.putconn(conn)
