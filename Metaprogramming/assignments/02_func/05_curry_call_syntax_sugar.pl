% TODO:
% 1. define the <# and # operators again
% 2. finish the following predicates
% 3. *DO NOT* copy the curry_call implementation
%    When testing, just load it from the 04_curry_call, e.g., ['04_curr_call.pl'] within the swipl command line

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