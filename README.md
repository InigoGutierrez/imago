# Imago

A Go AI.

## The project

Imago is a Go AI developed as a TFG (Final Degree Project) for the Bachelor of
Software Engineering of the University of Oviedo.

## Implementation

Imago is written in Python and the source code is inside the `imago` folder. The
implementation is on an early stage and includes core game logic, a basic GTP
engine and a placeholder AI function which plays on random empty vertices.

A game of go with no AI can be played by running the `go.py` script. This is
useful to test the core game logic. The GTP engine can be started by the
`imagocli.py` script. Following the GTP specification, known commands can be
listed by entering `list_commands` on the GTP engine's interface.

Tests are stored in the `tests` folder which as of now contains an example
tests file. The tests can be run with the `test.sh` script which uses the
Python package `coverage` to get coverage statistics.

## Documentation

The source code for a work in progress documentation is laid out inside the
`doc` folder, including a Makefile to compile it. This documentation compiling
process depends on `xelatex`, `biber`, `plantuml` and some `LaTeX` packages.
This documentation is fully subject to change in any moment of development and
it probably already contradicts the actual implementation.
