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

def save_flashcards(filename="flashcards.json"):
    """
    Saves all flashcards.
    """
    try:
        with open(filename, "w") as file:
            json.dump(flashcards, file, indent=4)
        print("\nQuiz Cards saved successfully.")
    except IOError:
        print_error("\nUnable to save Quiz Cards.")

def display_welcome_message():
    """
    Displays a welcome message and provides an overview of the program's 
    features, guiding the user through Quiz Cards functionality.
    """
    print("*****************************************")
    print("        Welcome to Quiz Cards!")
    print("*****************************************")
    print()
    print("The ultimate flashcard quiz tool to boost your knowledge!")
    print()
    print("With Quiz Cards, you can:")
    print()
    print("1. Add your own Quiz Cards for personalized learning.")
    print("2. View all Quiz Cards to review and reinforce your knowledge.")
    print("3. Sort Quiz Cards into categories to help keep your study deck organized.")
    print("4. Delete Quiz Cards you no longer need to keep your study deck fresh.")
    print("5. Test yourself with our Quiz mode to see how much you’ve learned.")
    print()
    print("Let’s get started and make learning fun and interactive!")

# --- Flashcard Management Functions ---

def add_flashcard():
    """
    Prompts the user to input a term, definition, and optional category to 
    create a new flashcard. Validates that both term and definition are provided.
    Assigns 'Uncategorized' if no category is given. Auto-saves flashcards upon 
    successful addition.
    """
    print("\nAdd a New Quiz Card")
    print("You’ll be asked to enter a term/question followed by its definition/answer, and an optional category.")
    print("Example: Term = Python, Definition = A high-level programming language, Category = Programming")
    
    term = input("Enter the term/question: ").strip()
    definition = input("Enter the definition/answer: ").strip()
    category = input("Enter the category (or press Enter to skip): ").strip().title()
    
    if term and definition:  # Validation for term and definition only followed by confirmation prompt
        print(f"\nYou entered:\nTerm: {term}\nDefinition: {definition}\nCategory: {category or 'Uncategorized'}")
        if confirm_action("Do you want to add this Quiz Card? (yes/no): "):
            flashcards.append({
                "term": term,
                "definition": definition,
                "category": category if category else "Uncategorized"
            })
            print("Quiz Card added successfully!")
            save_flashcards()  # Auto-save enabled
        else:
            print("Quiz Card not added.")
    else:
        print_error("Both term and definition are required.")

