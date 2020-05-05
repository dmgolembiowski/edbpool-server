# EDB Pool Server

> A simple interface for setting up your connection(s) to EdgeDB using the desirable asynchronous pools in the edgedb python client api. All you have to do is send your edgeql statements and it handles the rest. 

### Overview

This project started as something I wish existed a couple months after EdgeDB 1.0 alpha was released: an opinionated standalone instance that controls your EdgeDB connection pools. The primary aim for this service is to expose easily accessible routes for executing and querying under one hood. 

<br />

This standalone server aims to give clients the most performant way to interact with EdgeDB over a network, especially for systems that make heavy use of
reverse proxying or monolithic DNS topologies. Likewise, it aims to give Systems and Database Administrators an intuitive way to manage their company's EdgeDB assets, like those offered by enterprise database systems. 

## Installation
*ToDo*

## Development for Contributiors

> Install docker for your operating system

```bash

# (To Do later...)

# Debian/Ubuntu
...

# MacOS
...

# Arch
...

# Gentoo
...

# CentOS
...

# Alpine
...

# OpenSUSE
...

# Windows
...

```

```bash
git clone --recurse-submodules https://github.com/dmgolembiowski/edbpool.git
```

```bash
cd edbpool/modules/edgedb-docker
```

```bash
# Depending on your operating system or Docker installation,
# you may need to elevate to root/admin to run these next commands.
# Additionally, `1-alpha2` can be replaced with any other valid version.

docker build -t edgedb:1-alpha2 --build-arg version=1-alpha2 .
```

## QA/Testing Roadmap
Note: Tests and scripts are to be fashioned for running on the Docker instance rather than the developer's local environment.

## Phase 1 Requirements Plan

### 1. Simulated OS-check

- [ ] assert fail on MacOSX
- [ ] assert fail on Windows
- [ ] assert pass on Ubuntu/Debian
- [ ] assert fail on anything else

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
                       18888 - Reverse Shell/RPC-like/Xdotool controls
                               or some other comparable passthrough mechanism
                       18080 - HTTP Server related scripting
```

### 5. Give the docker image a set of installation steps for:
- [ ] https://edgedb.com/docs/internals/dev/
- [ ] https://edgedb.com/docs/tutorial/install#ref-tutorial-install

### 6. Run tests from (x) as described:
- [ ] at https://edgedb.com/docs/internals/dev#running-tests over the reverse shell.

## Phase 2 Requirements Plan

### 1. Create and test a mock HTTP server with seven distinct URIs:
- [X] `"/"                                                   -> '{}'`
- [X] `"/execute/<statement:str>"                            -> '{}'`
- [X] `"/fetchone_json/<query:str>"                          -> '[{}]'`
- [X] `"/fetchall_json/<query:str>"                          -> '[{}]'`
- [X] `"/result?requestID=<id:int32>"                        -> (CRUD server storage access endpoint)`
- [ ] `"/error?requestID=<id:uint32>&error_code=<err:uint32>"-> (Lookup logged data saved under '/result', or serve as a redirection endpoint for some non-defined route)`

### 2. Extend capabilities in the mock HTTP server for:
- [ ] `async def set_result`
- [ ] `async def get_result`

