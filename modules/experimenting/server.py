import edgedb
import asyncio
import contextvars
import functools
from edgedb import create_async_pool
from .env import Config
from enum import Flag, auto
from secrets import token_hex
import uvicorn

"""
Global namespace of mutable context vars
"""
# Contextually typed as `edgedb.AsyncioPool`.
# (I'm anticipating that when the server calls
# `aiopool_ctx.set(<var>)`, the Python runtime
# will magically track all of the reference counts 
# to an underlying `AsyncioPool` connection.
aiopool_ctx = contextvars.ContextVar('aiopool')


# Depending on `RequestKind`, `edb_result` might be an
# `asyncio.Future` that anticipates an EdgeSet, EdgeTuple, or JSON.
edb_result_ctx = contextvars.ContextVar('edb_result')

# A boolean value indicating whether we create transactions
use_transactions_ctx = contextvars.ContextVar('transact')

class UseTransactions(Flag):
    """class UseTransactions(enum.Flag):
    A boolean switch that enables the server
    to toggle between running the query as
    a transactional commit or not.
    To disable the default transactional mode,
    clients should supply: `"UseTransactions":"false"`
    in the POST request body."""
    true  = auto()
    false = auto()

# An interface for choosing which kind
# of query or statement execution will be
# made. (See `class FetchExecKind` below)
fetch_exec_kind = contextvars.ContextVar('fetchEx')

class FetchExecKind(Flag):
    """class FetchExecKind(enum.Flag):
    A prototype extracted from the request's data
    body. If `FetchExecKind` is not explicitly
    defined in the body as any of the following 
    options:
        1.) "FetchExecKind":"execute"
        2.) "FetchExecKind":"fetchone_json"
        3.) "FetchExecKind":"fetchall_json"
    then the connection will default to using 
    `fetchall_json` when formatting the database's
    return to the client.
    """
    execute       = auto()
    fetchone      = auto()
    fetchone_json = auto()
    fetchall      = auto()
    fetchall_json = auto()

async def handle_request(statement):
    """async def handle_request(request: dict) -> None
    This method dispatches the request prepared by
    the client.
    Any data created in this coroutine, including errors,
    will be returned."""
    fetchEx     = fetch_exec_kind.get('fetchEx')
    transact    = use_transactions_ctx.get('transact')
    aiopool     = aiopool_ctx.get('aiopool')
    loop        = asyncio.get_running_loop()
    db_response = loop.create_future()
    connection  = aiopool.acquire()

    # Initialize some names and handlers for retaining
    # DB responses
    res = None
    if transact & UseTransactions.true:
        async with connection.transaction():
            if fetchEx & FetchExecKind.fetchall_json:
                res = await connection.fetchall_json(statement)
            elif fetchEx & FetchExecKind.fetchall:
                res = await connection.fetchall(statement)
            elif fetchEx & FetchExecKind.fetchone_json:
                res = await connection.fetchone_json(statement)
            elif fetchEx & FetchExecKind.fetchone:
                res = await connection.fetchone(statement)
            elif fetchEx & FetchExecKind.execute:
                res = await connection.execute(statement)
            else:
                raise ValueError("""Client did not specify a valid
                execution kind. Aborting the transaction.""")        
            try:
                async with connection.transaction():
                    await connection.execute("SELECT {0}")
                    raise Exception
            except:
                pass
        while True:
            await aiopass()
            if res is not None:
                try:
                    db_response.set_result(res)
                except asyncio.CancelledError:
                    raise asyncio.CancelledError("""
                    Attempted to set the result of a
                    db_response future when it had
                    already been marked as completed.
                    """
                )
                finally:
                    break
            else:
                await aiopass()

    elif transact & UseTransactions.false:
        async with connection:
            if fetchEx & FetchExecKind.fetchall_json:
                res = await connection.fetchall_json(statement)
            elif fetchEx & FetchExecKind.fetchall:
                res = await connection.fetchall(statement)
            elif fetchEx & FetchExecKind.fetchone_json:
                res = await connection.fetchone_json(statement)
            elif fetchEx & FetchExecKind.fetchone:
                res = await connection.fetchone(statement)
            elif fetchEx & FetchExecKind.execute:
                res = await connection.execute(statement)
            else:
                raise ValueError("""
                Client did not specify a valid
                execution kind. Aborting the 
                transaction.""")    
        while True:
            await aiopass()
            if res is not None:
                break
            else:
                await aiopass()
        try:
            db_response.set_result(res)
        except asyncio.CancelledError as e:
            raise asyncio.CancelledError("""
            Attempted to set the result of a 
            db_response future when it had
            already been marked as completed.
            """
        )
        return db_response
    else:
        # Assume that `transact` was never set
        # in the first place properly by this
        # server, and throw a generic exception.
        raise Exception("Transaction kind (`true` or `false`) was never properly set. Exiting.")

async def aiopass():
    await asyncio.sleep(0.0000001)


