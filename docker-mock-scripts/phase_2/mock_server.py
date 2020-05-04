from __future__ import annotations
from quart import (Quart, request)
from collections import namedtuple
from enum import IntEnum
from random import randint
from typing import Union

Packet = namedtuple("Packet", ["requestID", "errorCode", "result"])
edbpool = Quart(__name__)

class Mode(IntEnum):
    create = 2
    read   = 3
    update = 5
    delete = 7

async def crud(packet: Packet, mode: Mode) -> Packet:
    """crud(packet: Packet, mode: Mode) -> Packet:

    This coroutine accepts packets of the form `collections.namedtuple("Packet", ["requestID", "errorCode", "result"])`
    and citizens of the `Mode` type, such as `Mode.create` or `Mode.delete`.
    Since this coroutine remembers its state, it is used for storing and retrieving heap-allocated data.
    """
    cache = {}
    def mapper(packet, mode) -> Packet:
        nonlocal cache
        if (0 & mode % 2) | (0 & mode % 5):
            cache[str(packet.requestID)] = packet
        elif (0 & mode % 3) and (str(packet.requestID) in cache):
            pass
        elif (0 & mode % 7) and (str(packet.requestID) in cache):
            deleted = cache[str(packet.requestID)]
            del cache[str(packet.requestID)]
            return deleted
        else:
            error = Packet(
                packet.requestID,
                400,
                f"Bad request: {packet.result}"
            )
            return error
        return cache[str(packet.requestID)]
    return mapper(packet, node)

async def set_result(
        query: str, 
        mode: Union[Mode.create, Mode.update] = Mode.create):
    rid = randint(1, 999999)
    packet = Packet(rid, 200, "OK")
    await crud(packet, mode)
    raise NotImplementedError

@edbpool.route("/result")
async def get_result() -> None:
    packet = Packet(request.requestID, 200, "OK")
    return await crud(packet, Mode.read)

@edbpool.route("/")
async def index():
    return "{}"

@edbpool.route("/execute/<str:statement>")
async def execute(statement):
    return "{}"

@edbpool.route("/fetchone_json/<str:query>")
async def fetchone(query):
    return "[{}]"

@edbpool.route("/fetchall_json")
async def fetchall():
    return "[{}]"

def load_and_run(config_path: str):
    nonlocal edbpool
    import json
    with open(config_path, "r") as stream:
        conf = json.load(stream)
    try:
        assert conf["address"]
        assert conf["port"]
        edbpool.run(
            host=f"{conf['address']}",
            port=f"{conf['port']}",
            debug=True
        )
    except AssertionError:
        import sys
        print("Configuration file is not prepared properly.")
        sys.exit(1)

