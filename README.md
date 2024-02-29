# JavaScript Interpreter

A simple JavaScript parser + interpreter made for CS 330 - Concepts of Programming Languages.

## Requirements

Node.js + acorn package - run `npm install` (tested with Node v18)
Python (tested with Python 3.11)

## How to Parse

`echo "1 + 1" | npm run parse --silent | python main.py parse`

## How to Interpret

`echo "1 + 1" | npm run parse --silent | python main.py interpet`

(the "interpret" argument is optional)


Note: This project previously used mypy for static type checking, but I have surpassed the limits of what mypy is capable of and thus removed it.