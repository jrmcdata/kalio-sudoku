# kalio-sudoku: a sudoku solving library

## Introduction

kalio-sudoku is a sudoku-solving python library. Sudoku() objects can be solved using deterministic or stochastic methods.

## Important variables

```
self.val
```

A 81-integer list of digits 0-9. Values 1-9 indicate an occupied site, 0 an unoccupied one.

```
self.nei
```

A 81-set list of integers. Integers in the sets correspond to the allowed integers for a given site, occupied sites have corresponding 1-element sets.

## Important methods

```
__init__(myArray)
```

Initializes a sudoku element depending on type(myArray)
* sudoku: clones sudoku object
* integer-list: creates a 9x9 sudoku grid from a 81-integer list of digits 0-9.
* none: creates a sudoku object with only zeroes

### Deterministic methods

```
solveSimple()
```

Attempts to solve board by assigning elements that only have one allowed possibility per region (domain, column, row).

```
solveUnique( self ):
```

Attempts to solve board by eliminating all elements that are allowed in just one site per region (domain, column, row).

```
solveTwins( self ):
```

Attempts to solve board by eliminating all pairs of allowed values that only appear twice per region (domain, column, row).

### Stochastic methods

```
solveRandom( self ):
```

Solves board by randomly picking high impact elements, and assigning a possible value.

## General methods

```
solve( self ):
```

Solves board by applying all deterministic methods. If they fail to solve board, applies stochastic method.

```
status( self ):
```

Checks the status of the board:
* -1: board is guaranteed to be unsolvable
*  1: board is solved
*  0: board is unsolved (but not necessarily unsolvable)
