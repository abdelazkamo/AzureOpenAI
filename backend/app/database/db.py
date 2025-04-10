import aioodbc
import asyncio
import pyodbc
from quart import current_app


class Database:
    _instance = None
    _lock = asyncio.Lock()  # Prevents concurrent reinitialization

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.pool = None
            cls._instance._closing_pool = None  # Track old pool during transition
        return cls._instance

    async def init_db(self):
        """Safely initialize or reinitialize the connection pool."""
        async with self._lock:  # Prevent multiple inits at the same time
            if self.pool is None:  # Don't reinitialize if already set
                # Create connection string for MSSQL
                print("ok", current_app.config["DRIVER"])
                conn_str = (
                    f"DRIVER={current_app.config['DRIVER']};"
                    f"SERVER={current_app.config['SERVER']};"
                    f"DATABASE={current_app.config['DATABASE']};"
                    f"UID={current_app.config['UID']};"
                    f"PWD={current_app.config['PWD']}"
                    # f"TrustServerCertificate=yes;"
                )

                self.pool = await aioodbc.create_pool(
                    dsn=conn_str,
                    minsize=5,
                    maxsize=50,
                    autocommit=False,
                    echo=False,
                    timeout=20,
                )

    async def getconn(self):
        """Get a connection from the active pool."""
        if self.pool is None:
            await self.init_db()  # Ensure pool is initialized before acquiring
        return await self.pool.acquire()

    async def putconn(self, conn):
        """Release a connection back to the correct pool."""
        if self.pool:
            await self.pool.release(conn)

    async def safe_reinitialize(self):
        """Safely reinitialize the pool without disrupting active queries."""
        async with self._lock:
            if self.pool is not None:
                self._closing_pool = self.pool  # Mark old pool as "closing"
            self.pool = None  # Prevent new connections from using the old pool
            await self.init_db()  # Create a new pool

            # Close the old pool **after active queries finish**
            if self._closing_pool:
                old_pool = self._closing_pool
                self._closing_pool = None
                await old_pool.close()
