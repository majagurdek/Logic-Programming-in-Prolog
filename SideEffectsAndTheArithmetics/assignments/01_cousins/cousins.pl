is_cousin(X,Y) :- retractall(cousin_list(_,_)),
    is_cousin_2(X,Y).

is_cousin_2(X,Y) :- is_ancestor(Z, X),
    is_ancestor(Z, Y),
    X \= Y, 
    \+ cousin_list(X,Y),
    \+ cousin_list(Y,X),
    assert(cousin_list(X,Y)).

:- dynamic cousin_list/2.
    
