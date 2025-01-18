# Collatz Conjecture (for dad)

This repository was originally developed for my father, providing him with a simple tool to play with, investigate, and visualize number series following the Collatz conjecture. The tool is now available for anyone interested.

## The conjecture

Starting with integer number (**n**), one of two rules is applied based on the parity of the number:

- If the number is even, divide it by 2:  **n/2**
- If the number is odd, multiply it by 3 and add 1: **3n+1**

The conjecture states that every positive integer will eventually reach the following loop:

**4 --> 2 --> 1 ---> 4**

Here is an example with n=7:

7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1

## Usage (TODO: improve section: conda environment, instructions, examples...)

After cloning the repo just run:

```bash
streamlit run script.py
```
