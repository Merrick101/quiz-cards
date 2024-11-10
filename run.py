import json
import os
import random
from datetime import datetime

flashcards = []
progress_file = "progress.json"  # JSON file for storing user progress

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
            print(
                "Progress file initialized as an empty list due to "
                "invalid data."
            )


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
        print("\nQuiz Cards loaded successfully.")
    except FileNotFoundError:
        print("\nNo saved Quiz Cards found. Starting with an empty list.")
    except json.JSONDecodeError:
        print_error("\nCorrupted file. Starting with an empty list.")
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
    print(
        "Boost your knowledge with Quiz Cards - "
        "your personal flashcard quiz tool!"
    )
    print()
    print("What you can do with Quiz Cards:")
    print("\n1. Add your own Quiz Cards for a custom learning experience.")
    print(
        "2. View and manage all Quiz Cards" "to reinforce what you've learned."
    )
    print("3. Sort Quiz Cards into categories to keep everything organized.")
    print("4. Delete Quiz Cards you no longer need to stay focused.")
    print(
        "5. Test yourself with the Quiz Mode and "
        "track your progress over time."
    )
    print()
    print(
        "Let’s get started and make your "
        "learning journey interactive and fun!"
    )


# --- Flashcard Management Functions ---


def add_flashcard():
    """
    Prompts the user to input a term, definition, and optional category to
    create a new flashcard.
    Validates that both term and definition are provided.
    Assigns 'Uncategorized' if no category is given. Auto-saves flashcards upon
    successful addition.
    """
    print_section_title("Add a New Quiz Card")
    print(
        "You’ll be asked to enter a term/question followed by its "
        "definition/answer, and an optional category."
    )
    print(
        "\nExample:\n \nTerm = Python"
        "\nDefinition = A high-level programming language"
        "\nCategory = Programming"
    )

    term = input(
        "\nEnter the term/question:\n"
    ).strip()

    definition = input(
        "Enter the definition/answer:\n"
    ).strip()

    category = input(
        "Enter the category (or press Enter to skip):\n"
    ).strip().title()

    if term and definition:  # Validation for term and definition
        print(
            f"\nYou entered:\nTerm: {term}\nDefinition: {definition}\n"
            f"Category: {category or 'Uncategorized'}"
        )
        if confirm_action("\nDo you want to add this Quiz Card? (yes/no): "):
            flashcards.append(
                {
                    "term": term,
                    "definition": definition,
                    "category": category if category else "Uncategorized",
                }
            )
            print("\nQuiz Card added successfully!")
            save_flashcards()  # Auto-save enabled
        else:
            print("\nQuiz Card not added.")
    else:
        print_error("\nBoth term and definition are required.")
        print("\nReturning to Previous Menu...")


def view_flashcards():
    """
    View flashcards by category or view all flashcards.
    Provides an option to view other flashcards or return to the main menu.
    """
    print_section_title("View Quiz Cards")
    if not flashcards:
        print("No Quiz Cards available.")
        print("\nReturning to Previous Menu...")
        return  # Exit if there are no flashcards to view

    while True:
        # Display user options
        unique_categories = sorted(
            set(
                fc["category"] if fc["category"] else "Uncategorized"
                for fc in flashcards
            )
        )
        print("Available Categories:\n")
        for idx, category in enumerate(unique_categories, start=1):
            print(f"{idx}. {category}")
        print(f"{len(unique_categories) + 1}. View All Quiz Cards")
        print(f"{len(unique_categories) + 2}. Return to Quiz Card Management")

        # Prompt user to select a category or view all flashcards
        try:
            selection = get_valid_integer(
                "\nSelect a category by number "
                "(or choose 'View All Quiz Cards'):",
                1,
                len(unique_categories) + 2,
            )
            if selection == len(unique_categories) + 2:
                # User chose to return to the previous menu
                print("\nReturning to Previous Menu...")
                return
            elif 1 <= selection <= len(unique_categories):
                # Selected a specific category
                selected_category = unique_categories[selection - 1]
                category_flashcards = [
                    fc
                    for fc in flashcards
                    if (fc["category"] if fc["category"] else "Uncategorized")
                    == selected_category
                ]
                print(f"\nQuiz Cards in category '{selected_category}':")
            else:
                # View all flashcards
                category_flashcards = flashcards
                print("\nAll Quiz Cards:")

            # Display the selected flashcards
            if not category_flashcards:
                print("\nNo Quiz Cards found in this category.")
            else:
                for index, flashcard in enumerate(
                    category_flashcards, start=1
                ):
                    category = (
                        flashcard["category"]
                        if flashcard["category"]
                        else "Uncategorized"
                    )
                    print(
                        f"\n{index}. Term: {flashcard['term']}  "
                        f"\nDefinition: {flashcard['definition']}  "
                        f"\nCategory: {category}"
                    )

            # Prompt user to view other flashcards or return to main menu
            while True:
                continue_choice = input(
                    "\nWould you like to view other flashcards? "
                    "(yes to continue, no to return):\n"
                ).strip().lower()
                if continue_choice in ("yes", "no"):
                    break  # Exit loop if the input is valid
                else:
                    print_error(
                        "Please enter 'yes' or 'no'."
                    )  # Re-prompt for valid input

            # Exit the view loop if the answer is 'no'
            if continue_choice == "no":
                break

        except ValueError:
            print_error("Please enter a valid number.")

    print("\nReturning to Previous Menu...")


def edit_flashcard():
    """
    Edits an existing flashcard. Displays all flashcards with index numbers,
    prompts for a flashcard to edit using a validated index, and asks for
    confirmation before making changes. Allows the user to update term,
    definition, or category. Changes are saved upon confirmation.
    """
    print_section_title("Edit a Quiz Card")
    if not flashcards:
        print("No Quiz Cards available to edit.")
        print("\nReturning to Previous Menu...")
        return

    display_flashcards()  # Display flashcards without navigation options

    # Get a valid flashcard index from the user
    index = get_valid_index(
        "\nEnter the number of the Quiz Card you want to edit: ",
        len(flashcards) - 1,
    )
    flashcard = flashcards[index]

    print(
        f"\nSelected Quiz Card: Term = '{flashcard['term']}', "
        f"Definition = '{flashcard['definition']}', "
        f"Category = '{flashcard['category'] or 'Uncategorized'}'"
    )
    # Ask for confirmation before allowing edits
    if not confirm_action("\nDo you want to edit this Quiz Card? (yes/no): "):
        print("\nEdit cancelled.")
        return

    new_term = input(
        "Enter new term (or press Enter to keep current term):\n"
    ).strip() or flashcard["term"]

    new_definition = input(
        "Enter new definition (or press Enter to keep current definition):\n"
    ).strip() or flashcard["definition"]

    new_category = input(
        "Enter new category (or press Enter to keep current category):\n"
    ).strip().title() or flashcard["category"]

    # Display changes and ask for final confirmation
    print(
        f"\nUpdated Quiz Card:\nTerm: {new_term}\n"
        f"Definition: {new_definition}\n"
        f"Category: {new_category or 'Uncategorized'}"
    )
    if confirm_action("\nDo you want to save these changes? (yes/no):\n "):
        flashcard.update(
            {
                "term": new_term,
                "definition": new_definition,
                "category": new_category if new_category else "Uncategorized",
            }
        )
        print("\nQuiz Card updated successfully!")
        save_flashcards()  # Auto-save enabled
    else:
        print("\nChanges not saved.")


def delete_flashcard():
    """
    Allows users to delete flashcards.
    Displays all flashcards using display_flashcards for selection,
    and prompts the user to select one for deletion by index.
    """
    print_section_title("Delete a Quiz Card")
    if not flashcards:
        print("No Quiz Cards to delete.")
        print("\nReturning to Previous Menu...")
        return

    # Display current flashcards without prompts
    display_flashcards()

    # Get a valid flashcard index from the user
    index = get_valid_index(
        "Enter the number of the Quiz Card to delete: ", len(flashcards) - 1
    )
    flashcard = flashcards[index]

    print(
        f"\nSelected Quiz Card:\nTerm: {flashcard['term']}\n"
        f"Definition: {flashcard['definition']}\n"
        f"Category: {flashcard['category'] or 'Uncategorized'}"
    )

    # Ask for confirmation before deletion
    if confirm_action(
        "\nAre you sure you want to delete this flashcard? (yes/no):\n"
    ):
        del flashcards[index]
        print("\nQuiz Card deleted successfully.")
        save_flashcards()  # Auto-save enabled
    else:
        print("\nQuiz Card not deleted.")


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
    prompt = "Enter a category (or press Enter to skip):\n"
    return input(prompt).strip().title()


# --- Helper & Validation Functions ---


def print_section_title(title):
    """
    Prints a formatted section title to indicate the start of a new option.
    """
    print("\n" + "*" * 40)
    print(f"{title.center(40)}")
    print("*" * 40 + "\n")


def confirm_action(message="Are you sure you want to proceed? (yes/no): \n"):
    """
    Displays a prompt for the user to confirm an action with 'yes' or 'no'.
    Repeats until valid input is received. Returns True for 'yes' and False
    for 'no' responses, used for potentially irreversible actions.
    """
    while True:
        choice = input(message + "\n").strip().lower()
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
            index = int(input(prompt + "\n")) - 1
            if 0 <= index <= max_index:
                return index
            else:
                print_error(
                    f"Please enter a number between 1 and {max_index + 1}."
                )
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")


def get_valid_integer(prompt, min_value, max_value):
    """
    Prompts the user to enter an integer within a specified range, re-prompting
    for invalid input.
    Ensures the integer falls between min_value and max_value.
    """
    while True:
        try:
            value = int(input(prompt + "\n"))
            if min_value <= value <= max_value:
                return value
            else:
                print_error(
                    f"Please enter a number between {min_value} and "
                    f"{max_value}."
                )
        except ValueError:
            print_error("\nInvalid input. Please enter a valid number.")


def display_flashcards():
    """
    Displays flashcards by category or all flashcards,
    without prompting for navigation.
    Used as a helper function in other parts of the program.
    """
    if not flashcards:
        print("No Quiz Cards available.")
        return

    unique_categories = sorted(
        set(
            fc["category"] if fc["category"] else "Uncategorized"
            for fc in flashcards
        )
    )
    print("Available Categories:\n")
    for idx, category in enumerate(unique_categories, start=1):
        print(f"{idx}. {category}")
    print(f"{len(unique_categories) + 1}. View All Quiz Cards")

    # Prompt user to select a category or view all flashcards
    try:
        selection = get_valid_integer(
            "Select a category by number (or choose 'View All Quiz Cards'): ",
            1,
            len(unique_categories) + 1,
        )
        if 1 <= selection <= len(unique_categories):
            selected_category = unique_categories[selection - 1]
            category_flashcards = [
                fc
                for fc in flashcards
                if (fc["category"] if fc["category"] else "Uncategorized")
                == selected_category
            ]
            print(f"\nQuiz Cards in category '{selected_category}':")
        else:
            category_flashcards = flashcards
            print("\nAll Quiz Cards:")

        if not category_flashcards:
            print("\nNo Quiz Cards found in this category.")
        else:
            for index, flashcard in enumerate(category_flashcards, start=1):
                category = (
                    flashcard["category"]
                    if flashcard["category"]
                    else "Uncategorized"
                )
                print(
                    f"\n{index}. Term: {flashcard['term']} "
                    f"\nDefinition: {flashcard['definition']} "
                    f"\nCategory: {category}"
                )
    except ValueError:
        print_error("\nPlease enter a valid number.")


# --- Quiz Functions ---


def start_quiz():
    """
    Initiates a quiz session with a selected category or all categories.
    Prompts the user to select a category and the number of questions.
    After the quiz, offers options to retry the same quiz,
    start a new quiz, or return to the main menu.
    """
    print_section_title("Quiz Mode")
    if not flashcards:
        print(
            "No Quiz Cards available for quiz. Please add Quiz Cards first."
        )
        print("\nReturning to Main Menu...")
        return

    while True:  # Main quiz loop for selecting categories and starting quizzes

        # Display available categories
        unique_categories = sorted(
            set(fc["category"] or "Uncategorized" for fc in flashcards)
        )
        print("\nAvailable Categories:")
        for idx, category in enumerate(unique_categories, start=1):
            print(f"\n{idx}. {category}")
        print(f"{len(unique_categories) + 1}. All Categories")

        # Prompt user for category selection
        try:
            selection = get_valid_integer(
                "\nSelect a category by number "
                "(or choose 'All Categories'):\n",
                1,
                len(unique_categories) + 1,
            )
            if 1 <= selection <= len(unique_categories):
                category = unique_categories[selection - 1]

                # Filter flashcards by the selected category
                category_flashcards = [
                    fc
                    for fc in flashcards
                    if (fc["category"] or "Uncategorized") == category
                ]

                # Check if there are any flashcards in the selected category
                if not category_flashcards:
                    print(
                        f"\nNo Quiz Cards found for category '{category}'. "
                        "Please add flashcards to this category."
                    )
                    return

                print(f"\nStarting quiz on category '{category}'...")
            elif selection == len(unique_categories) + 1:
                category_flashcards = flashcards  # All categories selected
                print("\nStarting quiz on all categories...")
            else:
                print_error(
                    "\nInvalid selection. "
                    "Please enter a number corresponding to the category list."
                )
                continue
        except ValueError:
            print_error("\nPlease enter a valid number.")
            continue

        # Prompt for the number of questions
        max_questions = len(category_flashcards)
        num_questions = get_valid_integer(
            f"\nHow many questions would you like? (1-{max_questions}):\n",
            1,
            max_questions,
        )
        # Run the quiz
        run_quiz(
            category_flashcards,
            num_questions,
            category_name=(
                unique_categories[selection - 1]
                if selection <= len(unique_categories)
                else "All Categories"
            ),
        )

        # Post-quiz options
        while True:
            print("\nQuiz Complete! What would you like to do next?")
            print("\n1. Try the same quiz again")
            print("2. Start a new quiz")
            print("3. Return to Main Menu")

            next_action = get_valid_integer(
                "\nChoose an option (1-3):\n",
                1,
                3,
            )

            if next_action == 1:
                # Retry the same quiz with the same category and question count
                run_quiz(
                    category_flashcards,
                    num_questions,
                    category_name=(
                        unique_categories[selection - 1]
                        if selection <= len(unique_categories)
                        else "All Categories"
                    ),
                )
            elif next_action == 2:
                # Restart the main quiz loop to select a new category
                break
            elif next_action == 3:
                # Exit to the main menu
                print("\nReturning to Main Menu...")
                return


def run_quiz(
    category_flashcards, num_questions, category_name="All Categories"
):
    """
    Runs the quiz for the selected category with a
    specified number of questions.
    Randomly selects flashcards to quiz the user, either term or definition,
    and tracks correct answers.
    If at least one question was attempted, saves progress.
    """
    correct_count = 0
    total_questions = 0

    while total_questions < num_questions:
        flashcard = random.choice(category_flashcards)
        question_asked = False  # Track if the question has been answered

        while not question_asked:
            if random.choice([True, False]):
                user_answer = input(
                    f"\nWhat is the definition of '{flashcard['term']}'? "
                    "(or type 'exit' to quit):\n"
                ).strip()
                correct_answer = flashcard["definition"]
            else:
                definition = flashcard['definition']
                user_answer = input(
                    f"\nWhat term matches the definition '{definition}'? "
                    "(or type 'exit' to quit): "
                ).strip()
                correct_answer = flashcard["term"]

            if user_answer.lower() == "exit":
                return  # End the quiz if the user wants to exit
            elif not user_answer:  # Check for empty input
                print("\nNo answer provided. Please enter an answer.")
            elif user_answer.lower() == correct_answer.lower():
                print("\nCorrect!")
                correct_count += 1
                question_asked = True  # Mark question as answered
            else:
                print(f"\nIncorrect. The correct answer is: {correct_answer}")
                question_asked = True  # Mark question as answered

        total_questions += 1

    # Only save progress if at least one question was attempted
    if total_questions > 0:
        print(
            f"\nQuiz complete! "
            f"You scored {correct_count} out of {total_questions}."
        )
        save_progress(category_name, correct_count, total_questions)
    else:
        print("\nNo questions were attempted; progress will not be saved.")


def save_progress(category, correct_count, total_questions):
    """
    Saves quiz results to the progress file with
    category, score, total questions, and success rate.
    If the file is missing or corrupted, initializes it as an
    empty list. Appends the new entry and saves it in JSON format.
    """
    # Calculate success rate
    success_rate = (
        (correct_count / total_questions) * 100 if total_questions > 0 else 0
    )
    # Create progress entry
    progress_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "score": correct_count,
        "total_questions": total_questions,
        "success_rate": round(success_rate, 2),
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

    print("\nProgress saved successfully!")


# --- Progress Management Function ---


def view_progress():
    """
    Displays all quiz progress entries with
    date, category, score, and success rate.
    Provides a summary, including total quizzes,
    average success rate, highest score,
    and a conditional lowest score.
    Allows the user to clear all progress entries
    with confirmation.
    """
    print_section_title("View Progress")
    try:
        with open(progress_file, "r") as file:
            progress_data = json.load(file)
        if not progress_data:
            print("No quiz progress available.")
            print("\nReturning to Main Menu...")
            return

        print("Quiz Progress History:")
        total_score = 0
        total_questions = 0
        highest_score = 0
        lowest_score = None
        num_quizzes = len(progress_data)
        all_zero_scores = True  # Flag to track if all scores are zero

        for entry in progress_data:
            print(f"Date: {entry['date']}")
            print(f"Category: {entry['category']}")
            print(f"Score: {entry['score']} / {entry['total_questions']}")
            print(f"Success Rate: {entry['success_rate']}%")
            print("-" * 30)

            # Accumulate statistics
            total_score += entry["score"]
            total_questions += entry["total_questions"]
            if entry["score"] > 0:
                all_zero_scores = False  # At least one non-zero score found
            if entry["score"] > highest_score:
                highest_score = entry["score"]
            if lowest_score is None or (
                entry["score"] < lowest_score and entry["score"] > 0
            ):
                lowest_score = entry["score"]
        # Calculate average success rate
        average_success_rate = (
            (total_score / total_questions) * 100 if total_questions > 0 else 0
        )
        # Display summary statistics
        print("\nProgress Summary:")
        print(f"Total Quizzes Taken: {num_quizzes}")
        print(f"Average Success Rate: {average_success_rate:.2f}%")
        print(f"Highest Score Achieved: {highest_score}")
        # Display lowest score or a message if all scores are zero
        if all_zero_scores:
            print(
                "Lowest Score Achieved:"
                "No completed quizzes with a non-zero score."
            )
        else:
            print(
                f"Lowest Score Achieved: "
                f"{lowest_score if lowest_score is not None else 0}"
            )
        # Offer option to clear progress with stricter input handling
        while True:
            clear_progress = input(
                "\nWould you like to clear all quiz progress? (yes/no):\n"
            ).strip().lower()
            if clear_progress == "yes":
                confirmation_message = (
                    "\nAre you sure you want to delete all progress? "
                    "This action cannot be undone. (yes/no): "
                )
                confirm_clear = input(
                    f"{confirmation_message}\n"
                ).strip().lower()
                if confirm_clear == "yes":
                    with open(progress_file, "w") as file:
                        json.dump([], file)
                    print("\nAll quiz progress has been cleared.")
                else:
                    print("\nClear progress cancelled.")
                break
            elif clear_progress == "no":
                print("\nReturning to Main Menu...")
                break
            else:
                print("\nInvalid input. Please enter 'yes' or 'no'.")

    except FileNotFoundError:
        print("\nNo quiz progress available.")
    except json.JSONDecodeError:
        print_error("\nProgress data file is corrupted.")


# --- Main Control Functions ---


def main_menu():
    """
    Navigation menu.
    """
    while True:
        print("\nQuiz Cards Main Menu\n")
        print("1. Quiz Card Management")
        print("2. Quiz Mode")
        print("3. Progress Tracking")
        print("4. Exit")

        choice = input("\nPlease select an option (1-4):\n")

        if choice == "1":
            flashcard_management_menu()
        elif choice == "2":
            start_quiz()
        elif choice == "3":
            view_progress()
        elif choice == "4":
            save_flashcards()
            break
        else:
            print_error("\nInvalid option. Please try again.")


def flashcard_management_menu():
    """
    Submenu for managing flashcards.
    """
    while True:
        print("\nQuiz Card Management\n")
        print("1. Add a New Quiz Card")
        print("2. View Quiz Cards")
        print("3. Edit a Quiz Card")
        print("4. Delete a Quiz Card")
        print("5. Return to Main Menu")

        choice = input("\nPlease select an option (1-5):\n")

        if choice == "1":
            add_flashcard()
        elif choice == "2":
            view_flashcards()
        elif choice == "3":
            edit_flashcard()
        elif choice == "4":
            delete_flashcard()
        elif choice == "5":
            print("\nReturning to Main Menu...")
            break
        else:
            print_error("\nInvalid option. Please try again.")


def main():
    """
    Run program functions, main_menu will handle options and submenus.
    """
    display_welcome_message()
    load_flashcards()
    initialize_progress_file()
    main_menu()
    print("\nThank you for using Quiz Cards! Goodbye!")  # Exit message


# --- Run the Program ---


main()
