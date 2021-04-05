Blackjack Grid SAT Checker

Given N card-tets, can the game be won?

Testing

`python -m unittest test.test_main`

Sources:
1. https://davefernig.com/2018/05/07/solving-sat-in-python/

```
# literal
("p", True)

# disjunctive clause (x1 v x2 v ~x3) [1]
{("x1", True), ("x2", True), ("x3", False)}

# conjunctive clause (x1 v x2 v ~x3) ^ (~x1 v ~x2 v ~x3) [1]
[{("x1", True), ("x2", True)}, {("x1", False), ("x2", False)}]
```