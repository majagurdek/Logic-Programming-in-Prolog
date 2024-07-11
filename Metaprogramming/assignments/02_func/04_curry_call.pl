curry_call(function(Func/Arity/Arity, Args), InputArg, Result) :-
    append(Args, [InputArg], NewArgs),
    func_call(Func/Arity/Arity, NewArgs, Result).

curry_call(function(Func/Arity/Index, Args), InputArg, function(Func/Arity/Index, NewArgs)) :-
    append(Args, [InputArg], NewArgs).

curry_call(function(Func/Arity, Args), InputArg, Result) :-
    functor(FuncTerm, Func, Arity),
    append(Args, [InputArg], NewArgs),
    curry_call(function(Func/Arity/Arity, NewArgs), _, Result).

curry_call(function(Func, Args), InputArg, Result) :-
    functor(FuncTerm, Func, Arity),
    append(Args, [InputArg], NewArgs),
    length(NewArgs, NewLength),
    curry_call(function(Func/Arity/NewLength, NewArgs), _, Result).
