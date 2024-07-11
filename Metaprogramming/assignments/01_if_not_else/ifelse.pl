ifelse(Condition, TrueQuery, _) :-
    Condition,
    !,
    call(TrueQuery).

ifelse(_, _, FalseQuery) :-
    call(FalseQuery).
