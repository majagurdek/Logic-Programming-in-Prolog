% Here we define a condition that should 
% be satsfied by the elements.
% Modifying this rule would change the result.
satisfies_conditions(X) :- X > 0.

% The base case, filtering an empty list
% always results in an empty list
filter([],[]).

% The positive case — the current head of the list 
% satisfies the defined condition.
% Such an element is copied from the left list to right one.
% Then we have still to filter the tail.
filter([GoodHead|Tail], [GoodHead|FilteredTail]) :-
  satisfies_conditions(GoodHead),
  filter(Tail, FilteredTail).

% The negative case - the current head does not satisfy
% the defined condition.
% Such an element is ignored.
% Still, we have to filter the tail.
filter([BadHead|Tail], FilteredTail) :-
  \+ satisfies_conditions(BadHead),
  filter(Tail, FilteredTail).


/** <examples>

?- filter([1, -1, 3, -4, 5], Result).

*/