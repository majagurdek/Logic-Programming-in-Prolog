func_call(Func/_/Index, X, Y) :- 
    nth1(Index, Arg, Y, X),
    Result =.. [Func|Arg], 
    call(Result).

