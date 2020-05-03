```
Phase 2 Requirements Plan
=========================

1. Create and test a mock EdgeDB HTTP pool server with seven distinct URIs:
    - "/"                                                   -> '{}'
    - "/execute/<statement:str>"                            -> '{}'
    - "/fetchone_json/<query:str>"                          -> '[{}]'
    - "/fetchall_json/<query:str>"                          -> '[{}]'
    - "/result?requestID=<id:int32>"                        -> (Relevant information)
    - "/error?requestID=<id:uint32>&error_code=<err:uint32>"-> (Lookup saved '/result' to return, also redirected to on non-defined route)
```
