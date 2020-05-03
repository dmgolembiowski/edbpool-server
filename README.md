# EDB Pool Server
> A simple interface for setting up your connection(s) to EdgeDB using the desirable asynchronous pools in the edgedb python client api. All you have to do is send your edgeql statements and it handles the rest. 
### Overview
This project started as something I wish existed a couple months after EdgeDB 1.0 alpha was released. At the time,
the connection pool APIs did not make opinionated decisions about how connection pools were to be managed after the initial
creation and usage, since the examples led me to believe that the pool would close as soon as the last query was ran.
<br />
This standalone server aims to give its users the most performant way to query EdgeDB, especially for systems that make heavy use of
reverse proxying. Likewise, it aims to give users a similar interface for those familiar with Oracle SQL administration which
defines properties in a file like the `tnsnames.ora` one would typically see on Redhat servers.

## Roadmap

> Phase 1 Requirements Plan

Prepare test cases for:
    1. Simulated OS-check
        - [ ] assert fail on MacOSX
        - [ ] assert fail on Windows
        - [ ] assert pass on Ubuntu/Debian
        - [ ] assert fail on anything else

    2. Reading values in from a config
        - [ ] EdgeDB DSN
        - [ ] HTTP test address
        - [ ] HTTP test port

    3. Pull down a docker image of Ubuntu
        with EdgeDB and add a network passthrough
            - [ ] localhost:5566, otherwise
            - [ ] localhost:15566

    4. Give the docker image a set of single
        port forwards:
            - [ ] 127.0.0.1:{ 5566 -> 5656,
                         15566 -> 5656,
                          6655 -> 6565,
                         16655 -> 6565,
                         18888 -> 18888,
                         18080 -> 18080 },

        where ports are allocated for

                {5566, 15566 (fallback)} - main EdgeDB CLI
                {6655, 16655 (fallback)} - async EDB pool master
                                   18888 - Reverse Shell/RPC-like/Xdotool controls
                                           or some other comparable passthrough mechanism
                                   18080 - HTTP Server related scripting

    5. Give the docker image a set of installation
        steps at:
            - [ ] https://edgedb.com/docs/internals/dev/
            - [ ] https://edgedb.com/docs/tutorial/install#ref-tutorial-install

    6. Run tests as described at https://edgedb.com/docs/internals/dev#running-tests
        over the reverse shell.

    7. Pull down edbpool mockscripts, which include:
        - [ ] Flask server with an index route ('/') and a mock route ('/edgedb')

> Phase 2 Requirements Plan

1. Create and test a mock EdgeDB HTTP pool server with seven distinct URIs:
    - [ ] "/"                                                   -> '{}'
    - [ ] "/execute/<statement:str>"                            -> '{}'
    - [ ] "/fetchone_json/<query:str>"                          -> '[{}]'
    - [ ] "/fetchall_json/<query:str>"                          -> '[{}]'
    - [ ] "/result?requestID=<id:int32>"                        -> (Relevant information)
    - [ ] "/error?requestID=<id:uint32>&error_code=<err:uint32>"-> (Lookup saved '/result' to return, also redirected to on non-defined route)
2. To be continued ...

