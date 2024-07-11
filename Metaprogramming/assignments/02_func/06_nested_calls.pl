% TODO:
% 1. define the <# and # operators again
% 2. also define a prefix operator #
% 3. reimplement the curry predicate handling the nesting
%    again, assume, the curry_call is already implemented

Result <# Function # ArgsChain :-
    initial_function(Function, IF),
    curry(IF, ArgsChain, Result).

initial_function(function(F,A), function(F,A)) :-
    !.
initial_function(F, function(F, [])).
                    
curry(F, A # T, Result) :-
    !,
    % there is still an arugment to process
    fail.
curry(F, A, Result) :-
    % we have reached the end of arguments
    fail.