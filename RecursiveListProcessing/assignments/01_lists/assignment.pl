remove_element(_, [], []).
remove_element(E1, [E1|Rest], Rest).
     
remove_element(El, [H|T], [H|Result]) :-
    El \= H,
    remove_element(El, T, Result).

remove_all_occurrences(_, [], []).
remove_all_occurrences(E1, [E1|Rest], Result) :-
    remove_all_occurrences(E1, Rest, Result).
     
remove_all_occurrences(El, [H|T], [H|Result]) :-
    El \= H,
    remove_all_occurrences(El, T, Result).

add_element(El, List, [El|List]).
add_element(El, [H|T], [H|Result]) :-
    add_element(El, T, Result).

list_reverse([], Acc, Acc).
list_reverse([H|T], Acc, Result) :-
    NewAcc = [H|Acc],
    list_reverse(T, NewAcc, Result).
list_reverse(List, Result) :-
    list_reverse(List, [], Result).

palindrome(List) :-
    list_reverse(List, List).

sublist([], []).
sublist([H|L1], [H|L2]) :- sublist(L1, L2).
sublist([_|L1], L2) :- sublist(L1, L2).

cut_off_left(0, List, List).
cut_off_left(N, List, Result):-
    length(F, N),
    append(F, Result, List).

cut_off_right(0, List, List).
cut_off_right(N, List, Result):-
    length(L, N),
    append(Result, L, List).

contains_list(L1, L2) :-
    append(L2, _, L1).

contains_list([_|Tail], L2) :-
    contains_list(Tail, L2).

permutation([], []).
permutation(List, [H|P]) :-
    remove(H, List, Rest),
    permutation(Rest, P).

remove(X, [X|T], T).
remove(X, [H|T], [H|Rest]) :-
    remove(X, T, Rest).

split([], [], []).
split([X], [X], []).
split([X, Y|Rest], [X|L], [Y|P]) :-
    split(Rest, L, P).

flat_list(NL, L) :- fail.
