#!/usr/bin/env bash

set -u # crash on missing env
set -e # stop on any error

echo() {
   builtin echo -e "$@"
}


echo "Lint checks (Ruff)"
ruff check --output-format=concise

echo "\nCheck formatting (Ruff)"
ruff format --diff

echo "\nCheck import sort (isort)"
isort --check --diff .

echo "\nCheck formatting (Black)"
black --check --diff .

echo "\nCheck typing (mypy)"
mypy .

echo "\nChecks complete"
