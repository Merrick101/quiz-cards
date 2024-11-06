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

def edit_flashcard():
    """
    Edits an existing flashcard. Displays all flashcards with index numbers,
    prompts for a flashcard to edit using a validated index, and asks for 
    confirmation before making changes. Allows the user to update term, 
    definition, or category. Changes are saved upon confirmation.
    """
    if not flashcards:
        print("No Quiz Cards available to edit.")
        print("Returning to Main Menu...")
        return
    
    view_flashcards()  # Display current flashcards with indexes
    
    # Get a valid flashcard index from the user
    index = get_valid_index("Enter the number of the Quiz Card you want to edit: ", len(flashcards) - 1)
    flashcard = flashcards[index]
    
    print(f"\nSelected Quiz Card: Term = '{flashcard['term']}', Definition = '{flashcard['definition']}', Category = '{flashcard['category'] or 'Uncategorized'}'")
    
    # Ask for confirmation before allowing edits
    if not confirm_action("Do you want to edit this Quiz Card? (yes/no): "):
        print("Edit canceled.")
        return
    
    new_term = input("Enter the new term (or press Enter to keep the current term): ").strip() or flashcard['term']
    new_definition = input("Enter the new definition (or press Enter to keep the current definition): ").strip() or flashcard['definition']
    new_category = input("Enter the new category (or press Enter to keep the current category): ").strip().title() or flashcard['category']

    # Display changes and ask for final confirmation
    print(f"\nUpdated Quiz Card:\nTerm: {new_term}\nDefinition: {new_definition}\nCategory: {new_category or 'Uncategorized'}")
    if confirm_action("Do you want to save these changes? (yes/no): "):
        flashcard.update({
            "term": new_term,
            "definition": new_definition,
            "category": new_category if new_category else "Uncategorized"
        })
        print("Quiz Card updated successfully!")
        save_flashcards()  # Auto-save enabled
    else:
        print("Changes not saved.")

def delete_flashcard():
    """
    Allows users to delete flashcards.
    """
    if not flashcards:
        print("No Quiz Cards to delete.")
        print("Returning to Main Menu...")
        return
    
    view_flashcards()  # Display current flashcards with indexes
    
    # Get a valid flashcard index from the user
    index = get_valid_index("Enter the number of the Quiz Card to delete: ", len(flashcards) - 1)
    flashcard = flashcards[index]
    
    print(f"\nSelected Quiz Card:\nTerm: {flashcard['term']}\nDefinition: {flashcard['definition']}\nCategory: {flashcard['category'] or 'Uncategorized'}")
    
    # Ask for confirmation before deletion
    if confirm_action("Are you sure you want to delete this flashcard? (yes/no): "):
        del flashcards[index]
        print("Quiz Card deleted successfully.")
        save_flashcards()  # Auto-save enabled
    else:
        print("Quiz Card not deleted.")

def list_categories():
    """
    Allows users to view all categories.
    """
    categories = set(fc["category"] for fc in flashcards if fc["category"])
    print("Available categories:", ", ".join(categories))

def choose_category():
    """
    Displays available categories and prompts the user to select one.
    """
    list_categories()
    return input("Enter a category (or press Enter to skip): ").strip().title()

