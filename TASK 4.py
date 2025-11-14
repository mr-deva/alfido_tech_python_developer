#!/usr/bin/env python3
"""
todo.py — Simple To-Do List CLI app
Features:
- Add, remove, view, complete, edit tasks
- Persist tasks to a JSON file
- Search and filter (all / pending / completed)
- Input validation, logging, and clean OOP structure
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

# --- Config ---
DATA_FILE = Path("todo_data.json")
LOG_FILE = "todo_app.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# --- Models ---
class Task:
    def __init__(self, title: str, description: str = "", due: Optional[str] = None,
                created_at: Optional[str] = None, completed: bool = False, id: Optional[int] = None):
        self.id = id or int(datetime.utcnow().timestamp() * 1000)  # simple unique id
        self.title = title.strip()
        self.description = description.strip()
        self.due = due  # optional due date string
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.completed = completed

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due": self.due,
            "created_at": self.created_at,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            title=d.get("title", ""),
            description=d.get("description", ""),
            due=d.get("due"),
            created_at=d.get("created_at"),
            completed=d.get("completed", False),
            id=d.get("id"),
        )


# --- Storage / Repository ---
class TodoRepository:
    def __init__(self, path: Path = DATA_FILE):
        self.path = path
        self._ensure_file()

    def _ensure_file(self):
        if not self.path.exists():
            self._write_data([])

    def _read_data(self) -> List[Dict]:
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_data(self, data: List[Dict]):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def list_tasks(self) -> List[Task]:
        return [Task.from_dict(d) for d in self._read_data()]

    def save_tasks(self, tasks: List[Task]):
        self._write_data([t.to_dict() for t in tasks])


# --- Service / Business Logic ---
class TodoService:
    def __init__(self, repo: TodoRepository):
        self.repo = repo
        self.tasks: List[Task] = self.repo.list_tasks()

    def _persist(self):
        self.repo.save_tasks(self.tasks)

    def add_task(self, title: str, description: str = "", due: Optional[str] = None) -> Task:
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        task = Task(title=title, description=description, due=due)
        self.tasks.append(task)
        self._persist()
        logging.info("Added task: %s (id=%s)", task.title, task.id)
        return task

    def remove_task(self, task_id: int) -> bool:
        original = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        removed = len(self.tasks) < original
        if removed:
            self._persist()
            logging.info("Removed task id=%s", task_id)
        return removed

    def edit_task(self, task_id: int, title: Optional[str] = None,
                description: Optional[str] = None, due: Optional[str] = None) -> bool:
        for t in self.tasks:
            if t.id == task_id:
                if title is not None and title.strip():
                    t.title = title.strip()
                if description is not None:
                    t.description = description.strip()
                if due is not None:
                    t.due = due
                self._persist()
                logging.info("Edited task id=%s", task_id)
                return True
        return False

    def complete_task(self, task_id: int) -> bool:
        for t in self.tasks:
            if t.id == task_id:
                t.completed = True
                self._persist()
                logging.info("Completed task id=%s", task_id)
                return True
        return False

    def list_tasks(self, filter_by: str = "all", query: Optional[str] = None) -> List[Task]:
        results = self.tasks
        if filter_by == "pending":
            results = [t for t in results if not t.completed]
        elif filter_by == "completed":
            results = [t for t in results if t.completed]

        if query:
            q = query.lower()
            results = [t for t in results if q in t.title.lower() or q in t.description.lower()]

        # sort by created_at ascending
        results.sort(key=lambda x: x.created_at)
        return results


# --- CLI Helpers ---
def prompt_choice(prompt: str, choices: List[str]) -> str:
    print(prompt)
    for i, c in enumerate(choices, start=1):
        print(f"{i}. {c}")
    while True:
        sel = input("Select an option: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(choices):
            return choices[int(sel) - 1]
        print("Invalid selection. Try again.")


def prompt_int(prompt: str) -> Optional[int]:
    val = input(prompt).strip()
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        print("Please enter a valid integer id.")
        return None


def pretty_print_tasks(tasks: List[Task]):
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        status = "✓" if t.completed else " "
        due = f" | due: {t.due}" if t.due else ""
        print(f"[{status}] id={t.id} | {t.title}{due}\n    {t.description}\n")


# --- Main Program ---
def main():
    repo = TodoRepository()
    service = TodoService(repo)

    print("=== Simple To-Do CLI (Alfido Tech Internship) ===\n")
    while True:
        action = prompt_choice("Choose action:", ["Add task", "Remove task", "Edit task",
        "Complete task", "View tasks", "Exit"])
        if action == "Add task":
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            description = input("Description (optional): ").strip()
            due = input("Due (optional, e.g. 2025-12-31): ").strip() or None
            task = service.add_task(title, description, due)
            print(f"Added: id={task.id} | {task.title}")

        elif action == "Remove task":
            id_val = prompt_int("Enter task id to remove: ")
            if id_val is None:
                continue
            removed = service.remove_task(id_val)
            print("Removed." if removed else "Task not found.")

        elif action == "Edit task":
            id_val = prompt_int("Enter task id to edit: ")
            if id_val is None:
                continue
            new_title = input("New title (leave blank to keep): ")
            new_desc = input("New description (leave blank to keep): ")
            new_due = input("New due (leave blank to keep): ")
            success = service.edit_task(id_val,
                                        title=new_title if new_title.strip() else None,
                                        description=new_desc if new_desc.strip() else None,
                                        due=new_due if new_due.strip() else None)
            print("Updated." if success else "Task not found.")

        elif action == "Complete task":
            id_val = prompt_int("Enter task id to mark completed: ")
            if id_val is None:
                continue
            ok = service.complete_task(id_val)
            print("Marked completed." if ok else "Task not found.")

        elif action == "View tasks":
            filt = prompt_choice("Filter by:", ["all", "pending", "completed"])
            q = input("Search query (optional): ").strip() or None
            tasks = service.list_tasks(filter_by=filt, query=q)
            pretty_print_tasks(tasks)

        elif action == "Exit":
            print("Goodbye 👋")
            break

        print()  # newline for readability


if __name__ == "__main__":
    main()
