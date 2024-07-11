neg(X) :-
    call(X),  
    !,           
    fail.       

neg(_). 
