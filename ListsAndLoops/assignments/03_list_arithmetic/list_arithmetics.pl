list_number([], 0).
list_number([_|T], L) :- list_number(T, L_r), L is L_r+1.

list_add([], L, L).
list_add([H|Tail], Second, [H|Rest]) :- list_add(Tail, Second, Rest).


reduce(_, X, Y) :- Y is X+1.
list_number_mfr(L, Length) :- foldl(reduce, L, 0, Length).


list_add_mfr(L1, L2, L3) :- fail.

