# =========================
# IMPORTS
# =========================

import tkinter as tk  # GUI library for building desktop apps
from tkinter import ttk, messagebox  # themed widgets + popup messages
import pandas as pd  # used for handling CSV data like a table
import os  # checks file existence
from datetime import datetime  # used for validating year input

# =========================
# CONFIGURATION
# =========================

BOOK_FILE = "book_details.csv"  # file where book data is stored persistently

# =========================
# INITIAL DATA (MY DUMMY DATA)
# =========================
books = [
    # Each dictionary in the list represents a single book record in the library system
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

# This creates CSV file if it does not exist yet
if not os.path.exists(BOOK_FILE):
    pd.DataFrame(books).to_csv(BOOK_FILE, index=False)

# =========================
# DATA FUNCTIONS (BACKEND LAYER)
# =========================

def load_books():
    # Load dataset from CSV file into a DataFrame
    df = pd.read_csv(BOOK_FILE)

    # Ensure BookID values are numeric integers for correct identification and sorting
    df["BookID"] = pd.to_numeric(df["BookID"], errors="coerce").fillna(0).astype(int)

    # Ensure Year values are numeric integers for accurate validation and comparison
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").fillna(0).astype(int)

    # Replace missing Status values with "Available" to maintain consistent book state tracking
    df["Status"] = df["Status"].fillna("Available")

    # Replace missing Borrower values with empty strings to avoid null-related errors
    df["Borrower"] = df["Borrower"].fillna("")

    return df


def save_books(df):
    # Ensure BookID is numeric to maintain correct sorting order
    df["BookID"] = pd.to_numeric(df["BookID"], errors="coerce")

    # Sort records by BookID for consistent dataset structure
    df = df.sort_values(by="BookID")

    # Save DataFrame to CSV, overwriting existing file
    df.to_csv(BOOK_FILE, index=False)

def find_book(df, book_id):
    # Filter the dataset to find a row matching the given BookID
    match = df[df["BookID"] == int(book_id)]

    # Return None if no matching record is found
    if match.empty:
        return None, None

    # Retrieve the index of the matched row
    idx = match.index[0]

    # Return both the index and the corresponding book record
    return idx, match.loc[idx]


# =========================
# MAIN APP
# =========================
class LibraryApp:
    def __init__(self, root):
        # I store the main Tkinter window reference for use throughout the class
        self.root = root

        # I set the title of the application window
        root.title("This is Michael's Library System")

        # I define the size of the application window
        root.geometry("1000x600")

        # I define a central colour theme dictionary for consistent UI styling across the application
        self.colors = {
            # I set the main background colour of the application
            "bg": "whitesmoke",

            # I define the surface colour used for panels and tables
            "surface": "white",

            # I define the main text colour used across the interface
            "text": "black",

            # I define a muted text colour for secondary labels and hints
            "muted": "gray40",

            # I define the primary colour used for headings and navigation elements
            "primary": "midnightblue",

            # I define a secondary colour used for non-critical actions and buttons
            "secondary": "lightsteelblue",

            # I define the accent colour used for primary action buttons
            "accent": "steelblue",

            # I define the success colour used for positive actions like adding data
            "success": "seagreen",

            # I define the danger colour used for destructive actions like delete
            "danger": "firebrick",

            # I define the warning colour used for caution or update actions
            "warning": "peru",
        }

        # I apply the background colour to the main application window
        self.root.configure(bg=self.colors["bg"])

        # I initialise the current user as None until a user logs in
        self.current_user = None

        # I display the welcome screen as the first interface when the application starts
        self.welcome_screen()

# =========================
# UI UTILITY HELPERS
# =========================
    def make_button(self, parent, text, command, color, fg="black"):
        # I create a reusable button component to ensure consistent styling across the application
        return tk.Button(
            parent,
            # I set the text that will be displayed on the button
            text=text,

            # I assign the function that will be executed when the button is clicked
            command=command,

            # I set the background colour of the button
            bg=color,

            # I set the text colour of the button
            fg=fg,

            # I apply a consistent font style for all buttons
            font=("Arial", 10, "bold"),

            # I add horizontal padding to improve spacing and click area
            padx=12,

            # I add vertical padding to improve button height and usability
            pady=6,

            # I remove the default border for a cleaner modern UI look
            bd=0,

            # I define the hover/click background effect for better visual feedback
            activebackground=self.colors["secondary"]
        )

    def buttons(self, admin=False):
        # I create a container frame that groups all action buttons into a single toolbar
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(pady=15)

        # I check whether the current user has admin privileges to determine available actions
        if admin:

            # I create a button that opens the form for adding a new book
            self.make_button(frame, "Add", self.add_book, self.colors["success"], fg="white").grid(row=0, column=0,
                                                                                                   padx=5)

            # I create a button that removes the currently selected book from the system
            self.make_button(frame, "Remove", self.remove_book, self.colors["danger"], fg="white").grid(row=0, column=1,
                                                                                                        padx=5)

            # I create a button that opens the update interface for editing book details
            self.make_button(frame, "Update", self.update_book, self.colors["warning"]).grid(row=0, column=2, padx=5)

        else:

            # I create a button that allows a member to borrow a selected book
            self.make_button(frame, "Borrow", self.borrow_book, self.colors["accent"]).grid(row=0, column=0, padx=5)

            # I create a button that allows a member to return a previously borrowed book
            self.make_button(frame, "Return", self.return_book, self.colors["secondary"]).grid(row=0, column=1, padx=5)

        # I create a shared logout button that returns any user back to the login screen
        self.make_button(frame, "Logout", self.login_screen, self.colors["primary"], fg="white").grid(row=0, column=3,
                                                                                                      padx=5)

    def clear(self):
        # I retrieve all widgets currently displayed in the main window
        for w in self.root.winfo_children():
            # I destroy each widget to clear the interface completely
            w.destroy()

        # I reset the window background to the default application theme colour
        self.root.configure(bg=self.colors["bg"])

    def get_selected_book_id(self):
        """Get selected BookID from the table safely."""

        # I retrieve the currently selected item(s) from the Treeview
        sel = self.tree.selection()

        # I return None if no row is selected to prevent downstream errors
        if not sel:
            return None

        # I extract the values from the first selected row
        values = self.tree.item(sel[0])["values"]

        # I return the BookID from the selected row as an integer
        return int(values[0])

    def reselect_book(self, book_id):
        """Re-select a book row in the Treeview by BookID."""

        # I first check if a valid BookID was provided
        if not book_id:
            return

        # I iterate through all rows currently displayed in the Treeview
        for item in self.tree.get_children():

            # I retrieve the values stored in the current row
            values = self.tree.item(item)["values"]

            # I compare the first column (BookID) with the target ID
            if int(values[0]) == book_id:
                # I programmatically select the matching row in the table
                self.tree.selection_set(item)

                # I set keyboard focus to the selected row
                self.tree.focus(item)

                # I ensure the selected row is visible in the viewport
                self.tree.see(item)

                # I stop the loop once the correct row has been found and selected
                break

    def mark_invalid(self, entry, reset_bg="white"):
        """
        Visually mark an Entry widget as invalid while keeping it visible,
        focused, and ready for correction.
        """

        # I set focus on the entry field so the user can immediately correct it
        entry.focus_set()

        # I change the background colour to indicate invalid input
        entry.config(bg="mistyrose")

        # I reset the background colour after a short delay to keep feedback non-intrusive
        entry.after(800, lambda: entry.config(bg=reset_bg))

#======================
# WELCOME SCREEN
#======================
    def welcome_screen(self):  # Create and display the initial welcome screen
        # I clear any existing widgets to ensure the welcome screen starts from a clean state
        self.clear()

        # I display the main welcome title of the application as the primary branding element
        tk.Label(
            self.root,
            text="WELCOME TO MICHAEL'S LIBRARY",
            font=("Arial", 20, "bold"),
            bg=self.colors["bg"],
            fg="darkblue"
        ).pack(pady=(70, 0))

        # I display a motivational slogan beneath the main title
        tk.Label(
            self.root,
            text="\"...making LEADERS out of READERS...\"",
            font=("Arial", 13, "italic", "bold"),
            bg=self.colors["bg"],
            fg=self.colors["muted"]
        ).pack(pady=(0, 20))

        # I create a button that allows the user to proceed into the system
        tk.Button(
            self.root,
            text="Click to Begin",
            font=("Arial", 12, "bold"),
            fg=self.colors["primary"],
            width=20,
            command=self.login_screen
        ).pack(pady=30)

# =====================
# LOGIN SCREEN FUNCTIONALITIES
# =====================
    def login_screen(self):
        # I clear all existing widgets to reset the interface to a clean login state
        self.clear()

        # I display the main login screen title as the primary navigation context
        tk.Label(
            self.root,
            text="USER LOGIN",
            font=("Arial", 16, "bold", "underline"),
            bg=self.colors["bg"],
            fg=self.colors["primary"]
        ).pack(pady=(20, 5))

        # I display a subtitle to guide the user in selecting a login option
        tk.Label(
            self.root,
            text="(click to choose a user login)",
            font=("Arial", 12, "bold", "italic"),
            bg=self.colors["bg"],
            fg="gray"
        ).pack(pady=(0, 20))

        # I create a button that navigates to the admin login screen
        self.make_button(
            self.root,
            "Admin Login",
            self.admin_login,
            self.colors["accent"]
        ).pack(pady=10)

        # I create a button that navigates to the member login screen
        self.make_button(
            self.root,
            "Member Login",
            self.member_login,
            self.colors["accent"]
        ).pack(pady=10)

        # I create a button that returns the user to the welcome screen
        self.make_button(
            self.root,
            "Exit",
            self.welcome_screen,
            self.colors["danger"],
            fg="white"
        ).pack(pady=10)

    def admin_login(self):
        # I clear the current window to display a fresh admin login interface
        self.clear()

        # I display a label prompting the user to enter the admin password
        tk.Label(
            self.root,
            text="Enter Admin Password",
            bg=self.colors["bg"],
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        # I create a password entry field for secure admin input
        self.admin_pass = tk.Entry(
            self.root,
            show="*",
            font=("Arial", 12)
        )
        self.admin_pass.pack(pady=5)

        # I create a container frame to hold the login action buttons
        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(pady=15)

        # I create a button to validate admin credentials and log in
        self.make_button(
            btn_frame,
            "Login",
            self.check_admin,
            self.colors["success"],
            fg="white"
        ).grid(row=0, column=0, padx=10)

        # I create a button to return the user to the main login screen
        self.make_button(
            btn_frame,
            "Back",
            self.login_screen,
            self.colors["danger"],
            fg="white"
        ).grid(row=0, column=1, padx=10)

    def check_admin(self):  # Validate admin password and control access to admin dashboard
        # I check whether the entered password matches the predefined admin credential
        if self.admin_pass.get() == "admin1234":

            # I grant access to the admin dashboard if the password is correct
            self.admin_dashboard()

        else:

            # I display an error message if the password is incorrect
            messagebox.showerror("Error", "Wrong password")

            # I return focus to the password entry field for immediate correction
            self.admin_pass.focus_set()

            # I visually mark the input as invalid to provide feedback to the user
            self.mark_invalid(self.admin_pass)

            return

    def member_login(self):  # Display the member login screen where user enters their name
        # I clear the current window to ensure a fresh and clean login interface
        self.clear()

        # I create a frame to structure and align the login prompt text neatly
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(pady=10)

        # I display the first part of the login prompt text
        tk.Label(
            frame,
            text="Enter ",
            font=("Arial", 12),
            bg=self.colors["bg"]
        ).pack(side="left")

        # I display the highlighted "Member Name" portion of the prompt
        tk.Label(
            frame,
            text="\'Member Name\'",
            font=("Arial", 12, "bold"),
            bg=self.colors["bg"]
        ).pack(side="left")

        # I complete the instruction prompt for the user
        tk.Label(
            frame,
            text=" to continue",
            font=("Arial", 12, "bold"),
            fg="darkgoldenrod",
            bg=self.colors["bg"]
        ).pack(side="left")

        # I create an input field for the user to enter their name
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        # I create a frame to hold the action buttons with proper spacing
        btn_frame = tk.Frame(self.root, bg=self.colors["bg"])
        btn_frame.pack(pady=15)

        # I create the "Enter" button to submit the member name and proceed
        self.make_button(
            btn_frame,
            "Enter",
            self.set_member,
            self.colors["success"],
            fg="white"
        ).grid(row=0, column=0, padx=10)

        # I create the "Back" button to return to the previous login screen
        self.make_button(
            btn_frame,
            "Back",
            self.login_screen,
            self.colors["danger"],
            fg="white"
        ).grid(row=0, column=1, padx=10)

    def set_member(self):
        # I validate the username input and prepare the user session for login

        # I check if the name field is empty or contains only whitespace
        if not self.name_entry.get().strip():
            # I display an error message when the input is invalid
            messagebox.showerror("Error", "Name cannot be empty")

            # I return focus to the input field for immediate correction
            self.name_entry.focus_set()

            # I visually mark the entry field as invalid for user feedback
            self.mark_invalid(self.name_entry)

            return

        # I store the validated username as the current active user
        self.current_user = self.name_entry.get()

        # I redirect the user to the member dashboard after successful login
        self.member_dashboard()

# =====================
# DASHBOARDS
# =====================
    def admin_dashboard(self):  # Define the layout and functionality of the Admin dashboard screen
        # I clear all existing widgets to reset the interface before loading the admin dashboard
        self.clear()

        # I create and display the main dashboard title to indicate admin access
        tk.Label(
            self.root,
            text="ADMIN DASHBOARD",
            font=("Arial", 14, "bold", "underline"),
            bg=self.colors["bg"],
            fg="darkgoldenrod"
        ).pack(pady=10)

        # I load and display the search and sort toolbar for managing book records
        self.search_sort_bar()

        # I build and display the main book table for data overview and management
        self.table()

        # I load and display admin-specific action buttons for managing the system
        self.buttons(admin=True)

    def member_dashboard(self):  # Define the layout and behaviour of the Member dashboard screen
        # I clear the current window to reset the interface before rendering the dashboard
        self.clear()

        # I display a personalised welcome message for the currently logged-in user
        tk.Label(
            self.root,
            text=f"Welcome {self.current_user}",
            font=("Arial", 14, "bold"),
            fg="darkgoldenrod",
            bg=self.colors["bg"]
        ).pack(pady=10)

        # I load and display the search and sort interface for members
        self.search_sort_bar()

        # I load and display the main book table for viewing available records
        self.table()

        # I load action buttons specific to member functionality such as borrow and return
        self.buttons(admin=False)

# =====================
# TABLE FUNCTIONS
# =====================
    def table(self):  # Define and configure the main table layout and appearance
        # I create a Style object to control the visual appearance of the Treeview widget
        style = ttk.Style()

        # I set the theme to "default" for consistent and predictable styling
        style.theme_use("default")

        # I configure the appearance of the Treeview body (data rows)
        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=28,
            background=self.colors["surface"]
        )

        # I configure the appearance of the Treeview headers (column titles)
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background=self.colors["primary"],
            foreground="white"
        )

        # I create the main container frame for the table section
        container = tk.Frame(self.root, bg=self.colors["bg"])
        container.pack(expand=True, fill="both")

        # I create a centered frame to align the table neatly in the UI
        center = tk.Frame(container, bg=self.colors["bg"])
        center.pack(expand=True)

        # I create the Treeview widget to display the tabular data
        self.tree = ttk.Treeview(
            center,
            selectmode="browse"
        )

        # I enable keyboard focus for the Treeview widget
        self.tree.configure(takefocus=True)

        # I bind a selection event placeholder for future enhancements
        self.tree.bind("<<TreeviewSelect>>", lambda e: None)

        # I define the table columns to match the dataset structure
        columns = ("BookID", "Title", "Author", "Year", "Genre", "Status", "Borrower")

        # I assign the columns to the Treeview widget
        self.tree["columns"] = columns

        # I hide the default empty column for a cleaner table layout
        self.tree["show"] = "headings"

        # I apply alternating row colours for better readability
        self.tree.tag_configure("even", background="gainsboro")
        self.tree.tag_configure("odd", background="white")

        # I create and configure each column header and alignment
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")

        # I create a vertical scrollbar for scrolling through rows
        scroll_y = ttk.Scrollbar(center, orient="vertical", command=self.tree.yview)

        # I create a horizontal scrollbar for wide tables
        scroll_x = ttk.Scrollbar(center, orient="horizontal", command=self.tree.xview)

        # I link the scrollbars to the Treeview scrolling behaviour
        self.tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        # I position the table and scrollbars using a grid layout
        self.tree.grid(row=0, column=0)
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # I configure grid expansion so the table resizes with the window
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(0, weight=1)

        # I load the initial dataset into the table on startup
        self.load_table()

    def load_table(self):
        # I store the currently selected book ID so I can restore selection after reloading
        selected_id = self.get_selected_book_id()

        # I clear all existing rows from the Treeview to refresh the display
        self.tree.delete(*self.tree.get_children())

        # I load the latest dataset from storage to ensure up-to-date display
        df = load_books()

        # I iterate through the dataset to insert each row into the table
        for i, (_, row) in enumerate(df.iterrows()):
            # I assign alternating row tags for improved readability
            tag = "even" if i % 2 == 0 else "odd"

            # I insert each record into the Treeview with its display styling
            self.tree.insert("", "end", values=list(row), tags=(tag,))

        # I restore the previously selected book to maintain user context
        self.reselect_book(selected_id)

    def reset_table_view(self, df):
        # I retrieve the currently selected book ID before refreshing the table
        selected_id = self.get_selected_book_id()

        # I clear all existing rows from the Treeview to prepare for fresh data
        self.tree.delete(*self.tree.get_children())

        # I iterate through the dataset row by row for display in the table
        for i, (_, row) in enumerate(df.iterrows()):
            # I apply alternating row tags to improve readability
            tag = "even" if i % 2 == 0 else "odd"

            # I insert each row into the Treeview with styling applied
            self.tree.insert("", "end", values=list(row), tags=(tag,))

        # I restore the previously selected book to maintain user context
        self.reselect_book(selected_id)

#=======================
# CRUD FUNCTIONS
#=======================

    def add_book(self):
        # I create a new top-level window for adding a book record
        win = tk.Toplevel(self.root)
        win.title("Add Book")
        win.configure(bg=self.colors["bg"])

        # I define the required fields for a complete book record
        fields = ["BookID", "Title", "Author", "Year", "Genre"]

        # I initialise a dictionary to store entry widgets for later retrieval
        entries = {}

        # I dynamically generate the input form based on the fields list
        for i, f in enumerate(fields):
            # I create a label for each input field
            tk.Label(
                win,
                text=f,
                bg=self.colors["bg"],
                fg=self.colors["muted"],
                font=("Arial", 10, "bold")
            ).grid(row=i, column=0, padx=10, pady=5, sticky="w")

            # I create an entry widget for user input
            e = tk.Entry(
                win,
                width=30,
                bg=self.colors["surface"],
                fg=self.colors["text"],
                insertbackground=self.colors["text"],
                relief="solid",
                bd=1
            )
            e.grid(row=i, column=1)

            # I store each entry widget using its field name as a key
            entries[f] = e

            # I enforce numeric-only input for the BookID field
            vcmd = win.register(lambda v: v.isdigit() or v == "")
            entries["BookID"].config(
                validate="key",
                validatecommand=(vcmd, "%P")
            )

        def save():
            """Validate input and safely add a new book to the dataset."""

            # I load the existing dataset before adding a new record
            df = load_books()

            # I collect and clean all user inputs
            data = {f: entries[f].get().strip() for f in entries}

            # I validate that no field is left empty
            for field, value in data.items():
                if value == "":
                    # I display an error and highlight the invalid field
                    messagebox.showerror("Error", f"{field} cannot be empty")
                    self.mark_invalid(entries[field], reset_bg=self.colors["surface"])
                    return

            # I validate BookID as a positive integer
            try:
                book_id = int(data["BookID"])
                if book_id <= 0:
                    raise ValueError
            except ValueError:

                # I notify the user of invalid BookID input
                messagebox.showerror("Error", "BookID must be a positive integer")
                self.mark_invalid(entries["BookID"], reset_bg=self.colors["surface"])
                return

            # I assign the validated BookID back into the dataset
            data["BookID"] = book_id

            # I check for duplicate BookID values
            if book_id in df["BookID"].values:
                # I prevent duplicate entries and alert the user
                messagebox.showerror("Error", "BookID already exists")
                self.mark_invalid(entries["BookID"], reset_bg=self.colors["surface"])
                return

            # I validate the Year field for correctness and range
            try:
                year = int(data["Year"])

                if year < 1400 or year > datetime.now().year:
                    messagebox.showerror("Error", "Invalid year")
                    self.mark_invalid(entries["Year"], reset_bg=self.colors["surface"])
                    return

                # I store the validated year back into the dataset
                data["Year"] = year

            except ValueError:

                # I handle non-numeric year input
                messagebox.showerror("Error", "Year must be numeric")
                self.mark_invalid(entries["Year"], reset_bg=self.colors["surface"])
                return

            # I set system-controlled default fields for new books
            data["Status"] = "Available"
            data["Borrower"] = ""

            # I append the new book record to the dataset
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

            # I save the updated dataset to storage
            save_books(df)

            # I refresh the table to reflect the new entry
            self.load_table()

            # I notify the user of successful addition
            messagebox.showinfo(
                "Success",
                f"'{data['Title']}' added successfully"
            )

            # I close the add-book window after successful completion
            win.destroy()

        # I create the save button and attach the save function
        self.make_button(
            win,
            "Save Book",
            save,
            self.colors["success"]
        ).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def borrow_book(self):
        """Allow a user to borrow a selected book."""

        # I retrieve the selected book ID using the centralised selection method
        book_id = self.get_selected_book_id()

        # I check whether a book has been selected before proceeding
        if not book_id:
            messagebox.showwarning("Warning", "Please select a book first")
            return

        # I load the latest dataset to ensure up-to-date operations
        df = load_books()

        # I print debug information to verify selection integrity
        print("Selected ID:", book_id)
        print("DF IDs:", df["BookID"].tolist())

        # I enforce the rule that a user can only borrow one book at a time
        if (df["Borrower"].fillna("") == self.current_user).any():
            messagebox.showwarning(
                "Warning",
                "Sorry, return your current book first to borrow another one."
            )
            return

        # I locate the selected book using the shared lookup function
        idx, book = find_book(df, book_id)

        # I handle cases where the book cannot be found in the dataset
        if idx is None:
            messagebox.showerror("Error", "Book not found")
            return

        # I prevent borrowing if the book is already marked as borrowed
        if book["Status"] == "Borrowed":
            messagebox.showerror("Error", "Book already borrowed")
            return

        # I request confirmation from the user before proceeding
        confirm = messagebox.askyesno(
            "Confirm Borrow",
            f"Proceed to borrow '{book['Title']}'?"
        )

        # I stop execution if the user cancels the action
        if not confirm:
            return

        # I update the book status to indicate it has been borrowed
        df.loc[idx, "Status"] = "Borrowed"

        # I assign the current user as the borrower of the book
        df.loc[idx, "Borrower"] = self.current_user

        # I save the updated dataset to persist changes
        save_books(df)

        # I refresh the table to reflect the updated status immediately
        self.load_table()

        # I display a success message confirming the borrowing action
        messagebox.showinfo(
            "Success",
            f"Nice one {self.current_user}, you have successfully borrowed '{book['Title']}'"
        )

    def return_book(self):
        # I load the latest dataset to ensure accurate return processing
        df = load_books()

        # I retrieve the selected book ID using the centralised selection method
        book_id = self.get_selected_book_id()

        # I check whether a book has been selected before proceeding
        if not book_id:
            messagebox.showwarning("Warning", "Please select a book first")
            return

        # I locate the selected book using the shared lookup function
        idx, book = find_book(df, book_id)

        # I handle cases where the book cannot be found in the dataset
        if idx is None:
            messagebox.showerror("Error", "Book not found")
            return

        # I verify that the current user is the borrower of the book
        if book["Borrower"] != self.current_user:
            messagebox.showerror("Error", "You did not borrow this book")
            return

        # I update the book status to indicate it has been returned
        df.loc[idx, "Status"] = "Available"

        # I clear the borrower field to remove user association
        df.loc[idx, "Borrower"] = ""

        # I save the updated dataset to persist the return action
        save_books(df)

        # I refresh the table to reflect the updated status immediately
        self.load_table()

        # I display a success message confirming the return action
        messagebox.showinfo(
            "Success",
            f"Thank you {self.current_user}, "
            f"you successfully returned '{book['Title']}'"
        )

    def remove_book(self):
        """Delete a selected book from the system."""

        # I retrieve the selected book ID using the centralised selection method
        book_id = self.get_selected_book_id()

        # I check whether a book has been selected before proceeding
        if not book_id:
            messagebox.showwarning("Alert", "Please select a book first")
            return

        # I load the latest dataset to ensure accurate and safe operations
        df = load_books()

        # I locate the selected book using the shared lookup function
        idx, book = find_book(df, book_id)

        # I handle cases where the book cannot be found in the dataset
        if idx is None:
            messagebox.showerror("Error", "Book not found")
            return

        # I prevent deletion of a borrowed book to maintain data integrity
        if book["Status"] == "Borrowed":
            messagebox.showerror(
                "Error",
                "Cannot delete a borrowed book. Return it first."
            )
            return

        # I extract the book title for clearer user confirmation messaging
        title = book["Title"]

        # I request confirmation from the user before deleting the record
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{title}'?"
        )

        # I stop execution if the user cancels the deletion
        if not confirm:
            return

        # I remove the selected book from the dataset using its BookID
        df = df[df["BookID"] != book_id]

        # I save the updated dataset to persist the deletion
        save_books(df)

        # I refresh the table to reflect the updated dataset immediately
        self.load_table()

        # I display a success message confirming successful deletion
        messagebox.showinfo(
            "Success",
            f"'{title}' removed successfully"
        )

    def update_book(self):
        """Handle updating details of a selected book."""

        # I load the latest dataset to ensure accurate and consistent updates
        df = load_books()

        # I retrieve the selected book ID using the centralised selection method
        book_id = self.get_selected_book_id()

        # I verify that a book has been selected before proceeding
        if not book_id:
            messagebox.showwarning("Alert", "Please select a book first")
            return

        # I locate the selected book using the shared lookup function
        idx, book = find_book(df, book_id)

        # I handle cases where the book cannot be found in the dataset
        if idx is None:
            messagebox.showerror("Error", "Book not found")
            return

        # I open a new window for editing book details
        win = tk.Toplevel(self.root)
        win.title("Update Book")

        # I define the list of editable fields only
        fields = ["Title", "Author", "Year", "Genre"]

        # I initialise a dictionary to store entry widgets
        entries = {}

        # I build the update form dynamically and pre-fill it with existing values
        for i, field in enumerate(fields):
            tk.Label(
                win, text=field, width=15, anchor="w"
            ).grid(row=i, column=0, padx=10, pady=5)

            # I create an entry field pre-filled with current book data
            e = tk.Entry(win, width=30)
            e.insert(0, str(book[field]))
            e.grid(row=i, column=1, padx=10, pady=5)

            # I store the entry widget for later retrieval
            entries[field] = e

        def save():
            try:
                """Save updated book details."""

                # I reload the dataset to ensure I work with the latest version
                df = load_books()

                # I collect and clean updated values from the form
                updated = {f: entries[f].get().strip() for f in entries}

                # I validate that no field is left empty
                for key, value in updated.items():
                    if value == "":
                        messagebox.showerror("Error", f"{key} cannot be empty")
                        self.mark_invalid(entries[key], reset_bg=self.colors["surface"])
                        return

                # I validate the Year field for correctness and valid range
                year = int(updated["Year"])
                if year < 1400 or year > datetime.now().year:
                    messagebox.showerror("Error", "Invalid year")
                    self.mark_invalid(entries["Year"], reset_bg=self.colors["surface"])
                    return

                # I store the validated year back into the dataset
                updated["Year"] = year

                # I locate the correct record using a boolean mask
                mask = df["BookID"] == book_id

                # I ensure the record exists before applying updates
                if not mask.any():
                    messagebox.showerror("Error", "Failed to update book (ID mismatch)")
                    return

                # I update only the allowed editable fields
                for field in updated:
                    df.loc[mask, field] = updated[field]

                # I save the updated dataset to persistent storage
                save_books(df)

                # I refresh the UI table to reflect changes immediately
                self.load_table()

                # I display a success message to confirm the update
                messagebox.showinfo("Success", f"{updated['Title']} updated successfully")

                # I close the update window after successful completion
                win.destroy()

            except Exception as e:

                # I handle unexpected errors to prevent application crashes
                messagebox.showerror("Debug Error", str(e))

        # I create the update button and attach it to the save function
        tk.Button(
            win,
            text="Update Book",
            command=save,
            bg=self.colors["accent"],
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6,
            bd=0,
            activebackground=self.colors["secondary"]
        ).grid(row=len(fields), column=0, columnspan=2, pady=10)

# =======================
# SEARCH and SORT FUNCTIONS
# =======================

    def search_books_gui(self):  # Handle searching based on user input
        # I load the latest dataset to ensure search results reflect current data
        df = load_books()

        # I retrieve the selected search field and the user-entered keyword
        field = self.search_field.get()
        keyword = self.search_entry.get().strip().lower()

        # I validate that the selected field exists in the dataset
        if not field or field not in df.columns:
            messagebox.showerror("Error", "Please select a valid search field")
            return

        # I check if the search keyword is empty and reset the table if it is
        if not keyword:
            self.search_entry.focus_set()
            self.reset_table_view(df)
            return

        # I perform a case-insensitive search on the selected column
        results = df[
            df[field].astype(str).str.contains(
                keyword, case=False, na=False, regex=False
            )
        ]

        # I handle the case where no matching results are found
        if results.empty:
            messagebox.showinfo("No Results", "No matching books found")
            self.reset_table_view(df)
        else:
            # I update the table to display only the filtered search results
            self.reset_table_view(results)

    def sort_books_gui(self):  # Sort books based on the user's selected options
        # Load the latest dataset so sorting reflects current data
        df = load_books()

        # Get sorting field and order from the UI
        field = self.sort_field.get()
        order = self.sort_order.get()

        # Convert order selection into boolean for pandas sorting
        ascending = True if order == "Ascending" else False

        # Ensure a valid sort field is selected
        if not field:
            messagebox.showerror("Error", "Please select a field to sort")
            return

        # Handle numeric-safe sorting for Year column
        if field == "Year":
            df["_YearSort"] = pd.to_numeric(df["Year"], errors="coerce")
            sorted_df = df.sort_values(by="_YearSort", ascending=ascending)
            sorted_df = sorted_df.drop(columns="_YearSort")
        else:
            # Perform standard sorting for non-numeric fields
            sorted_df = df.sort_values(by=field, ascending=ascending)

        # Update table view without saving changes to file
        self.reset_table_view(sorted_df)

    def search_sort_bar(self):
        # Create a container frame to group search and sort controls
        frame = tk.Frame(self.root, bg=self.colors["bg"])
        frame.pack(pady=5)

        # Define consistent styling for buttons
        btn_font = ("Arial", 8, "bold")
        btn_options = {"font": btn_font, "padx": 10, "pady": 5}

        # Define consistent styling for labels
        lbl_font = ("Arial", 8, "bold")
        lbl_options = {"font": lbl_font, "padx": 10, "pady": 5}

        # SEARCH SECTION

        # Label for search field selection
        tk.Label(frame, text="Search by:", **lbl_options).grid(row=0, column=0)

        # Dropdown for selecting search field
        self.search_field = ttk.Combobox(
            frame,
            values=["BookID", "Title", "Author", "Genre", "Year", "Status"],
            width=10
        )

        # Set default search field
        self.search_field.current(0)
        self.search_field.grid(row=0, column=1)

        # Input field for search keyword
        self.search_entry = tk.Entry(frame, width=20)
        self.search_entry.grid(row=0, column=2)

        # Live search trigger on typing
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_books_gui())

        # Search button for manual search
        tk.Button(
            frame,
            text="Search",
            command=self.search_books_gui,
            bg=self.colors["secondary"],
            **btn_options
        ).grid(row=0, column=3)

        # SORT SECTION

        # Label for sorting controls
        tk.Label(frame, text="Sort by:", **lbl_options).grid(row=0, column=4)

        # Dropdown for sort field selection
        self.sort_field = ttk.Combobox(
            frame,
            values=["BookID", "Title", "Author", "Year", "Genre", "Status"],
            width=10
        )

        # Set default sort field
        self.sort_field.current(0)
        self.sort_field.grid(row=0, column=5)

        # Dropdown for sort order selection
        self.sort_order = ttk.Combobox(
            frame,
            values=["Ascending", "Descending"],
            width=10
        )

        # Set default sort order
        self.sort_order.current(0)
        self.sort_order.grid(row=0, column=6)

        # Sort execution button
        tk.Button(
            frame,
            text="Sort",
            command=self.sort_books_gui,
            **btn_options
        ).grid(row=0, column=7)

        # Reset button to restore full dataset view
        tk.Button(
            frame,
            text="Reset",
            command=self.load_table,
            **btn_options
        ).grid(row=0, column=8)

# =========================
# RUN APP
# =========================
# Create the main Tkinter application window
root = tk.Tk()

# Initialize the LibraryApp with the main window
# This sets up the full GUI and application logic
app = LibraryApp(root)

# Start the Tkinter event loop to keep the application running
# This listens for all user interactions (clicks, typing, events)
root.mainloop()