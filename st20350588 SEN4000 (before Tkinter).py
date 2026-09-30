# STEP BY STEP BUILD OF MY LMS SYSTEM

'''
TASK 1:
IMPORT REQUIRED LIBRARIES
'''
import sys  # used to completely exit the program
import os
import pandas as pd  # used for handling table-like data (DataFrame)
from tabulate import tabulate  # used to display data in clean table format
from datetime import datetime  # used for validating year input

# -----------------------------------------------------------------------------------------------------------------------
'''
TASK 2: CREATING A DUMMY DICTIONARY DATA FOR MY LMS

Each book contains:
    - BookID (unique identifier)
    - Title
    - Author
    - Year
    - Genre
    - Status (Available/Borrowed)
    - Borrower (name of member who borrowed the book)
'''

'''
books=[
    {"BookID":"",
     "Title": "",
     "Author": "",
     "Year": "",
     "Genre": "",
     "Status": "",
     "Borrower": ""},
]
'''

books = [
    {"BookID": "1", "Title": "Harry Potter", "Author": "J.K. Rowling", "Year": "1997", "Genre": "Fantasy",
     "Status": "Available", "Borrower": ""},
    {"BookID": "2", "Title": "The Hobbit", "Author": "J.R.R. Tolkien", "Year": "1937", "Genre": "Fantasy",
     "Status": "Available", "Borrower": ""},
    {"BookID": "3", "Title": "1984", "Author": "George Orwell", "Year": "1949", "Genre": "Dystopian",
     "Status": "Available", "Borrower": ""},
    {"BookID": "4", "Title": "To Kill a Mockingbird", "Author": "Harper Lee", "Year": "1960", "Genre": "Fiction",
     "Status": "Available", "Borrower": ""},
    {"BookID": "5", "Title": "Pride and Prejudice", "Author": "Jane Austen", "Year": "1813", "Genre": "Romance",
     "Status": "Available", "Borrower": ""},
    {"BookID": "6", "Title": "The Great Gatsby", "Author": "F. Scott Fitzgerald", "Year": "1925", "Genre": "Classic",
     "Status": "Available", "Borrower": ""},
    {"BookID": "7", "Title": "Moby Dick", "Author": "Herman Melville", "Year": "1851", "Genre": "Adventure",
     "Status": "Available", "Borrower": ""},
    {"BookID": "8", "Title": "The Catcher in the Rye", "Author": "J.D. Salinger", "Year": "1951", "Genre": "Fiction",
     "Status": "Available", "Borrower": ""},
    {"BookID": "9", "Title": "The Lord of the Rings", "Author": "J.R.R. Tolkien", "Year": "1954", "Genre": "Fantasy",
     "Status": "Available", "Borrower": ""},
    {"BookID": "10", "Title": "The Alchemist", "Author": "Paulo Coelho", "Year": "1988", "Genre": "Fiction",
     "Status": "Available", "Borrower": ""}
]

# -----------------------------------------------------------------------------------------------------------------------
'''
TASK 3: Convert dictionary into DataFrame and save as CSV
'''
df = pd.DataFrame(books)  # convert list of dictionaries into a DataFrame
df.to_csv('book_details.csv',index=False)  # save dataframe to CSV file
print("\nBook details saved to 'book_details.csv' successfully.")

FILE_NAME = 'book_details.csv'

#-----------------------------------------------------------------------------------------------------------------------
def load_data():
    return pd.read_csv(FILE_NAME, dtype={"BookID": str})

def save_data(df):
    df.to_csv(FILE_NAME, index=False)
# -----------------------------------------------------------------------------------------------------------------------
'''
TASK 4: MAIN MENU SYSTEM
'''

def welcome():
    # This function displays the welcome screen of the LMS and starts the program.
    # It ensures the user explicitly types 'Start' to proceed to the main menu.
    while True:  # Keeps prompting until the user enters 'Start'
        print("\n---WELCOME TO MICHAEL'S LIBRARY---")  # Display welcome message
        start_prompt = input("Enter 'Start' to proceed: ").strip().lower()  # Get user input and normalize it to lowercase

        # If user enters 'start', proceed to main menu
        if start_prompt == "start":
            print("\n")  # Adds a blank line for cleaner display
            main_menu()  # Call the main menu function to navigate LMS

        # Handle invalid input
        else:
            print("\nInvalid input. Please try again.")  # Prompt user again if input is incorrect


def main_menu():
    # This is the central navigation menu of my LMS.
    # It serves as the starting point and links to all other functions like a switchboard.
    while True:  # Keeps the main menu running until the user chooses to exit
        # Display main menu options
        print("---MAIN MENU---")
        print("1. Admin Login")   # Option to log in as Admin
        print("2. Member Login")  # Option to log in as a Member
        print("3. Exit LMS")      # Option to exit the entire LMS program

        # Prompt user to select a login mode or exit
        login_request = input("\nChoose a login mode (1 or 2) or enter 3 to exit LMS: ").strip()

        # Admin login selection
        if login_request == "1":
            admin_login()  # Calls the function to handle admin login

        # Member login selection
        elif login_request == "2":
            member_login()  # Calls the function to handle member login

        # Exit option
        elif login_request == "3":
            print("\nLeaving already? Hope to see you next time soon, bye for now.")
            sys.exit()  # Completely stops the program

        # Handle invalid input
        else:
            print("\nInvalid input. Please try again.\n")  # Prompts user to try again if input is invalid


def admin_login():
    # This function handles admin authentication
    admin_password = "admin1234"
    attempts = 3  # maximum number of login attempts set at 3

    while attempts > 0:
        password_request = input("Enter admin password: ").strip()

        # admin password check
        if password_request == admin_password:
            print("Welcome, Admin!")
            admin_menu()  # takes user to admin menu after successful login
            return  # exit function after successful login

        else:
            attempts -= 1  # reduce remaining attempts
            print(f"Incorrect password. {attempts} attempts left.")

            # if no attempts left, stop asking
            if attempts == 0:
                break

            # ask user if they want to try again
            proceed = input("Try again? (y/n): ").strip().lower()

            if proceed == "y":
                continue  # Restarts the while loop
            elif proceed == "n":
                print("\nReturning to Main Menu...")
                return  # exits function completely when request to proceed = 'n'
            else:
                print("Invalid input. Enter (y/n).")

    # After 3 failed login attempts, program displays this message
    print("\nToo many failed attempts. Returning to welcome page.")


def member_login():
    # Handles member login (no password, just name)
    member_name = input("\nEnter your name: ").strip()
    print(f"\nWelcome, {member_name}!")
    member_menu(member_name)

# -----------------------------------------------------------------------------------------------------------------------
'''
TASK 5: ADMIN FUNCTIONS:

 1. View Inventory
    ▪ Display all book details in a clean, readable format.

2. Add New Books:
    Add details such as
    ▪ Book ID (must be unique)
    ▪ Title
    ▪ Author
    ▪ Year published
    ▪ Genre
    ▪ Status (default: “Available”)
    ▪ Borrower (default: “nan”)
    
3. Update Book Details:
    ▪ Allow admin to update any of the details (e.g., title, author, availability).
4. Remove a Book
    ▪ Remove a book using its ID.
5. Return to Main Menu
'''

def admin_menu():  # This defines the Admin Menu and allows access to all admin functions one choice at a time
    while True:  # Keeps the menu running until the admin chooses to logout

        # Dictionary linking menu options to their corresponding functions
        admin_functions = {
            "1": view_inventory,  # View all books in the library
            "2": add_book,        # Add a new book to the library
            "3": update_book,     # Update details of an existing book
            "4": remove_book,     # Remove a book completely from the library
        }

        # Display the admin menu options
        print("\n--- ADMIN MENU ---")
        print("1. View Inventory")
        print("2. Add Book")
        print("3. Update Book")
        print("4. Remove Book")
        print("5. Logout")  # Option to exit the admin menu and return to the main menu

        # Prompt admin for a choice
        admin_choice = input("\nChoose a menu option from (1-5): ").strip()

        # Execute the selected function if valid
        if admin_choice in admin_functions:
            admin_functions[admin_choice]()  # Calls the function associated with the chosen option

        # Logout option
        elif admin_choice == "5":
            print("\nExiting 'Admin Menu', returning to 'Main Menu'...\n")
            break  # Exit the while loop and return to main menu

        # Handle invalid input
        else:
            print("Invalid choice. Please try again.")


def view_inventory():
    # This function displays all current books in the library in a clean table format

    # Load the latest book data from the CSV file
    df = pd.read_csv('book_details.csv', dtype={"BookID": str})

    # Check if the library is empty
    if df.empty:
        print("No books available.")  # Inform the user if there are no books

    else:
        # Display all books in a tabular format using `tabulate`
        print("\nCurrent Inventory:")
        print(tabulate(df, headers="keys", tablefmt="pretty", showindex=False))
        # 'headers="keys"' uses the column names from the DataFrame
        # 'tablefmt="pretty"' displays the table in a well-structured format
        # 'showindex=False' hides the DataFrame index for cleaner output


def add_book():
    while True:
        df = load_data()
        books = df.to_dict(orient='records')

        # --- INPUT BOOK ID ---
        book_id = input("\nEnter new Book ID: ").strip()

        # --- CHECK DUPLICATE ID ---
        if any(book["BookID"] == book_id for book in books):
            print("Book ID already exists.")

            retry = input("Try again? (y/n): ").strip().lower()
            if retry != "y":
                print("\nReturning to Admin Menu...")
                return
            continue

        # --- COLLECT BOOK DETAILS ---
        title = input("Enter Title: ").strip()
        author = input("Enter Author: ").strip()

        # --- VALIDATE YEAR ---
        while True:
            try:
                year = int(input("Enter Year: ").strip())

                if year < 1600 or year > datetime.now().year:
                    print(f"Invalid year. Enter a year between 1600 and {datetime.now().year}.")
                    continue

                break

            except ValueError:
                print("Invalid input. Year must be a number.")

        genre = input("Enter Genre: ").strip()

        # --- CREATE BOOK RECORD ---
        new_book = {
            "BookID": book_id,
            "Title": title,
            "Author": author,
            "Year": year,
            "Genre": genre,
            "Status": "Available",
            "Borrower": ""
        }

        # --- SAVE DATA ---
        books.append(new_book)
        df = pd.DataFrame(books)
        save_data(df)

        # --- DISPLAY RESULT ---
        print(f"\n Book '{title}' added successfully!")
        print("\nNew Record:")
        print(tabulate([new_book], headers="keys", tablefmt="pretty", showindex=False))

        # --- CONTINUE OR EXIT ---
        again = input("\nAdd another book? (y/n): ").strip().lower()
        if again != "y":
            print("\nReturning to Admin Menu...")
            return


def update_book():  # This defines the process to update information for existing books
    book_info = ["Title", "Author", "Year", "Genre", "Status"]  # These are valid fields that can be updated

    while True:  # Keep running until user chooses to exit

        # Load latest book data from CSV
        df = pd.read_csv('book_details.csv', dtype={"BookID": str})
        books = df.to_dict(orient='records')  # Convert DataFrame into a list of dictionaries for easier handling

        # Ask user for the Book ID to update
        book_id = input("Enter Book ID: ").strip()
        found = False  # Track whether the book exists

        # Search for the book in the list
        for book in books:
            if book["BookID"] == book_id:
                found = True
                print(f"\nUpdating: {book['Title']}")

                while True:
                    # Display update options
                    print("Key Fields: Title, Author, Year, Genre, Status, None")
                    choice = input("Choose a field to update? ").strip().capitalize()

                    if choice in book_info:
                        while True:
                            print(f"\nYou have chosen to update the '{choice}' field of '{book['Title']}'.")
                            print(f"Current value: {book[choice]}")

                            new_value = input(f"\nEnter new {choice}: ").strip()

                            # Ask for confirmation before updating the book
                            confirm = input("Proceed with update? (y/n): ").strip().lower()

                            if confirm == "y":
                                # Update the selected field
                                book[choice] = new_value

                                print(f"\n---The {book[choice]} field of {book['Title']} has been updated successfully!---")

                                # Save changes back to CSV
                                df = pd.DataFrame(books)
                                df.to_csv('book_details.csv', index=False)

                                break  # Exit confirmation loop after updating

                            elif confirm == "n":
                                # User cancels update process
                                print("Update cancelled. No changes were made.")
                                break  # Exit confirmation loop without updating

                            else:
                                # Handle invalid input
                                print("Invalid input. Enter (y/n)")


                    elif choice.lower() == "none":
                        print("No update made.")

                    else:
                        print("Invalid option.")
                        continue  # Ask for choice again

                    # Ask if the user wants to update more fields
                    while True:
                        continue_update = input("Do you want to continue updating? (y/n): ").strip().lower()

                        if continue_update == "y":
                            break  # Restart the outer while loop to update again
                        elif continue_update == "n":
                            print("\nReturning to Admin Menu...")
                            return  # Exit the function completely
                        else:
                            print("Invalid input.")  # Continue until valid input is given

                    break  # Exit inner update loop
                break  # Exit search loop after finding the book

        # If no book matched the entered Book ID
        if not found:
            print("Book not found.")

            # Ask user if they want to retry searching for a book to update
            while True:
                retry = input("Would you like to try again? (y/n): ").strip().lower()
                if retry == "y":
                    break  # Restart outer while loop
                elif retry == "n":
                    print("Exiting 'Update Books'...")
                    return  # Exit the function completely
                else:
                    print("\nInvalid response. choose y/n.")  # Loop until valid input is given


def remove_book():  # This defines the process to remove an entire book's record from the library
    while True:  # Keep running until user exits or completes a removal

        # Load the latest book data from the CSV file
        df = pd.read_csv('book_details.csv', dtype={"BookID": str})

        # Convert DataFrame into a list of dictionaries for easier handling
        books = df.to_dict(orient='records')

        # Ask the user to input the Book ID of the book they want to remove
        book_id = input("Enter Book ID to remove: ").strip()

        found = False  # This variable tracks whether the entered Book ID exists

        # Loop through all books to find the matching Book ID
        for book in books:
            if book["BookID"] == book_id:
                found = True  # Book exists

                # Ask for confirmation before deleting the book
                while True:
                    print(f"\nYou have indicated to remove the book: '{book['Title']}'.")
                    confirm = input("Are you sure? (y/n): ").strip().lower()

                    if confirm == "y":
                        # Remove the selected book from the list
                        books.remove(book)

                        # Display the removed book in a table for user reference
                        print("\n---Removed record---")
                        print(tabulate([book], headers="keys", tablefmt="pretty", showindex=False))

                        # Save the updated book list back to CSV
                        df = pd.DataFrame(books)
                        df.to_csv('book_details.csv', index=False)

                        print("Book removed successfully.")
                        break  # Exit confirmation loop after deletion

                    elif confirm == "n":
                        # User cancels deletion
                        print("Deletion cancelled.")
                        break  # Exit confirmation loop without deleting

                    else:
                        # Handle invalid input
                        print("Invalid input. Enter (y/n)")

                break  # Stop searching after the book is found

        # This block runs if no book matched the entered Book ID
        if not found:
            print("Book not found.")

        # Ask user if they want to remove another book
        while True:
            choose_another = input("Do you want to remove another book instead? (y/n): ").strip().lower()

            if choose_another == "y":
                break  # Restart the process to remove another book

            elif choose_another == "n":
                # Exit the function completely if user does not want to remove another book
                print("\nExiting \"Remove Book\"...")
                return

            else:
                # Handle invalid input
                print("Invalid response. choose (y/n).")


# -----------------------------------------------------------------------------------------------------------------------
'''
TASK 6: MEMBER FUNCTIONS:

1. View Available Books
  Display a list of available books with the following information:
  ▪ Book ID (must be unique)
  ▪ Title (e.g., "Harry Potter and the Sorcerer’s Stone")
  ▪ Author (e.g., "J.K. Rowling")
  ▪ Year Published
  ▪ Genre (e.g., Fiction, Mystery)
  ▪ Status (Available)

2. Search for Books:
   (search for books must be based on at least one of the following criteria)
   ▪ By Title
   ▪ By Author
   ▪ By Genre

3. Borrowing a Book
  ▪ Users can borrow a book by entering the Book ID.
  ▪ Borrowing should update the status to “Borrowed”.
  ▪ The system must prevent: Borrowing an already borrowed book
  ▪ The system must prevent: Borrowing when user has a borrowed book which hasn't been returned 

4. Returning a Book
  ▪ User returns a book using the Book ID.
  ▪ Status must update back to “Available”.
  ▪ The system must prevent returning a book that is already marked as available.
  ▪ The system must ensure that user can only return a book for which the 'Borrowed' status is tagged to their name.
'''


def member_menu(member_name): #This displays the member functions and how they are accessed with one choice input at a time
    while True:  # keeps showing the menu until user exits
        print("\n---MEMBER MENU---")
        print("1. View Available Books")
        print("2. Search for a Book")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Logout")

        # dictionary linking menu options to functions
        member_functions = {
            "1": view_available_books,
            "2": search_books,
            "3": lambda: borrow_book(member_name),
            "4": lambda: return_book(member_name),
        }

        # get user input
        member_choice = input("\n Choose a menu option from (1-5): ").strip()

        if member_choice in member_functions:
            member_functions[member_choice]()  # call the selected function
        elif member_choice == "5":
            print("\nExiting 'Member Menu', returning to 'Main Menu'...")
            break  # exit the menu loop when user input is '5' i.e. 'EXIT' and logout
        else:
            print("Invalid input. Please try again.")


def view_available_books(): # This defines the program to view/access available books in the library

    # load latest book data from CSV
    df = pd.read_csv('book_details.csv', dtype={"BookID": str})
    books = df.to_dict(orient='records')  # convert to list of dictionaries

    found = False  # to check if any available book is found

    for book in books:
        if book["Status"] == "Available":
            print(tabulate([book], headers="keys", tablefmt="pretty", showindex=False))
            found = True  # This is 'True' if at least one available book exists

    if not found:
        print("No available books")


def search_books():
    # This loop keeps the search feature running until the user chooses to exit
    while True:

        # Load the most recent book data from the CSV file
        df = pd.read_csv('book_details.csv', dtype={"BookID": str})

        # Convert the DataFrame into a list of dictionaries
        books = df.to_dict(orient='records')

        # This tracks if any book was found
        found = False

        # Ask the user what type of search they want to perform
        print("\nSearch by:")
        print("1. Title")
        print("2. Author")
        print("3. Genre")

        option = input("Choose option (1-3): ").strip()

        # ---------------- SEARCH BY TITLE ----------------
        if option == "1":
            # Ask user to enter the book title
            title_input = input("\nEnter book title: ").strip().lower()

            # Loop through all books
            for book in books:
                # Compare user input with book title (case-insensitive)
                if book["Title"].lower() == title_input:
                    print("\nBook found!\n")

                    # Display the matched book in a table format
                    print(tabulate([book], headers="keys", tablefmt="pretty", showindex=False))

                    found = True

                    # Since titles are unique, stop searching after finding one match
                    break

            # If no book matched the title
            if not found:
                print("Book not found.")

        # ---------------- SEARCH BY AUTHOR ----------------
        elif option == "2":
            # Ask user to enter author name
            author_input = input("\nEnter author name: ").strip().lower()

            # Create an empty list to store all matching books
            results = []

            # Loop through all books
            for book in books:
                # Check if the author's name appears in the book record
                if book["Author"].lower() == author_input:
                    results.append(book)  # Add matching book to results list

            # If we found at least one matching book
            if results:
                print(f"\n{len(results)} {author_input} book(s) found:\n")

                # Display all matching books at once
                print(tabulate(results, headers="keys", tablefmt="pretty", showindex=False))

                found = True
            else:
                print("No books found for this author.")

        # ---------------- SEARCH BY GENRE ----------------
        elif option == "3":
            # Ask user to enter genre
            genre_input = input("\nEnter genre: ").strip().lower()

            # Create an empty list to store matching books
            results = []

            # Loop through all books
            for book in books:
                # Check if the genre matches (partial match allowed)
                if book["Genre"].lower() == genre_input:
                    results.append(book)

            # If matches were found
            if results:
                print(f"\n{len(results)} {genre_input} book(s) found:\n")

                # Display all results in a table
                print(tabulate(results, headers="keys", tablefmt="pretty", showindex=False))

                found = True
            else:
                print("No books found for this genre.")

        # ---------------- INVALID OPTION ----------------
        else:
            print("Invalid option. Please choose between 1 and 3.")
            continue  # Restart the loop immediately

        # ---------------- REPEAT SEARCH PROMPT ----------------
        # Ask the user if they want to perform another search
        while True:
            again = input("\nSearch again? (y/n): ").strip().lower()

            if again == "y":
                break  # Restart the main search loop
            elif again == "n":
                return  # Exit the function completely
            else:
                print("Invalid input. Enter (y/n).")



def borrow_book(member_name): # This defines the program to borrow a book at a time by a member
    while True:  # loop keeps running until user exits or successfully borrows a book

        # load latest book data from CSV file into a DataFrame
        df = pd.read_csv('book_details.csv', dtype={"BookID": str})

        # convert DataFrame into a list of dictionaries for easier handling
        books = df.to_dict(orient='records')

        # Check if member already has a borrowed book
        # This ensures that each member can only borrow ONE book at a time
        for book in books:
            if book["Borrower"] == member_name and book["Status"] == "Borrowed":
                print(f"\nSorry {member_name}, you have already borrowed '{book['Title']}'. Return it first before borrowing another book.")
                return  # exit function immediately if condition is met

        # The next part will only run if member has no borrowed book to their name
        # Ask user to input the Book ID of the book they want to borrow
        book_id = input("\nEnter a book ID: ").strip()

        found = False  # This tracks whether the entered Book ID exists

        # Loop through all books to find a match for the entered Book ID
        for book in books:
            if book["BookID"] == book_id:
                found = True  # This marks that the book has been found

                # Check if the book is available for borrowing
                if book["Status"] == "Available":
                    print(f"\nBook '{book['Title']}' is available!")

                    # Ask user to confirm if they want to borrow the book
                    confirm = input("Proceed to borrow this book? (y/n): ").strip().lower()

                    if confirm == "y":
                        # Update the book's status to 'Borrowed'
                        book["Status"] = "Borrowed"

                        # Record the name of the member who borrowed the book
                        book["Borrower"] = member_name

                        print(f"\nCongratulations {member_name}, you have successfully borrowed book: '{book['Title']}'.")
                        print("Enjoy your reading, return on time and borrow another book.")

                        # Save the updated book list back to the CSV file
                        df = pd.DataFrame(books)
                        df.to_csv('book_details.csv', index=False)

                        return # exit function after successful borrowing

                    elif confirm == "n":
                        print("Borrowing cancelled")
                        try_again=input(f"\nStill want to borrow a book? (y/n): ")
                        if try_again == "y":
                            break  # exit current loop and restart the main while loop
                        elif try_again == "n":
                            return # exit the function completely
                        else:
                            print("Invalid response. Enter y/n.")

                    else:
                        # Handles invalid inputs
                        print("(Invalid response. Enter y/n.)")

                else:
                    # This runs if the book is already borrowed by someone else
                    print(f"Sorry, '{book['Title']}' is already borrowed.")

                break  # stop searching once the book is found

        # This block runs if no book matched the entered Book ID
        if not found:
            print("Book ID not found.")

            # Ask the user if they want to try entering another Book ID
            try_again = input("\nWould you like to try again? (y/n): ").strip().lower()

            if try_again == "y":
                continue  # restart the loop and ask again
            elif try_again == "n":
                print("Exiting to Member Menu...")
                return  # exit function completely
            else:
                # Handles invalid inputs
                print("Invalid response. Enter y/n.")


def return_book(member_name): # This defines the program to return a borrowed book
    while True:  # Keep running until user successfully returns a book or chooses to exit

        # Load the latest book data from the CSV file
        df = pd.read_csv('book_details.csv', dtype={"BookID": str})

        # Convert DataFrame into a list of dictionaries for easier handling
        books = df.to_dict(orient='records')

        # Ask user to enter the Book ID they want to return
        book_id = input("\nEnter the book ID: ").strip()

        found = False  # This variable tracks whether the entered Book ID exists

        # Loop through all books to find the matching Book ID
        for book in books:
            if book["BookID"] == book_id:
                found = True  # Book exists

                # Check if the book is currently borrowed by this member
                if book["Status"] == "Borrowed" and book["Borrower"] == member_name:
                    # Update book status to 'Available' since it is being returned
                    book["Status"] = "Available"

                    # Remove borrower's name from the record
                    book["Borrower"] = ""

                    print(f"\nThank you {member_name}, you have successfully returned '{book['Title']}'.")

                    # Save the updated book list back to CSV
                    df = pd.DataFrame(books)
                    df.to_csv('book_details.csv', index=False)

                    return # Exit the function completely

                # This handles a situation where the book is already available (not borrowed)
                elif book["Status"] == "Available":
                    print(f"This book '{book['Title']}' was not borrowed.")
                    print(f"\nEnsure the bookID is correct and try again.")

                    # Ask user if they want to try again
                    try_again = input("Try again? (y/n): ").strip().lower()

                    if try_again == "y":
                        continue  # Restart the main loop
                    elif try_again == "n":
                        print("Exiting to Member Menu...")
                        return  # Exit the function completely
                    else:
                        # Handles invalid input
                        print("Invalid response. choose y/n.")


                # This handles a situation where the book is borrowed by someone else
                else:
                    print(f"You cannot return a book you did not borrow")
                    print(f"\nEnsure the bookID is correct and try again.")

                    # Ask user if they want to try again
                    try_again = input("Try again? (y/n): ").strip().lower()

                    if try_again == "y":
                        continue  # Restart the main loop
                    elif try_again == "n":
                        print("Exiting to Member Menu...")
                        return  # Exit the function completely
                    else:
                        # Handles invalid input
                        print("Invalid response. choose y/n.")

        # This block runs if no book matched the entered Book ID
        if not found:
            print("Book ID not found.")
            print("Check the book ID and try again or exit.")

            # Ask user if they want to try again
            try_again = input("Would you like to try again? (y/n): ").strip().lower()

            if try_again == "y":
                continue  # Restart the main loop
            elif try_again == "n":
                print("Exiting to Member Menu...")
                return  # Exit function
            else:
                # This handles invalid input
                print("Invalid response. choose y/n.")


if __name__ == "__main__":
    welcome()  # start the program