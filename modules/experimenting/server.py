import edgedb
import asyncio
import contextvars
from edgedb import asyncio_pool
from .env import Config
from enum import Flag, auto

"""
Namespace of mutable globals
"""
# Contextually typed as `edgedb.AsyncioPool`
aiopool_ctx = contextvars.ContextVar('aiopool')

# Depending on `RequestKind`, `edb_result` might be an
# `asyncio.Future` that anticipates an EdgeSet, EdgeTuple, or JSON.
edb_result_ctx = contextvars.ContextVar('edb_result')

# A boolean value indicating whether we create transactions
use_transactions_ctx = contextvars.ContextVar('use_trans')

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
fetch_exec_kind = contextvars.ContextVar('fek')

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
    fetchone_json = auto()
    fetchall_json = auto()

class PoolInterface:
    def __create_pool
