import edgedb
import asyncio
from async_timeout import timeout
import contextvars
import functools
from edgedb import create_async_pool
from env import Config
from enum import Flag, auto
from secrets import token_hex
import uvicorn

from quart import Quart, request, abort

class AdaptedQuart(Quart):
    def __init__(self, name):
        self._edbconfig = {}
        super().__init__(name)

    def __getitem__(self, key):
        return self._edbconfig[key]
    
    def __setitem__(self, key, value):
        self._edbconfig[key] = value

app = AdaptedQuart(__name__)

"""
Global namespace of mutable context vars
"""
# Contextually typed as `edgedb.AsyncioPool`.
# (I'm anticipating that when the server calls
# `aiopool_ctx.set(<var>)`, the Python runtime
# will magically track all of the reference counts 
# to an underlying `AsyncioPool` connection.
# global aiopool_ctx
# aiopool_ctx = contextvars.ContextVar('aiopool')

'''
# Depending on `RequestKind`, `edb_result` might be an
# `asyncio.Future` that anticipates an EdgeSet, EdgeTuple, or JSON.
edb_result_ctx = contextvars.ContextVar('edb_result')
'''

# Request-specific query
statement_ctx = contextvars.ContextVar('statement')

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
    body. Because `edgedb.Set` instances do not 
    directly support pickling or binary object serialization,
    it doesn't make sense to allow the client to call the 
    `fetchone` or `fetchall` methods. 
    If `FetchExecKind` is not explicitly defined in the body 
    as any of the following options:
        1.) "FetchExecKind":"execute"
        3.) "FetchExecKind":"fetchone_json"
        4.) "FetchExecKind":"fetchall_json"
    then the connection will default to using 
    `fetchall_json` when formatting the database's
    return to the client.
    """
    execute       = auto()
    fetchone      = auto()
    fetchone_json = auto()
    fetchall      = auto()
    fetchall_json = auto()

async def handle_request(response_future):
    """async def handle_request(request: dict) -> None
    This method dispatches the request prepared by
    the client.
    Any data created in this coroutine, including errors,
    will be returned."""
    fetchEx     = fetch_exec_kind.get('fetchEx')
    transact    = use_transactions_ctx.get('transact')
    statement   = statement_ctx.get('statement')
    connection  = app["pool"].acquire()

    # Initialize some names and handlers for retaining
    # DB responses
    res = None
    if transact & UseTransactions.true:
        async with connection.transaction():
            if fetchEx & FetchExecKind.fetchall_json:
                res = await connection.fetchall_json(statement)
            elif fetchEx & FetchExecKind.fetchone_json:
                res = await connection.fetchone_json(statement)
            elif fetchEx & FetchExecKind.execute:
                res = await connection.execute(statement)
            else:
                abort(400, description="""Client did not specify a valid
                execution kind. Aborting the transaction.""")        
            try:
                # Nested transaction for the savepoint
                async with connection.transaction():
                    await connection.execute("select 0;")
                    raise Exception
            except:
                pass
        while True:
            await aiopass()
            if res is not None:
                try:
                    response_future.set_result(res)
                except asyncio.CancelledError:
                    abort(400, description="""
                    Attempted to set the result of a
                    response_future future when it had
                    already been marked as completed.
                    """)
                break
            else:
                await aiopass()

    elif transact & UseTransactions.false:
        async with connection:
            if fetchEx & FetchExecKind.fetchall_json:
                res = await connection.fetchall_json(statement)
            elif fetchEx & FetchExecKind.fetchone_json:
                res = await connection.fetchone_json(statement)
            elif fetchEx & FetchExecKind.execute:
                res = await connection.execute(statement)
            else:
                abort(400, description="""
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
            response_future.set_result(res)
        except asyncio.CancelledError as e:
            abort(400, description="""
            Attempted to set the result of a 
            response_future future when it had
            already been marked as completed.
            """
        )
    else:
        # Assume that `transact` was never set
        # in the first place properly by this
        # server, and throw a generic exception.
        abort(400 description="""Transaction kind (`true` or `false`) 
        was never properly set. Exiting.""")

async def aiopass():
    await asyncio.sleep(0.0000001)

@app.route('/', methods=['POST'])
async def recv():
    data = None
    loop = asyncio.get_running_loop()
    database_response_future = loop.create_future()
    async with timeout(Config.BODY_TIMEOUT):
        data = request.get_data()
    while True:
        await aiopass()
        if data is not None:
            # Set context vars with data keys.
            # Return '{"error": -1}' if
            # everything required was not present
            try:
                transact.set(UseTransactions.true if data["UseTransactions"] else UseTransactions.false)
                fetchEx.set(
                    FetchExecKind.fetchall_json if data["FetchExecKind"] == "fetchall_json" else
                        FetchExecKind.fetchone_json if data["FetchExecKind"] == "fetchone_json" else
                            FetchExecKind.execute
                )
                statement.set(data["statement"])
                await handle_request(database_response_future)
                await database_future_response
                return database_future_response.get()
            except KeyError:
                return abort(400, description="""
                The client's POST request body did not contain
                the sufficient data.""")
    
@app.before_serving
async def create_db_pool():
    app["pool"] = await edgedb.create_async_pool(
        dsn=Config.dsn(),
        min_size=Config.min_size,
        max_size=Config.max_size
    )

if __name__ == "__main__":
    app.run(
        host=Config.host,
        port=Config.port,
        debug=True
    )

