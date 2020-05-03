```
Phase 1 Requirements Plan
=========================

Prepare test cases for:
    1. Simulated OS-check
        - assert fail on MacOSX
        - assert fail on Windows
        - assert pass on Ubuntu/Debian
        - assert fail on anything else

    2. Reading values in from a config
        - EdgeDB DSN
        - HTTP test address
        - HTTP test port

    3. Pull down a docker image of Ubuntu
        with EdgeDB and add a network passthrough
            - localhost:5566, otherwise
            - localhost:15566

    4. Give the docker image a set of single
        port forwards:
            - 127.0.0.1:{ 5566 -> 5656,
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
            - https://edgedb.com/docs/internals/dev/
            - https://edgedb.com/docs/tutorial/install#ref-tutorial-install

    6. Run tests as described at https://edgedb.com/docs/internals/dev#running-tests
        over the reverse shell.

    7. Pull down edbpool mockscripts, which include:
        - Flask server with an index route ('/') and a mock route ('/edgedb')
```
