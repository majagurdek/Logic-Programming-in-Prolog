# TODO:
# Implement fibonacci function in our programming language.
# You may base it on the 10_letrec_iseven.tl
# As input use {{input}} template, e.g.
#
#   letrec iseven : Nat->Bool = \x:Nat.
#               (if iszero x then true
#               else if iszero (pred x) then false
#               else iseven (pred (pred x)))
#   in iseven {{input}}
#
# tip 1. you may have first define recursive `plus` function
#        plus x 0 = x
#        plus x (succ y) = plus (succ x) y 
# tip 2. parser is a bit stupid... to use 2-arg function, one has to use parenthesis, e.g.
#        write '(plus 0) 0' instead of the easier 'plus 0 0'