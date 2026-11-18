import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import random
import csv
import time
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path


# ============================================================
# QUIZMASTER - CONFIGURATION
# ============================================================

APP_TITLE = "QuizMaster"
DB_FILE = Path(__file__).with_name("quizmaster.db")

BG = "#0B1220"
SIDEBAR = "#111C2F"
PANEL = "#162338"
PANEL_ALT = "#1C2D45"
TEXT = "#F4F7FB"
MUTED = "#9BAAC0"
ACCENT = "#6C8CFF"
TEAL = "#39C6B5"
GREEN = "#39C98A"
RED = "#F06B78"
YELLOW = "#F4BD5B"
BORDER = "#263A55"

FONT = "Segoe UI"


# ============================================================
# DATABASE
# ============================================================

@contextmanager
def database():
    """Open a database connection and always close it."""
    connection = sqlite3.connect(DB_FILE, timeout=10)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with database() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT DEFAULT ''
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                total_questions INTEGER NOT NULL,
                correct_answers INTEGER NOT NULL,
                percentage REAL NOT NULL,
                duration INTEGER NOT NULL,
                played_at TEXT NOT NULL
            )
        """)

        count = con.execute(
            "SELECT COUNT(*) FROM questions"
        ).fetchone()[0]

        if count == 0:
            seed_questions(con)


def seed_questions(con):
    """Insert the initial sample question bank."""

    questions = [
        # PYTHON
        # =====================================================
    # PYTHON - BEGINNER (10 QUESTIONS)
    # =====================================================

    ("Python", "Beginner",
     "Which keyword is used to define a function?",
     "function", "def", "fun", "define", "B",
     "The def keyword defines a function in Python."),

    ("Python", "Beginner",
     "Which symbol is used for single-line comments?",
     "//", "/*", "#", "--", "C",
     "The hash symbol is used for single-line comments."),

    ("Python", "Beginner",
     "Which data type stores True or False?",
     "int", "str", "bool", "float", "C",
     "The bool data type stores Boolean values."),

    ("Python", "Beginner",
     "Which function is used to display output?",
     "input()", "print()", "display()", "show()", "B",
     "The print() function displays output."),

    ("Python", "Beginner",
     "Which operator is used for exponentiation?",
     "*", "//", "**", "%", "C",
     "The double asterisk operator performs exponentiation."),

    ("Python", "Beginner",
     "Which brackets are used to create a list?",
     "()", "{}", "[]", "<>", "C",
     "Square brackets are used to create lists."),

    ("Python", "Beginner",
     "Which function accepts input from the user?",
     "scan()", "input()", "read()", "get()", "B",
     "The input() function accepts user input."),

    ("Python", "Beginner",
     "What is the index of the first element in a Python list?",
     "1", "-1", "0", "2", "C",
     "Python uses zero-based indexing."),

    ("Python", "Beginner",
     "Which keyword is used for decision-making?",
     "for", "if", "def", "return", "B",
     "The if keyword executes a block based on a condition."),

    ("Python", "Beginner",
     "Which function converts a value into an integer?",
     "str()", "float()", "int()", "bool()", "C",
     "The int() function converts a compatible value into an integer."),


    # =====================================================
    # PYTHON - INTERMEDIATE (10 QUESTIONS)
    # =====================================================

    ("Python", "Intermediate",
     "Which collection does not allow duplicate elements?",
     "List", "Tuple", "Set", "String", "C",
     "A set stores unique elements."),

    ("Python", "Intermediate",
     "What does len([10, 20, 30]) return?",
     "2", "3", "4", "30", "B",
     "The list contains three elements."),

    ("Python", "Intermediate",
     "Which keyword is used to handle exceptions?",
     "catch", "error", "except", "check", "C",
     "The except block handles exceptions raised inside a try block."),

    ("Python", "Intermediate",
     "Which method adds an element to the end of a list?",
     "add()", "append()", "insertEnd()", "push()", "B",
     "The append() method adds one element to the end of a list."),

    ("Python", "Intermediate",
     "What is the output of 10 // 3?",
     "3.33", "3", "1", "4", "B",
     "Floor division returns the quotient rounded down."),

    ("Python", "Intermediate",
     "Which keyword is used to create a class?",
     "object", "struct", "class", "define", "C",
     "The class keyword defines a class."),

    ("Python", "Intermediate",
     "Which method removes and returns the last list element by default?",
     "remove()", "delete()", "pop()", "clear()", "C",
     "pop() removes and returns the last element when no index is supplied."),

    ("Python", "Intermediate",
     "Which loop is generally used to iterate over a sequence?",
     "if", "for", "try", "class", "B",
     "A for loop iterates over the elements of an iterable."),

    ("Python", "Intermediate",
     "Which keyword is used to import a module?",
     "include", "using", "import", "module", "C",
     "The import keyword loads a module for use."),

    ("Python", "Intermediate",
     "What does the range(5) function generate?",
     "1 to 5", "0 to 4", "0 to 5", "1 to 4", "B",
     "range(5) generates values from 0 up to, but not including, 5."),


    # =====================================================
    # PYTHON - ADVANCED (10 QUESTIONS)
    # =====================================================

    ("Python", "Advanced",
     "Which module is commonly used for regular expressions?",
     "regex", "re", "pattern", "match", "B",
     "The re module provides regular expression operations."),

    ("Python", "Advanced",
     "What is the output of bool([])?",
     "True", "False", "None", "Error", "B",
     "An empty list is considered False in Boolean contexts."),

    ("Python", "Advanced",
     "Which method is used to create an iterator from an iterable?",
     "iter()", "next()", "range()", "loop()", "A",
     "iter() returns an iterator from an iterable object."),

    ("Python", "Advanced",
     "Which keyword is used to define an anonymous function?",
     "def", "lambda", "anonymous", "function", "B",
     "The lambda keyword creates a small anonymous function."),

    ("Python", "Advanced",
     "Which statement is used to generate a value from a generator?",
     "return", "yield", "break", "pass", "B",
     "The yield statement produces values from a generator."),

    ("Python", "Advanced",
     "Which module provides access to command-line arguments?",
     "math", "sys", "random", "time", "B",
     "The sys module provides access to sys.argv and other interpreter features."),

    ("Python", "Advanced",
     "Which keyword allows a function to modify a global variable?",
     "local", "static", "global", "extern", "C",
     "The global keyword allows assignment to a global variable."),

    ("Python", "Advanced",
     "Which file mode opens a file for appending?",
     "r", "w", "a", "x", "C",
     "The a mode opens a file for appending data."),

    ("Python", "Advanced",
     "What is the purpose of __init__() in a class?",
     "Delete an object", "Initialize an object",
     "Import a module", "Stop a program", "B",
     "__init__() initializes a newly created class instance."),

    ("Python", "Advanced",
     "Which data structure is commonly used to implement a LIFO system?",
     "Queue", "Stack", "Graph", "Tree", "B",
     "A stack follows Last In, First Out."),


        # C++
        # =====================================================
    # C++ - BEGINNER (10 QUESTIONS)
    # =====================================================

    ("C++", "Beginner",
     "Which symbol is used to terminate most C++ statements?",
     ":", ".", ";", ",", "C",
     "A semicolon terminates most C++ statements."),

    ("C++", "Beginner",
     "Which header is commonly used for cout and cin?",
     "<iostream>", "<stdio.h>", "<string>", "<math.h>", "A",
     "The iostream header provides standard input and output streams."),

    ("C++", "Beginner",
     "Which keyword declares an integer variable?",
     "number", "integer", "int", "var", "C",
     "The int keyword declares an integer variable."),

    ("C++", "Beginner",
     "Which operator is used for equality comparison?",
     "=", "==", "!=", "<>", "B",
     "The == operator checks whether two values are equal."),

    ("C++", "Beginner",
     "Which function is the usual entry point of a C++ program?",
     "start()", "main()", "run()", "begin()", "B",
     "The main() function is the usual entry point of a C++ program."),

    ("C++", "Beginner",
     "Which object is used to display output?",
     "cin", "cout", "cerrin", "input", "B",
     "cout is used for standard output."),

    ("C++", "Beginner",
     "Which data type stores a single character?",
     "string", "int", "char", "float", "C",
     "The char data type stores a character."),

    ("C++", "Beginner",
     "Which operator is used to obtain the remainder?",
     "/", "*", "%", "//", "C",
     "The modulus operator % returns the remainder of integer division."),

    ("C++", "Beginner",
     "Which keyword is used to make a decision?",
     "if", "loop", "define", "caseonly", "A",
     "The if keyword executes code based on a condition."),

    ("C++", "Beginner",
     "Which loop checks its condition before each iteration?",
     "do-while", "while", "switch", "case", "B",
     "A while loop checks its condition before executing its body."),


    # =====================================================
    # C++ - INTERMEDIATE (10 QUESTIONS)
    # =====================================================

    ("C++", "Intermediate",
     "Which concept allows multiple functions with the same name but different parameters?",
     "Inheritance", "Function overloading",
     "Encapsulation", "Abstraction", "B",
     "Function overloading uses the same function name with different parameter lists."),

    ("C++", "Intermediate",
     "Which operator accesses a member through an object?",
     "->", ".", "::", "&", "B",
     "The dot operator accesses members through an object."),

    ("C++", "Intermediate",
     "Which keyword is used to create a class?",
     "object", "class", "structonly", "define", "B",
     "The class keyword declares a class."),

    ("C++", "Intermediate",
     "Which access specifier allows access from anywhere the object is accessible?",
     "private", "protected", "public", "internal", "C",
     "Public members can be accessed from outside the class through an accessible object."),

    ("C++", "Intermediate",
     "Which operator is used to allocate memory dynamically?",
     "malloc only", "new", "create", "alloc", "B",
     "The new operator dynamically allocates memory and constructs an object."),

    ("C++", "Intermediate",
     "Which loop executes its body at least once?",
     "for", "while", "do-while", "nested for", "C",
     "A do-while loop evaluates its condition after the body executes."),

    ("C++", "Intermediate",
     "Which concept combines data and functions into a single unit?",
     "Inheritance", "Encapsulation", "Polymorphism", "Recursion", "B",
     "Encapsulation bundles data and the functions that operate on it."),

    ("C++", "Intermediate",
     "Which keyword is used to inherit a base class?",
     "extends", "inherits", "public", "super", "C",
     "In C++, a derived class specifies inheritance using an access specifier such as public."),

    ("C++", "Intermediate",
     "Which function is automatically called when an object is created?",
     "Destructor", "Constructor", "Main", "Friend", "B",
     "A constructor initializes an object when it is created."),

    ("C++", "Intermediate",
     "Which container follows First In, First Out?",
     "Stack", "Queue", "Set", "Map", "B",
     "A queue follows the First In, First Out principle."),


    # =====================================================
    # C++ - ADVANCED (10 QUESTIONS)
    # =====================================================

    ("C++", "Advanced",
     "Which feature supports runtime polymorphism in C++?",
     "Templates", "Virtual functions", "Macros", "Namespaces", "B",
     "Virtual functions enable dynamic dispatch through base-class interfaces."),

    ("C++", "Advanced",
     "Which keyword prevents a virtual function from being overridden further?",
     "static", "const", "final", "friend", "C",
     "The final specifier prevents further overriding of a virtual function."),

    ("C++", "Advanced",
     "Which pointer represents the current object inside a non-static member function?",
     "self", "this", "current", "object", "B",
     "The this pointer points to the current object."),

    ("C++", "Advanced",
     "Which feature allows a class to use another class's private members through a declaration?",
     "Virtual", "Friend class", "Static class", "Abstract class", "B",
     "A friend class can access the private and protected members of the class that declares it as a friend."),

    ("C++", "Advanced",
     "Which header provides the std::unique_ptr smart pointer?",
     "<memory>", "<pointer>", "<stdlib.h>", "<utility>", "A",
     "The memory header provides unique_ptr and other smart-pointer facilities."),

    ("C++", "Advanced",
     "Which principle describes releasing resources when an object leaves scope?",
     "FIFO", "RAII", "LIFO sorting", "Overloading", "B",
     "RAII ties resource lifetime to object lifetime."),

    ("C++", "Advanced",
     "Which cast is primarily used for checked conversions within an inheritance hierarchy?",
     "reinterpret_cast", "static_cast",
     "dynamic_cast", "const_cast", "C",
     "dynamic_cast performs runtime-checked conversions for polymorphic class hierarchies."),

    ("C++", "Advanced",
     "Which function is called when an object is destroyed?",
     "Constructor", "Destructor", "Operator", "Friend function", "B",
     "A destructor performs cleanup when an object is destroyed."),

    ("C++", "Advanced",
     "Which template feature allows a function to work with different data types?",
     "Function template", "Virtual function",
     "Friend function", "Inline variable", "A",
     "A function template defines a family of functions for different types."),

    ("C++", "Advanced",
     "Which standard container provides average constant-time key lookup?",
     "vector", "list", "unordered_map", "deque", "C",
     "unordered_map provides average constant-time lookup using hashing."),

        # JAVA
        # =====================================================
    # JAVA - BEGINNER (10 QUESTIONS)
    # =====================================================

    ("Java", "Beginner",
     "Which keyword is used to create an object?",
     "class", "new", "this", "object", "B",
     "The new keyword creates an object in Java."),

    ("Java", "Beginner",
     "Which method is the standard entry point of a Java application?",
     "start()", "run()", "main()", "init()", "C",
     "The main method is the standard entry point of a Java application."),

    ("Java", "Beginner",
     "Which symbol is used to terminate most Java statements?",
     ":", ";", ".", ",", "B",
     "A semicolon terminates most Java statements."),

    ("Java", "Beginner",
     "Which primitive data type stores whole numbers?",
     "float", "char", "int", "boolean", "C",
     "The int primitive type stores integer values."),

    ("Java", "Beginner",
     "Which keyword is used to declare a class?",
     "object", "class", "define", "struct", "B",
     "The class keyword declares a Java class."),

    ("Java", "Beginner",
     "Which operator is used for logical AND?",
     "&", "&&", "||", "!", "B",
     "The && operator performs conditional logical AND."),

    ("Java", "Beginner",
     "Which package contains the Scanner class?",
     "java.io", "java.util", "java.net", "java.lang", "B",
     "Scanner is available in the java.util package."),

    ("Java", "Beginner",
     "Which keyword is used to create a constant variable?",
     "static", "final", "const", "fixed", "B",
     "The final keyword prevents reassignment of a variable."),

    ("Java", "Beginner",
     "Which statement is used to display output?",
     "System.out.println()", "Console.read()",
     "System.input()", "print.output()", "A",
     "System.out.println() displays output and moves to a new line."),

    ("Java", "Beginner",
     "Which data type stores true or false?",
     "int", "char", "boolean", "double", "C",
     "The boolean primitive type stores true or false."),


    # =====================================================
    # JAVA - INTERMEDIATE (10 QUESTIONS)
    # =====================================================

    ("Java", "Intermediate",
     "Which keyword is used for class inheritance?",
     "implements", "extends", "inherits", "superclass", "B",
     "The extends keyword establishes class inheritance."),

    ("Java", "Intermediate",
     "Which collection does not allow duplicate elements?",
     "ArrayList", "LinkedList", "HashSet", "Vector", "C",
     "HashSet stores unique elements."),

    ("Java", "Intermediate",
     "Which block handles exceptions?",
     "check", "catch", "error", "handle", "B",
     "A catch block handles exceptions from a corresponding try block."),

    ("Java", "Intermediate",
     "Which keyword refers to the current object?",
     "super", "this", "self", "current", "B",
     "The this keyword refers to the current object."),

    ("Java", "Intermediate",
     "Which keyword is used to implement an interface?",
     "extends", "implements", "interface", "inherits", "B",
     "A class uses implements to implement an interface."),

    ("Java", "Intermediate",
     "Which method returns the number of characters in a String?",
     "size()", "length()", "count()", "getLength()", "B",
     "The String length() method returns the number of characters."),

    ("Java", "Intermediate",
     "Which collection maintains insertion order and allows duplicates?",
     "HashSet", "ArrayList", "TreeSet", "HashMap", "B",
     "ArrayList maintains element order and allows duplicate elements."),

    ("Java", "Intermediate",
     "Which keyword prevents a method from being overridden?",
     "static", "final", "privateonly", "abstract", "B",
     "A final method cannot be overridden in a subclass."),

    ("Java", "Intermediate",
     "Which keyword is used to call a superclass constructor?",
     "this", "parent", "super", "base", "C",
     "The super keyword can invoke a superclass constructor."),

    ("Java", "Intermediate",
     "Which loop is useful when the number of iterations is known?",
     "if", "for", "switch", "try", "B",
     "A for loop is commonly used when the iteration count is known."),


    # =====================================================
    # JAVA - ADVANCED (10 QUESTIONS)
    # =====================================================

    ("Java", "Advanced",
     "Which component executes Java bytecode?",
     "JDK", "JRE", "JVM", "JAR", "C",
     "The Java Virtual Machine executes Java bytecode."),

    ("Java", "Advanced",
     "Which keyword makes a method belong to the class rather than an instance?",
     "final", "static", "private", "abstract", "B",
     "A static method belongs to the class rather than an individual instance."),

    ("Java", "Advanced",
     "Which interface is commonly used to define a task for a thread?",
     "Runnable", "Serializable", "Comparable", "Cloneable", "A",
     "Runnable defines a task that can be executed by a thread."),

    ("Java", "Advanced",
     "Which collection provides average constant-time lookup by key?",
     "ArrayList", "LinkedList", "HashMap", "TreeSet", "C",
     "HashMap provides average constant-time key lookup under normal hashing conditions."),

    ("Java", "Advanced",
     "Which keyword is used to create an abstract class?",
     "virtual", "abstract", "interface", "static", "B",
     "The abstract keyword declares an abstract class or method."),

    ("Java", "Advanced",
     "Which keyword is used to prevent a class from being inherited?",
     "static", "const", "final", "private", "C",
     "A final class cannot be subclassed."),

    ("Java", "Advanced",
     "Which method is called to begin a new Thread's execution?",
     "run()", "execute()", "start()", "begin()", "C",
     "start() starts a new thread, which then invokes its run() method."),

    ("Java", "Advanced",
     "Which interface is used to define natural ordering of objects?",
     "Comparator", "Comparable", "Serializable", "Runnable", "B",
     "Comparable defines natural ordering through compareTo()."),

    ("Java", "Advanced",
     "Which keyword is used to explicitly throw an exception?",
     "throws", "throw", "try", "catch", "B",
     "The throw keyword explicitly throws an exception object."),

    ("Java", "Advanced",
     "Which memory area stores objects created at runtime?",
     "Stack", "Heap", "Method parameter", "CPU register", "B",
     "Objects and arrays are allocated in the JVM heap.")
    ]

    con.executemany("""
        INSERT INTO questions (
            category, difficulty, question,
            option_a, option_b, option_c, option_d,
            correct_answer, explanation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, questions)


# ============================================================
# MAIN APPLICATION
# ============================================================

class QuizMaster:

    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1200x760")
        self.root.minsize(1000, 650)
        self.root.configure(bg=BG)

        self.timer_job = None
        self.quiz_active = False
        self.questions = []
        self.current_index = 0
        self.answers = {}
        self.remaining_seconds = 0
        self.seconds_per_question = 30
        self.quiz_start_time = 0
        self.player_name = ""
        self.category = ""
        self.difficulty = ""
        self.last_result_id = None
        self.last_duration = 0
        self.last_correct = 0
        self.last_percentage = 0

        self.setup_style()
        self.build_layout()
        self.show_dashboard()

    # --------------------------------------------------------
    # GENERAL UI
    # --------------------------------------------------------

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=TEXT,
            fieldbackground=PANEL,
            rowheight=30,
            font=(FONT, 10)
        )

        style.configure(
            "Treeview.Heading",
            background=SIDEBAR,
            foreground=TEXT,
            font=(FONT, 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", "white")]
        )

        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=PANEL_ALT,
            background=TEAL,
            bordercolor=PANEL_ALT,
            lightcolor=TEAL,
            darkcolor=TEAL
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(self.root, bg=BG)
        self.main_area.pack(side="right", fill="both", expand=True)

        tk.Label(
            self.sidebar,
            text="QUIZMASTER",
            bg=SIDEBAR,
            fg=TEXT,
            font=(FONT, 20, "bold")
        ).pack(pady=(30, 5))

        tk.Label(
            self.sidebar,
            text="LEARN • PRACTICE • IMPROVE",
            bg=SIDEBAR,
            fg=MUTED,
            font=(FONT, 8, "bold")
        ).pack(pady=(0, 35))

        self.nav_button("Dashboard", self.show_dashboard)
        self.nav_button("Start Quiz", self.show_quiz_setup)
        self.nav_button("Question Bank", self.show_question_bank)
        self.nav_button("Quiz History", self.show_history)

        tk.Frame(self.sidebar, bg=BORDER, height=1).pack(
            fill="x", padx=20, pady=25
        )

        tk.Label(
            self.sidebar,
            text="Python Desktop Project",
            bg=SIDEBAR,
            fg=MUTED,
            font=(FONT, 9)
        ).pack(side="bottom", pady=20)

        self.content = tk.Frame(self.main_area, bg=BG)
        self.content.pack(fill="both", expand=True, padx=30, pady=25)

    def nav_button(self, text, command):
        button = tk.Button(
            self.sidebar,
            text="   " + text,
            command=command,
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=PANEL_ALT,
            activeforeground=TEXT,
            relief="flat",
            anchor="w",
            padx=20,
            pady=13,
            font=(FONT, 11),
            cursor="hand2"
        )
        button.pack(fill="x", padx=12, pady=3)

    def clear_content(self):
        self.cancel_timer()

        for widget in self.content.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle=""):
        tk.Label(
            self.content,
            text=title,
            bg=BG,
            fg=TEXT,
            font=(FONT, 25, "bold")
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                self.content,
                text=subtitle,
                bg=BG,
                fg=MUTED,
                font=(FONT, 10)
            ).pack(anchor="w", pady=(5, 20))

    def card(self, parent, title, value, color=ACCENT):
        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        tk.Label(
            frame,
            text=title.upper(),
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 9, "bold")
        ).pack(anchor="w", padx=18, pady=(17, 6))

        tk.Label(
            frame,
            text=value,
            bg=PANEL,
            fg=color,
            font=(FONT, 25, "bold")
        ).pack(anchor="w", padx=18, pady=(0, 17))

        return frame

    def make_button(self, parent, text, command,
                    color=ACCENT, width=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            font=(FONT, 10, "bold"),
            padx=18,
            pady=10,
            width=width,
            cursor="hand2"
        )

    def make_label(self, parent, text, size=10, color=TEXT,
                   bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=(FONT, size, "bold" if bold else "normal")
        )

    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    def show_dashboard(self):
        self.quiz_active = False
        self.clear_content()
        self.heading(
            "Dashboard",
            "Welcome to QuizMaster. Track your learning progress."
        )

        with database() as con:
            total_quizzes = con.execute(
                "SELECT COUNT(*) FROM results"
            ).fetchone()[0]

            average = con.execute(
                "SELECT AVG(percentage) FROM results"
            ).fetchone()[0] or 0

            best = con.execute(
                "SELECT MAX(percentage) FROM results"
            ).fetchone()[0] or 0

            question_count = con.execute(
                "SELECT COUNT(*) FROM questions"
            ).fetchone()[0]

            recent = con.execute("""
                SELECT player_name, category, percentage, played_at
                FROM results
                ORDER BY id DESC
                LIMIT 5
            """).fetchall()

        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=10)

        values = [
            ("Quizzes Completed", str(total_quizzes), ACCENT),
            ("Average Score", f"{average:.1f}%", TEAL),
            ("Personal Best", f"{best:.1f}%", GREEN),
            ("Question Bank", str(question_count), YELLOW)
        ]

        for index, (title, value, color) in enumerate(values):
            item = self.card(stats, title, value, color)
            item.grid(
                row=0, column=index, sticky="nsew",
                padx=6, pady=5
            )
            stats.grid_columnconfigure(index, weight=1)

        section = tk.Frame(self.content, bg=BG)
        section.pack(fill="both", expand=True, pady=(25, 0))

        tk.Label(
            section,
            text="Recent Activity",
            bg=BG,
            fg=TEXT,
            font=(FONT, 16, "bold")
        ).pack(anchor="w", pady=(0, 12))

        columns = ("player", "category", "score", "date")
        tree = ttk.Treeview(
            section, columns=columns, show="headings", height=7
        )

        for col, label in zip(
            columns,
            ("Player", "Category", "Score", "Date")
        ):
            tree.heading(col, text=label)
            tree.column(col, width=150)

        tree.pack(fill="x")

        for row in recent:
            tree.insert("", "end", values=(
                row["player_name"],
                row["category"],
                f'{row["percentage"]:.1f}%',
                row["played_at"]
            ))

        self.make_button(
            self.content,
            "Start a New Quiz",
            self.show_quiz_setup,
            color=ACCENT
        ).pack(anchor="w", pady=20)

    # --------------------------------------------------------
    # QUIZ SETUP
    # --------------------------------------------------------

    def show_quiz_setup(self):
        self.quiz_active = False
        self.clear_content()
        self.heading(
            "Start a Quiz",
            "Choose your quiz preferences before starting."
        )

        panel = tk.Frame(
            self.content,
            bg=PANEL,
            padx=30,
            pady=25,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        panel.pack(anchor="nw", fill="x", padx=5)

        self.player_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Python")
        self.difficulty_var = tk.StringVar(value="All Levels")
        self.count_var = tk.StringVar(value="10")
        self.timer_var = tk.StringVar(value="30")

        self.form_field(panel, "Player Name", self.player_var, "Your name")
        self.form_dropdown(
            panel, "Category", self.category_var,
            ["Python", "C++", "Java"]
        )
        self.form_dropdown(
            panel, "Difficulty", self.difficulty_var,
            ["All Levels", "Beginner", "Intermediate", "Advanced"]
        )

        self.count_combo = self.form_dropdown(
            panel,
            "Number of Questions",
            self.count_var,
            ["5", "10", "15", "20", "All Questions"]
        )

        # Update the question-count choices whenever difficulty changes.
        self.difficulty_var.trace_add(
            "write", self.update_question_count_options
        )

        self.form_dropdown(
                    panel, "Seconds per Question", self.timer_var,
                    ["15", "30", "45", "60"]
                )

        
        self.make_button(
            panel, "Start Quiz", self.start_quiz, color=TEAL
        ).pack(anchor="w", pady=(20, 0))

    def form_field(self, parent, label, variable, placeholder=""):
        tk.Label(
            parent,
            text=label,
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor="w", pady=(12, 5))

        entry = tk.Entry(
            parent,
            textvariable=variable,
            bg=PANEL_ALT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=(FONT, 11),
            width=42
        )
        entry.pack(anchor="w", ipady=9, ipadx=8)

    def form_dropdown(self, parent, label, variable, options):
        tk.Label(
            parent,
            text=label,
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 10, "bold")
        ).pack(anchor="w", pady=(12, 5))

        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=options,
            state="readonly",
            width=39,
            font=(FONT, 10)
        )
        combo.pack(anchor="w", ipady=5)
        return combo

    def start_quiz(self):
        name = self.player_var.get().strip()

        if not name:
            messagebox.showwarning(
                "Player Name Required",
                "Please enter your name before starting."
            )
            return

        category = self.category_var.get()
        difficulty = self.difficulty_var.get()

#        with database() as con:
#            rows = con.execute("""
#                SELECT * FROM questions
#                WHERE category = ? AND difficulty = ?
#            """, (category, difficulty)).fetchall()
        if difficulty == "All Levels":
            with database() as con:
                rows = con.execute("""
                    SELECT * FROM questions
                    WHERE category = ?
                """, (category,)).fetchall()
        else:
            with database() as con:
                rows = con.execute("""
                    SELECT * FROM questions
                    WHERE category = ? AND difficulty = ?
                """, (category, difficulty)).fetchall()
        if not rows:
            messagebox.showinfo(
                "No Questions",
                "There are no questions for this selection. "
                "Add questions in the Question Bank."
            )
            return

        self.questions = [dict(row) for row in rows]
        random.shuffle(self.questions)

        selected_count = self.count_var.get()
        if selected_count != "All Questions":
            requested_count = int(selected_count)
            self.questions = self.questions[:requested_count]

        self.player_name = name
        self.category = category
        self.difficulty = difficulty
        self.seconds_per_question = int(self.timer_var.get())

        self.current_index = 0
        self.answers = {}
        self.quiz_active = True
        self.quiz_start_time = time.time()

        self.show_question()

    # --------------------------------------------------------
    # QUIZ SCREEN AND TIMER
    # --------------------------------------------------------

    def show_question(self):
        self.clear_content()

        if not self.quiz_active:
            return

        question = self.questions[self.current_index]

        self.remaining_seconds = self.seconds_per_question
        self.selected_answer = tk.StringVar(
            value=self.answers.get(question["id"], "")
        )

        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x")

        tk.Label(
            top,
            text=f"Question {self.current_index + 1} "
                 f"of {len(self.questions)}",
            bg=BG,
            fg=TEXT,
            font=(FONT, 17, "bold")
        ).pack(side="left")

        self.timer_label = tk.Label(
            top,
            text="",
            bg=BG,
            fg=YELLOW,
            font=(FONT, 15, "bold")
        )
        self.timer_label.pack(side="right")

        progress = ttk.Progressbar(
            self.content,
            maximum=len(self.questions),
            value=self.current_index,
            style="Horizontal.TProgressbar"
        )
        progress.pack(fill="x", pady=18)

        panel = tk.Frame(
            self.content,
            bg=PANEL,
            padx=28,
            pady=30,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        panel.pack(fill="both", expand=True)

        tk.Label(
            panel,
            text=f'{question["category"]}  •  {question["difficulty"]}',
            bg=PANEL,
            fg=TEAL,
            font=(FONT, 10, "bold")
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(
            panel,
            text=question["question"],
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 17, "bold"),
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=(0, 25))

        options = [
            ("A", question["option_a"]),
            ("B", question["option_b"]),
            ("C", question["option_c"]),
            ("D", question["option_d"])
        ]

        for key, option in options:
            radio = tk.Radiobutton(
                panel,
                text=f"{key}.  {option}",
                variable=self.selected_answer,
                value=key,
                bg=PANEL,
                fg=TEXT,
                selectcolor=PANEL_ALT,
                activebackground=PANEL,
                activeforeground=TEXT,
                font=(FONT, 12),
                anchor="w",
                padx=10,
                pady=10,
                cursor="hand2"
            )
            radio.pack(fill="x", anchor="w")

        bottom = tk.Frame(self.content, bg=BG)
        bottom.pack(fill="x", pady=18)

        self.make_button(
            bottom, "Exit Quiz", self.confirm_exit, color=RED
        ).pack(side="left")

        button_text = (
            "Finish Quiz" if self.current_index == len(self.questions) - 1
            else "Next Question"
        )

        self.make_button(
            bottom, button_text, self.next_question, color=TEAL
        ).pack(side="right")

        self.update_timer()
        
    def update_question_count_options(self, *args):
        difficulty = self.difficulty_var.get()

        if difficulty == "All Levels":
            options = ["5", "10", "15", "20", "All Questions"]
        else:
            options = ["5", "10"]

        self.count_combo["values"] = options

        if self.count_var.get() not in options:
            self.count_var.set("10")

    def update_timer(self):
        if not self.quiz_active:
            return

        self.timer_label.config(
            text=f"Time Left: {self.remaining_seconds}s",
            fg=RED if self.remaining_seconds <= 5 else YELLOW
        )

        if self.remaining_seconds <= 0:
            self.answers[
                self.questions[self.current_index]["id"]
            ] = self.selected_answer.get()

            messagebox.showinfo(
                "Time Up",
                "Your time for this question has ended."
            )
            self.next_question()
            return

        self.remaining_seconds -= 1
        self.timer_job = self.root.after(1000, self.update_timer)

    def cancel_timer(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    def next_question(self):
        if not self.quiz_active:
            return

        self.cancel_timer()

        question = self.questions[self.current_index]
        self.answers[question["id"]] = self.selected_answer.get()

        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.show_question()
        else:
            self.finish_quiz()

    def confirm_exit(self):
        if messagebox.askyesno(
            "Exit Quiz",
            "Are you sure you want to leave? "
            "Your current quiz progress will not be saved."
        ):
            self.quiz_active = False
            self.cancel_timer()
            self.show_dashboard()

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    def finish_quiz(self):
        self.cancel_timer()
        self.quiz_active = False

        correct = 0

        for question in self.questions:
            if self.answers.get(question["id"]) == question["correct_answer"]:
                correct += 1

        total = len(self.questions)
        percentage = (correct / total) * 100 if total else 0
        duration = int(time.time() - self.quiz_start_time)

        self.last_correct = correct
        self.last_percentage = percentage
        self.last_duration = duration

        with database() as con:
            cursor = con.execute("""
                INSERT INTO results (
                    player_name, category, difficulty,
                    total_questions, correct_answers,
                    percentage, duration, played_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.player_name,
                self.category,
                self.difficulty,
                total,
                correct,
                percentage,
                duration,
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ))

            self.last_result_id = cursor.lastrowid

        self.show_results()

    def show_results(self):
        self.clear_content()

        self.heading(
            "Quiz Completed",
            f"Well done, {self.player_name}! Here is your performance."
        )

        panel = tk.Frame(
            self.content,
            bg=PANEL,
            padx=35,
            pady=30,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        panel.pack(fill="x", padx=5, pady=10)

        tk.Label(
            panel,
            text=f"{self.last_percentage:.1f}%",
            bg=PANEL,
            fg=TEAL if self.last_percentage >= 60 else YELLOW,
            font=(FONT, 42, "bold")
        ).pack(pady=(5, 8))

        tk.Label(
            panel,
            text="YOUR SCORE",
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 10, "bold")
        ).pack()

        tk.Label(
            panel,
            text=f"{self.last_correct} correct out of "
                 f"{len(self.questions)} questions",
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 15)
        ).pack(pady=15)

        if self.last_percentage >= 80:
            feedback = "Excellent work! You have performed very well."
        elif self.last_percentage >= 60:
            feedback = "Good effort! Keep practising to improve."
        elif self.last_percentage >= 40:
            feedback = "You're making progress. Review the answers and try again."
        else:
            feedback = "Keep learning. Every attempt is a chance to improve."

        tk.Label(
            panel,
            text=feedback,
            bg=PANEL,
            fg=MUTED,
            font=(FONT, 11),
            wraplength=700
        ).pack(pady=(0, 20))

        details = tk.Frame(panel, bg=PANEL)
        details.pack()

        for label, value in [
            ("Category", self.category),
            ("Difficulty", self.difficulty),
            ("Time Taken", f"{self.last_duration} seconds")
        ]:
            item = tk.Frame(details, bg=PANEL)
            item.pack(side="left", padx=25)

            tk.Label(
                item, text=label.upper(), bg=PANEL,
                fg=MUTED, font=(FONT, 8, "bold")
            ).pack()

            tk.Label(
                item, text=value, bg=PANEL,
                fg=TEXT, font=(FONT, 11, "bold")
            ).pack(pady=5)

        actions = tk.Frame(self.content, bg=BG)
        actions.pack(anchor="w", pady=20)

        self.make_button(
            actions, "Review Answers", self.show_review, color=ACCENT
        ).pack(side="left", padx=(0, 10))

        self.make_button(
            actions, "Play Again", self.show_quiz_setup, color=TEAL
        ).pack(side="left", padx=10)

        self.make_button(
            actions, "Dashboard", self.show_dashboard, color=PANEL_ALT
        ).pack(side="left", padx=10)

    # --------------------------------------------------------
    # ANSWER REVIEW
    # --------------------------------------------------------

    def show_review(self):
        self.clear_content()
        self.heading(
            "Answer Review",
            "Review your selected answers and understand the correct ones."
        )

        canvas = tk.Canvas(
            self.content,
            bg=BG,
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            self.content, orient="vertical", command=canvas.yview
        )
        inner = tk.Frame(canvas, bg=BG)

        inner.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for index, question in enumerate(self.questions, start=1):
            selected = self.answers.get(question["id"], "")
            correct = question["correct_answer"]
            is_correct = selected == correct

            panel = tk.Frame(
                inner,
                bg=PANEL,
                padx=20,
                pady=18,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            panel.pack(fill="x", pady=7, padx=5)

            tk.Label(
                panel,
                text=f"Question {index}: {question['question']}",
                bg=PANEL,
                fg=TEXT,
                font=(FONT, 11, "bold"),
                wraplength=760,
                justify="left"
            ).pack(anchor="w", pady=(0, 10))

            tk.Label(
                panel,
                text=f"Your answer: {selected or 'Not answered'}",
                bg=PANEL,
                fg=GREEN if is_correct else RED,
                font=(FONT, 10)
            ).pack(anchor="w", pady=3)

            tk.Label(
                panel,
                text=f"Correct answer: {correct}",
                bg=PANEL,
                fg=TEAL,
                font=(FONT, 10, "bold")
            ).pack(anchor="w", pady=3)

            if question["explanation"]:
                tk.Label(
                    panel,
                    text=f"Explanation: {question['explanation']}",
                    bg=PANEL,
                    fg=MUTED,
                    font=(FONT, 9),
                    wraplength=760,
                    justify="left"
                ).pack(anchor="w", pady=(7, 0))

        self.make_button(
            self.content, "Back to Results", self.show_results
        ).pack(anchor="w", pady=10)

    # --------------------------------------------------------
    # QUIZ HISTORY
    # --------------------------------------------------------

    def show_history(self):
        self.quiz_active = False
        self.clear_content()
        self.heading(
            "Quiz History",
            "View previous attempts and export your results."
        )

        columns = (
            "id", "player", "category", "difficulty",
            "total", "correct", "percentage", "duration", "date"
        )

        tree = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=15
        )

        headings = [
            ("id", "ID", 45),
            ("player", "Player", 110),
            ("category", "Category", 90),
            ("difficulty", "Difficulty", 100),
            ("total", "Questions", 80),
            ("correct", "Correct", 70),
            ("percentage", "Score", 80),
            ("duration", "Duration", 85),
            ("date", "Played At", 145)
        ]

        for key, label, width in headings:
            tree.heading(key, text=label)
            tree.column(key, width=width, anchor="center")

        tree.pack(fill="both", expand=True, pady=10)

        with database() as con:
            rows = con.execute("""
                SELECT * FROM results ORDER BY id DESC
            """).fetchall()

        for row in rows:
            tree.insert("", "end", values=(
                row["id"],
                row["player_name"],
                row["category"],
                row["difficulty"],
                row["total_questions"],
                row["correct_answers"],
                f'{row["percentage"]:.1f}%',
                f'{row["duration"]} sec',
                row["played_at"]
            ))

        actions = tk.Frame(self.content, bg=BG)
        actions.pack(anchor="w", pady=12)

        self.make_button(
            actions, "Export History to CSV",
            self.export_history, color=TEAL
        ).pack(side="left", padx=(0, 10))

        self.make_button(
            actions, "Refresh",
            self.show_history, color=PANEL_ALT
        ).pack(side="left")

    def export_history(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="quizmaster_history.csv"
        )

        if not path:
            return

        with database() as con:
            rows = con.execute("""
                SELECT * FROM results ORDER BY id DESC
            """).fetchall()

        headers = [
            "ID", "Player", "Category", "Difficulty",
            "Total Questions", "Correct Answers",
            "Percentage", "Duration", "Played At"
        ]

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(headers)

                for row in rows:
                    writer.writerow([
                        row["id"],
                        row["player_name"],
                        row["category"],
                        row["difficulty"],
                        row["total_questions"],
                        row["correct_answers"],
                        row["percentage"],
                        row["duration"],
                        row["played_at"]
                    ])

            messagebox.showinfo(
                "Export Successful",
                "Quiz history has been exported successfully."
            )

        except OSError as error:
            messagebox.showerror("Export Error", str(error))

    # --------------------------------------------------------
    # QUESTION BANK
    # --------------------------------------------------------

    def show_question_bank(self):
        self.quiz_active = False
        self.clear_content()
        self.heading(
            "Question Bank",
            "Manage the questions available in your quizzes."
        )

        toolbar = tk.Frame(self.content, bg=BG)
        toolbar.pack(fill="x", pady=(0, 12))

        self.make_button(
            toolbar, "Add Question", self.show_add_question,
            color=TEAL
        ).pack(side="left", padx=(0, 10))

        self.make_button(
            toolbar, "Delete Selected", self.delete_question,
            color=RED
        ).pack(side="left", padx=10)

        columns = (
            "id", "category", "difficulty", "question", "answer"
        )

        self.question_tree = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings",
            height=17
        )

        for key, label, width in [
            ("id", "ID", 50),
            ("category", "Category", 100),
            ("difficulty", "Difficulty", 110),
            ("question", "Question", 590),
            ("answer", "Correct", 80)
        ]:
            self.question_tree.heading(key, text=label)
            self.question_tree.column(key, width=width)

        self.question_tree.pack(fill="both", expand=True)

        self.refresh_question_bank()

    def refresh_question_bank(self):
        for item in self.question_tree.get_children():
            self.question_tree.delete(item)

        with database() as con:
            rows = con.execute("""
                SELECT id, category, difficulty, question, correct_answer
                FROM questions ORDER BY id DESC
            """).fetchall()

        for row in rows:
            self.question_tree.insert("", "end", values=(
                row["id"],
                row["category"],
                row["difficulty"],
                row["question"],
                row["correct_answer"]
            ))

    def delete_question(self):
        selected = self.question_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Question",
                "Please select a question to delete."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete the selected question?"
        ):
            return

        values = self.question_tree.item(selected[0], "values")
        question_id = values[0]

        with database() as con:
            con.execute(
                "DELETE FROM questions WHERE id = ?",
                (question_id,)
            )

        self.refresh_question_bank()

        messagebox.showinfo(
            "Deleted",
            "The question has been deleted successfully."
        )

    def show_add_question(self):
        window = tk.Toplevel(self.root)
        window.title("Add New Question")
        window.geometry("600x720")
        window.configure(bg=BG)
        window.transient(self.root)
        window.grab_set()

        panel = tk.Frame(
            window, bg=PANEL, padx=25, pady=20
        )
        panel.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            panel,
            text="Add New Question",
            bg=PANEL,
            fg=TEXT,
            font=(FONT, 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        category = tk.StringVar(value="Python")
        difficulty = tk.StringVar(value="Beginner")
        correct = tk.StringVar(value="A")

        fields = {}

        def add_label(text):
            tk.Label(
                panel, text=text, bg=PANEL, fg=TEXT,
                font=(FONT, 9, "bold")
            ).pack(anchor="w", pady=(9, 4))

        add_label("Category")
        ttk.Combobox(
            panel, textvariable=category,
            values=["Python", "C++", "Java"],
            state="readonly", width=55
        ).pack(anchor="w")

        add_label("Difficulty")
        ttk.Combobox(
            panel, textvariable=difficulty,
            values=["Beginner", "Intermediate", "Advanced"],
            state="readonly", width=55
        ).pack(anchor="w")

        add_label("Question")
        fields["question"] = tk.Text(
            panel, height=3, width=58,
            bg=PANEL_ALT, fg=TEXT,
            insertbackground=TEXT, relief="flat"
        )
        fields["question"].pack(anchor="w")

        for key in ["A", "B", "C", "D"]:
            add_label(f"Option {key}")
            entry = tk.Entry(
                panel, width=60, bg=PANEL_ALT,
                fg=TEXT, insertbackground=TEXT,
                relief="flat"
            )
            entry.pack(anchor="w", ipady=5)
            fields[f"option_{key.lower()}"] = entry

        add_label("Correct Answer")
        ttk.Combobox(
            panel, textvariable=correct,
            values=["A", "B", "C", "D"],
            state="readonly", width=55
        ).pack(anchor="w")

        add_label("Explanation (Optional)")
        fields["explanation"] = tk.Text(
            panel, height=3, width=58,
            bg=PANEL_ALT, fg=TEXT,
            insertbackground=TEXT, relief="flat"
        )
        fields["explanation"].pack(anchor="w")

        def save_question():
            question_text = fields["question"].get(
                "1.0", "end"
            ).strip()

            option_values = [
                fields[f"option_{key.lower()}"].get().strip()
                for key in ["A", "B", "C", "D"]
            ]

            explanation = fields["explanation"].get(
                "1.0", "end"
            ).strip()

            if not question_text or not all(option_values):
                messagebox.showwarning(
                    "Missing Information",
                    "Please enter the question and all four options.",
                    parent=window
                )
                return

            with database() as con:
                con.execute("""
                    INSERT INTO questions (
                        category, difficulty, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer, explanation
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    category.get(),
                    difficulty.get(),
                    question_text,
                    *option_values,
                    correct.get(),
                    explanation
                ))

            self.refresh_question_bank()
            messagebox.showinfo(
                "Saved",
                "Question added successfully.",
                parent=window
            )
            window.destroy()

        self.make_button(
            panel, "Save Question", save_question, color=TEAL
        ).pack(anchor="w", pady=18)


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():
    try:
        initialize_database()

        root = tk.Tk()
        app = QuizMaster(root)

        root.mainloop()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Unable to start the application:\n{error}"
        )
    except Exception as error:
        messagebox.showerror(
            "Application Error",
            f"An unexpected error occurred:\n{error}"
        )


if __name__ == "__main__":
    main()