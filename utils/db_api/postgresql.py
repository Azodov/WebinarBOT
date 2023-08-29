from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NULL UNIQUE,
        otp BIGINT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NOT NULL UNIQUE,
        language VARCHAR(255) NOT NULL DEFAULT 'uz',
        region VARCHAR(255) NOT NULL,
        fullname VARCHAR(255) NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        selected_service VARCHAR(255) NULL,
        amount_paid VARCHAR(255) NULL,
        cheques VARCHAR(255) NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    """
    ---------------------------------------------CONTROL ADMINS--------------------------------------------------------
    """

    async def add_admin(self, telegram_id: int, name: str, otp: int):
        sql = """
                INSERT INTO admins(telegram_id, name, otp) VALUES($1, $2, $3)
                """
        await self.execute(sql, telegram_id, name, otp, execute=True)

    async def select_admin(self, **kwargs):
        sql = """
            SELECT * FROM admins WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_admin(self, **kwargs):
        sql = """
            DELETE FROM admins WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def update_admin(self, telegram_id: int, action: str, otp: int):
        sql = """
            UPDATE admins SET telegram_id=$1, otp=$2 WHERE otp=$3
            """
        return await self.execute(sql, telegram_id, action, otp, execute=True)

    async def select_all_admins(self):
        sql = """
            SELECT * FROM admins
            """
        return await self.execute(sql, fetch=True)

    """
    ---------------------------------------------USER CONTROLLER--------------------------------------------------------
    """

    async def add_user(self, telegram_id: int, language: str, region: str, fullname: str, phone_number: str,
                       selected_service: str, amount_paid: str, cheques: str = None):
        sql = """
                INSERT INTO users(telegram_id, language, region, fullname, phone_number, selected_service, amount_paid, cheques) 
                VALUES($1, $2, $3, $4, $5, $6, $7, $8)
                """
        await self.execute(sql, telegram_id, language, region, fullname, phone_number, selected_service, amount_paid,
                           cheques, execute=True)

    async def select_user(self, **kwargs):
        sql = """
            SELECT * FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_users_by_condition(self, **kwargs):
        sql = """
            SELECT * FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_daily_users(self):
        sql = """
            SELECT * FROM users WHERE created_at::date = CURRENT_DATE
            """
        return await self.execute(sql, fetch=True)

    async def delete_user(self, **kwargs):
        sql = """
            DELETE FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def select_all_users(self):
        sql = """
            SELECT * FROM users
            """
        return await self.execute(sql, fetch=True)

    async def count_users(self):
        sql = """
            SELECT COUNT(*) FROM users
            """
        return await self.execute(sql, fetchval=True)
