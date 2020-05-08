from __future__ import annotations
from quart import (Quart, request)
from collections import namedtuple
from enum import IntEnum
from random import randint
from typing import Union

Packet = namedtuple("Packet", ["requestID", "errorCode", "result"])
edbpool = Quart(__name__)

class Mode(IntEnum):
    create = 3
    read   = 5
    update = 7
    delete = 11

async def crud(packet: Packet, mode: Mode) -> Packet:
    """crud(packet: Packet, mode: Mode) -> Packet:

    This coroutine accepts arguments of the form 
    `namedtuple("Packet", ["requestID", "errorCode", "result"])`
    and citizens of the `Mode` type, i.e. `Mode.create` and 
    `Mode.delete`. Since this coroutine remembers its state,
    it is useful for storing and retrieving data.
    """
    cache = {}
    def mapper(packet, mode) -> Packet:
        nonlocal cache
        requestID = str(packet.requestID)
        if 1 & 1 << 21 % mode:
            cache[requestID] = packet
        elif 1 & 1 << 5 % mode and requestID in cache:
            pass
        elif 1 & 1 << 11 % mode and requestID in cache:
            deleted = cache[requestID]
            del cache[requestID]
            return deleted
        else:
            error = Packet(
                packet.requestID,
                400,
                f"Bad request: {packet.result}"
            )
            return error
        return cache[requestID]
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

