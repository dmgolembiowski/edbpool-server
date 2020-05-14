# EDB Pool Server

> A simple interface for setting up your connection(s) to EdgeDB using the desirable asynchronous pools in the edgedb python client api. All you have to do is send your edgeql statements and it handles the rest. 

### Overview

This project started as something I wish existed a couple months after EdgeDB 1.0 alpha was released: an opinionated standalone instance that controls your EdgeDB connection pools. The primary aim for this service is to expose easily accessible routes for executing and querying under one hood. 

<br />

This standalone server aims to give clients the most performant way to interact with EdgeDB over a network, especially for systems that make heavy use of
reverse proxying or monolithic DNS topologies. Likewise, it aims to give Systems and Database Administrators an intuitive way to manage their company's EdgeDB assets, like those offered by enterprise database systems. 

## Installation
*ToDo*

## Development Requirements for Contributiors on any OS
- Docker

## Contribution instructions
```bash
git clone --recurse-submodules https://github.com/dmgolembiowski/edbpool.git
git submodule foreach git pull origin master
```
then follow the [remaining instructions](https://github.com/dmgolembiowski/edgedb-docker) on the Edbpool-Server's Docker repository.

```bash
cd edbpool/modules/edgedb-docker
```

```bash
# Depending on your operating system or Docker installation,
# you may need to elevate to root/admin to run these next commands.
# Additionally, `1-alpha2` can be replaced with any other valid version.

docker build -t edgedb:1-alpha2 --build-arg version=1-alpha2 .
docker run -it --rm \
    -p 15656:5656 \
    -p 5656:5656 \
    -p 6565:16565 \
    -p 16565:16565 \
    -p 18888:18888 \
    -p 8888:8888 \
    --name=edgedb-server \
    -v <datadir>:/var/lib/edgedb/data edgedb:1-alpha2
# See appendix 2 for a one-liner
```

## QA/Testing Roadmap
Note: Tests and scripts are to be fashioned for running on the Docker instance rather than the developer's local environment.

## Phase 1 Requirements Plan

### 1. Simulated OS-check
> Check the platform and distribution for
- [X] fail on MacOSX
- [X] fail on Windows
- [X] pass on Ubuntu Linux
- [X] pass on Debian Linux

### 2. Reading values in from a config
- [X] EdgeDB DSN
- [X] HTTP test address
- [X] HTTP test port

### 3. Have a "pullable" docker image of Debian with EdgeDB and add a set of single port forwards 127.0.0.1:{from -> to} 
- [X]         5566 -> 5656 if 5566 is available, otherwise 15566 + (x: n + 1) -> 5656
- [X]         6655 -> 6565 if 6655 is available, otherwise 16655 + (x: n + 1) -> 6565
- [X]        18888 -> 18888 if 18888 is available, otherwise ( n + 1 ) as above
- [X]        18080 -> 18080 if 18080 is available, otherwise ( n + 1 ) as above
```
    where ports are allocated for

    {5566, 15566 (fallback)} - main EdgeDB CLI
    {6655, 16655 (fallback)} - async EDB pool master
                       18888 - Reverse Shell/RPC-like controls
                               or some other comparable passthrough mechanism
                       18080 - HTTP Server related scripting
```

### 5. Give the docker image a set of installation steps like those at:
- [X] https://edgedb.com/docs/internals/dev/
- [X] https://edgedb.com/docs/tutorial/install#ref-tutorial-install

### 6. Run tests from (x) as described:
~~- [ ] at https://edgedb.com/docs/internals/dev#running-tests over the reverse shell.~~

## Phase 2 Requirements Plan

### 1. Create a Docker container mock script for:
- [X] PyEnv installation
- [X] Dual-purpose Reverse-Shell/Remote procedure call server to run within Docker
- [X] Python interface to directly coordinate test actions with the `edbpool` user in Docker over the RPC reverse shell API
<!-- - [ ] -->

### 2. Create and test a mock HTTP server with seven distinct URIs:
- [X] `"/"                                                   -> '{}'`
- [X] `"/execute/<statement:str>"                            -> '{}'`
- [X] `"/fetchone_json/<query:str>"                          -> '[{}]'`
- [X] `"/fetchall_json/<query:str>"                          -> '[{}]'`
- [X] `"/result?requestID=<id:int32>"                        -> (CRUD server storage access endpoint)`
- [ ] `"/error?requestID=<id:uint32>&error_code=<err:uint32>"-> (Lookup logged data saved under '/result', or serve as a redirection endpoint for some non-defined route)`

### 3. Extend capabilities in the mock HTTP server for:
- [ ] `async def set_result`
- [ ] `async def get_result`

### 4. Updates to the edgedb-docker Dockerfile
- [ ] Adding capability for data persistence for the `edbpool` user in `/var/data/edbpool/` such that `/home/` and `/srv/` are preserved

## Phase 3

### 1. Research and development
- [ ] Perform an in-depth analysis on the edgedb-python asynchronous connection pool API
- [ ] Integrate logic from the [test pool](https://github.com/edgedb/edgedb-python/blob/master/tests/test_pool.py) to recreate the behavior of `test_pool_no_acquire_deadlock` with an `asyncio.LifoQueue`

### 2. Application of prototyping
Using concepts gathered from Phase 2.2 and Phase 3.1, create an HTTP server with the following requirements:
- [ ] At least two non-deadlocking, reachable, and concurrent `edgedb.AsyncIOPool` such that pools P<sub>1</sub>, P<sub>2</sub>, ... , P<sub>n</sub> are open for databases DB<sub>1</sub>, DB<sub>2</sub>, ... , DB<sub>n</sub>.
- [ ] Each connection class is used
- [ ] DNS initialization information is gathered from a supplied properties file
- [ ] The service can be remotely started and stopped by the `edbpool.mock.edbpool_exec` API

## Phase 4a

### 1. Logging
- [ ] Create a logging interface for single owner file buffers 
- [ ] Create a logging interface for single owner INET streams
- [ ] Create a logging interface for multiple, sharing local owner file buffer
- [ ] Create a logging interface for multiple, sharing owner INET streams

### 2. Fault Tolerance Review
- [ ] Prepare an analysis of likely errors and exceptions to occur during with the Phase 3.2 prototype, and append those to this remaining section
- [ ]
- [ ]
- [ ] 
- [ ]
- [ ]

### 3. Fault Tolerance Revisions
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]

### 4. Advanced Edbpool Server Configuration and Deployment Scripts
- [ ]
- [ ]
- [ ]

### 5. Official Release (earliest projection at July 30)
- [ ] PyPI
- [ ] Debian Repository
- [ ] Ubuntu PPA
- [ ] Docker

### Ongoing: Maintaining README files and contributor setup instructions

> Appendix
    - <insert command here>
    - docker run -it --rm -p 15656:5656 -p 5656:5656 -p 6565:16565 -p 16565:16565 -p 18888:18888 -p 8888:8888 --name=edgedb-server -v /tmp/:/var/lib/edgedb/data edgedb:1-alpha2
