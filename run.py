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

# --- Helper & Validation Functions ---

def confirm_action(message="Are you sure you want to proceed? (yes/no): "):
    """
    Displays a prompt for the user to confirm an action with 'yes' or 'no'.
    Repeats until valid input is received. Returns True for 'yes' and False 
    for 'no' responses, used for potentially irreversible actions.
    """
    while True:
        choice = input(message).strip().lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print_error("Please enter 'yes' or 'no'.")

def print_error(message):
    print(f"\n**ERROR**: {message}")

def get_valid_index(prompt, max_index):
    """
    Validates and returns a zero-based index input within the specified range.
    Ensures user input falls between 1 and max_index + 1 (inclusive).
    """
    while True:
        try:
            index = int(input(prompt)) - 1  # Adjusting to zero-based index
            if 0 <= index <= max_index:
                return index
            else:
                print_error(f"Please enter a number between 1 and {max_index + 1}.")
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")

def get_valid_integer(prompt, min_value, max_value):
    """
    Prompts the user to enter an integer within a specified range, re-prompting 
    for invalid input. Ensures the integer falls between min_value and max_value.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print_error(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")

# --- Quiz Functions ---

def start_quiz():
    """
    Initiates a quiz session with a selected category or all categories. Prompts
    the user to select a category and the number of questions. After the quiz, 
    offers options to retry the same quiz, start a new quiz, or return to the 
    main menu.
    """
    if not flashcards:
        print("No Quiz Cards available for quiz. Please add Quiz Cards first.")
        print("Returning to Main Menu...")
        return

    while True:  # Main quiz loop for selecting categories and starting quizzes
        print("\nQuiz Mode")

        # Display available categories
        unique_categories = sorted(set(fc["category"] or "Uncategorized" for fc in flashcards))
        print("Available Categories:")
        for idx, category in enumerate(unique_categories, start=1):
            print(f"{idx}. {category}")
        print(f"{len(unique_categories) + 1}. All Categories")
        
        # Prompt user for category selection
        try:
            selection = get_valid_integer("Select a category by number (or choose 'All Categories'): ", 1, len(unique_categories) + 1)
            if 1 <= selection <= len(unique_categories):
                category = unique_categories[selection - 1]
                
                # Filter flashcards by the selected category
                category_flashcards = [fc for fc in flashcards if (fc["category"] or "Uncategorized") == category]
                
                # Check if there are any flashcards in the selected category
                if not category_flashcards:
                    print(f"No Quiz Cards found for category '{category}'. Please add flashcards to this category.")
                    return
                
                print(f"Starting quiz on category '{category}'...")
            elif selection == len(unique_categories) + 1:
                category_flashcards = flashcards  # All categories selected
                print("Starting quiz on all categories...")
            else:
                print_error("Invalid selection. Please enter a number corresponding to the category list.")
                continue
        except ValueError:
            print_error("Please enter a valid number.")
            continue
        
        # Prompt for the number of questions if flashcards are available in the chosen category
        max_questions = len(category_flashcards)
        num_questions = get_valid_integer(f"How many questions would you like? (1-{max_questions}): ", 1, max_questions)
        
        # Run the quiz
        run_quiz(category_flashcards, num_questions, category_name=unique_categories[selection - 1] if selection <= len(unique_categories) else "All Categories")

        # Post-quiz options
        while True:
            print("\nQuiz Complete! What would you like to do next?")
            print("1. Try the same quiz again")
            print("2. Start a new quiz")
            print("3. Return to Main Menu")
            
            next_action = get_valid_integer("Choose an option (1-3): ", 1, 3)

            if next_action == 1:
                # Retry the same quiz with the same category and question count
                run_quiz(category_flashcards, num_questions, category_name=unique_categories[selection - 1] if selection <= len(unique_categories) else "All Categories")
            elif next_action == 2:
                # Restart the main quiz loop to select a new category
                break
            elif next_action == 3:
                # Exit to the main menu
                print("Returning to Main Menu...")
                return

def run_quiz(category_flashcards, num_questions, category_name="All Categories"):
    """
    Runs the quiz for the selected category with a specified number of questions. 
    Randomly selects flashcards to quiz the user, either term or definition, and 
    tracks correct answers. If at least one question was attempted, saves progress.
    """
    correct_count = 0
    total_questions = 0

    while total_questions < num_questions:
        flashcard = random.choice(category_flashcards)
        if random.choice([True, False]):
            user_answer = input(f"What is the definition of '{flashcard['term']}'? (or type 'exit' to quit): ").strip()
            correct_answer = flashcard['definition']
        else:
            user_answer = input(f"What term matches the definition '{flashcard['definition']}'? (or type 'exit' to quit): ").strip()
            correct_answer = flashcard['term']

        if user_answer.lower() == "exit":
            break
        elif user_answer.lower() == correct_answer.lower():
            print("Correct!")
            correct_count += 1
        else:
            print(f"Incorrect. The correct answer is: {correct_answer}")
        total_questions += 1

    # Only save progress if at least one question was attempted
    if total_questions > 0:
        print(f"Quiz complete! You scored {correct_count} out of {total_questions}.")
        save_progress(category_name, correct_count, total_questions)
    else:
        print("No questions were attempted; progress will not be saved.")

def save_progress(category, correct_count, total_questions):
    """
    Saves quiz results to the progress file with category, score, total questions, 
    and success rate. If the file is missing or corrupted, initializes it as an 
    empty list. Appends the new entry and saves it in JSON format.
    """
    # Calculate success rate
    success_rate = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    # Create progress entry
    progress_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "score": correct_count,
        "total_questions": total_questions,
        "success_rate": round(success_rate, 2)
    }
    try:
        # Load existing progress data or create new list
        with open(progress_file, "r") as file:
            progress_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        progress_data = []
    
    # Append new entry and save back to file
    progress_data.append(progress_entry)
    with open(progress_file, "w") as file:
        json.dump(progress_data, file, indent=4)

    print("Progress saved successfully!")

