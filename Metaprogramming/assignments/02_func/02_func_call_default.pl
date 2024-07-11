func_call(Func/_/Index, X, Y) :- 
    nth1(Index, Arg, Y, X),
    Result =.. [Func|Arg], 
    call(Result).


func_call(Func/N, X, Y) :-
    length(X, L),
    Index is L + 1,
    func_call(Func/N/Index, X, Y). 
