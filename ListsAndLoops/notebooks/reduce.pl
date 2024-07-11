% Reduces a single element.
% OldValue is the old value of the accumulator.
% New value is result of reducing the Element. 
reduce_element(OldValue, Element, NewValue) :- 
	NewValue is OldValue * Element.

% Base Case
% Reducing an empty list does not change the accumulater value
reduce([], CurrentAccumulator, CurrentAccumulator). 

% Recursive Case
% 1. reduces head (`H`) using the current accumulator value
%    result in a new value
% 2. reduces rest of the list using the new value as the new accumulator
% 3. result od of the reduction is the copied to the result.
reduce([H|T], CurrentAccumulator, Result) :- 
	reduce_element(H, CurrentAccumulator, NextAccumulator),
	reduce(T, NextAccumulator, Result).

/** <examples>

?- reduce([1, -1, 3, -4, 5], 1, Result).

*/