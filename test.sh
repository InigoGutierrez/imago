#!/bin/sh
coverage run --source=imago -m unittest discover tests/  && coverage report -m --skip-empty
