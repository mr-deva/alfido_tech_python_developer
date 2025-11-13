#!/usr/bin/env python3
"""
calc_with_history.py

Simple CLI calculator demonstrating:
- Python 3 features
- File handling (JSON)
- Control structures (if/else, loops)
- Data types (float, dict, list, str)
- Functions and modular code
"""

import json
import math
from pathlib import Path
from datetime import datetime

HISTORY_PATH = Path("calc_history.json")


# ----- Arithmetic functions -----
def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b

def power(a: float, b: float) -> float:
    return math.pow(a, b)

def modulus(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Modulus by zero is not allowed.")
    return a % b


# ----- History (file handling) -----
def load_history() -> list:
    """Load calculation history from HISTORY_PATH. Return list of dicts."""
    if not HISTORY_PATH.exists():
        return []
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, return empty history
        return []
    return []


def save_history(history: list) -> None:
    """Save history list to HISTORY_PATH as JSON."""
    try:
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"Warning: Could not save history: {e}")


def log_calculation(history: list, expr: str, result) -> None:
    """Append a new entry to history (in-memory) and persist to disk."""
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "expression": expr,
        "result": result
    }
    history.append(entry)
    save_history(history)


# ----- Input helpers -----
def get_number(prompt: str) -> float:
    """Prompt user repeatedly until a valid float is entered."""
    while True:
        s = input(prompt).strip()
        try:
            return float(s)
        except ValueError:
            print("Invalid number. Please enter a numeric value.")


def choose_operation() -> str:
    print("\nChoose operation:")
    print("  +   Addition")
    print("  -   Subtraction")
    print("  *   Multiplication")
    print("  /   Division")
    print("  ^   Power (a^b)")
    print("  %   Modulus (a % b)")
    print("  h   Show history")
    print("  c   Clear history")
    print("  q   Quit")
    return input("Operation: ").strip().lower()


def format_expression(a: float, op: str, b: float) -> str:
    return f"{a} {op} {b}"


# ----- Main program -----
def main():
    print("=== Python CLI Calculator (with history) ===")
    history = load_history()

    while True:
        op = choose_operation()

        if op == "q":
            print("Goodbye!")
            break

        if op == "h":
            if not history:
                print("No history yet.")
            else:
                print("\n--- Calculation History (most recent last) ---")
                for i, entry in enumerate(history, start=1):
                    ts = entry.get("timestamp", "")
                    expr = entry.get("expression", "")
                    res = entry.get("result", "")
                    print(f"{i}. [{ts}] {expr} = {res}")
            continue

        if op == "c":
            confirm = input("Are you sure you want to clear history? (y/n): ").strip().lower()
            if confirm == "y":
                history.clear()
                save_history(history)
                print("History cleared.")
            else:
                print("Clear history canceled.")
            continue

        if op in {"+", "-", "*", "/", "^", "%"}:
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            expr = format_expression(a, op, b)

            try:
                if op == "+":
                    res = add(a, b)
                elif op == "-":
                    res = subtract(a, b)
                elif op == "*":
                    res = multiply(a, b)
                elif op == "/":
                    res = divide(a, b)
                elif op == "^":
                    res = power(a, b)
                elif op == "%":
                    res = modulus(a, b)
                else:
                    print("Unsupported operation.")
                    continue

                # Display nicely (strip trailing .0 for integer-results)
                display_res = int(res) if isinstance(res, float) and res.is_integer() else res
                print(f"Result: {expr} = {display_res}")

                # Log to history
                log_calculation(history, expr, display_res)

            except ZeroDivisionError as zde:
                print(f"Error: {zde}")
            except Exception as exc:
                print(f"An error occurred: {exc}")

        else:
            print("Invalid choice. Please select a valid operation or 'h', 'c', 'q'.")


if __name__ == "__main__":
    main()
