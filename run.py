import json
import os
import random
from datetime import datetime

flashcards = []
progress_file = "progress.json" # JSON file for storing user progress

# --- Core Setup Functions ---

def initialize_progress_file():
    """
    Initializes the progress tracking file. Creates an empty list-based JSON 
    file if it does not exist, or if existing data is not in list format.
    Ensures valid progress tracking data structure.
    """
    if not os.path.exists(progress_file):
        with open(progress_file, "w") as file:
            json.dump([], file)
    else:
        try:
            with open(progress_file, "r") as file:
                data = json.load(file)
            if not isinstance(data, list):  # Reset if data is not a list
                raise ValueError("Progress data is not a list.")
        except (json.JSONDecodeError, ValueError):
            with open(progress_file, "w") as file:
                json.dump([], file)
            print("Progress file initialized as an empty list due to invalid data.")

def load_flashcards(filename="flashcards.json"):
    """
    Loads flashcards from the specified JSON file. If the file is missing, 
    starts with an empty flashcard list. If data is corrupted, initializes
    with an empty list and displays an error message.
    """
    global flashcards
    try:
        with open(filename, "r") as file:
            flashcards = json.load(file)
        print("Quiz Cards loaded successfully.")
    except FileNotFoundError:
        print("No saved Quiz Cards found. Starting with an empty list.")
    except json.JSONDecodeError:
        print_error("Corrupted file. Starting with an empty list.")
        flashcards = []

