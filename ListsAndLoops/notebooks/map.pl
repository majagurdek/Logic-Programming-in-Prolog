% Translates a single element of the list.
% Changing this rule would change the resulting list.
map_element(X, Y) :- Y is X * 2.

% The base case: 
% Mapping an empty list always result in an empty list.
map([], []).

% Recursive case:
% 1. translates the list's head and copies result to the output list.
% 2. map the tail and copy it to the output list
map([Head|Tail], [TranslatedHead|TranslatedTail]) :-
  map_element(Head, TranslatedHead),
  map(Tail, TranslatedTail).

/** <examples>

?- map([1, -1, 3, -4, 5], Result).

*/