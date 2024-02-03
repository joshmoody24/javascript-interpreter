# JavaScript Interpreter

A simple JavaScript parser + interpreter made for CS 330 - Concepts of Programming Languages.

## Requirements

Node.js + acorn package - run `npm install` (tested with Node v18)
Python + mypy package - run `pip install -r requirements.txt` (tested with Python 3.11)

## How to Parse

`echo "1 + 1" | npm run parse --silent | python main.py parse`

## How to Interpret

`echo "1 + 1" | npm run parse --silent | python main.py interpet`

(the "interpret" argument is optional)

## Static Type Checking

This wasn't required, but I did it anyway to learn more about static type checking in Python.

`mypy .`