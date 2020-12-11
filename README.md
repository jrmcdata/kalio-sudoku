# kalio-sudoku: a sudoku solving library

## Introduction

NONE

## Important methods

```
__init__(myArray)
```

Initalizes a sudoku element depending on type(myArray)
* sudoku: clones sudoku object
* int list: creates a 9x9 sudoku grid from a 81x1 list with integers 0-9
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

### Random methods

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
* -1 board is guaranteed to be unsolvable
*  1 board is olved
*  0 board is unsolved (but not necessarily unsolvable)
