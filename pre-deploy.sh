#!/bin/bash
echo ""
echo "-- Running Black formatter --"
python -m black .
echo ""
echo "-- Running MyPy --"
python -m mypy .
echo "-- done --"
echo ""
echo "-- Running Pylint --"
python -m pylint . --rcfile=.pylintrc
echo "-- done --"
echo ""
