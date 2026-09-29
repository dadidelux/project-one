from django.core.management.base import BaseCommand
from accounts.models import User
from courses.models import Course, Chapter, Lesson, Quiz, Question, Choice


class Command(BaseCommand):
    help = 'Seed the database with sample Data Science courses'

    def _add_quiz(self, lesson, questions):
        """Create an idempotent practice quiz for a lesson.

        questions: list of (question_text, [(choice_text, is_correct), ...]) tuples.
        Each question must have exactly one correct choice.
        """
        quiz, _ = Quiz.objects.get_or_create(
            lesson=lesson,
            defaults={
                'title': f'{lesson.title} Practice Quiz',
                'description': f'Test your understanding of {lesson.title}.',
                'passing_score': 70,
                'time_limit_minutes': None,
            }
        )
        for order, (text, choices) in enumerate(questions, start=1):
            question, _ = Question.objects.get_or_create(
                quiz=quiz,
                order=order,
                defaults={'text': text}
            )
            for choice_text, is_correct in choices:
                Choice.objects.get_or_create(
                    question=question,
                    text=choice_text,
                    defaults={'is_correct': is_correct}
                )
        return quiz

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create instructor
        instructor, created = User.objects.get_or_create(
            username='instructor',
            defaults={
                'email': 'instructor@example.com',
                'is_instructor': True,
                'first_name': 'John',
                'last_name': 'Doe',
            }
        )
        if created:
            instructor.set_password('instructor123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS('Created instructor: instructor / instructor123'))

        # Create student
        student, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
            }
        )
        if created:
            student.set_password('student123')
            student.save()
            self.stdout.write(self.style.SUCCESS('Created student: student / student123'))

        # ──────────────────────────────────────────────
        # Course 1: Introduction to Data Science
        # ──────────────────────────────────────────────
        course1, _ = Course.objects.get_or_create(
            title='Introduction to Data Science',
            defaults={
                'description': 'Explore the foundations of data science - what it is, how data is structured, and why it drives modern decision-making.',
                'is_published': True,
            }
        )

        # Chapter 1: Getting Started
        ch1_1, _ = Chapter.objects.get_or_create(
            course=course1,
            title='Getting Started',
            defaults={'order': 1, 'description': 'Core concepts every data scientist needs first'}
        )
        l1_1_1, _ = Lesson.objects.get_or_create(
            chapter=ch1_1,
            title='What is Data Science',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>What is Data Science?</h2>
<p>Data science combines statistics, programming, and domain expertise to extract meaningful patterns from data. It helps organisations make evidence-based decisions rather than relying on intuition alone.</p>
<h3>The Data Science Process</h3>
<ol>
<li><strong>Define the question</strong> - What problem are we trying to solve?</li>
<li><strong>Collect data</strong> - Gather relevant information from databases, APIs, sensors, or surveys.</li>
<li><strong>Clean and prepare</strong> - Remove errors, handle missing values, and format the data.</li>
<li><strong>Explore and analyse</strong> - Use visualisations and statistics to find patterns.</li>
<li><strong>Model and predict</strong> - Build algorithms that forecast future outcomes.</li>
<li><strong>Communicate results</strong> - Present findings so stakeholders can act on them.</li>
</ol>
<h3>Where Data Science Is Used</h3>
<ul>
<li>Healthcare - predicting patient outcomes and optimising treatments</li>
<li>Finance - fraud detection and risk assessment</li>
<li>Retail - recommendation engines and demand forecasting</li>
<li>Sports - player performance analysis and strategy optimisation</li>
</ul>'''
            }
        )
        self._add_quiz(l1_1_1, [
            ("What is the first step in the data science process described in the lesson?", [
                ("Collect data", False), ("Define the question", True),
                ("Model and predict", False), ("Communicate results", False)]),
            ("Which step involves removing errors, handling missing values, and formatting data?", [
                ("Explore and analyse", False), ("Collect data", False),
                ("Clean and prepare", True), ("Communicate results", False)]),
            ("According to the lesson, which industry example uses data science for fraud detection and risk assessment?", [
                ("Healthcare", False), ("Finance", True),
                ("Retail", False), ("Sports", False)]),
            ("Data science combines statistics, programming, and which other element?", [
                ("Domain expertise", True), ("Marketing skills", False),
                ("Graphic design", False), ("Legal knowledge", False)]),
        ])
        l1_1_2, _ = Lesson.objects.get_or_create(
            chapter=ch1_1,
            title='What is Data',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>What is Data?</h2>
<p>Data is a collection of facts - numbers, text, observations, or measurements - that can be processed to generate information and insights.</p>
<h3>Types of Data</h3>
<table>
<thead><tr><th>Type</th><th>Description</th><th>Examples</th></tr></thead>
<tbody>
<tr><td>Numerical</td><td>Quantities that can be measured</td><td>Height, temperature, revenue</td></tr>
<tr><td>Categorical</td><td>Labels that describe groups or categories</td><td>Gender, colour, country</td></tr>
<tr><td>Ordinal</td><td>Categories with a meaningful order</td><td>Education level, star rating</td></tr>
<tr><td>Boolean</td><td>True / False values</td><td>Is paid, is active</td></tr>
</tbody>
</table>
<h3>Structured vs Unstructured Data</h3>
<p><strong>Structured data</strong> lives in rows and columns (spreadsheets, SQL tables). <strong>Unstructured data</strong> has no predefined format - text documents, images, audio files, and social media posts are common examples. Roughly 80% of the world's data is unstructured, which is why natural language processing and computer vision are growing fields.</p>'''
            }
        )
        self._add_quiz(l1_1_2, [
            ("Which data type describes categories with a meaningful order, such as education level or star rating?", [
                ("Numerical", False), ("Categorical", False),
                ("Ordinal", True), ("Boolean", False)]),
            ("According to the lesson, roughly what percentage of the world's data is unstructured?", [
                ("20%", False), ("50%", False), ("80%", True), ("95%", False)]),
            ("Which type of data lives in rows and columns, such as spreadsheets or SQL tables?", [
                ("Structured data", True), ("Unstructured data", False),
                ("Ordinal data", False), ("Boolean data", False)]),
            ("True/False values like \"is paid\" or \"is active\" are an example of which data type?", [
                ("Numerical", False), ("Ordinal", False),
                ("Boolean", True), ("Categorical", False)]),
        ])
        l1_1_3, _ = Lesson.objects.get_or_create(
            chapter=ch1_1,
            title='Database Tables',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Database Tables</h2>
<p>Most structured data lives in relational databases, organised into tables. Understanding how tables work is essential for any data scientist who needs to query and manipulate data.</p>
<h3>Table Structure</h3>
<ul>
<li><strong>Rows</strong> - each row represents a single record (observation)</li>
<li><strong>Columns</strong> - each column represents a variable (feature)</li>
<li><strong>Primary key</strong> - a unique identifier for every row</li>
<li><strong>Foreign key</strong> - a column that references a primary key in another table, creating relationships</li>
</ul>
<h3>Example: Students Table</h3>
<pre><code>CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    enrollment_date DATE DEFAULT CURRENT_DATE
);</code></pre>
<h3>Querying Tables with SQL</h3>
<pre><code>SELECT name, enrollment_date
FROM students
WHERE enrollment_date > '2025-01-01'
ORDER BY name;</code></pre>
<p>SQL is the universal language for extracting data from relational databases, and nearly every data science role expects proficiency with it.</p>'''
            }
        )
        self._add_quiz(l1_1_3, [
            ("In a relational database table, what does a primary key provide?", [
                ("A unique identifier for every row", True), ("A description of the column data type", False),
                ("A link to another table only", False), ("The total row count", False)]),
            ("In the lesson's example, which SQL keyword marks the id column as a unique identifier?", [
                ("UNIQUE", False), ("NOT NULL", False),
                ("PRIMARY KEY", True), ("DEFAULT", False)]),
            ("What does a foreign key do?", [
                ("References a primary key in another table, creating relationships", True), ("Encrypts sensitive data", False),
                ("Automatically deletes duplicate rows", False), ("Converts data types", False)]),
            ("In the example query, which clause filters students who enrolled after '2025-01-01'?", [
                ("ORDER BY", False), ("GROUP BY", False),
                ("WHERE", True), ("HAVING", False)]),
        ])

        # Chapter 2: Python Refresher
        ch1_2, _ = Chapter.objects.get_or_create(
            course=course1,
            title='Python Refresher',
            defaults={'order': 2, 'description': 'A full Python fundamentals pass for beginners'}
        )
        l1_2_1, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Printing, Variables & Arithmetic',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Printing, Variables & Arithmetic</h2>
<p>Python is one of the most readable programming languages. You can start writing useful code with just a few basics.</p>
<h3>Printing Output</h3>
<pre><code>print("Hello, world!")
print("My name is", "Alice")</code></pre>
<h3>Variables</h3>
<p>Variables store data. Python does not require you to declare a type - it figures it out automatically.</p>
<pre><code>name = "Alice"
age = 25
height = 1.68
is_student = True</code></pre>
<h3>Arithmetic Operators</h3>
<table>
<thead><tr><th>Operator</th><th>Meaning</th><th>Example</th></tr></thead>
<tbody>
<tr><td>+</td><td>Addition</td><td>3 + 2 # 5</td></tr>
<tr><td>-</td><td>Subtraction</td><td>10 - 4 # 6</td></tr>
<tr><td>*</td><td>Multiplication</td><td>6 * 3 # 18</td></tr>
<tr><td>/</td><td>Division</td><td>15 / 4 # 3.75</td></tr>
<tr><td>//</td><td>Floor division</td><td>15 // 4 # 3</td></tr>
<tr><td>%</td><td>Modulo (remainder)</td><td>15 % 4 # 3</td></tr>
<tr><td>**</td><td>Exponent</td><td>2 ** 3 # 8</td></tr>
</tbody>
</table>
<h3>User Input</h3>
<pre><code>name = input("What is your name? ")
print("Hello,", name)</code></pre>
<p>The <code>input()</code> function always returns a string. Use <code>int()</code> or <code>float()</code> to convert it for arithmetic.</p>'''
            }
        )
        self._add_quiz(l1_2_1, [
            ("What does the input() function always return?", [
                ("An integer", False), ("A string", True),
                ("A float", False), ("A boolean", False)]),
            ("What is the result of 15 // 4 according to the lesson's table?", [
                ("3.75", False), ("3", True), ("4", False), ("60", False)]),
            ("What is the result of 15 % 4?", [
                ("3", True), ("3.75", False), ("0", False), ("11", False)]),
            ("Does Python require you to declare a variable's type before assigning a value?", [
                ("Yes, always", False), ("No, Python infers it automatically", True),
                ("Only for numbers", False), ("Only for strings", False)]),
        ])
        l1_2_2, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Data Types, Type Casting & Checking Types',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>Data Types, Type Casting & Checking Types</h2>
<p>Every value in Python has a type. Understanding types helps you avoid bugs and write clearer code.</p>
<h3>Built-in Types</h3>
<table>
<thead><tr><th>Type</th><th>Example</th><th>Description</th></tr></thead>
<tbody>
<tr><td>int</td><td>42</td><td>Whole numbers</td></tr>
<tr><td>float</td><td>3.14</td><td>Decimal numbers</td></tr>
<tr><td>str</td><td>"hello"</td><td>Text (strings)</td></tr>
<tr><td>bool</td><td>True / False</td><td>Boolean values</td></tr>
<tr><td>list</td><td>[1, 2, 3]</td><td>Ordered, mutable collection</td></tr>
<tr><td>dict</td><td>{"a": 1}</td><td>Key-value mappings</td></tr>
</tbody>
</table>
<h3>Checking Types</h3>
<pre><code>x = 42
print(type(x))       # <class 'int'>
print(isinstance(x, int))  # True</code></pre>
<h3>Type Casting</h3>
<p>Convert between types explicitly:</p>
<pre><code>x = "100"
y = int(x)       # String to integer
z = float(x)     # String to float

num = 42
s = str(num)      # Integer to string

print(int(3.9))   # 3 (truncates, does not round)
print(float("3.14"))  # 3.14</code></pre>
<p>If a conversion is not possible, Python raises a <code>ValueError</code>.</p>'''
            }
        )
        self._add_quiz(l1_2_2, [
            ("Which function would you use to check if a variable is an instance of a particular type?", [
                ("type()", False), ("isinstance()", True),
                ("cast()", False), ("check()", False)]),
            ("What error does Python raise when a type conversion is not possible?", [
                ("TypeError", False), ("ValueError", True),
                ("NameError", False), ("SyntaxError", False)]),
            ("According to the lesson, what does int(3.9) return?", [
                ("4", False), ("3.9", False), ("3", True), ("An error", False)]),
            ("Which built-in type represents ordered, mutable collections like [1, 2, 3]?", [
                ("dict", False), ("tuple", False), ("list", True), ("set", False)]),
        ])
        l1_2_3, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Lists',
            defaults={
                'order': 3,
                'is_free': True,
                'content': '''<h2>Lists</h2>
<p>Lists are ordered, mutable collections. They are the most commonly used data structure in Python.</p>
<h3>Creating Lists</h3>
<pre><code>fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]</code></pre>
<h3>Accessing Elements</h3>
<pre><code>print(fruits[0])     # "apple" (first item)
print(fruits[-1])    # "cherry" (last item)
print(fruits[1:3])   # ["banana", "cherry"] (slice)</code></pre>
<h3>Modifying Lists</h3>
<pre><code>fruits.append("date")       # Add to end
fruits.insert(1, "blueberry")  # Insert at index1
fruits.remove("banana")     # Remove by value
popped = fruits.pop()       # Remove and return last item</code></pre>
<h3>Useful List Operations</h3>
<pre><code>numbers = [3, 1, 4, 1, 5, 9]
len(numbers)            # 6
sorted(numbers)         # [1, 1, 3, 4, 5, 9]
numbers.sort()          # Sort in place
numbers.reverse()       # Reverse in place
3 in numbers            # True (membership test)</code></pre>
<h3>List Comprehensions</h3>
<pre><code>squares = [x ** 2 for x in range(6)]  # [0, 1, 4, 9, 16, 25]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]</code></pre>'''
            }
        )
        self._add_quiz(l1_2_3, [
            ("What does fruits[-1] return?", [
                ("The first item", False), ("The last item", True),
                ("An empty list", False), ("An error", False)]),
            ("Which method adds an item to the end of a list?", [
                ("insert()", False), ("append()", True),
                ("extend()", False), ("push()", False)]),
            ("What does the list comprehension [x for x in range(10) if x % 2 == 0] produce?", [
                ("All odd numbers 0-9", False), ("All even numbers 0-9", True),
                ("Numbers 0-10", False), ("An error", False)]),
            ("Which method removes and returns the last item of a list?", [
                ("remove()", False), ("pop()", True),
                ("delete()", False), ("clear()", False)]),
        ])
        l1_2_4, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Tuples',
            defaults={
                'order': 4,
                'is_free': True,
                'content': '''<h2>Tuples</h2>
<p>Tuples are ordered, <strong>immutable</strong> collections. Once created, you cannot add, remove, or change elements.</p>
<h3>Creating Tuples</h3>
<pre><code>coordinates = (10, 20)
rgb = (255, 128, 0)
single = (42,)  # Note the comma for a one-element tuple</code></pre>
<h3>Accessing Elements</h3>
<pre><code>print(coordinates[0])   # 10
print(coordinates[1])   # 20
print(rgb[0:2])         # (255, 128)</code></pre>
<h3>Unpacking Tuples</h3>
<pre><code>x, y = coordinates
print(x)  # 10
print(y)  # 20</code></pre>
<h3>When to Use Tuples</h3>
<ul>
<li><strong>Fixed data</strong> - coordinates, RGB colours, database rows</li>
<li><strong>Dictionary keys</strong> - tuples can be dict keys, lists cannot</li>
<li><strong>Multiple return values</strong> - functions can return tuples</li>
</ul>
<pre><code>def get_min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = get_min_max([3, 1, 4, 1, 5])
print(lo, hi)  # 1 5</code></pre>
<p>Use tuples when the data should not change. Use lists when you need to modify the collection.</p>'''
            }
        )
        self._add_quiz(l1_2_4, [
            ("What is the defining characteristic of a tuple compared to a list?", [
                ("Tuples are immutable", True), ("Tuples can only hold numbers", False),
                ("Tuples are always sorted", False), ("Tuples cannot be unpacked", False)]),
            ("How do you correctly create a one-element tuple containing 42?", [
                ("(42)", False), ("[42]", False), ("(42,)", True), ("{42}", False)]),
            ("Why can tuples be used as dictionary keys while lists cannot?", [
                ("Tuples are immutable and hashable", True), ("Tuples are faster", False),
                ("Lists take more memory", False), ("Dictionaries reject lists arbitrarily", False)]),
            ("What does x, y = coordinates do when coordinates = (10, 20)?", [
                ("Raises an error", False), ("Unpacks values into x and y", True),
                ("Creates a new tuple", False), ("Converts the tuple to a list", False)]),
        ])
        l1_2_5, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Dictionaries',
            defaults={
                'order': 5,
                'is_free': True,
                'content': '''<h2>Dictionaries</h2>
<p>Dictionaries store data as key-value pairs. They are fast for lookups and one of Python's most powerful built-in types.</p>
<h3>Creating Dictionaries</h3>
<pre><code>person = {
    "name": "Alice",
    "age": 30,
    "city": "London"
}</code></pre>
<h3>Accessing Values</h3>
<pre><code>print(person["name"])           # "Alice"
print(person.get("email", "N/A"))  # "N/A" (default if key missing)</code></pre>
<h3>Modifying Dictionaries</h3>
<pre><code>person["age"] = 31              # Update a value
person["email"] = "a@b.com"     # Add a new key
del person["city"]              # Remove a key</code></pre>
<h3>Useful Methods</h3>
<pre><code>person.keys()       # dict_keys(["name", "age", "email"])
person.values()     # dict_values(["Alice", 31, "a@b.com"])
person.items()      # Key-value pairs as tuples
"name" in person    # True (membership test)</code></pre>
<h3>Looping Over Dictionaries</h3>
<pre><code>for key, value in person.items():
    print(f"{key}: {value}")</code></pre>
<p>Dictionaries are ideal for structured data - think of them as rows in a table where the column names are keys.</p>'''
            }
        )
        self._add_quiz(l1_2_5, [
            ("What does person.get(\"email\", \"N/A\") return if \"email\" is not a key in person?", [
                ("None", False), ("An error", False), ("\"N/A\"", True), ("An empty string", False)]),
            ("Which statement removes a key from a dictionary?", [
                ("pop_key()", False), ("remove()", False), ("del person[key]", True), ("drop()", False)]),
            ("What does person.items() return?", [
                ("Only the keys", False), ("Only the values", False),
                ("Key-value pairs as tuples", True), ("A sorted list of keys", False)]),
            ("What is the main advantage of dictionaries for lookups, per the lesson?", [
                ("They are always sorted", False), ("They are fast for lookups", True),
                ("They use less memory than lists always", False), ("They cannot be modified", False)]),
        ])
        l1_2_6, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Conditional (If) Statements',
            defaults={
                'order': 6,
                'is_free': True,
                'content': '''<h2>Conditional (If) Statements</h2>
<p>Conditionals let your program make decisions based on whether conditions are true or false.</p>
<h3>Basic If / Elif / Else</h3>
<pre><code>score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")</code></pre>
<h3>Comparison Operators</h3>
<table>
<thead><tr><th>Operator</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>==</td><td>Equal to</td></tr>
<tr><td>!=</td><td>Not equal to</td></tr>
<tr><td>&gt;</td><td>Greater than</td></tr>
<tr><td>&lt;</td><td>Less than</td></tr>
<tr><td>&gt;=</td><td>Greater than or equal</td></tr>
<tr><td>&lt;=</td><td>Less than or equal</td></tr>
</tbody>
</table>
<h3>Logical Operators</h3>
<pre><code>age = 25
has_id = True

if age >= 18 and has_id:
    print("Entry allowed")

if age < 18 or not has_id:
    print("Entry denied")</code></pre>
<h3>Indentation Matters</h3>
<p>Python uses indentation (spaces or tabs) to define code blocks. The standard is4 spaces per level.</p>'''
            }
        )
        self._add_quiz(l1_2_6, [
            ("In the lesson's grading example, what grade is printed for a score of 85?", [
                ("A", False), ("B", True), ("C", False), ("F", False)]),
            ("What does the and operator require for a compound condition to be True?", [
                ("Only one condition needs to be True", False), ("Both conditions must be True", True),
                ("Neither condition needs to be True", False), ("It negates the condition", False)]),
            ("What is the standard indentation used to define code blocks in Python, per the lesson?", [
                ("2 spaces", False), ("4 spaces", True),
                ("A single tab only", False), ("8 spaces", False)]),
            ("Which operator checks for \"not equal to\" in Python?", [
                ("<>", False), ("=/=", False), ("!=", True), ("!==", False)]),
        ])
        l1_2_7, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='For-Loops',
            defaults={
                'order': 7,
                'is_free': True,
                'content': '''<h2>For-Loops</h2>
<p>For-loops iterate over a sequence - a list, string, range of numbers, or any iterable object.</p>
<h3>Looping Over a List</h3>
<pre><code>fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)</code></pre>
<h3>Looping with range()</h3>
<pre><code>for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

for i in range(2, 6):
    print(i)  # 2, 3, 4, 5</code></pre>
<h3>Looping with Index</h3>
<pre><code>for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")</code></pre>
<h3>Looping Over Dictionaries</h3>
<pre><code>person = {"name": "Alice", "age": 30}

for key, value in person.items():
    print(f"{key} = {value}")</code></pre>
<h3>List Comprehensions</h3>
<p>A compact way to create lists from loops:</p>
<pre><code>squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

names = ["alice", "bob", "charlie"]
upper = [n.upper() for n in names]
# ["ALICE", "BOB", "CHARLIE"]</code></pre>
<p>Use <code>break</code> to exit a loop early and <code>continue</code> to skip to the next iteration.</p>'''
            }
        )
        self._add_quiz(l1_2_7, [
            ("What does range(2, 6) produce when looped over?", [
                ("2, 3, 4, 5", True), ("2, 3, 4, 5, 6", False),
                ("0, 1, 2, 3, 4, 5", False), ("6, 5, 4, 3, 2", False)]),
            ("Which function lets you loop over a list while also getting the index of each item?", [
                ("index()", False), ("enumerate()", True), ("zip()", False), ("range()", False)]),
            ("What does continue do inside a loop?", [
                ("Exits the loop completely", False), ("Skips to the next iteration", True),
                ("Pauses the loop", False), ("Restarts the loop from the beginning", False)]),
            ("What is a compact way to build a list from a loop, according to the lesson?", [
                ("A while loop", False), ("A list comprehension", True),
                ("A dictionary comprehension", False), ("A tuple", False)]),
        ])
        l1_2_8, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='While Loops',
            defaults={
                'order': 8,
                'is_free': True,
                'content': '''<h2>While Loops</h2>
<p>While-loops repeat as long as a condition is true. They are useful when you do not know in advance how many iterations you need.</p>
<h3>Basic While Loop</h3>
<pre><code>count = 0

while count < 5:
    print(count)
    count += 1</code></pre>
<h3>User Input Loop</h3>
<pre><code>password = ""

while password != "secret":
    password = input("Enter password: ")

print("Access granted")</code></pre>
<h3>While with Break</h3>
<pre><code>while True:
    command = input("Enter command (quit to exit): ")
    if command == "quit":
        break
    print(f"You entered: {command}")</code></pre>
<h3>While with Continue</h3>
<pre><code>i = 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)  # 1, 3, 5, 7, 9</code></pre>
<h3>Caution: Infinite Loops</h3>
<p>If the condition never becomes False, the loop runs forever. Always make sure the loop variable is updated inside the body.</p>'''
            }
        )
        self._add_quiz(l1_2_8, [
            ("When are while-loops especially useful, according to the lesson?", [
                ("When you know exactly how many iterations you need", False),
                ("When you do not know in advance how many iterations you need", True),
                ("Only for looping over lists", False), ("Only for looping over dictionaries", False)]),
            ("What causes an infinite loop?", [
                ("Using break inside the loop", False), ("The condition never becoming False", True),
                ("Using continue inside the loop", False), ("Setting count = 0 before the loop", False)]),
            ("In the example `while True: ... if command == \"quit\": break`, what causes the loop to end?", [
                ("The password matching", False), ("count reaching 5", False),
                ("Entering \"quit\"", True), ("An error being raised", False)]),
            ("What does continue do in the even-number-skipping example?", [
                ("Stops the loop entirely", False), ("Skips printing when i is even", True),
                ("Skips printing when i is odd", False), ("Doubles the value of i", False)]),
        ])
        l1_2_9, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Functions',
            defaults={
                'order': 9,
                'is_free': True,
                'content': '''<h2>Functions</h2>
<p>Functions let you group reusable logic. Define once, call many times.</p>
<h3>Defining and Calling</h3>
<pre><code>def greet(name):
    return f"Hello, {name}!"

message = greet("Alice")
print(message)  # Hello, Alice!</code></pre>
<h3>Parameters and Return Values</h3>
<pre><code>def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8</code></pre>
<h3>Default Parameters</h3>
<pre><code>def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))              # Hello, Alice!
print(greet("Alice", "Hi"))        # Hi, Alice!</code></pre>
<h3>Functions with No Return</h3>
<pre><code>def print_report(title, value):
    print(f"Report: {title}")
    print(f"Value: {value}")

print_report("Sales", 1500)</code></pre>
<p>This is a light introduction. The deeper Functions lesson in the next chapter covers docstrings, type hints, and lambda functions.</p>'''
            }
        )
        self._add_quiz(l1_2_9, [
            ("What keyword is used to define a function in Python?", [
                ("func", False), ("def", True), ("function", False), ("define", False)]),
            ("In def greet(name, greeting=\"Hello\"), what is \"Hello\"?", [
                ("A required argument", False), ("A default parameter value", True),
                ("A return value", False), ("A type hint", False)]),
            ("What does greet(\"Alice\") return using the lesson's default-parameter example?", [
                ("\"Hello, Alice!\"", True), ("\"Hi, Alice!\"", False),
                ("None", False), ("An error, since greeting is missing", False)]),
            ("What is true of a function like print_report that only calls print() internally?", [
                ("It must return a value", False), ("It can execute without returning a value", True),
                ("It cannot take parameters", False), ("It always raises an error", False)]),
        ])
        l1_2_10, _ = Lesson.objects.get_or_create(
            chapter=ch1_2,
            title='Functional Programming Concepts',
            defaults={
                'order': 10,
                'is_free': True,
                'content': '''<h2>Functional Programming Concepts</h2>
<p>Python supports a functional programming style. These concepts help you write cleaner, more concise code.</p>
<h3>Lambda Functions</h3>
<p>Small, anonymous functions defined in one line:</p>
<pre><code>double = lambda x: x * 2
print(double(5))  # 10

add = lambda a, b: a + b
print(add(3, 4))  # 7</code></pre>
<h3>map() - Apply a Function to Every Item</h3>
<pre><code>numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
# [1, 4, 9, 16, 25]</code></pre>
<h3>filter() - Keep Items That Match</h3>
<pre><code>numbers = [1, 2, 3, 4, 5, 6, 7, 8]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6, 8]</code></pre>
<h3>sorted() with a Key Function</h3>
<pre><code>words = ["banana", "apple", "cherry"]
by_length = sorted(words, key=lambda w: len(w))
# ["apple", "banana", "cherry"]</code></pre>
<h3>When to Use Functional Style</h3>
<ul>
<li><strong>Lambda + map/filter</strong> - quick transformations without defining a named function</li>
<li><strong>List comprehensions</strong> - usually more Pythonic than map/filter for simple cases</li>
<li><strong>Higher-order functions</strong> - functions that take other functions as arguments (common in data pipelines)</li>
</ul>
<p>In data science, you will see lambda functions used frequently with Pandas <code>apply()</code> and <code>transform()</code>.</p>'''
            }
        )
        self._add_quiz(l1_2_10, [
            ("What does double = lambda x: x * 2 create?", [
                ("A named function called double", False),
                ("An anonymous one-line function assigned to double", True),
                ("A list of doubled values", False), ("A syntax error", False)]),
            ("What does filter(lambda x: x % 2 == 0, numbers) do?", [
                ("Doubles every number", False), ("Keeps only even numbers", True),
                ("Keeps only odd numbers", False), ("Sorts the numbers", False)]),
            ("What does sorted(words, key=lambda w: len(w)) sort words by?", [
                ("Alphabetical order", False), ("Length", True),
                ("Reverse alphabetical order", False), ("First letter only", False)]),
            ("Where does the lesson say lambda functions are frequently used in data science?", [
                ("With Pandas apply() and transform()", True), ("Only in web development", False),
                ("Only for sorting numbers", False), ("Never, they are discouraged", False)]),
        ])

        # Chapter 3: Python for Data Science
        ch1_3, _ = Chapter.objects.get_or_create(
            course=course1,
            title='Python for Data Science',
            defaults={'order': 3, 'description': 'Essential Python skills for working with data'}
        )
        l1_3_1, _ = Lesson.objects.get_or_create(
            chapter=ch1_3,
            title='Classes and Dataclasses',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Classes and Dataclasses</h2>
<h3>A Brief Introduction to Classes and OOP</h3>
<p>Object-oriented programming (OOP) is a language model that reduces code duplication and makes code easier to update, maintain, and reuse. As a result, most commercial software is now built using OOP.</p>
<p>Whereas procedural programming is built around actions and logic, OOP is built around data structures, known as objects, that consist of data and functions (called methods) that act on the data. Objects are built from classes, which are like blueprints for the objects.</p>
<p>A class is a data type, and when you create an object of that data type, it is also known as an instance of that class. The process of setting the initial values and behaviors of the instance is called instantiation.</p>
<p>As instances of a class, objects allow you to create multiple copies with the same structure but potentially different data. For example, if you're building a space combat game, you can conveniently bundle the attributes of a certain spaceship, like its size, speed, and armament, with the methods that control its flight and weapons operation. Then, when you create a new spaceship of that type, you only need to worry about giving it a unique name.</p>
<p>Because Python is an object-oriented programming language, you've already been using objects and methods defined by other people. But unlike languages such as Java, Python doesn't force you to use OOP for your programs. It provides ways to encapsulate and separate abstraction layers using other approaches such as procedural or functional programming.</p>
<p>Having this choice is important. If you implement OOP in small programs, most of them will feel over-engineered. To paraphrase computer scientist Joe Armstrong, "The problem with object-oriented languages is they've got all this implicit environment that they carry around with them. You wanted a banana, but what you got was a gorilla holding the banana and the whole damn jungle!"</p>
<p>If you're a scientist or engineer, you can get a lot done without OOP, but that doesn't mean you should ignore it. OOP makes it easy to simulate many objects at a time, such as a flock of birds, a network of power plants, or a cluster of galaxies. It's also important when things that are manipulated, like a GUI button or window, must persist for a long time in the computer's memory.</p>
<p>Since it's easier to demonstrate OOP than it is to talk about it, let's look at an example using a Dungeons and Dragons–type board game in which players can be different characters, such as dwarves, elves, and wizards. These games use character cards to list important information for each character type. If you let your playing piece represent a dwarf, it inherits the characteristics on the card.</p>
<h3>The Dwarf and Elf Classes</h3>
<p>The following code reproduces board game–style play, letting you create virtual cards for a dwarf and an elf, name your characters, and have them fight. The outcome of the fight will impact one of the character's body points, which represents the character's health. Be sure to note how OOP allows you to easily create many identical objects — in this case, dwarves or elves — by "stamping" them out of the predefined template, called a class.</p>
<pre><code>import random

class Dwarf(object):
    def __init__(self, name):
        self.name = name
        self.attack = 3
        self.defend = 4
        self.move = 2
        self.body = 5

    def talk(self):
        print("I'm a blade-man, I'll cut ya!!!")</code></pre>
<p>We started by importing <code>random</code> to simulate rolling a die; this is how your character will fight. Then we defined a class for a <em>Dwarf</em> character, capitalizing the first letter of the class name, and passed it an <code>object</code> argument. This <code>object</code> argument represents the <em>base class</em> of all types in Python.</p>
<p><strong>TIP:</strong> Because <code>object</code> is the default parameter, you don't have to state it explicitly when defining a class. It's used here for clarity.</p>
<p>As mentioned previously, a class is a template for creating objects of a <em>certain type</em>. For example, when you create a list or dictionary in Python, you are creating them from a class.</p>
<p>The <code>Dwarf</code> class definition is like the card in the previous figure; it's the "genetic" blueprint for a dwarf. It will assign attributes, like strength and vitality, and methods, like how the character moves or talks. Attributes are variables associated with an object, and methods are attributes that also happen to be functions, which are passed a reference to their instance when they run.</p>
<p>Immediately after the <code>class</code> definition, we defined a <em>constructor</em> method, also referred to as the <em>initialization</em> method. It sets up the initial attribute values for the object. The <code>__init__()</code> method is a special built-in method that Python automatically invokes as soon as a new object is created. In this case, we passed two arguments: <code>self</code> and the <code>name</code> of the object.</p>
<p>The <code>__init__()</code> method is a <em>dunder</em> (double underscore) method, meaning its name is preceded and followed by double underscores. Also called <em>magic</em> or <em>special</em> methods, they let you create classes that behave like native Python data structures such as lists, tuples, and sets.</p>
<p>The <code>self</code> parameter is a reference to the instance of the class that is being created, or a reference to the instance a method was invoked on, technically referred to as a <em>context</em> instance. You can think of it as a placeholder for the actual name you will give the object.</p>
<p>If you create a new dwarf and name it "Steve," <code>self</code> will become Steve behind the scenes. For example, <code>self.attack</code> becomes "Steve's attack." If you create another dwarf named "Flint," <code>self</code> for that object will become "Flint." This way, the scope of Steve's health attribute is kept separate from Flint's.</p>
<p>Next, we listed some attributes for a dwarf beneath the constructor definition. We added a name so you can tell one dwarf from another, as well as the value of key combat characteristics. Notice how this list resembles the character card.</p>
<p><strong>TIP:</strong> While it's possible to use methods to assign new attributes later, it's best to initialize them all within the <code>__init__</code> method. This way, all the available attributes are conveniently listed in an easy-to-find location.</p>
<p>We next defined a <code>talk()</code> method and passed it <code>self</code>. By passing it <code>self</code>, you linked the method to the object. In more comprehensive games, methods might include behaviors like movement and the ability to disarm traps.</p>
<p>With the class definition complete, we'll use the code below to create an instance of the <code>Dwarf</code> class and assign this object to the local variable <code>lenn</code>, the dwarf's name. We'll print the name and attack attributes to demonstrate that we have access to them, and finish by invoking the <code>talk()</code> method. Note how both attributes and methods are invoked with dot notation syntax (such as <code>lenn.attack</code> and <code>lenn.talk()</code>):</p>
<pre><code>lenn = Dwarf("Lenn")
print(f"Dwarf name = {lenn.name}")
print(f"Lenn's attack strength = {lenn.attack}")
lenn.talk()</code></pre>
<pre><code>Dwarf name = Lenn
Lenn's attack strength = 3
I'm a blade-man, I'll cut ya!!!</code></pre>
<p>Now we'll create an <em>elf</em> character, using the same process, and have it fight the dwarf. The elf's body attribute will be updated to reflect the outcome of the battle.</p>
<pre><code>class Elf(object):
    pointed_ears = True

    def __init__(self, name):
        self.name = name
        self.attack = 4
        self.defend = 4
        self.move = 4
        self.body = 4

esseden = Elf("Esseden")
print(f"Elf name = {esseden.name}")
print(f"Esseden body value = {esseden.body}")</code></pre>
<pre><code>Elf name = Esseden
Esseden body value = 4</code></pre>
<p>First, we defined an <code>Elf</code> class and passed it <code>object</code>, as we did with the <code>Dwarf</code> class. Next, for instructional purposes, we did something different. We added an attribute, <code>pointed_ears</code>, immediately <em>after</em> defining the class and <em>before</em> defining the initialization method.</p>
<p>Classes are objects, too, so they can have their own attributes. <em>Class attributes</em> are common to <em>all</em> objects made from the class and behave sort of like global variables.</p>
<p>In this case, all the elves you build will have pointed ears. By placing this at the class level, you don't need to include it at the object level. Likewise, you can define <em>class methods</em>, that act on all objects. For example, all pirate characters might say "Arrgh!" before they speak.</p>
<p>Next, we defined the initialization method and assigned some attributes. We made them slightly different from the dwarf's and well-balanced, like an elf. We then instantiated an elf named Esseden and accessed his name and body attributes using <code>print()</code>.</p>
<p>Next, we'll have our two characters interact using the roll of a virtual die with a maximum value equal to the character's attack or defend value. We'll use the random module to choose a roll value in a range of 1 to Lenn's attack attribute plus 1, then repeat this process to get Esseden's defense.</p>
<p>We'll calculate the damage to Esseden by subtracting Esseden's roll value from Lenn's roll value, and if the damage is a <em>positive</em> number, subtract it from Esseden's body attribute. We'll use <code>print()</code> to confirm the elf's current health.</p>
<pre><code>lenn_attack_roll = random.randrange(1, lenn.attack + 1)
print(f"Lenn attack roll = {lenn_attack_roll}")

esseden_defend_roll = random.randrange(1, esseden.defend + 1)
print(f"Esseden defend roll = {esseden_defend_roll}")

damage = lenn_attack_roll - esseden_defend_roll
if damage > 0:
    esseden.body -= damage

print(f"Esseden current body value = {esseden.body}")</code></pre>
<pre><code>Lenn attack roll = 3
Esseden defend roll = 1
Esseden body value = 2</code></pre>
<p>The roll results here are random, so you may get a different outcome.</p>
<p>As you can imagine, building many similar characters and keeping track of their changing attributes could quickly get complicated with procedural programming. OOP provides a modular structure for your program, makes it easy to hide complexity and ownership of scope with encapsulation, permits problem-solving in bite-sized chunks, and produces sharable templates that can be modified and used elsewhere.</p>
<h3>Adding a Class with Inheritance</h3>
<p><em>Inheritance</em>, a key concept in OOP, lets you define a new <em>child</em> class based on an existing <em>parent</em> or <em>ancestor</em> class. (Technically, the original class is called a <em>base class</em> or <em>superclass</em>. The new class is called a <em>derived class</em> or <em>subclass</em>.)</p>
<p>The new subclass inherits all of the attributes and methods of the existing superclass. This makes it easy to copy and extend an existing base class by adding new attributes and methods specific to the subclass.</p>
<p>Let's make a new elf class called <code>Elden</code> that inherits from and modifies our current <code>Elf</code> class. We'll assume the Elden are "high elves" which are archers and come with a quiver of arrows. Otherwise, they have the same attributes as a common elf.</p>
<pre><code>class Elden(Elf):
    def __init__(self, name):
        Elf.__init__(self, name)
        self.arrows = 24

    def fire_arrow(self):
        if self.arrows > 0:
            self.arrows -= 1
            print(f"\\nPphsssssttttttt!")
            print(f"{self.name} arrows remaining = {self.arrows}")
        else:
            print("\\nArrows depleted")</code></pre>
<p>To create a child class, we passed the class statement the name of the parent, or superclass, which in this case is <code>Elf</code>. Remember that, when you first defined <code>Elf</code>, you passed it <code>object</code>. This meant that the <code>Elf</code> class was inherited from the <code>object</code> class, which is the root of all Python objects. The <code>object</code> class provides the default implementation of common methods that all derived classes might need. By passing <code>Elf</code> instead of <code>object</code>, you got the attributes and methods under <code>object</code> as well as the new ones you added to the <code>Elf</code> class.</p>
<p>Next, we defined the <code>__init__()</code> initialization method for the <code>Elden</code> class, which, like the <code>Elf</code> class, has a <code>self</code> and <code>name</code> parameter. Immediately beneath it, we called the initialization method from the <code>Elf</code> class and passed it <code>Elf</code> instead of <code>self</code>, along with a <code>name</code> parameter. Passing in the <code>Elf</code> class gives you access to all the attributes in the <code>Elf.__init__()</code> method, such as <code>attack</code>, <code>defend</code>, and <code>body</code> attributes, so you don't need to duplicate any code.</p>
<p>If you don't define an <code>__init__()</code> method for a child class, it will use the <code>__init__()</code> method from the parent class. If you want to <em>override</em> some of the attribute values in the parent class or add new attributes, you'll need to include an <code>__init__()</code> method for the child class, as we did in this example.</p>
<p>Our original <code>Elf</code> class did not allow for arrows, so we added a new <code>self.arrows</code> attribute. We set the complement of arrows to 24. The Elden elf will need a way to fire the arrows, so we defined a new method called <code>fire_arrow()</code>. If we were writing a complete game this would include an advantage such as rolling an extra attack die or being able to attack from a distance.</p>
<p>Now, let's instantiate an Elden named Legolas, access their name, and shoot an arrow.</p>
<pre><code>legolas = Elden("Legolas")
print(f"Elden name = {legolas.name} ")

legolas.fire_arrow()</code></pre>
<pre><code>Elden name = Legolas

Pphsssssttttttt!
Legolas arrows remaining = 23</code></pre>
<p>By using inheritance, we reduced the amount of code we needed to write for the new <code>Elden</code> class by "borrowing" from the existing <code>Elf</code> class. And it gets better. In the next section, we'll look at another way to reduce the amount of code needed to define classes.</p>
<h3>Using the super() Function for Inheritance</h3>
<p>The <code>super()</code> built-in function removes the need for an explicit call to a base class name when invoking base class methods. It works with both single and multiple inheritance.</p>
<p>For example, in the <code>Elden</code> class definition, you called the <code>Elf</code> class's <code>__init__()</code> method within the <code>Elden</code> class's <code>__init__()</code> method, as follows:</p>
<pre><code>class Elden(Elf):
    def __init__(self, name):
        Elf.__init__(self, name)</code></pre>
<p>This lets the <code>Elden</code> class inherit from <code>Elf</code>. Alternatively, you could have used the <code>super()</code> function, which returns a <em>proxy object</em> that allows access to methods of the base class:</p>
<pre><code>class Elden(Elf):
    def __init__(self, name):
        super().__init__(name)</code></pre>
<p>In this case, <code>super()</code> removes the need for an explicit call to the <code>Elf</code> class. When using single inheritance, <code>super()</code> is just a fancier way to refer to the base type. It makes the code a bit more maintainable.</p>
<p>For example, if you are using <code>super()</code> everywhere and want to change the name of the base class (such as from <code>Elf</code> to <code>CommonElf</code>) you need to change the name only once when defining the base class.</p>
<p>Another use for <code>super()</code> is to access inherited methods that have been overridden in a new class. Let's assume we've made a new <code>HighElf</code> class where the elf character uses the inherited <code>Elden</code> class's <code>fire_arrow()</code> method to fire <em>two</em> arrows at a time instead of one. We've overridden the method, but if we run into a situation where we want to fire a <em>single</em> arrow, we can call the base class's method by using <code>super().fire_arrow()</code>. This references the original method, which fires a single arrow.</p>
<p>The use of <code>super()</code> is somewhat controversial. On one hand, it makes code more maintainable. On the other, it makes it less explicit, which violates the Zen of Python edict "Explicit is better than implicit."</p>
<h3>The Dataclass</h3>
<p>The built-in <code>dataclass</code> module introduced in Python 3.7 provides a convenient way to reduce code redundancy by making classes less verbose. Although primarily designed for classes that <em>store data</em>, data classes work just like regular classes and can include methods that interact with the data. Some use cases include classes for bank accounts, the content of scientific articles, and employee information.</p>
<p>A dataclass comes with basic "boilerplate" functionality already implemented. You can instantiate, print, and compare dataclass instances straight out of the box. Many of the common things you do in a class can be reduced to a few basic instructions.</p>
<p>Dataclasses are implemented using a helpful and powerful Python tool called a <em>decorator</em>. A decorator is a function designed to wrap around (encapsulate) another function or class to alter or enhance the wrapped object's behavior. It lets you modify the behavior without permanently changing the object.</p>
<p>Decorators also let you avoid duplicating code when you're running the same process on multiple functions, such as checking memory use, adding logging, or testing performance.</p>
<h3>Decorator Basics</h3>
<p>To see how decorators work, let's define a function that squares a number. Then, we'll define a decorator function that squares that result. Enter the following in a text editor:</p>
<pre><code>def square_it(x):
    return x**2

def square_it_again(func):
    def wrapper(*args, **kwargs):
        result = (func(*args, **kwargs))**2
        return result
    return wrapper</code></pre>
<p>The first function, <code>square_it()</code>, takes a number, represented by x, and returns its square. The second function, <code>square_it_again()</code>, will serve as a decorator to the first function and is a little more complicated.</p>
<p>The decorator function has a <code>func</code> parameter, representing a function. Because functions are objects, you can pass a function to another function as an argument and even define a function within a function. When we <em>call</em> this decorator function, we'll pass it the <code>square_it()</code> function as an argument.</p>
<p>Next, we defined an inner function, which we called <code>wrapper()</code>. Because <code>square_it()</code> takes an argument, we need to set up the inner function to handle arguments by using the special positional and keyword arguments <code>*args</code> and <code>**kwargs</code>.</p>
<p>The <code>*args</code> and <code>**kwargs</code> syntax provide flexibility in handling variable numbers of arguments, both positional and keyword, in Python functions. The <code>*args</code> syntax in a function definition allows the function to accept any number of positional arguments. The <code>**kwargs</code> syntax allows a function to accept any number of keyword arguments. Combining both <code>*args</code> and <code>**kwargs</code> allows a function to accept any combination of positional and keyword arguments.</p>
<p>Within the <code>wrapper()</code> function, we called the function we passed to the decorator (<code>func</code>), squared its output, assigned the resulting number to the <code>result</code> variable, and returned <code>result</code>. Finally, we returned the <code>wrapper()</code> function.</p>
<p>To use the <code>square_it_again()</code> decorator, call it, pass it the function that you want to decorate (<code>square_it()</code>), and assign the result to a variable (<code>square</code>), which also represents a function:</p>
<pre><code>square = square_it_again(square_it)
print(type(square))</code></pre>
<pre><code>&lt;class 'function'&gt;</code></pre>
<p>You can now call the new function and pass it an appropriate argument:</p>
<pre><code>print(square(3))</code></pre>
<pre><code>81</code></pre>
<p>In this example, we <em>manually</em> called the decorator function. This demonstrated how decorators work, but it's a bit verbose and contorted. In the next section, we'll look at a more convenient method for using a decorator.</p>
<h3>Decorator Syntactic Sugar</h3>
<p>In computer science, <em>syntactic sugar</em> is clear, concise syntax that simplifies the language and makes it "sweeter" for human use. The syntactic sugar for a decorator is the @ symbol, which must be immediately followed by the name of the decorator function. The next line must be the definition statement for the function or class being wrapped, as follows:</p>
<pre><code>@decorator_func_name
def new_func():
    do something</code></pre>
<p>In this case, <code>decorator_func_name</code> represents the decorator function, and <code>new_func()</code> is the function being wrapped. A class definition can be substituted for the <code>def</code> statement.</p>
<p>To see how it works, let's re-create our number-squaring example from the beginning. We'll leave off assigning the <code>square</code> variable, as we don't need it anymore:</p>
<pre><code>def square_it_again(func):
    def wrapper(*args, **kwargs):
        result = (func(*args, **kwargs))**2
        return result
    return wrapper

@square_it_again
def square_it(x):
    return x**2

print(square_it(3))</code></pre>
<pre><code>81</code></pre>
<p>After defining our <code>square_it_again()</code> function again, we added the decorator and defined the <code>square_it()</code> function. After that, we called the <code>square_it()</code> function the same way we would if the decorator didn't exist.</p>
<p><strong>NOTE:</strong> when using the @ symbol, use the decorator function name <strong>without parentheses</strong>.</p>
<p>If decorators make your head spin a little, don't worry. If you can type <code>@dataclass</code>, you can use dataclasses. This decorator modifies regular Python classes so that you can define them using shorter and sweeter syntax.</p>
<h3>Demonstrating Dataclasses</h3>
<p>To see the benefits of dataclasses, let's define a <em>regular</em> class and then repeat the exercise using a <em>dataclass</em>. Our goal will be to make generic ship objects that we can track on a simulation grid. For each ship, we'll need to supply a name, a classification (like "frigate"), a country of registry, and a location.</p>
<h3>Defining Ship as a Regular Class</h3>
<p>To define a regular class called <code>Ship</code>, in a text editor, enter the following and then save it as <em>ship_tracker.py</em>:</p>
<pre><code>class Ship:
    def __init__(self, name, classification, registry, location):
        self.name = name
        self.classification = classification
        self.registry = registry
        self.location = location
        self.obj_type = 'ship'
        self.obj_color = 'black'</code></pre>
<p>The initialization method contains multiple parameters, such as a <code>name</code> and <code>registry</code>. These will need to be passed as arguments when instantiating an object based on this class.</p>
<p>Note how we're forced to duplicate code by repeating each parameter name, like <code>classification</code>, three times: once as a parameter and twice when assigning the instance attribute. The more data you need to pass to the method, the greater this redundancy.</p>
<p>In addition to the parameters passed to the initialization method, the <code>Ship</code> class includes two "fixed" attributes representing the object <em>type</em> and <em>color</em>. These are assigned using an equal sign, as with a regular class. Because these attributes are always the same for a given object, there's no need to pass them as arguments. Now, let's instantiate a new ship object. Enter the following, save the file, and run it:</p>
<pre><code>garcia = Ship('Garcia', 'frigate', 'USA', (20, 15))
print(garcia)</code></pre>
<pre><code>&lt;__main__.Ship object at 0x0000021F5FF501F0&gt;</code></pre>
<p>This created a US frigate named <code>garcia</code> at grid location <code>(20, 15)</code>. But when you print the object, the output isn't very helpful.</p>
<p>The issue here is that printing information on an object requires you to define additional <em>dunder methods</em>, like <code>__str__</code> and <code>__repr__</code>, that return string representations of objects for informational and debugging purposes.</p>
<p>Another useful method is <code>__eq__</code>, which lets you compare instances of a class. The list of special methods in Python is long, but a few basic examples are listed in the following table:</p>
<table>
<thead><tr><th>Special Method</th><th>Description</th></tr></thead>
<tbody>
<tr><td><code>__init__(self)</code></td><td>Called when initializing an object from a class.</td></tr>
<tr><td><code>__del__(self)</code></td><td>Called to destroy an object.</td></tr>
<tr><td><code>__repr__(self)</code></td><td>Returns a printable string for the object to use in debugging.</td></tr>
<tr><td><code>__str__(self)</code></td><td>Returns a string for pretty-printing useful information about an object. If not implemented, <code>__repr__</code> is used instead.</td></tr>
<tr><td><code>__eq__(self, other)</code></td><td>Performs an equal to (==) comparison of two objects.</td></tr>
</tbody>
</table>
<p>Defining these methods for each class you write can become a burden, which is where dataclasses come in. Dataclasses automatically handle the redundancy issues around attributes and dunder methods.</p>
<h3>Defining Ship as a Dataclass</h3>
<p>Now, let's define the <code>Ship</code> class again as a dataclass. Do this in a new file named <em>ship_tracker_dc.py</em> (for "ship tracker dataclass"):</p>
<pre><code>from math import dist
from dataclasses import dataclass

@dataclass
class Ship:
    name: str
    classification: str
    registry: str
    location: tuple
    obj_type = 'ship'
    obj_color = 'black'</code></pre>
<p>We started by importing the <code>math</code> and <code>dataclass</code> modules. We'll use the <code>dist</code> method from <code>math</code> to calculate the distance between ships, and <code>dataclass</code> to decorate our <code>Ship</code> class. (To use <code>dist</code>, you'll need Python 3.8 or higher).</p>
<p>Next, we prefixed <code>dataclass</code> with the @ symbol, to make it a decorator, and started defining the <code>Ship</code> class on the following line.</p>
<p>Normally, the next step would be to define the <code>__init__()</code> method with <code>self</code> and other parameters, but dataclasses don't need this. The initialization is handled behind the scenes, removing the need for this code. You'll still need to list the attributes, however, but with a lot less redundancy than before.</p>
<p>For each attribute that must be passed as an argument, we entered the attribute name, followed by a colon, followed by a <em>type hint</em>, or type <em>annotation</em>. A type hint tells people reading your code what types of data to expect. Static analysis tools can also use type hints to check your code for errors.</p>
<p>A class variable with a type hint is called a <em>field</em>. The <code>@dataclass</code> decorator examines classes to find fields. Without a type hint, the attribute won't become a field in the dataclass. In this example, all the fields in the <code>Ship</code> class use the string data type (<code>str</code>), except for <code>location</code>, which uses a tuple (for a pair of x and y coordinates).</p>
<p><strong>TIP:</strong> You can use default values with the type annotations. For example, <code>location: tuple = (0, 0)</code> will place new <code>Ship</code> objects at coordinates x = 0, y = 0 if none are specified when the object is created. When you use a default parameter, however, <strong>all subsequent parameters must have default values</strong>.</p>
<p>Because we don't need to pass the <code>obj_type</code> and <code>obj_color</code> attributes as arguments when creating a new object, we defined them using an equal sign rather than a colon, and with <em>no</em> type hints. By assigning them as we would in a regular class, every <code>Ship</code> object will, by default, be designated a "ship" and have a consistent color attribute for plotting.</p>
<p>Dataclasses can have methods, just like regular classes. Next, we'll define a method that calculates the Euclidian distance between two ships. Note that the <code>def</code> statement below is indented four spaces relative to the class definition:</p>
<pre><code>def distance_to(self, other):
    distance = round(dist(self.location, other.location), 2)
    return str(distance) + ' ' + 'km'</code></pre>
<p>The <code>distance_to()</code> method takes the current ship object and another ship object as arguments. It then uses the built-in <code>dist</code> method to get the distance between them. This method returns the Euclidean distance between two points (x and y), where x and y are the coordinates of that point. The distance is returned as a <em>string</em>, so we can include a reference to kilometers.</p>
<p>Now, in the global scope with no indentation, create three ship objects, passing them the following information:</p>
<pre><code>garcia = Ship('Garcia', 'frigate', 'USA', (20, 15))
ticonderoga = Ship('Ticonderoga', 'destroyer', 'USA', (5, 10))
kobayashi = Ship('Kobayashi', 'maru', 'Federation', (10, 22))</code></pre>
<p>If you're working in an IDE, such as Spyder, as soon as you begin entering the <code>Ship()</code> class arguments, a window should appear, prompting you on the proper inputs.</p>
<p>Because classes you create are legitimate datatypes in Python, they behave like built-in datatypes. As a result, IDEs like Spyder will use the type hints to guide you when creating the ship objects.</p>
<p>It's also worth noting that you don't need to use the correct data type for a parameter. Because Python is a <em>dynamically typed language</em> (meaning that variable types are <em>inferred</em> at runtime, not at compile-time, based on the value assigned) you can assign an integer as the classification argument, and the program will still run.</p>
<p><strong>TIP:</strong> Even though the Python interpreter ignores type hints, you can use third-party static type-checking tools, like Mypy, to analyze your code and check for errors before the program runs.</p>
<p>The <code>@dataclass</code> decorator is a code generator that automatically adds methods under the hood. This includes the <code>__repr__</code> method. This means that you now get useful information when you call <code>print(garcia)</code>:</p>
<pre><code>print(garcia)</code></pre>
<pre><code>Ship(name='Garcia', classification='frigate', registry='USA', location=(20, 15))</code></pre>
<p>Now, let's check that our data is there and that the method works. Add the following lines and rerun the script:</p>
<pre><code>ships = [garcia, ticonderoga, kobayashi]

for ship in ships:
    print(f"The {ship.classification} {ship.name} is visible.")
    print(f"{ship.name} is a {ship.registry} {ship.obj_type}.")
    print(f"The {ship.name} is currently at grid position {ship.location}\\n")
print(f"Garcia is {garcia.distance_to(kobayashi)} from the Kobayashi")</code></pre>
<pre><code>The frigate Garcia is visible.
Garcia is a USA ship.
The Garcia is currently at grid position (20, 15)

The destroyer Ticonderoga is visible.
Ticonderoga is a USA ship.
The Ticonderoga is currently at grid position (5, 10)

The maru Kobayashi is visible.
Kobayashi is a Federation ship.
The Kobayashi is currently at grid position (10, 22)

Garcia is 12.21 km from the Kobayashi</code></pre>
<p>By putting the ship objects in a list, we were able to loop through the list, access attributes using dot notation, and print the results.</p>
<p>The <code>Ship</code> dataclass lets you instantiate a ship object and store data such as the ship's name and location in type-annotated fields. By reducing redundancy and automatically generating required class methods such as <code>__init__()</code> and <code>__repr__()</code>, the <code>@dataclass</code> decorator lets you produce code that's easier to read and write.</p>
<p><strong>FYI:</strong> The <code>@classmethod</code> and <code>@staticmethod</code> decorators let you define methods inside a class namespace that are not connected to a particular instance of that class. Neither of these are commonly used and can often be replaced with regular functions. You should be aware of their existence, however, as they're often mentioned in OOP tutorials and can be useful in some cases.</p>
<h3>Plotting with the Ship Dataclass</h3>
<p>To get a better feel for how you might use OOP, let's take this project a step further and plot our ship objects on a grid. To plot the ships, we'll use the Matplotlib plotting library.</p>
<p>In a text editor, save or copy your <em>ship_tracker_dc.py</em> file to a new file called <em>ship_display.py</em> and edit it as follows:</p>
<pre><code>from math import dist
from dataclasses import dataclass
import matplotlib.pyplot as plt

@dataclass
class Ship:
    name: str
    classification: str
    registry: str
    location: tuple
    obj_type = 'ship'
    obj_color = 'black'

    def distance_to(self, other):
        distance = round(dist(self.location, other.location), 2)
        return str(distance) + ' ' + 'km'

garcia = Ship('Garcia', 'frigate', 'USA', (20, 15))
ticonderoga = Ship('Ticonderoga', 'destroyer', 'USA', (5, 10))
kobayashi = Ship('Kobayashi', 'maru', 'Federation', (10, 22))

VISIBLE_SHIPS = [garcia, ticonderoga, kobayashi]

def plot_ship_dist(ship1, ship2):
    sep = ship1.distance_to(ship2)
    for ship in VISIBLE_SHIPS:
        plt.scatter(x=ship.location[0],
                     y=ship.location[1],
                     marker='d',
                     color=ship.obj_color)
        plt.text(ship.location[0], ship.location[1], ship.name)
    plt.plot([ship1.location[0], ship2.location[0]],
              [ship1.location[1], ship2.location[1]],
              color='gray',
              linestyle="--")
    plt.text((ship2.location[0]),
              (ship2.location[1] - 2),
              sep,
              c='gray')
    plt.xlim(0, 30)
    plt.ylim([0, 30])
    plt.show()

plot_ship_dist(kobayashi, garcia)</code></pre>
<p>We started by adding a line to import Matplotlib. After instantiating the three ship objects, we replaced the remaining code starting at <code>VISIBLE_SHIPS</code>. This line assigned a list of the three ship objects that represent the ships you can see on the simulation grid. We treated this as a constant, hence the all-caps format.</p>
<p>Next, we defined a function for calculating the distance between two ships (<code>ship1</code> and <code>ship2</code>) and for plotting all the visible ships. We called the <code>Ship</code> class's <code>distance_to()</code> method on the two ships, assigned the result to a variable named <code>sep</code> (for separation), and then looped through the visible list, plotting each ship in a scatterplot. For this, Matplotlib needs the ship's x and y locations, a marker style ('d' represents a diamond shape), and a color (the <code>ship.obj_color</code> attribute).</p>
<p>Next, we used Matplotlib's <code>plt.plot()</code> method to draw a dashed line between the ships used for the distance measurement. This method takes the x–y locations of each ship, a color, and a line style. We followed this with the <code>plt.text()</code> method, for adding text to the plot. As arguments, we passed it a location, the <code>sep</code> variable, and a color.</p>
<p>We completed the function by setting x and y limits to the plot and then calling the <code>plt.show()</code> method to display the plot.</p>
<p>Back in the global scope, we called the <code>plot_ship_dist()</code> function and passed it the <code>kobayashi</code> and <code>garcia</code> ship objects.</p>
<p>After saving and running the file, you should see a plot like the one below:</p>
<img src="/media/lesson_images/classes_dataclasses_ship_plot.png" alt="Scatter plot of the Garcia, Ticonderoga, and Kobayashi ship objects on a 30x30 grid, with a dashed line and distance label between Garcia and Kobayashi" style="max-width: 100%;" />
<p>Bundling data and methods into dataclasses produces compact, intuitive objects that you can manipulate <em>en masse</em>. Thanks to OOP, we could easily generate and track a multitude of ship objects on our grid.</p>
<h3>Using Fields and Post-Init Processing</h3>
<p>Sometimes you'll want to initialize an attribute that depends on the value of another attribute. Because this other attribute must already exist, you'll need to initialize the second attribute outside the <code>__init__</code> function. Fortunately, Python comes with the built-in <code>__post_init__</code> function that's expressly designed for this purpose.</p>
<p>Let's look at an example based on a naval war game simulation. Because alliances can change through time, a ship registered to a certain country might switch from ally to enemy. Although the <code>registry</code> attribute is <em>fixed</em>, its allegiance is <em>uncertain</em>, and you might want to evaluate its friend-or-foe status <em>post-initialization</em>.</p>
<p>To create a version of the <code>Ship</code> dataclass that accommodates this need, in the text editor, enter the following and then save it as <em>ship_allegiance_post_init.py</em>:</p>
<pre><code>from dataclasses import dataclass, field

@dataclass
class Ship:
    name: str
    classification: str
    registry: str
    location: tuple
    obj_type = 'ship'
    obj_color = 'black'
    friendly: bool = field(init=False)

    def __post_init__(self):
        unfriendlies = ('IKS')
        self.friendly = self.registry not in unfriendlies</code></pre>
<p>In this case, we started by importing both <code>dataclass</code> and <code>field</code> from the <code>dataclasses</code> module. The <code>field</code> method helps you change various properties of attributes in the dataclass, such as by providing them with default values.</p>
<p>Next, we initialized the <code>Ship</code> class like we did in the <em>ship_tracker_dc.py</em> program, except that we added a new attribute, <code>friendly</code>, that's set to a Boolean data type with a default value of <code>False</code>. Note that we set this default value by calling the <code>field</code> method and using the keyword argument <code>init</code>.</p>
<p>We defined the <code>__post_init__()</code> method with <code>self</code> as a parameter. We then assigned a tuple of unfriendly registry designations to a variable named <code>unfriendlies</code>.</p>
<p>Finally, we assigned <code>True</code> or <code>False</code> to the <code>self.friendly</code> attribute by checking whether the current object's <code>self.registry</code> attribute is present in the <code>unfriendlies</code> tuple.</p>
<p>Let's test it out by making two ships, one friendly and one unfriendly. Note that you don't pass the <code>Ship</code> class an argument for the <code>friendly</code> attribute; this is because it uses a default value and is ultimately determined by the <code>__post_init__()</code> method:</p>
<pre><code>homer = Ship('Homer', 'tug', 'USA', (20, 9))
bortas = Ship('Bortas', 'D5', 'IKS', (15, 25))
print(homer)
print(bortas)</code></pre>
<pre><code>Ship(name='Homer', classification='tug', registry='USA', location=(20, 9), friendly=True)
Ship(name='Bortas', classification='D5', registry='IKS', location=(15, 25), friendly=False)</code></pre>
<p>You may have noticed that you didn't need to explicitly call the <code>__post_init__()</code> method. This is because the dataclass-generated <code>__init__()</code> code calls the method automatically if it's defined in the class.</p>
<p><strong>TIP:</strong> Inheritance (mostly) works the same with dataclasses as with regular classes. One thing to be careful of is that dataclasses combine attributes in a way that prevents the use of attributes with defaults in a parent class when a child contains attributes without defaults. So, you'll want to avoid setting field defaults on classes that are to be used as base classes.</p>
<h3>Optimizing Dataclasses with __slots__</h3>
<p>If you're using a dataclass for storing lots of data, or if you expect to instantiate thousands to millions of objects from a single class, you should consider using the class variable <code>__slots__</code>. This special attribute optimizes the performance of a class by decreasing both memory consumption and the time it takes to access attributes.</p>
<p>A regular class stores instance attributes in an internally managed dictionary named <code>__dict__</code>. The <code>__slots__</code> variable stores them using highly efficient, array-related data structures implemented in the C programming language.</p>
<p>Here's an example using a standard dataclass called <code>Ship</code>, followed by a <code>ShipSlots</code> dataclass that uses <code>__slots__</code>. Enter this code in a text editor and save it as <em>ship_slots.py</em>:</p>
<pre><code>from dataclasses import dataclass

@dataclass
class Ship:
    name: str
    classification: str
    registry: str
    location: tuple

@dataclass
class ShipSlots:
    __slots__ = 'name', 'classification', 'registry', 'location'
    name: str
    classification: str
    registry: str
    location: tuple</code></pre>
<p>The only difference between the two class definitions is the assignment of a tuple of attribute names to the <code>__slots__</code> variable. This variable lets you explicitly state which instance attributes you expect your objects to have.</p>
<p>Now, instead of having a <em>dynamic dictionary</em> (<code>__dict__</code>) that permits you to add attributes to objects after the creation of an object, you have a <em>static structure</em> that saves the overhead of one dictionary for every object that uses <code>__slots__</code>. Because it's considered good practice to initialize all of an object's attributes at once, the inability to dynamically add attributes with <code>__slots__</code> is not necessarily a detriment.</p>
<p>Using <code>__slots__</code> with multiple inheritance can become problematic, however. Likewise, you'll want to avoid using it when providing default values via class attributes for instance variables. You can find more caveats in the official docs and a Stack Overflow answer on the topic.</p>
<h3>The Recap</h3>
<p>Object-oriented programming helps you organize code while reducing its redundancy. Classes let you combine related data — and functions that act on that data — into new custom data types.</p>
<p>Functions in OOP are called <em>methods</em>. When you define a class using a class statement, you couple related elements together so that the relationship between the data and the methods is clear, and so the proper methods are used with the appropriate data. Consequently, you'll want to consider using classes when you have multiple kinds of data, multiple functions that go with each kind of data, and a growing codebase that's becoming increasingly complex.</p>
<p>A class serves as a template or factory for making objects, also called <em>instances</em> of a class. You create objects by calling the class's name using function notation. As with regular functions, this practice introduces a new local name scope, and all names assigned in the class statement generate object attributes shared by all instances of the class. Attributes store data, and each object's attributes might change over time to reflect changes in the object's state.</p>
<p>Classes can <em>inherit</em> attributes and methods from other classes, letting you reuse code. In this case, the new class is a <em>child</em> or <em>subclass</em>, and the preexisting class is the <em>parent</em> or <em>base class</em>. Inherited attributes and methods can be overwritten in the subclass to modify or enhance the inherited behaviors.</p>
<p>The built-in <code>super()</code> function is a shorthand way to create subclasses that are easy to maintain. With <code>super()</code>, you can also call original methods from a base class if they've been modified in the subclass. Because Python lets classes inherit from multiple parents, this can result in complex code that's difficult to understand, so use <code>super()</code> with caution.</p>
<p><em>Decorators</em> are functions that modify the behavior of another function without permanently changing the modified function. They also help you avoid duplicating code.</p>
<p>The <code>@dataclass</code> decorator decorates class statements and makes them more concise. Although dataclasses were designed for classes that mainly store data, they can still be used as regular classes. A nice feature is that IDEs like Spyder will use the dataclass fields to prompt users with the proper class names, arguments, methods, and documentation, removing the need to see all of the class definition code. A downside, however, is that the use of multiple inheritance can be more difficult with dataclasses than with regular classes.</p>
<p>The <code>__slots__</code> class variable optimizes both memory usage and attribute access speeds. It comes with some limitations, however, such as, but not limited to, the inability to dynamically create attributes after initialization and increased complexity when using multiple inheritance.</p>
<p>One thing we didn't touch on here is that you can combine related class statements and save them as Python files. These class libraries then can be imported into other programs as modules, just like you imported the <code>dataclass</code> module.</p>
<p>There's a lot more to OOP than what we've covered here — it is the whole damn jungle, after all. If you think your projects would benefit from OOP and want to explore the topic further, you can find the official Python tutorial on classes <a href="https://docs.python.org/3/tutorial/classes.html">here</a>, the official dataclass documentation <a href="https://docs.python.org/3/library/dataclasses.html">here</a>, and the <a href="https://peps.python.org/pep-0557/">PEP 557</a> dataclass enhancement proposal <a href="https://peps.python.org/pep-0557/">here</a>.</p>
<p><em>Adapted from "Introducing Python Classes and Dataclasses" by Lee Vaughan, TDS Archive (Medium), Jan 23, 2024.</em></p>'''
            }
        )
        self._add_quiz(l1_3_1, [
            ("What decorator eliminates boilerplate by auto-generating __init__, __repr__, and __eq__?", [
                ("@property", False), ("@dataclass", True),
                ("@staticmethod", False), ("@classmethod", False)]),
            ("In the Elf class example, what makes pointed_ears different from attributes like name and attack?", [
                ("It's a class attribute, defined at the class level and shared by every elf", True),
                ("It's set inside __init__ like the other attributes", False),
                ("It only exists on the Elden subclass, not the base Elf class", False),
                ("It stores a reference to a method, not a value", False)]),
            ("According to the lesson, dataclasses were introduced in which Python version?", [
                ("Python 2.7", False), ("Python 3.0", False),
                ("Python 3.7+", True), ("Python 3.10+", False)]),
            ("In the Ship allegiance example, why is the friendly attribute defined with field(init=False)?", [
                ("Because its value is computed in __post_init__ from the registry attribute, not passed in when creating the object", True),
                ("Because Boolean fields can't have default values", False),
                ("To make the attribute immutable once set", False),
                ("Because __slots__ requires every field to declare init=False", False)]),
            ("According to the lesson, what's the main criticism of using super()?", [
                ("It makes code less explicit, which violates \"Explicit is better than implicit\"", True),
                ("It doesn't work with single inheritance", False),
                ("It can't be used to override a method", False),
                ("It permanently changes the base class it's called on", False)]),
        ])
        l1_3_2, _ = Lesson.objects.get_or_create(
            chapter=ch1_3,
            title='DataFrames',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>DataFrames</h2>
<p>A DataFrame is the primary data structure in Pandas - think of it as a programmable spreadsheet with labelled rows and columns.</p>
<h3>Creating a DataFrame</h3>
<pre><code>import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "score": [88, 92, 75]
}

df = pd.DataFrame(data)
print(df)</code></pre>
<h3>Common Operations</h3>
<pre><code># Select a column
df["age"]

# Filter rows
df[df["score"] > 80]

# Add a new column
df["passed"] = df["score"] >= 80

# Summary statistics
df.describe()</code></pre>
<p>DataFrames make it easy to clean, transform, filter, and aggregate tabular data - the bread and butter of data science work.</p>'''
            }
        )
        self._add_quiz(l1_3_2, [
            ("What is a DataFrame described as in the lesson?", [
                ("A one-dimensional array", False),
                ("A programmable spreadsheet with labelled rows and columns", True),
                ("A type of Python list", False), ("A SQL database engine", False)]),
            ("Which code correctly filters rows where the score column is greater than 80?", [
                ("df.score > 80", False), ("df[df[\"score\"] > 80]", True),
                ("df.filter(score > 80)", False), ("df[\"score\"].where(80)", False)]),
            ("What does df.describe() provide?", [
                ("Summary statistics", True), ("A list of duplicate rows", False),
                ("The file path of the data", False), ("A count of missing values only", False)]),
            ("In the lesson's example, how is a new \"passed\" column added based on the score column?", [
                ("df.add(\"passed\")", False), ("df[\"passed\"] = df[\"score\"] >= 80", True),
                ("df.passed = True", False), ("df.new_column(\"passed\", 80)", False)]),
        ])
        l1_3_3, _ = Lesson.objects.get_or_create(
            chapter=ch1_3,
            title='Functions',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Functions in Python</h2>
<p>Functions let you encapsulate reusable logic. In data science, they help you keep analysis code modular and testable.</p>
<h3>Defining Functions</h3>
<pre><code>def calculate_mean(values):
    """Return the arithmetic mean of a list of numbers."""
    return sum(values) / len(values)

data = [10, 20, 30, 40, 50]
print(calculate_mean(data))  # 30.0</code></pre>
<h3>Lambda Functions</h3>
<p>Short, anonymous functions useful for quick transformations:</p>
<pre><code>double = lambda x: x * 2
print(double(5))  # 10

# Common with Pandas
df["age_dog_years"] = df["age"].apply(lambda x: x * 7)</code></pre>
<h3>Docstrings and Type Hints</h3>
<pre><code>def normalise(values: list[float]) -> list[float]:
    """Scale values to the 0-1 range."""
    min_val, max_val = min(values), max(values)
    return [(v - min_val) / (max_val - min_val) for v in values]</code></pre>
<p>Good documentation and type hints make your code easier for teammates (and future you) to understand.</p>'''
            }
        )
        self._add_quiz(l1_3_3, [
            ("What does the calculate_mean function in the lesson return for the list [10, 20, 30, 40, 50]?", [
                ("25.0", False), ("30.0", True), ("150", False), ("50.0", False)]),
            ("In the lesson's Pandas example, what does df[\"age\"].apply(lambda x: x * 7) do?", [
                ("Filters ages over 7", False), ("Multiplies each age value by 7", True),
                ("Divides each age by 7", False), ("Adds 7 to the DataFrame", False)]),
            ("What is the purpose of a docstring, as shown in the normalise function example?", [
                ("To declare variable types", False), ("To document what the function does", True),
                ("To improve performance", False), ("To catch errors automatically", False)]),
            ("What does the type hint list[float] in normalise(values: list[float]) -> list[float] indicate?", [
                ("The function takes and returns a list of floats", True),
                ("The function only works with a single float", False),
                ("The function returns a string", False), ("The function is deprecated", False)]),
        ])
        l1_3_4, _ = Lesson.objects.get_or_create(
            chapter=ch1_3,
            title='Data Preparation',
            defaults={
                'order': 4,
                'is_free': False,
                'content': '''<h2>Data Preparation</h2>
<p>Raw data is almost never ready for analysis. Data preparation - sometimes called data wrangling - is the process of cleaning and transforming data into a usable format.</p>
<h3>Common Tasks</h3>
<ul>
<li><strong>Handling missing values</strong> - drop rows, fill with a default, or impute using statistics</li>
<li><strong>Removing duplicates</strong> - exact-match deduplication</li>
<li><strong>Data type conversion</strong> - strings to dates, objects to categories</li>
<li><strong>Outlier detection</strong> - identifying values that fall far from the norm</li>
</ul>
<h3>Example: Cleaning a Dataset</h3>
<pre><code>import pandas as pd

df = pd.read_csv("raw_sales.csv")

# Drop rows where critical fields are missing
df = df.dropna(subset=["price", "date"])

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Remove duplicates
df = df.drop_duplicates()

# Flag outliers using IQR
q1 = df["price"].quantile(0.25)
q3 = df["price"].quantile(0.75)
iqr = q3 - q1
df = df[(df["price"] >= q1 - 1.5 * iqr) & (df["price"] <= q3 + 1.5 * iqr)]</code></pre>
<p>Data scientists often spend 60-80% of their time on data preparation. Getting this right is critical - garbage in, garbage out.</p>'''
            }
        )
        self._add_quiz(l1_3_4, [
            ("According to the lesson, what percentage of a data scientist's time is often spent on data preparation?", [
                ("10-20%", False), ("30-40%", False), ("60-80%", True), ("90-100%", False)]),
            ("In the example, what does df.dropna(subset=[\"price\", \"date\"]) do?", [
                ("Drops rows where price or date is missing", True),
                ("Drops the price and date columns entirely", False),
                ("Fills missing prices with the median", False), ("Converts price and date to strings", False)]),
            ("What method is used in the example to detect outliers?", [
                ("Standard deviation only", False), ("IQR (interquartile range)", True),
                ("Correlation matrix", False), ("Regression residuals", False)]),
            ("What is the common term for the process of cleaning and transforming raw data into a usable format?", [
                ("Data mining", False), ("Data wrangling", True),
                ("Data warehousing", False), ("Data encryption", False)]),
        ])

        # ──────────────────────────────────────────────
        # Course 2: Data Science Math & Statistics
        # ──────────────────────────────────────────────
        course2, _ = Course.objects.get_or_create(
            title='Data Science Math & Statistics',
            defaults={
                'description': 'Build the mathematical and statistical foundation needed for data science - from linear functions to correlation analysis.',
                'is_published': True,
            }
        )

        # Chapter 1: Math Foundations
        ch2_1, _ = Chapter.objects.get_or_create(
            course=course2,
            title='Math Foundations',
            defaults={'order': 1, 'description': 'Essential math concepts for data analysis'}
        )
        l2_1_1, _ = Lesson.objects.get_or_create(
            chapter=ch2_1,
            title='Linear Functions',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Linear Functions</h2>
<p>A linear function describes a straight-line relationship between two variables. It is the building block of many data science models.</p>
<h3>The Equation</h3>
<p>A linear function is written as:</p>
<pre><code>y = mx + b</code></pre>
<ul>
<li><strong>y</strong> - the output (dependent variable)</li>
<li><strong>x</strong> - the input (independent variable)</li>
<li><strong>m</strong> - the slope (how much y changes per unit of x)</li>
<li><strong>b</strong> - the y-intercept (value of y when x = 0)</li>
</ul>
<h3>Example</h3>
<p>If a company charges a $50 base fee plus $20 per hour for consulting:</p>
<pre><code>def total_cost(hours):
    return 20 * hours + 50

print(total_cost(5))  # $150</code></pre>
<p>Linear functions appear everywhere in data science: linear regression, feature scaling, and even as activation functions in simple neural networks.</p>'''
            }
        )
        self._add_quiz(l2_1_1, [
            ("In the linear equation y = mx + b, what does 'm' represent?", [
                ("The y-intercept", False), ("The slope", True),
                ("The output variable", False), ("The error term", False)]),
            ("In the consulting example, what is the base fee before any hourly charges?", [
                ("$20", False), ("$50", True), ("$100", False), ("$150", False)]),
            ("According to the example function total_cost(hours) = 20 * hours + 50, what is the cost for 5 hours?", [
                ("$100", False), ("$120", False), ("$150", True), ("$170", False)]),
            ("What does 'b' represent in y = mx + b?", [
                ("The slope", False), ("The value of y when x = 0", True),
                ("The independent variable", False), ("The number of data points", False)]),
        ])
        l2_1_2, _ = Lesson.objects.get_or_create(
            chapter=ch2_1,
            title='Plotting Functions',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>Plotting Functions</h2>
<p>Visualising mathematical functions helps you understand their behaviour and communicate relationships in data.</p>
<h3>Plotting with Matplotlib</h3>
<pre><code>import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 100)
y = 2 * x + 3  # Linear function

plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("y = 2x + 3")
plt.grid(True)
plt.show()</code></pre>
<h3>Different Function Shapes</h3>
<ul>
<li><strong>Linear:</strong> y = 2x + 3 (straight line)</li>
<li><strong>Quadratic:</strong> y = x² (parabola)</li>
<li><strong>Exponential:</strong> y = 2^x (rapid growth)</li>
<li><strong>Logarithmic:</strong> y = log(x) (diminishing returns)</li>
</ul>
<h3>Why It Matters</h3>
<p>Plotting helps you spot trends, outliers, and the shape of your data before building models. A scatter plot can reveal whether a linear model is appropriate or if you need something more complex.</p>'''
            }
        )
        self._add_quiz(l2_1_2, [
            ("Which Matplotlib function is used to display a plotted figure, per the lesson's example?", [
                ("plt.render()", False), ("plt.show()", True),
                ("plt.display()", False), ("plt.output()", False)]),
            ("Which function shape is described as \"rapid growth\"?", [
                ("Linear", False), ("Quadratic", False), ("Exponential", True), ("Logarithmic", False)]),
            ("What does np.linspace(-10, 10, 100) do in the example?", [
                ("Creates 100 evenly spaced values between -10 and 10", True),
                ("Creates a plot title", False), ("Draws a grid", False), ("Filters outliers", False)]),
            ("According to the lesson, what can a scatter plot help you decide?", [
                ("Whether a linear model is appropriate for the data", True),
                ("The exact regression coefficients", False),
                ("The sample size needed", False), ("The database schema", False)]),
        ])
        l2_1_3, _ = Lesson.objects.get_or_create(
            chapter=ch2_1,
            title='Slope and Intercept',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Slope and Intercept</h2>
<p>The slope and intercept of a line tell you the rate of change and the starting point of a relationship.</p>
<h3>Slope (m)</h3>
<p>The slope measures how much y changes for each one-unit increase in x:</p>
<pre><code>m = (y2 - y1) / (x2 - x1)</code></pre>
<p>A positive slope means y increases as x increases. A negative slope means y decreases.</p>
<h3>Y-Intercept (b)</h3>
<p>The y-intercept is the value of y when x = 0 - where the line crosses the vertical axis.</p>
<h3>Calculating with Python</h3>
<pre><code>x = [1, 2, 3, 4, 5]
y = [3, 5, 7, 9, 11]

# Slope
n = len(x)
m = (n * sum(xi*yi for xi, yi in zip(x, y)) - sum(x) * sum(y)) / \
    (n * sum(xi**2 for xi in x) - sum(x)**2)

# Intercept
b = (sum(y) - m * sum(x)) / n

print(f"y = {m}x + {b}")  # y = 2.0x + 1.0</code></pre>
<p>In linear regression, the algorithm finds the slope and intercept that minimise the distance between the line and the actual data points.</p>'''
            }
        )
        self._add_quiz(l2_1_3, [
            ("What does the slope formula m = (y2 - y1) / (x2 - x1) calculate?", [
                ("The average of x and y", False), ("The rate of change of y per unit of x", True),
                ("The y-intercept", False), ("The correlation coefficient", False)]),
            ("What does a negative slope indicate?", [
                ("y increases as x increases", False), ("y decreases as x increases", True),
                ("There is no relationship", False), ("The line is vertical", False)]),
            ("In the Python example, what values are computed for m and b?", [
                ("m = 1.0, b = 2.0", False), ("m = 2.0, b = 1.0", True),
                ("m = 0, b = 0", False), ("m = 3.0, b = 5.0", False)]),
            ("In linear regression, what does the algorithm find, according to the lesson?", [
                ("The mean and median of the data", False),
                ("The slope and intercept that minimise distance to the data points", True),
                ("The maximum value only", False), ("The number of outliers", False)]),
        ])

        # Chapter 2: Statistics Fundamentals
        ch2_2, _ = Chapter.objects.get_or_create(
            course=course2,
            title='Statistics Fundamentals',
            defaults={'order': 2, 'description': 'Statistical concepts for analysing and interpreting data'}
        )
        l2_2_1, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Introduction to Statistics',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Introduction to Statistics</h2>
<p>Statistics is the science of collecting, organising, analysing, and interpreting data. It is the backbone of data science.</p>
<h3>Two Branches</h3>
<ul>
<li><strong>Descriptive statistics</strong> - summarise and describe features of a dataset (mean, median, charts)</li>
<li><strong>Inferential statistics</strong> - draw conclusions about a population from a sample (hypothesis testing, confidence intervals)</li>
</ul>
<h3>Population vs Sample</h3>
<p>The <strong>population</strong> is the entire group you want to study. A <strong>sample</strong> is a subset of that group. Since studying entire populations is usually impractical, we collect samples and use statistics to make inferences.</p>
<h3>Key Terminology</h3>
<table>
<thead><tr><th>Term</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Variable</td><td>A characteristic that can vary (e.g., age, income)</td></tr>
<tr><td>Observation</td><td>A single data point or row in a dataset</td></tr>
<tr><td>Distribution</td><td>The pattern of how values are spread across a range</td></tr>
<tr><td>Outlier</td><td>A value significantly different from most other observations</td></tr>
</tbody>
</table>'''
            }
        )
        self._add_quiz(l2_2_1, [
            ("Which branch of statistics summarises and describes features of a dataset, like mean and median?", [
                ("Inferential statistics", False), ("Descriptive statistics", True),
                ("Predictive statistics", False), ("Applied statistics", False)]),
            ("What is a \"sample\" in statistics, per the lesson?", [
                ("The entire group being studied", False), ("A subset of the population", True),
                ("A type of chart", False), ("A statistical error", False)]),
            ("According to the lesson's terminology table, what is an \"observation\"?", [
                ("A characteristic that can vary", False), ("A single data point or row in a dataset", True),
                ("The spread of values", False), ("A value very different from others", False)]),
            ("Why do we typically collect samples rather than study entire populations?", [
                ("Samples are always more accurate", False),
                ("Studying entire populations is usually impractical", True),
                ("Populations don't have variability", False), ("Samples eliminate the need for statistics", False)]),
        ])
        l2_2_2, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Percentiles',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>Percentiles</h2>
<p>Percentiles tell you the value below which a given percentage of observations fall. They are useful for understanding the spread and relative standing of data points.</p>
<h3>Common Percentiles</h3>
<ul>
<li><strong>25th percentile (Q1)</strong> - 25% of data falls below this value</li>
<li><strong>50th percentile (Median)</strong> - the midpoint of the data</li>
<li><strong>75th percentile (Q3)</strong> - 75% of data falls below this value</li>
</ul>
<h3>Calculating Percentiles</h3>
<pre><code>import numpy as np

salaries = [35000, 42000, 48000, 55000, 60000, 72000, 85000, 95000, 120000, 200000]

p25 = np.percentile(salaries, 25)
p50 = np.percentile(salaries, 50)
p75 = np.percentile(salaries, 75)

print(f"25th: ${p25:,.0f}")  # $48,750
print(f"50th: ${p50:,.0f}")  # $66,000
print(f"75th: ${p75:,.0f}")  # $101,250</code></pre>
<h3>The Interquartile Range (IQR)</h3>
<p>The IQR is Q3 minus Q1 - it captures the middle 50% of data and is a robust measure of spread that is not affected by outliers.</p>
<pre><code>iqr = p75 - p25  # $52,500</code></pre>'''
            }
        )
        self._add_quiz(l2_2_2, [
            ("What does the 50th percentile represent?", [
                ("The lowest value", False), ("The median", True),
                ("The highest value", False), ("The mean", False)]),
            ("In the lesson's salary example, what is the computed 50th percentile?", [
                ("$48,750", False), ("$66,000", True), ("$101,250", False), ("$52,500", False)]),
            ("What does the IQR (interquartile range) measure?", [
                ("The full range of the dataset", False), ("The middle 50% of the data", True),
                ("The standard deviation", False), ("The correlation between variables", False)]),
            ("Which NumPy function is used to calculate percentiles in the lesson?", [
                ("np.mean()", False), ("np.percentile()", True),
                ("np.median()", False), ("np.quantile_range()", False)]),
        ])
        l2_2_3, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Standard Deviation',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Standard Deviation</h2>
<p>Standard deviation measures how spread out values are from the mean. A low standard deviation means data points cluster tightly around the average; a high one means they are widely dispersed.</p>
<h3>Formula</h3>
<pre><code>σ = √( Σ(xᵢ - μ)² / N )</code></pre>
<p>Where μ is the mean, xᵢ is each value, and N is the number of observations.</p>
<h3>Python Example</h3>
<pre><code>import numpy as np

test_scores = [78, 82, 85, 88, 90, 92, 95, 98, 100, 65]

mean = np.mean(test_scores)
std_dev = np.std(test_scores)

print(f"Mean: {mean}")       # 87.3
print(f"Std Dev: {std_dev:.2f}")  # 10.02</code></pre>
<h3>The 68-95-99.7 Rule</h3>
<p>For normally distributed data:</p>
<ul>
<li>~68% of values fall within 1 standard deviation of the mean</li>
<li>~95% fall within 2 standard deviations</li>
<li>~99.7% fall within 3 standard deviations</li>
</ul>
<p>This rule helps you quickly assess whether a value is typical or unusual.</p>'''
            }
        )
        self._add_quiz(l2_2_3, [
            ("What does a low standard deviation indicate about a dataset?", [
                ("Values are widely dispersed", False), ("Values cluster tightly around the mean", True),
                ("The dataset has no mean", False), ("The dataset contains only outliers", False)]),
            ("According to the 68-95-99.7 rule, approximately what percentage of values fall within 2 standard deviations of the mean for normally distributed data?", [
                ("68%", False), ("95%", True), ("99.7%", False), ("100%", False)]),
            ("In the lesson's Python example, what standard deviation is computed for the test scores?", [
                ("87.3", False), ("10.02", True), ("100", False), ("65", False)]),
            ("Which NumPy function computes standard deviation directly?", [
                ("np.mean()", False), ("np.std()", True), ("np.var()", False), ("np.percentile()", False)]),
        ])
        l2_2_4, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Variance',
            defaults={
                'order': 4,
                'is_free': False,
                'content': '''<h2>Variance</h2>
<p>Variance is the average of the squared differences from the mean. It quantifies how much a dataset spreads out - standard deviation is simply the square root of variance.</p>
<h3>Formula</h3>
<pre><code>σ² = Σ(xᵢ - μ)² / N</code></pre>
<h3>Population vs Sample Variance</h3>
<ul>
<li><strong>Population variance (σ²)</strong> - divides by N (when you have all data)</li>
<li><strong>Sample variance (s²)</strong> - divides by N-1 (when working with a sample, to correct bias)</li>
</ul>
<pre><code>import numpy as np

data = [4, 8, 6, 5, 3, 7, 9, 2, 10, 1]

pop_var = np.var(data)        # Population variance
sample_var = np.var(data, ddof=1)  # Sample variance

print(f"Population variance: {pop_var}")   # 7.7
print(f"Sample variance: {sample_var:.2f}")  # 8.56</code></pre>
<h3>Why Square the Differences?</h3>
<p>Squaring ensures positive and negative deviations don't cancel each other out. However, it also means variance is expressed in squared units (e.g., dollars squared), which is why we prefer standard deviation for interpretation.</p>'''
            }
        )
        self._add_quiz(l2_2_4, [
            ("What is the relationship between variance and standard deviation?", [
                ("They are unrelated", False), ("Standard deviation is the square root of variance", True),
                ("Variance is always larger than the mean", False),
                ("Variance is the square root of standard deviation", False)]),
            ("What divisor does sample variance use to correct bias, compared to population variance?", [
                ("N", False), ("N-1", True), ("N+1", False), ("2N", False)]),
            ("In the lesson's NumPy example, what argument gives the sample variance instead of population variance?", [
                ("ddof=0", False), ("ddof=1", True), ("bias=True", False), ("sample=True", False)]),
            ("Why does the formula square the differences from the mean?", [
                ("To make the result negative", False),
                ("To prevent positive and negative deviations from cancelling out", True),
                ("To convert the units to dollars", False), ("To simplify computation only", False)]),
        ])
        l2_2_5, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Correlation',
            defaults={
                'order': 5,
                'is_free': False,
                'content': '''<h2>Correlation</h2>
<p>Correlation measures the strength and direction of the linear relationship between two variables. It ranges from -1 to +1.</p>
<h3>Interpreting Correlation</h3>
<table>
<thead><tr><th>Value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>+1</td><td>Perfect positive relationship</td></tr>
<tr><td>0</td><td>No linear relationship</td></tr>
<tr><td>-1</td><td>Perfect negative relationship</td></tr>
</tbody>
</table>
<h3>Pearson Correlation Coefficient</h3>
<pre><code>import numpy as np

hours_studied = [2, 3, 5, 7, 8, 10]
exam_score    = [55, 60, 70, 78, 85, 92]

corr = np.corrcoef(hours_studied, exam_score)[0, 1]
print(f"Correlation: {corr:.3f}")  # 0.994 (very strong positive)</code></pre>
<h3>Visualising with a Scatter Plot</h3>
<pre><code>import matplotlib.pyplot as plt

plt.scatter(hours_studied, exam_score)
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.title("Study Time vs Exam Performance")
plt.show()</code></pre>
<p>A strong positive correlation suggests that more study time is associated with higher scores - but remember, correlation does not prove causation.</p>'''
            }
        )
        self._add_quiz(l2_2_5, [
            ("What is the range of the Pearson correlation coefficient?", [
                ("0 to 1", False), ("-1 to +1", True), ("-100 to +100", False), ("0 to 100", False)]),
            ("What does a correlation of 0 indicate?", [
                ("A perfect positive relationship", False), ("A perfect negative relationship", False),
                ("No linear relationship", True), ("An error in calculation", False)]),
            ("In the study-hours vs exam-score example, what correlation value is computed?", [
                ("0.312", False), ("0.994", True), ("-0.994", False), ("0.5", False)]),
            ("What important caveat does the lesson raise about correlation?", [
                ("Correlation always implies causation", False), ("Correlation does not prove causation", True),
                ("Correlation can only be calculated with NumPy", False), ("Correlation cannot be negative", False)]),
        ])
        l2_2_6, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Correlation Matrix',
            defaults={
                'order': 6,
                'is_free': False,
                'content': '''<h2>Correlation Matrix</h2>
<p>A correlation matrix shows the pairwise correlation coefficients between multiple variables at once. It is a quick way to scan for relationships in a dataset.</p>
<h3>Building a Correlation Matrix</h3>
<pre><code>import pandas as pd
import numpy as np

data = pd.DataFrame({
    "hours_studied": [2, 3, 5, 7, 8, 10],
    "exam_score":    [55, 60, 70, 78, 85, 92],
    "sleep_hours":   [6, 7, 7, 8, 6, 5],
    "anxiety_level": [8, 7, 5, 4, 3, 2]
})

corr_matrix = data.corr()
print(corr_matrix)</code></pre>
<h3>Heatmap Visualisation</h3>
<pre><code>import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Matrix")
plt.show()</code></pre>
<h3>Reading the Matrix</h3>
<ul>
<li>The diagonal is always 1 (a variable perfectly correlates with itself)</li>
<li>The matrix is symmetric - corr(A,B) = corr(B,A)</li>
<li>Look for values close to +1 or -1 for strong relationships</li>
<li>Values near 0 suggest weak or no linear relationship</li>
</ul>'''
            }
        )
        self._add_quiz(l2_2_6, [
            ("What value always appears on the diagonal of a correlation matrix?", [
                ("0", False), ("-1", False), ("1", True), ("The mean of the dataset", False)]),
            ("What does it mean that a correlation matrix is \"symmetric\"?", [
                ("corr(A,B) = corr(B,A)", True), ("All values are equal", False),
                ("It has the same number of rows and columns only", False), ("It contains no negative values", False)]),
            ("Which Pandas method computes a correlation matrix for all numeric columns?", [
                ("data.corr()", True), ("data.correlate()", False),
                ("data.matrix()", False), ("data.pairwise()", False)]),
            ("Which library and function does the lesson use to visualise the correlation matrix as a heatmap?", [
                ("matplotlib.pyplot.matrix()", False), ("seaborn.heatmap()", True),
                ("pandas.plot_heatmap()", False), ("numpy.heatmap()", False)]),
        ])
        l2_2_7, _ = Lesson.objects.get_or_create(
            chapter=ch2_2,
            title='Correlation vs Causality',
            defaults={
                'order': 7,
                'is_free': False,
                'content': '''<h2>Correlation vs Causality</h2>
<p>One of the most important concepts in data science: just because two variables move together does not mean one causes the other.</p>
<h3>Classic Examples</h3>
<ul>
<li><strong>Ice cream sales and drowning rates</strong> - both rise in summer. The hidden variable (confounder) is hot weather, not ice cream causing drowning.</li>
<li><strong>Shoe size and reading ability</strong> - positively correlated in children, because both increase with age.</li>
</ul>
<h3>Why Correlation ≠ Causation</h3>
<ol>
<li><strong>Confounding variables</strong> - a third, unmeasured variable drives both</li>
<li><strong>Reverse causality</strong> - the cause-effect direction is the opposite of what you assume</li>
<li><strong>Coincidence</strong> - some correlations are pure chance, especially with many variables</li>
</ol>
<h3>Establishing Causation</h3>
<p>To claim causation, you generally need:</p>
<ul>
<li><strong>Randomised controlled experiments</strong> (A/B tests)</li>
<li><strong>Temporal precedence</strong> - the cause must happen before the effect</li>
<li><strong>Ruling out confounders</strong> - through study design or statistical techniques</li>
</ul>
<pre><code># Observational data can suggest hypotheses
# But only experiments can confirm causation

# A/B test example
# Group A: sees old design (control)
# Group B: sees new design (treatment)
# If conversion rate differs significantly, the design change caused it</code></pre>
<p>As a data scientist, always ask: "Is there a confounding variable?" before declaring a causal relationship.</p>'''
            }
        )
        self._add_quiz(l2_2_7, [
            ("In the ice cream and drowning example, what is the hidden confounding variable?", [
                ("Ice cream flavor", False), ("Hot weather", True),
                ("Swimming pool capacity", False), ("Season length", False)]),
            ("What does \"reverse causality\" mean?", [
                ("There is no relationship at all", False),
                ("The cause-effect direction is the opposite of what is assumed", True),
                ("The correlation is exactly 0", False), ("The data was measured incorrectly", False)]),
            ("What kind of study design does the lesson say is generally needed to establish causation?", [
                ("Observational surveys", False), ("Randomised controlled experiments", True),
                ("Correlation matrices", False), ("Percentile analysis", False)]),
            ("What is \"temporal precedence\" in the context of establishing causation?", [
                ("The cause must happen before the effect", True), ("The data must be recent", False),
                ("The sample size must be large", False), ("The p-value must be below 0.05", False)]),
        ])

        # ──────────────────────────────────────────────
        # Course 3: Regression Analysis
        # ──────────────────────────────────────────────
        course3, _ = Course.objects.get_or_create(
            title='Regression Analysis',
            defaults={
                'description': 'Learn linear regression from the ground up - from the maths behind the model to interpreting coefficients, p-values, and R-squared in real-world datasets.',
                'is_published': True,
            }
        )

        # Chapter 1: Linear Regression
        ch3_1, _ = Chapter.objects.get_or_create(
            course=course3,
            title='Linear Regression',
            defaults={'order': 1, 'description': 'Understanding and applying linear regression models'}
        )
        l3_1_1, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='Linear Regression Basics',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Linear Regression Basics</h2>
<p>Linear regression models the relationship between a dependent variable (y) and one or more independent variables (x) by fitting a straight line to the data.</p>
<h3>Simple Linear Regression</h3>
<p>One independent variable:</p>
<pre><code>y = β₀ + β₁x + ε</code></pre>
<ul>
<li><strong>β₀</strong> - intercept (predicted y when x = 0)</li>
<li><strong>β₁</strong> - slope (change in y per unit change in x)</li>
<li><strong>ε</strong> - error term (the part of y the model can't explain)</li>
</ul>
<h3>Python Implementation</h3>
<pre><code>from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

model = LinearRegression()
model.fit(X, y)

print(f"Intercept: {model.intercept_}")   # 2.2
print(f"Slope: {model.coef_[0]}")         # 0.6
print(f"R²: {model.score(X, y):.3f}")     # 0.72</code></pre>
<p>The model finds the line that minimises the sum of squared residuals - the differences between actual and predicted values.</p>'''
            }
        )
        self._add_quiz(l3_1_1, [
            ("In the simple linear regression equation y = β₀ + β₁x + ε, what does ε represent?", [
                ("The slope", False), ("The intercept", False),
                ("The error term", True), ("The R-squared value", False)]),
            ("In the lesson's sklearn example, what is the computed intercept?", [
                ("0.6", False), ("2.2", True), ("0.72", False), ("5", False)]),
            ("Which scikit-learn class is used to fit a linear regression model?", [
                ("LinearModel", False), ("LinearRegression", True),
                ("OLSRegressor", False), ("sklearn.fit()", False)]),
            ("What does the linear regression model minimise when fitting the line?", [
                ("The number of data points", False), ("The sum of squared residuals", True),
                ("The p-value", False), ("The correlation coefficient", False)]),
        ])
        l3_1_2, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='Regression Table',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>Regression Table</h2>
<p>A regression table summarises the results of a regression model. Learning to read one is essential for interpreting model output.</p>
<h3>Using Statsmodels for Detailed Output</h3>
<pre><code>import statsmodels.api as sm
import numpy as np

X = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

X_with_const = sm.add_constant(X)
model = sm.OLS(y, X_with_const).fit()
print(model.summary())</code></pre>
<h3>Key Columns in the Table</h3>
<table>
<thead><tr><th>Column</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>coef</td><td>Estimated coefficient for each variable</td></tr>
<tr><td>std err</td><td>Standard error of the coefficient estimate</td></tr>
<tr><td>t</td><td>t-statistic (coef / std err)</td></tr>
<tr><td>P>|t|</td><td>p-value - probability the result occurred by chance</td></tr>
<tr><td>[0.025, 0.975]</td><td>95% confidence interval for the coefficient</td></tr>
</tbody>
</table>
<h3>Bottom Section</h3>
<ul>
<li><strong>R-squared</strong> - proportion of variance explained by the model</li>
<li><strong>F-statistic</strong> - tests whether the model as a whole is significant</li>
<li><strong>AIC / BIC</strong> - model comparison metrics (lower is better)</li>
</ul>'''
            }
        )
        self._add_quiz(l3_1_2, [
            ("Which library does the lesson use to produce a detailed regression summary table?", [
                ("scikit-learn", False), ("statsmodels", True), ("seaborn", False), ("scipy", False)]),
            ("What does the \"P>|t|\" column in a regression table represent?", [
                ("The coefficient estimate", False),
                ("The p-value - probability the result occurred by chance", True),
                ("The confidence interval width", False), ("The R-squared value", False)]),
            ("For model comparison, what does the lesson say about AIC and BIC values?", [
                ("Higher is better", False), ("Lower is better", True),
                ("They must equal zero", False), ("They are irrelevant to comparison", False)]),
            ("What does the F-statistic test in a regression table?", [
                ("Whether a single coefficient is zero", False),
                ("Whether the model as a whole is significant", True),
                ("The variance of residuals", False), ("The sample size adequacy", False)]),
        ])
        l3_1_3, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='Regression Info',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Regression Info</h2>
<p>Before trusting a regression model, you need to check several assumptions and diagnostic metrics.</p>
<h3>Key Assumptions of Linear Regression</h3>
<ol>
<li><strong>Linearity</strong> - the relationship between x and y is linear</li>
<li><strong>Independence</strong> - observations are independent of each other</li>
<li><strong>Homoscedasticity</strong> - constant variance of residuals across all levels of x</li>
<li><strong>Normality of residuals</strong> - errors are normally distributed</li>
</ol>
<h3>Checking Assumptions</h3>
<pre><code>import matplotlib.pyplot as plt
import scipy.stats as stats

residuals = model.resid

# Residual plot (check homoscedasticity)
plt.scatter(model.fittedvalues, residuals)
plt.axhline(y=0, color="r", linestyle="--")
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.show()

# Q-Q plot (check normality)
stats.probplot(residuals, dist="norm", plot=plt)
plt.show()</code></pre>
<h3>When Assumptions Are Violated</h3>
<ul>
<li>Non-linearity → try polynomial features or non-linear models</li>
<li>Heteroscedasticity → use weighted least squares or transform the variable</li>
<li>Non-normal residuals → consider robust regression or bootstrapping</li>
</ul>'''
            }
        )
        self._add_quiz(l3_1_3, [
            ("What does \"homoscedasticity\" refer to as a regression assumption?", [
                ("Independence of observations", False),
                ("Constant variance of residuals across all levels of x", True),
                ("Normal distribution of the predictors", False), ("Linear relationship between variables", False)]),
            ("Which plot is used in the lesson to check the normality of residuals?", [
                ("Residual plot", False), ("Q-Q plot", True), ("Bar chart", False), ("Histogram of x values", False)]),
            ("What is suggested as a remedy when the relationship is non-linear?", [
                ("Ignore it", False), ("Try polynomial features or non-linear models", True),
                ("Remove all data points", False), ("Use only categorical variables", False)]),
            ("What should you check to detect heteroscedasticity?", [
                ("A residual plot showing non-constant spread", True), ("The dataset's row count", False),
                ("The correlation matrix", False), ("The p-value of the intercept", False)]),
        ])
        l3_1_4, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='Coefficients',
            defaults={
                'order': 4,
                'is_free': False,
                'content': '''<h2>Regression Coefficients</h2>
<p>Coefficients tell you how much the dependent variable changes for each one-unit change in an independent variable, holding all other variables constant.</p>
<h3>Interpreting Coefficients</h3>
<pre><code># Example: predicting house prices
# Coefficients:
#   bedrooms:   25,000
#   bathrooms:  18,000
#   sqft:          120
#   age:         -1,500

# Interpretation:
# Each additional bedroom adds ~$25,000 to price
# Each additional year of age reduces price by ~$1,500</code></pre>
<h3>Standardised Coefficients</h3>
<p>Raw coefficients are in the units of the variable, making it hard to compare importance. Standardised coefficients (beta weights) allow comparison:</p>
<pre><code>from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model_scaled = LinearRegression()
model_scaled.fit(X_scaled, y)
print(model_scaled.coef_)  # Now comparable across variables</code></pre>
<h3>Confidence Intervals</h3>
<p>A 95% confidence interval for a coefficient means: if we repeated the study 100 times, the true coefficient would fall within this range in about 95 of them.</p>'''
            }
        )
        self._add_quiz(l3_1_4, [
            ("In the house price example, how much does each additional bedroom add to the predicted price?", [
                ("$18,000", False), ("$25,000", True), ("$120", False), ("$1,500", False)]),
            ("What does the negative coefficient for \"age\" (-1,500) indicate?", [
                ("Each additional year of age adds $1,500 to the price", False),
                ("Each additional year of age reduces price by about $1,500", True),
                ("Age has no effect on price", False), ("The model is invalid", False)]),
            ("Why would you use standardised coefficients instead of raw coefficients?", [
                ("To make coefficients comparable across variables with different units", True),
                ("To make the model run faster", False),
                ("To eliminate the need for confidence intervals", False), ("To increase R-squared", False)]),
            ("What does a 95% confidence interval for a coefficient represent, per the lesson?", [
                ("The coefficient is 95% likely to be exactly this value", False),
                ("If the study were repeated 100 times, the true coefficient would fall in this range about 95 times", True),
                ("95% of the data falls in this range", False), ("The model is 95% accurate", False)]),
        ])
        l3_1_5, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='P-Value',
            defaults={
                'order': 5,
                'is_free': False,
                'content': '''<h2>P-Value</h2>
<p>The p-value tells you the probability of observing results at least as extreme as what you got, assuming there is no real relationship (the null hypothesis).</p>
<h3>Interpreting P-Values</h3>
<table>
<thead><tr><th>P-Value</th><th>Interpretation</th></tr></thead>
<tbody>
<tr><td>&lt; 0.01</td><td>Strong evidence against the null hypothesis</td></tr>
<tr><td>&lt; 0.05</td><td>Moderate evidence - commonly used threshold</td></tr>
<tr><td>&lt; 0.10</td><td>Weak evidence - suggestive but not conclusive</td></tr>
<tr><td>≥ 0.10</td><td>No significant evidence of a relationship</td></tr>
</tbody>
</table>
<h3>Example</h3>
<pre><code>import statsmodels.api as sm

X = sm.add_constant(np.array([1, 2, 3, 4, 5]))
y = np.array([2, 4, 5, 4, 5])

model = sm.OLS(y, X).fit()
print(f"Coefficient: {model.params[1]:.3f}")
print(f"P-value: {model.pvalues[1]:.3f}")</code></pre>
<h3>Common Misconceptions</h3>
<ul>
<li>A p-value of 0.03 does NOT mean there is a 97% chance the relationship is real</li>
<li>It does NOT tell you the size of the effect - a tiny effect can have a small p-value with enough data</li>
<li>It does NOT prove the null hypothesis is false - it only measures evidence against it</li>
</ul>
<p>Always report effect sizes alongside p-values for a complete picture.</p>'''
            }
        )
        self._add_quiz(l3_1_5, [
            ("According to the lesson's table, what does a p-value less than 0.01 indicate?", [
                ("No significant evidence", False), ("Weak evidence", False),
                ("Strong evidence against the null hypothesis", True), ("Proof of causation", False)]),
            ("What is the commonly used significance threshold mentioned in the lesson?", [
                ("0.10", False), ("0.05", True), ("0.01", False), ("0.50", False)]),
            ("Which of these statements about p-values is TRUE according to the lesson?", [
                ("A p-value of 0.03 means there is a 97% chance the relationship is real", False),
                ("A p-value tells you the size of the effect", False),
                ("A small p-value does not prove the null hypothesis is false, only that there is evidence against it", True),
                ("A p-value proves causation", False)]),
            ("What does the lesson recommend reporting alongside p-values for a complete picture?", [
                ("Only the sample size", False), ("Effect sizes", True),
                ("The dataset's file format", False), ("The programming language used", False)]),
        ])
        l3_1_6, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='R-Squared',
            defaults={
                'order': 6,
                'is_free': False,
                'content': '''<h2>R-Squared</h2>
<p>R-squared (coefficient of determination) measures how well your model explains the variation in the dependent variable. It ranges from 0 to 1.</p>
<h3>Formula</h3>
<pre><code>R² = 1 - (SS_res / SS_tot)</code></pre>
<ul>
<li><strong>SS_res</strong> - sum of squared residuals (unexplained variance)</li>
<li><strong>SS_tot</strong> - total sum of squares (total variance)</li>
</ul>
<h3>Interpreting R-Squared</h3>
<table>
<thead><tr><th>R² Value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>0.0</td><td>Model explains none of the variance</td></tr>
<tr><td>0.5</td><td>Model explains half the variance</td></tr>
<tr><td>0.8</td><td>Model explains 80% of the variance</td></tr>
<tr><td>1.0</td><td>Model perfectly predicts the data</td></tr>
</tbody>
</table>
<h3>Adjusted R-Squared</h3>
<p>Regular R-squared always increases when you add more variables, even if they are useless. Adjusted R-squared penalises unnecessary variables:</p>
<pre><code># R² = 0.85 with 3 variables
# R² = 0.86 with 10 variables (but adjusted R² might be lower)
# Adjusted R² accounts for model complexity</code></pre>
<p>A high R-squared doesn't guarantee a good model. Always check residual plots and assumptions alongside it.</p>'''
            }
        )
        self._add_quiz(l3_1_6, [
            ("What does an R-squared value of 0.0 mean?", [
                ("The model perfectly predicts the data", False), ("The model explains none of the variance", True),
                ("The model has negative predictions", False), ("There was a calculation error", False)]),
            ("What is SS_res in the R-squared formula?", [
                ("Total sum of squares", False), ("Sum of squared residuals - unexplained variance", True),
                ("The sample size", False), ("The correlation coefficient", False)]),
            ("Why might adjusted R-squared be preferred over regular R-squared when comparing models?", [
                ("It always increases with more variables", False), ("It penalises unnecessary variables", True),
                ("It cannot be calculated for regression models", False), ("It ignores model complexity entirely", False)]),
            ("An R-squared of 0.8 means the model explains what percentage of the variance?", [
                ("20%", False), ("50%", False), ("80%", True), ("100%", False)]),
        ])
        l3_1_7, _ = Lesson.objects.get_or_create(
            chapter=ch3_1,
            title='Case Study: Predicting House Prices',
            defaults={
                'order': 7,
                'is_free': False,
                'content': '''<h2>Case Study: Predicting House Prices</h2>
<p>Let's walk through a complete linear regression workflow using a house price dataset.</p>
<h3>Step 1: Load and Explore</h3>
<pre><code>import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("house_prices.csv")
print(df.describe())
print(df.corr()["price"].sort_values(ascending=False))</code></pre>
<h3>Step 2: Prepare Features</h3>
<pre><code>from sklearn.model_selection import train_test_split

features = ["sqft", "bedrooms", "bathrooms", "age", "garage"]
X = df[features]
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)</code></pre>
<h3>Step 3: Train and Evaluate</h3>
<pre><code>from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
print(f"MAE: ${mean_absolute_error(y_test, y_pred):,.0f}")

# Interpret coefficients
for feature, coef in zip(features, model.coef_):
    print(f"  {feature}: ${coef:,.0f}")</code></pre>
<h3>Step 4: Interpret Results</h3>
<p>If sqft has a coefficient of 150, it means each additional square foot adds ~$150 to the predicted price, holding all other features constant.</p>
<p>An R² of 0.78 means the model explains 78% of the variance in house prices - a solid starting point, but there's room to improve with feature engineering or more complex models.</p>'''
            }
        )
        self._add_quiz(l3_1_7, [
            ("What test size is used in the lesson's train_test_split call?", [
                ("0.1", False), ("0.2", True), ("0.3", False), ("0.5", False)]),
            ("Which features are used to predict house prices in the case study?", [
                ("sqft, bedrooms, bathrooms, age, garage", True), ("name, age, city", False),
                ("date, price, name", False), ("hours_studied, exam_score", False)]),
            ("In the interpretation step, what does a sqft coefficient of 150 mean?", [
                ("Each additional square foot adds about $150 to the predicted price", True),
                ("The house has 150 square feet", False),
                ("The model's accuracy is 150%", False), ("150 houses were used in training", False)]),
            ("What R² value is reported in the case study's example results, and what does it mean?", [
                ("0.78 - the model explains 78% of the variance", True), ("1.0 - perfect prediction", False),
                ("0.0 - no predictive power", False), ("78 - the number of features used", False)]),
        ])

        # ──────────────────────────────────────────────
        # Course 4: Pandas for Data Science
        # ──────────────────────────────────────────────
        course4, _ = Course.objects.get_or_create(
            title='Pandas for Data Science',
            defaults={
                'description': 'Master Pandas - the essential Python library for data manipulation. Learn Series, DataFrames, reading files, cleaning data, and analysis.',
                'is_published': True,
            }
        )

        # Chapter 1: Getting Started with Pandas
        ch4_1, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Getting Started with Pandas',
            defaults={'order': 1, 'description': 'Core Pandas concepts and data structures'}
        )
        l4_1_1, _ = Lesson.objects.get_or_create(
            chapter=ch4_1,
            title='Pandas Intro',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Pandas Intro</h2>
<p>Pandas is the most popular Python library for data analysis and manipulation. It provides fast, flexible data structures that make working with structured data intuitive.</p>
<h3>Why Pandas?</h3>
<ul>
<li>Load data from CSV, Excel, JSON, SQL, and more</li>
<li>Clean, filter, group, and reshape datasets</li>
<li>Handle missing data gracefully</li>
<li>Perform aggregations and statistical operations</li>
<li>Integrates seamlessly with NumPy, Matplotlib, and scikit-learn</li>
</ul>
<h3>Installation</h3>
<pre><code>pip install pandas</code></pre>
<h3>Importing Pandas</h3>
<pre><code>import pandas as pd
import numpy as np</code></pre>
<p>By convention, pandas is imported as <code>pd</code>. Almost every data science project starts with this import.</p>'''
            }
        )
        self._add_quiz(l4_1_1, [
            ("By convention, Pandas is imported using which alias?", [
                ("ps", False), ("pd", True), ("pandas", False), ("pn", False)]),
            ("Which command installs Pandas via pip?", [
                ("pip get pandas", False), ("pip install pandas", True),
                ("pip add pandas", False), ("python -m pandas", False)]),
            ("Which of the following is NOT listed in the lesson as something Pandas integrates with?", [
                ("NumPy", False), ("Matplotlib", False), ("scikit-learn", False), ("TensorFlow", True)]),
            ("What is one thing Pandas is described as being able to do?", [
                ("Compile Python to machine code", False),
                ("Load data from CSV, Excel, JSON, and SQL", True),
                ("Render 3D graphics", False), ("Train neural networks natively", False)]),
        ])
        l4_1_2, _ = Lesson.objects.get_or_create(
            chapter=ch4_1,
            title='Getting Started',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>Getting Started with Pandas</h2>
<p>The two primary data structures in Pandas are <strong>Series</strong> (one-dimensional) and <strong>DataFrame</strong> (two-dimensional). Everything you do in Pandas revolves around these.</p>
<h3>Creating Your First DataFrame</h3>
<pre><code>import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [25, 30, 35, 28],
    "city": ["New York", "London", "Paris", "Tokyo"]
}

df = pd.DataFrame(data)
print(df)

#       name  age      city
# 0    Alice   25  New York
# 1      Bob   30    London
# 2  Charlie   35     Paris
# 3    Diana   28     Tokyo</code></pre>
<h3>Quick Inspection</h3>
<pre><code>df.head()        # First 5 rows
df.shape         # (4, 3) - rows, columns
df.dtypes        # Data types of each column
df.info()        # Summary of the DataFrame
df.describe()    # Statistics for numeric columns</code></pre>
<p>Always inspect your data first - check shape, types, and missing values before any analysis.</p>'''
            }
        )
        self._add_quiz(l4_1_2, [
            ("What are the two primary data structures in Pandas?", [
                ("List and Dict", False), ("Series and DataFrame", True),
                ("Array and Matrix", False), ("Table and Column", False)]),
            ("What does df.shape return for a DataFrame with 4 rows and 3 columns?", [
                ("12", False), ("(4, 3)", True), ("3", False), ("[4, 3, 3]", False)]),
            ("Which method shows the first 5 rows of a DataFrame by default?", [
                ("df.top()", False), ("df.head()", True), ("df.first()", False), ("df.preview()", False)]),
            ("What does the lesson recommend checking before any analysis?", [
                ("Only the column names", False), ("Shape, types, and missing values", True),
                ("The file size only", False), ("The operating system version", False)]),
        ])
        l4_1_3, _ = Lesson.objects.get_or_create(
            chapter=ch4_1,
            title='Series',
            defaults={
                'order': 3,
                'is_free': True,
                'content': '''<h2>Series</h2>
<p>A Series is a one-dimensional labelled array - like a single column from a spreadsheet. It holds data of any type (numbers, strings, dates) with an associated index.</p>
<h3>Creating a Series</h3>
<pre><code>import pandas as pd

# From a list
prices = pd.Series([29.99, 49.99, 19.99, 39.99])
print(prices)

# 0    29.99
# 1    49.99
# 2    19.99
# 3    39.99</code></pre>
<h3>Custom Index</h3>
<pre><code>prices = pd.Series(
    [29.99, 49.99, 19.99, 39.99],
    index=["shirt", "jacket", "socks", "shoes"]
)
print(prices["jacket"])  # 49.99</code></pre>
<h3>Common Operations</h3>
<pre><code>prices.mean()       # Average price
prices.max()        # Highest price
prices[prices > 30]  # Filter: items over $30
prices.sort_values() # Sort ascending</code></pre>
<p>A DataFrame is essentially a collection of Series objects sharing the same index.</p>'''
            }
        )
        self._add_quiz(l4_1_3, [
            ("How is a Series best described?", [
                ("A two-dimensional table", False), ("A one-dimensional labelled array", True),
                ("A SQL table", False), ("A Python dictionary only", False)]),
            ("In the custom index example, what does prices[\"jacket\"] return?", [
                ("29.99", False), ("49.99", True), ("19.99", False), ("39.99", False)]),
            ("What does prices[prices > 30] do?", [
                ("Sorts prices ascending", False), ("Filters items over $30", True),
                ("Returns the mean price", False), ("Removes all prices", False)]),
            ("What is the relationship between a DataFrame and Series, per the lesson?", [
                ("They are unrelated structures", False),
                ("A DataFrame is a collection of Series sharing the same index", True),
                ("A Series is a collection of DataFrames", False), ("A Series can only hold strings", False)]),
        ])
        l4_1_4, _ = Lesson.objects.get_or_create(
            chapter=ch4_1,
            title='DataFrames',
            defaults={
                'order': 4,
                'is_free': True,
                'content': '''<h2>DataFrames</h2>
<p>A DataFrame is a two-dimensional table with labelled rows and columns. It is the workhorse of Pandas - most of your time will be spent working with DataFrames.</p>
<h3>Selecting Data</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({
    "product": ["Shirt", "Jacket", "Socks", "Shoes"],
    "price": [29.99, 49.99, 19.99, 39.99],
    "stock": [150, 80, 300, 120]
})

# Select a column
df["price"]

# Select multiple columns
df[["product", "price"]]

# Select rows by condition
df[df["price"] > 30]

# Select by row index
df.iloc[0]     # First row
df.iloc[1:3]   # Rows 1-2</code></pre>
<h3>Adding and Removing Columns</h3>
<pre><code># Add a new column
df["value"] = df["price"] * df["stock"]

# Remove a column
df = df.drop(columns=["value"])</code></pre>
<h3>Sorting</h3>
<pre><code>df.sort_values("price", ascending=False)</code></pre>'''
            }
        )
        self._add_quiz(l4_1_4, [
            ("Which syntax selects multiple columns from a DataFrame?", [
                ("df[\"product\", \"price\"]", False), ("df[[\"product\", \"price\"]]", True),
                ("df.columns(\"product\", \"price\")", False), ("df.select(\"product\", \"price\")", False)]),
            ("What does df.iloc[1:3] select?", [
                ("Columns 1 to 3", False), ("Rows 1 and 2", True),
                ("Row 1 only", False), ("The last 3 rows", False)]),
            ("How do you remove a column named \"value\" from a DataFrame?", [
                ("df.delete(\"value\")", False), ("df = df.drop(columns=[\"value\"])", True),
                ("del df.value", False), ("df.remove_column(\"value\")", False)]),
            ("Which call sorts a DataFrame by the \"price\" column in descending order?", [
                ("df.sort_values(\"price\")", False), ("df.sort_values(\"price\", ascending=False)", True),
                ("df.order_by(\"price desc\")", False), ("df.sort(\"price\", desc=True)", False)]),
        ])

        # Chapter 2: Working with Data
        ch4_2, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Working with Data',
            defaults={'order': 2, 'description': 'Reading, analysing, and summarising data'}
        )
        l4_2_1, _ = Lesson.objects.get_or_create(
            chapter=ch4_2,
            title='Read CSV',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Read CSV</h2>
<p>CSV (Comma-Separated Values) is the most common file format for tabular data. Pandas makes loading CSV files a one-liner.</p>
<h3>Basic CSV Reading</h3>
<pre><code>import pandas as pd

df = pd.read_csv("sales_data.csv")
print(df.head())</code></pre>
<h3>Common Parameters</h3>
<pre><code># Specify delimiter (for TSV or other separators)
df = pd.read_csv("data.tsv", sep="\\t")

# Select specific columns
df = pd.read_csv("data.csv", usecols=["name", "age", "salary"])

# Set a column as the index
df = pd.read_csv("data.csv", index_col="id")

# Handle missing values during load
df = pd.read_csv("data.csv", na_values=["N/A", "missing", ""])

# Parse dates automatically
df = pd.read_csv("data.csv", parse_dates=["date_column"])</code></pre>
<h3>Writing CSV</h3>
<pre><code>df.to_csv("output.csv", index=False)</code></pre>
<p>Always pass <code>index=False</code> when saving unless you need the row index in the file.</p>'''
            }
        )
        self._add_quiz(l4_2_1, [
            ("Which parameter specifies a custom delimiter when reading a TSV file?", [
                ("delimiter", False), ("sep", True), ("split", False), ("tab", False)]),
            ("What does the na_values parameter do when reading a CSV?", [
                ("Sets a default numeric value", False),
                ("Specifies which strings should be treated as missing values", True),
                ("Removes all NaN values automatically", False), ("Converts NaN to zero", False)]),
            ("What does the lesson recommend passing to to_csv() unless you need the row index saved?", [
                ("header=False", False), ("index=False", True), ("sep=\",\"", False), ("mode=\"w\"", False)]),
            ("Which parameter automatically converts a column to datetime while reading a CSV?", [
                ("parse_dates", True), ("to_datetime", False), ("date_format", False), ("convert_dates", False)]),
        ])
        l4_2_2, _ = Lesson.objects.get_or_create(
            chapter=ch4_2,
            title='Read JSON',
            defaults={
                'order': 2,
                'is_free': False,
                'content': '''<h2>Read JSON</h2>
<p>JSON (JavaScript Object Notation) is widely used in APIs and web data. Pandas can load JSON data and convert it to DataFrames.</p>
<h3>Reading JSON Files</h3>
<pre><code>import pandas as pd

# From a JSON file
df = pd.read_json("data.json")

# From a JSON string
json_str = \'\'\'[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]\'\'\'
df = pd.read_json(json_str)</code></pre>
<h3>Nested JSON</h3>
<p>Real-world JSON is often nested. Use <code>json_normalize</code> to flatten it:</p>
<pre><code>import json
from pandas import json_normalize

with open("nested_data.json") as f:
    data = json.load(f)

df = json_normalize(data, record_path="results", meta=["id", "timestamp"])</code></pre>
<h3>Writing JSON</h3>
<pre><code>df.to_json("output.json", orient="records", indent=2)</code></pre>
<p>The <code>orient</code> parameter controls the JSON structure - <code>"records"</code> produces a list of objects, which is the most common format for APIs.</p>'''
            }
        )
        self._add_quiz(l4_2_2, [
            ("Which Pandas function loads JSON data into a DataFrame?", [
                ("pd.read_json()", True), ("pd.load_json()", False),
                ("pd.from_json()", False), ("pd.json_to_df()", False)]),
            ("What is json_normalize used for?", [
                ("Converting DataFrames to JSON", False), ("Flattening nested JSON structures", True),
                ("Removing missing values", False), ("Sorting JSON keys", False)]),
            ("What does orient=\"records\" produce when writing JSON?", [
                ("A single nested object", False), ("A list of objects", True),
                ("A CSV file", False), ("A SQL table", False)]),
            ("Why does the lesson say orient=\"records\" is the most common format?", [
                ("It is the smallest file size", False), ("It is the most common format for APIs", True),
                ("It is required by Pandas", False), ("It cannot contain missing values", False)]),
        ])
        l4_2_3, _ = Lesson.objects.get_or_create(
            chapter=ch4_2,
            title='Analyzing Data',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Analyzing Data</h2>
<p>Once you have data in a DataFrame, Pandas provides powerful tools to explore and understand it.</p>
<h3>Summary Statistics</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({
    "product": ["A", "B", "C", "D", "E"],
    "sales": [150, 200, 80, 320, 175],
    "returns": [5, 12, 2, 18, 8]
})

df.describe()  # count, mean, std, min, 25%, 50%, 75%, max</code></pre>
<h3>Grouping and Aggregation</h3>
<pre><code># Group by a category and aggregate
df.groupby("category")["sales"].sum()
df.groupby("category").agg({"sales": "sum", "returns": "mean"})</code></pre>
<h3>Value Counts</h3>
<pre><code># Count occurrences of each value
df["category"].value_counts()</code></pre>
<h3>Crosstab</h3>
<pre><code># Frequency table between two variables
pd.crosstab(df["region"], df["category"])</code></pre>
<h3>Correlation</h3>
<pre><code># Correlation between numeric columns
df[["sales", "returns", "discount"]].corr()</code></pre>
<p>These operations help you understand your data before building any models.</p>'''
            }
        )
        self._add_quiz(l4_2_3, [
            ("Which method counts the occurrences of each unique value in a column?", [
                ("df.count()", False), ("df[\"category\"].value_counts()", True),
                ("df.tally()", False), ("df.unique_counts()", False)]),
            ("What does df.groupby(\"category\")[\"sales\"].sum() compute?", [
                ("The total sales per category", True), ("The average sales overall", False),
                ("The number of categories", False), ("The correlation between sales and category", False)]),
            ("What does pd.crosstab(df[\"region\"], df[\"category\"]) produce?", [
                ("A correlation matrix", False), ("A frequency table between two variables", True),
                ("A scatter plot", False), ("A single summary number", False)]),
            ("What does df.describe() return for numeric columns?", [
                ("count, mean, std, min, 25%, 50%, 75%, max", True), ("Only the column names", False),
                ("A plot", False), ("The data types only", False)]),
        ])

        # Chapter 3: Data Cleaning
        ch4_3, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Data Cleaning',
            defaults={'order': 3, 'description': 'Handling messy real-world data'}
        )
        l4_3_1, _ = Lesson.objects.get_or_create(
            chapter=ch4_3,
            title='Cleaning Empty Cells',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Cleaning Empty Cells</h2>
<p>Missing data is inevitable in real datasets. Pandas represents missing values as <code>NaN</code> (Not a Number) and provides tools to detect and handle them.</p>
<h3>Detecting Missing Values</h3>
<pre><code>import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Alice", "Bob", None, "Diana"],
    "age": [25, np.nan, 35, 28],
    "salary": [50000, 60000, np.nan, 55000]
})

df.isnull()          # Boolean mask
df.isnull().sum()    # Count missing per column</code></pre>
<h3>Option 1: Drop Rows with Missing Values</h3>
<pre><code>df.dropna()                    # Drop any row with NaN
df.dropna(subset=["age"])      # Drop only if 'age' is NaN</code></pre>
<h3>Option 2: Fill Missing Values</h3>
<pre><code>df["age"].fillna(0)               # Fill with a fixed value
df["salary"].fillna(df["salary"].mean())  # Fill with mean
df["name"].fillna("Unknown")      # Fill with placeholder
df.fillna(method="ffill")         # Forward-fill (use previous row's value)</code></pre>
<h3>Which Approach?</h3>
<ul>
<li><strong>Drop</strong> - when missing data is minimal (&lt;5%) and random</li>
<li><strong>Fill with mean/median</strong> - for numeric columns where zero would skew analysis</li>
<li><strong>Forward/backward fill</strong> - for time-series data where order matters</li>
</ul>'''
            }
        )
        self._add_quiz(l4_3_1, [
            ("What does Pandas use to represent missing values?", [
                ("None only", False), ("NaN", True), ("-1", False), ("An empty string only", False)]),
            ("What does df.dropna(subset=[\"age\"]) do?", [
                ("Drops all rows regardless of column", False), ("Drops rows only where \"age\" is NaN", True),
                ("Fills \"age\" with zero", False), ("Removes the \"age\" column entirely", False)]),
            ("Which fillna approach is recommended for time-series data where order matters?", [
                ("Drop rows", False), ("Fill with a fixed value", False),
                ("Forward/backward fill", True), ("Fill with an unrelated column", False)]),
            ("According to the lesson, when is dropping rows with missing data appropriate?", [
                ("Always, regardless of amount", False),
                ("When missing data is minimal (<5%) and random", True),
                ("Only for numeric columns", False), ("Never", False)]),
        ])
        l4_3_2, _ = Lesson.objects.get_or_create(
            chapter=ch4_3,
            title='Cleaning Wrong Format',
            defaults={
                'order': 2,
                'is_free': False,
                'content': '''<h2>Cleaning Wrong Format</h2>
<p>Data often arrives in inconsistent formats - dates stored as strings, numbers with currency symbols, mixed case text. Pandas can fix these.</p>
<h3>Converting Data Types</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({
    "date": ["2025-01-15", "2025-02-20", "2025-03-10"],
    "price": ["$29.99", "$49.99", "$19.99"],
    "name": ["  Alice ", "BOB", "charlie"]
})

# Convert string dates to datetime
df["date"] = pd.to_datetime(df["date"])

# Strip currency symbols and convert to float
df["price"] = df["price"].str.replace("$", "").astype(float)

# Normalise text: strip whitespace, title case
df["name"] = df["name"].str.strip().str.title()</code></pre>
<h3>Handling Mixed Formats</h3>
<pre><code># When date formats vary in the same column
df["date"] = pd.to_datetime(df["date"], format="mixed")</code></pre>
<h3>Replacing Values</h3>
<pre><code># Replace inconsistent values
df["status"] = df["status"].replace({"Y": "Yes", "N": "No", "n/a": "Unknown"})</code></pre>
<p>Always check <code>df.dtypes</code> after loading data - wrong types cause silent errors in analysis.</p>'''
            }
        )
        self._add_quiz(l4_3_2, [
            ("What does df[\"price\"].str.replace(\"$\", \"\").astype(float) accomplish?", [
                ("Removes rows with dollar signs", False),
                ("Strips the currency symbol and converts to a float", True),
                ("Converts float to string", False), ("Rounds prices to 2 decimals", False)]),
            ("What does format=\"mixed\" handle when parsing dates?", [
                ("Multiple currencies in one column", False),
                ("Dates with varying formats in the same column", True),
                ("Mixed data types in a column", False), ("Duplicate date entries", False)]),
            ("What does str.title() do to a text column?", [
                ("Converts to lowercase", False), ("Converts to uppercase", False),
                ("Converts to title case", True), ("Removes whitespace only", False)]),
            ("What should you always check after loading data, per the lesson?", [
                ("df.dtypes", True), ("df.shape only", False),
                ("The file's creation date", False), ("The number of columns only", False)]),
        ])
        l4_3_3, _ = Lesson.objects.get_or_create(
            chapter=ch4_3,
            title='Cleaning Wrong Data',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Cleaning Wrong Data</h2>
<p>Wrong data includes impossible values (negative age), outliers, and entries that don't make logical sense. These are harder to catch than missing values.</p>
<h3>Detecting Outliers with IQR</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({"age": [25, 30, 35, 200, 28, -5, 40]})

q1 = df["age"].quantile(0.25)
q3 = df["age"].quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[(df["age"] < lower_bound) | (df["age"] > upper_bound)]
print(outliers)  # age 200 and -5</code></pre>
<h3>Fixing Wrong Data</h3>
<pre><code># Replace impossible values
df.loc[df["age"] < 0, "age"] = df["age"].median()
df.loc[df["age"] > 120, "age"] = df["age"].median()</code></pre>
<h3>Logical Validation</h3>
<pre><code># Ensure start_date is before end_date
invalid = df[df["start_date"] > df["end_date"]]

# Ensure percentages are between 0 and 100
df.loc[df["score"] > 100, "score"] = 100
df.loc[df["score"] < 0, "score"] = 0</code></pre>
<p>Domain knowledge matters - what counts as "wrong" depends on context. An age of 150 is impossible, but a salary of $0 might be valid (unpaid internship).</p>'''
            }
        )
        self._add_quiz(l4_3_3, [
            ("In the lesson's example dataset [25, 30, 35, 200, 28, -5, 40], which values are flagged as outliers using IQR?", [
                ("25 and 30", False), ("200 and -5", True), ("35 and 40", False), ("28 only", False)]),
            ("What does df.loc[df[\"age\"] < 0, \"age\"] = df[\"age\"].median() do?", [
                ("Deletes all negative ages", False), ("Replaces negative ages with the median age", True),
                ("Converts negative ages to positive", False), ("Raises an error", False)]),
            ("What kind of check does df[df[\"start_date\"] > df[\"end_date\"]] perform?", [
                ("Missing value detection", False), ("Logical validation of date ordering", True),
                ("Duplicate detection", False), ("Outlier detection", False)]),
            ("According to the lesson, why does \"wrong\" data depend on context?", [
                ("It never depends on context", False),
                ("Because a salary of $0 might be valid but an age of 150 is impossible", True),
                ("Because Pandas defines it universally", False), ("Because all outliers are always wrong", False)]),
        ])
        l4_3_4, _ = Lesson.objects.get_or_create(
            chapter=ch4_3,
            title='Removing Duplicates',
            defaults={
                'order': 4,
                'is_free': False,
                'content': '''<h2>Removing Duplicates</h2>
<p>Duplicate rows inflate your data and skew analysis. Pandas makes it easy to detect and remove them.</p>
<h3>Detecting Duplicates</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Alice", "Charlie", "Bob"],
    "age": [25, 30, 25, 35, 30],
    "city": ["NYC", "London", "NYC", "Paris", "London"]
})

# Check for duplicates
df.duplicated()          # Boolean Series
df.duplicated().sum()    # Count of duplicates</code></pre>
<h3>Removing Duplicates</h3>
<pre><code># Remove exact duplicates (keeps first occurrence)
df_clean = df.drop_duplicates()

# Remove based on specific columns
df_clean = df.drop_duplicates(subset=["name"])

# Keep the last occurrence instead of first
df_clean = df.drop_duplicates(subset=["name"], keep="last")</code></pre>
<h3>When to Remove</h3>
<ul>
<li><strong>Exact duplicates</strong> - almost always remove (likely a data entry error)</li>
<li><strong>Partial duplicates</strong> - same name but different dates? Might be legitimate records. Investigate before removing.</li>
</ul>
<pre><code># Check how many duplicates exist before removing
print(f"Rows before: {len(df)}")
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Rows after: {len(df.drop_duplicates())}")</code></pre>'''
            }
        )
        self._add_quiz(l4_3_4, [
            ("What does df.duplicated().sum() return?", [
                ("The total number of rows", False), ("The count of duplicate rows", True),
                ("The number of columns", False), ("The sum of all values", False)]),
            ("What does df.drop_duplicates(subset=[\"name\"], keep=\"last\") do?", [
                ("Keeps the first occurrence of each name", False),
                ("Keeps the last occurrence of each duplicate name", True),
                ("Removes all rows with that name", False), ("Removes the \"name\" column", False)]),
            ("According to the lesson, what should you do before removing partial duplicates?", [
                ("Remove them immediately", False), ("Investigate whether they are legitimate records", True),
                ("Ignore them entirely", False), ("Convert them to NaN", False)]),
            ("What does drop_duplicates() do by default when it finds a duplicate row?", [
                ("Removes both occurrences", False), ("Keeps the first occurrence and removes later ones", True),
                ("Keeps the last occurrence only", False), ("Merges the rows", False)]),
        ])

        # Chapter 4: Analysis & Visualization
        ch4_4, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Analysis & Visualization',
            defaults={'order': 4, 'description': 'Finding patterns and visualising data'}
        )
        l4_4_1, _ = Lesson.objects.get_or_create(
            chapter=ch4_4,
            title='Correlations',
            defaults={
                'order': 1,
                'is_free': False,
                'content': '''<h2>Correlations in Pandas</h2>
<p>Correlation reveals how variables move together. Pandas makes it easy to compute pairwise correlations across your entire dataset.</p>
<h3>Correlation Matrix</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({
    "hours_studied": [2, 3, 5, 7, 8, 10],
    "exam_score": [55, 60, 70, 78, 85, 92],
    "sleep_hours": [6, 7, 7, 8, 6, 5],
    "anxiety": [8, 7, 5, 4, 3, 2]
})

corr = df.corr()
print(corr)</code></pre>
<h3>Finding Strong Correlations</h3>
<pre><code># Correlation with a specific variable
corr_with_score = df.corr()["exam_score"].sort_values(ascending=False)
print(corr_with_score)

# exam_score        1.000
# hours_studied     0.994
# sleep_hours       0.312
# anxiety          -0.994</code></pre>
<h3>Visualising with Heatmap</h3>
<pre><code>import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()</code></pre>
<p>Strong correlations (close to +1 or -1) suggest relationships worth investigating further - but remember, correlation is not causation.</p>'''
            }
        )
        self._add_quiz(l4_4_1, [
            ("In the lesson's example, what is the correlation between exam_score and anxiety?", [
                ("0.994", False), ("0.312", False), ("-0.994", True), ("1.000", False)]),
            ("What does df.corr()[\"exam_score\"].sort_values(ascending=False) produce?", [
                ("A random ordering of correlations", False),
                ("Correlations with exam_score, sorted from highest to lowest", True),
                ("Only positive correlations", False), ("The mean exam score", False)]),
            ("Which Seaborn function is used to visualise the correlation matrix?", [
                ("sns.heatmap()", True), ("sns.corrplot()", False),
                ("sns.matrix()", False), ("sns.pairplot()", False)]),
            ("What caveat does the lesson repeat about strong correlations?", [
                ("They always indicate causation", False), ("Correlation is not causation", True),
                ("They only apply to numeric data", False), ("They must be visualised to be valid", False)]),
        ])
        l4_4_2, _ = Lesson.objects.get_or_create(
            chapter=ch4_4,
            title='Plotting',
            defaults={
                'order': 2,
                'is_free': False,
                'content': '''<h2>Plotting with Pandas</h2>
<p>Pandas has built-in plotting powered by Matplotlib. Quick visualisations are just one method call away.</p>
<h3>Line Plot</h3>
<pre><code>import pandas as pd

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "sales": [150, 200, 180, 250, 300]
})

df.plot(x="month", y="sales", kind="line", marker="o")
plt.title("Monthly Sales")
plt.ylabel("Units Sold")
plt.show()</code></pre>
<h3>Bar Chart</h3>
<pre><code>df.plot(x="month", y="sales", kind="bar", color="steelblue")
plt.title("Sales by Month")
plt.show()</code></pre>
<h3>Histogram</h3>
<pre><code># Distribution of a numeric column
df["age"].plot(kind="hist", bins=20, edgecolor="black")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.show()</code></pre>
<h3>Scatter Plot</h3>
<pre><code>df.plot(x="hours_studied", y="exam_score", kind="scatter")
plt.title("Study Hours vs Exam Score")
plt.show()</code></pre>
<p>For publication-quality charts, use Matplotlib or Seaborn directly. Pandas plotting is best for quick exploration.</p>'''
            }
        )
        self._add_quiz(l4_4_2, [
            ("Which kind argument creates a bar chart using df.plot()?", [
                ("kind=\"line\"", False), ("kind=\"bar\"", True), ("kind=\"hist\"", False), ("kind=\"scatter\"", False)]),
            ("What does df[\"age\"].plot(kind=\"hist\", bins=20) create?", [
                ("A scatter plot", False), ("A histogram with 20 bins", True),
                ("A line chart", False), ("A pie chart", False)]),
            ("According to the lesson, when should you use Matplotlib or Seaborn directly instead of Pandas plotting?", [
                ("Never", False), ("For publication-quality charts", True),
                ("Only for line charts", False), ("Pandas plotting should always be used instead", False)]),
            ("What is Pandas' built-in plotting powered by?", [
                ("Seaborn", False), ("Matplotlib", True), ("Plotly", False), ("Bokeh", False)]),
        ])

        # ──────────────────────────────────────────────
        # Course 5: Matplotlib for Data Visualization
        # ──────────────────────────────────────────────
        course5, _ = Course.objects.get_or_create(
            title='Matplotlib for Data Visualization',
            defaults={
                'description': 'Learn Matplotlib from scratch - the foundational Python library for creating static, animated, and interactive visualisations.',
                'is_published': True,
            }
        )

        # Chapter 1: Getting Started
        ch5_1, _ = Chapter.objects.get_or_create(
            course=course5,
            title='Getting Started',
            defaults={'order': 1, 'description': 'Fundamentals of Matplotlib'}
        )
        l5_1_1, _ = Lesson.objects.get_or_create(
            chapter=ch5_1,
            title='Matplotlib Intro',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Matplotlib Intro</h2>
<p>Matplotlib is the most widely used plotting library in Python. It gives you full control over every element of a figure - from line colours to axis labels to subplot layouts.</p>
<h3>Why Matplotlib?</h3>
<ul>
<li>Produces publication-quality figures</li>
<li>Highly customisable - control every pixel</li>
<li>Supports dozens of chart types</li>
<li>Integrates with Pandas, NumPy, and Jupyter</li>
<li>Foundation for higher-level libraries like Seaborn</li>
</ul>
<h3>Installation</h3>
<pre><code>pip install matplotlib</code></pre>
<h3>Quick Example</h3>
<pre><code>import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.title("Simple Line Plot")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()</code></pre>
<p>The <code>pyplot</code> interface (<code>plt</code>) is the most common way to use Matplotlib - it provides a MATLAB-like experience.</p>'''
            }
        )
        self._add_quiz(l5_1_1, [
            ("Which command installs Matplotlib via pip?", [
                ("pip install matplotlib", True), ("pip get matplotlib", False),
                ("pip add-plot", False), ("conda install only", False)]),
            ("What style of experience does the pyplot interface provide, per the lesson?", [
                ("A MATLAB-like experience", True), ("A pure object-oriented experience", False),
                ("A database query experience", False), ("A markup language experience", False)]),
            ("What is Matplotlib described as being the foundation for?", [
                ("Pandas", False), ("NumPy", False),
                ("Higher-level libraries like Seaborn", True), ("Scikit-learn", False)]),
            ("In the quick example, which function sets the plot's x-axis label?", [
                ("plt.title()", False), ("plt.xlabel()", True), ("plt.ylabel()", False), ("plt.label()", False)]),
        ])
        l5_1_2, _ = Lesson.objects.get_or_create(
            chapter=ch5_1,
            title='Get Started',
            defaults={
                'order': 2,
                'is_free': True,
                'content': '''<h2>Get Started with Matplotlib</h2>
<p>Every Matplotlib figure follows the same pattern: create a figure, add plots, customise, and display.</p>
<h3>The Basic Workflow</h3>
<pre><code>import matplotlib.pyplot as plt

# 1. Create figure and axes
fig, ax = plt.subplots()

# 2. Plot data
ax.plot([1, 2, 3, 4], [10, 20, 25, 30])

# 3. Customise
ax.set_title("My First Plot")
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")

# 4. Display
plt.show()</code></pre>
<h3>Figure vs Axes</h3>
<ul>
<li><strong>Figure</strong> - the entire canvas (can contain multiple plots)</li>
<li><strong>Axes</strong> - a single plot within the figure</li>
</ul>
<pre><code># Multiple axes in one figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.plot([1, 2, 3], [1, 4, 9])
ax1.set_title("Plot 1")

ax2.bar(["A", "B", "C"], [5, 3, 7])
ax2.set_title("Plot 2")

plt.tight_layout()
plt.show()</code></pre>
<p>Use the <code>fig, ax</code> interface (object-oriented) for complex plots - it gives you explicit control over which plot you're modifying.</p>'''
            }
        )
        self._add_quiz(l5_1_2, [
            ("What is the difference between a Figure and Axes in Matplotlib?", [
                ("They are the same thing", False),
                ("A Figure is the entire canvas; Axes is a single plot within it", True),
                ("Axes is bigger than the Figure", False), ("A Figure can only contain one Axes", False)]),
            ("Which function creates a figure with 1 row and 2 columns of subplots?", [
                ("plt.subplots(1, 2)", True), ("plt.figure(1, 2)", False),
                ("plt.axes(1, 2)", False), ("plt.grid(1, 2)", False)]),
            ("What interface does the lesson recommend for complex plots requiring explicit control?", [
                ("The pyplot state-machine interface", False),
                ("The object-oriented fig, ax interface", True),
                ("The pandas plotting interface", False), ("The seaborn interface", False)]),
            ("What is step 1 of the \"basic workflow\" described in the lesson?", [
                ("Display the plot", False), ("Customise the axes", False),
                ("Create figure and axes", True), ("Plot the data", False)]),
        ])
        l5_1_3, _ = Lesson.objects.get_or_create(
            chapter=ch5_1,
            title='Pyplot',
            defaults={
                'order': 3,
                'is_free': True,
                'content': '''<h2>Pyplot</h2>
<p><code>matplotlib.pyplot</code> is a collection of functions that make Matplotlib work like MATLAB. Each function makes some change to a figure - adding a line, changing colours, labelling axes.</p>
<h3>Common Pyplot Functions</h3>
<pre><code>import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 4, 9, 16, 25]

plt.figure(figsize=(8, 5))     # Set figure size
plt.plot(x, y, "ro-")          # Red, circle markers, solid line
plt.title("Quadratic Growth")   # Title
plt.xlabel("x")                # X axis label
plt.ylabel("y = x²")           # Y axis label
plt.grid(True)                 # Show grid
plt.legend(["y = x²"])         # Legend
plt.savefig("plot.png", dpi=150)  # Save to file
plt.show()                     # Display</code></pre>
<h3>Format Strings</h3>
<p>The shorthand <code>"ro-"</code> means: red (r), circle marker (o), solid line (-).</p>
<pre><code>"b-"   # Blue solid line
"g--"  # Green dashed line
"k^:"  # Black triangle-up markers, dotted line
"ms"   # Magenta square markers, no line</code></pre>
<p>Pyplot is great for quick plots. For production code, prefer the object-oriented <code>fig, ax</code> interface.</p>'''
            }
        )
        self._add_quiz(l5_1_3, [
            ("What does the format string \"ro-\" mean?", [
                ("Blue dashed line", False), ("Red, circle markers, solid line", True),
                ("Green dotted line", False), ("Black square markers", False)]),
            ("Which function saves a plot to a file?", [
                ("plt.export()", False), ("plt.savefig()", True), ("plt.save()", False), ("plt.write()", False)]),
            ("What does the format string \"g--\" represent?", [
                ("Green dashed line", True), ("Grey solid line", False),
                ("Gold dotted line", False), ("Green solid line", False)]),
            ("According to the lesson, when is pyplot best suited versus the object-oriented interface?", [
                ("For production code", False), ("For quick plots", True),
                ("Never, pyplot should be avoided", False), ("Only for 3D plots", False)]),
        ])
        l5_1_4, _ = Lesson.objects.get_or_create(
            chapter=ch5_1,
            title='Plotting',
            defaults={
                'order': 4,
                'is_free': True,
                'content': '''<h2>Plotting Data</h2>
<p>Matplotlib supports many plot types. Here are the most commonly used ones for data science.</p>
<h3>Line Plot - Trends Over Time</h3>
<pre><code>import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [12000, 15000, 13500, 18000, 22000, 19500]

plt.plot(months, revenue, marker="o", linewidth=2, color="#2563eb")
plt.fill_between(months, revenue, alpha=0.1, color="#2563eb")
plt.title("Monthly Revenue")
plt.ylabel("Revenue ($)")
plt.show()</code></pre>
<h3>Bar Chart - Comparisons</h3>
<pre><code>categories = ["Python", "R", "SQL", "Julia", "Scala"]
popularity = [85, 45, 60, 15, 10]

plt.bar(categories, popularity, color=["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6"])
plt.title("Language Popularity in Data Science")
plt.ylabel("Popularity Score")
plt.show()</code></pre>
<h3>Histogram - Distribution</h3>
<pre><code>import numpy as np

data = np.random.normal(100, 15, 1000)

plt.hist(data, bins=30, edgecolor="black", alpha=0.7)
plt.title("Distribution of Test Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.show()</code></pre>
<p>Choose the right chart for your data: line for trends, bar for comparisons, histogram for distributions.</p>'''
            }
        )
        self._add_quiz(l5_1_4, [
            ("Which chart type does the lesson recommend for showing trends over time?", [
                ("Bar chart", False), ("Line plot", True), ("Pie chart", False), ("Histogram", False)]),
            ("In the bar chart example, which language has the highest popularity score?", [
                ("R", False), ("SQL", False), ("Python", True), ("Julia", False)]),
            ("Which function is used to shade the area under a line plot in the revenue example?", [
                ("plt.shade()", False), ("plt.fill_between()", True),
                ("plt.area()", False), ("plt.fill_under()", False)]),
            ("What does the lesson recommend for visualising a distribution of a numeric variable?", [
                ("A histogram", True), ("A pie chart", False),
                ("A bar chart", False), ("A scatter plot only", False)]),
        ])

        # Chapter 2: Styling Plots
        ch5_2, _ = Chapter.objects.get_or_create(
            course=course5,
            title='Styling Plots',
            defaults={'order': 2, 'description': 'Customising the look of your charts'}
        )
        l5_2_1, _ = Lesson.objects.get_or_create(
            chapter=ch5_2,
            title='Markers',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Markers</h2>
<p>Markers highlight individual data points on a plot. They are especially useful in scatter plots and line plots with sparse data.</p>
<h3>Marker Styles</h3>
<pre><code>import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 8, 5]

# Different marker styles
plt.plot(x, y, marker="o", label="Circle")
plt.plot(x, [v+1 for v in y], marker="s", label="Square")
plt.plot(x, [v+2 for v in y], marker="^", label="Triangle")
plt.plot(x, [v+3 for v in y], marker="D", label="Diamond")
plt.legend()
plt.title("Marker Styles")
plt.show()</code></pre>
<h3>Customising Markers</h3>
<pre><code>plt.plot(x, y,
    marker="o",
    markersize=10,           # Size
    markerfacecolor="red",   # Fill colour
    markeredgecolor="black", # Border colour
    markeredgewidth=2        # Border width
)</code></pre>
<h3>Common Marker Codes</h3>
<table>
<thead><tr><th>Code</th><th>Marker</th></tr></thead>
<tbody>
<tr><td>o</td><td>Circle</td></tr>
<tr><td>s</td><td>Square</td></tr>
<tr><td>^</td><td>Triangle up</td></tr>
<tr><td>D</td><td>Diamond</td></tr>
<tr><td>*</td><td>Star</td></tr>
<tr><td>+</td><td>Plus</td></tr>
</tbody>
</table>'''
            }
        )
        self._add_quiz(l5_2_1, [
            ("What marker shape does the code \"s\" represent, per the lesson's table?", [
                ("Circle", False), ("Square", True), ("Triangle up", False), ("Diamond", False)]),
            ("Which parameter controls the fill colour of a marker?", [
                ("markeredgecolor", False), ("markerfacecolor", True), ("markersize", False), ("color", False)]),
            ("What marker code represents a triangle pointing up?", [
                ("o", False), ("s", False), ("^", True), ("D", False)]),
            ("Where are markers especially useful, according to the lesson?", [
                ("Pie charts only", False), ("Scatter plots and line plots with sparse data", True),
                ("Bar charts only", False), ("Heatmaps", False)]),
        ])
        l5_2_2, _ = Lesson.objects.get_or_create(
            chapter=ch5_2,
            title='Line',
            defaults={
                'order': 2,
                'is_free': False,
                'content': '''<h2>Line Styling</h2>
<p>Line style controls how connecting lines appear between data points - solid, dashed, dotted, or dash-dot.</p>
<h3>Line Styles</h3>
<pre><code>import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4, 5]
y1 = [0, 1, 4, 9, 16, 25]
y2 = [0, 2, 4, 6, 8, 10]
y3 = [25, 20, 15, 10, 5, 0]

plt.plot(x, y1, linestyle="-",  linewidth=2, label="Solid")
plt.plot(x, y2, linestyle="--", linewidth=2, label="Dashed")
plt.plot(x, y3, linestyle=":",  linewidth=2, label="Dotted")
plt.legend()
plt.title("Line Styles")
plt.show()</code></pre>
<h3>Line Width and Colour</h3>
<pre><code>plt.plot(x, y1, color="#2563eb", linewidth=3, alpha=0.8)
plt.plot(x, y2, color="crimson", linewidth=1.5)</code></pre>
<h3>Available Line Styles</h3>
<table>
<thead><tr><th>Code</th><th>Style</th></tr></thead>
<tbody>
<tr><td>-</td><td>Solid</td></tr>
<tr><td>--</td><td>Dashed</td></tr>
<tr><td>:</td><td>Dotted</td></tr>
<tr><td>-.</td><td>Dash-dot</td></tr>
</tbody>
</table>
<p>Use different line styles to distinguish multiple series, especially when printing in black and white.</p>'''
            }
        )
        self._add_quiz(l5_2_2, [
            ("Which linestyle code represents a dashed line?", [
                ("-", False), ("--", True), (":", False), ("-.", False)]),
            ("What does the alpha parameter control when styling a line?", [
                ("Line width", False), ("Transparency", True), ("Marker size", False), ("Color hue", False)]),
            ("What does the linestyle code \"-.\" represent?", [
                ("Solid", False), ("Dashed", False), ("Dotted", False), ("Dash-dot", True)]),
            ("Why does the lesson recommend using different line styles for multiple series?", [
                ("To increase file size", False),
                ("To distinguish series, especially in black and white printing", True),
                ("It is required by Matplotlib", False), ("To slow down rendering", False)]),
        ])
        l5_2_3, _ = Lesson.objects.get_or_create(
            chapter=ch5_2,
            title='Labels',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Labels</h2>
<p>Labels and titles make your plots readable. Without them, your audience has no idea what they're looking at.</p>
<h3>Essential Labels</h3>
<pre><code>import matplotlib.pyplot as plt

x = ["Q1", "Q2", "Q3", "Q4"]
revenue = [120, 150, 135, 180]
costs = [90, 100, 95, 110]

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(x, revenue, marker="o", label="Revenue")
ax.plot(x, costs, marker="s", label="Costs")

ax.set_title("Quarterly Financial Performance", fontsize=14, fontweight="bold")
ax.set_xlabel("Quarter", fontsize=12)
ax.set_ylabel("Amount ($K)", fontsize=12)
ax.legend(loc="upper left", fontsize=10)

plt.tight_layout()
plt.show()</code></pre>
<h3>Text Annotations</h3>
<pre><code># Add text at a specific point
ax.annotate("Peak", xy=("Q4", 180), xytext=("Q3", 190),
            arrowprops=dict(arrowstyle="->", color="red"),
            fontsize=10, color="red")</code></pre>
<h3>Rotating Labels</h3>
<pre><code># Useful when labels overlap
plt.xticks(rotation=45, ha="right")</code></pre>
<p>Good labels answer: What is being measured? What are the units? What time period?</p>'''
            }
        )
        self._add_quiz(l5_2_3, [
            ("Which method adds an arrow annotation pointing to a specific data point?", [
                ("ax.text()", False), ("ax.annotate()", True), ("ax.label()", False), ("ax.point()", False)]),
            ("What does plt.xticks(rotation=45, ha=\"right\") help with?", [
                ("Changing plot colours", False), ("Preventing overlapping x-axis labels", True),
                ("Adding a legend", False), ("Setting the figure size", False)]),
            ("What three things should good labels answer, according to the lesson?", [
                ("What is measured, what are the units, what time period", True),
                ("Who made the chart, when, and why", False),
                ("The file name, size, and format", False), ("The programming language and version", False)]),
            ("Which parameter controls where the legend appears on the plot?", [
                ("loc", True), ("position", False), ("place", False), ("anchor", False)]),
        ])
        l5_2_4, _ = Lesson.objects.get_or_create(
            chapter=ch5_2,
            title='Grid',
            defaults={
                'order': 4,
                'is_free': False,
                'content': '''<h2>Grid</h2>
<p>Grid lines help readers estimate values from a plot. They're optional but often improve readability.</p>
<h3>Basic Grid</h3>
<pre><code>import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 25, 18, 35, 28]

plt.plot(x, y, marker="o")
plt.grid(True)
plt.title("With Grid")
plt.show()</code></pre>
<h3>Customising the Grid</h3>
<pre><code>plt.plot(x, y, marker="o")

plt.grid(True,
    linestyle="--",    # Dashed lines
    alpha=0.5,         # Semi-transparent
    color="gray",      # Grey colour
    linewidth=0.5      # Thin lines
)

plt.title("Customised Grid")
plt.show()</code></pre>
<h3>Axis-Specific Grid</h3>
<pre><code>ax.grid(True, axis="y")   # Horizontal lines only
ax.grid(True, axis="x")   # Vertical lines only</code></pre>
<h3>Grid Behind the Data</h3>
<pre><code># Set zorder so grid draws behind the plot line
ax.set_axisbelow(True)
ax.grid(True, linestyle="--", alpha=0.3)</code></pre>
<p>Use subtle grids - thick, dark lines compete with the data. Light dashed lines are the standard.</p>'''
            }
        )
        self._add_quiz(l5_2_4, [
            ("What does ax.set_axisbelow(True) accomplish?", [
                ("Hides the grid", False), ("Draws the grid behind the plotted data", True),
                ("Removes the axis labels", False), ("Makes the grid bold", False)]),
            ("Which parameter restricts grid lines to horizontal only?", [
                ("axis=\"x\"", False), ("axis=\"y\"", True), ("axis=\"both\"", False), ("axis=\"horizontal\"", False)]),
            ("What style of grid lines does the lesson recommend as the standard?", [
                ("Thick, dark solid lines", False), ("Light dashed lines", True),
                ("No grid at all", False), ("Bright red lines", False)]),
            ("What does plt.grid(True) do?", [
                ("Removes the grid", False), ("Displays grid lines on the plot", True),
                ("Changes the plot colour", False), ("Adds a legend", False)]),
        ])

        # Chapter 3: Chart Types
        ch5_3, _ = Chapter.objects.get_or_create(
            course=course5,
            title='Chart Types',
            defaults={'order': 3, 'description': 'Different chart types for different data'}
        )
        l5_3_1, _ = Lesson.objects.get_or_create(
            chapter=ch5_3,
            title='Subplot',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Subplot</h2>
<p>Subplots let you display multiple charts in a single figure - essential for dashboards and comparing related data side by side.</p>
<h3>Creating Subplots</h3>
<pre><code>import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top-left: Line plot
axes[0, 0].plot([1, 2, 3, 4], [1, 4, 9, 16])
axes[0, 0].set_title("Line Plot")

# Top-right: Bar chart
axes[0, 1].bar(["A", "B", "C"], [5, 3, 7])
axes[0, 1].set_title("Bar Chart")

# Bottom-left: Scatter plot
axes[1, 0].scatter([1, 2, 3, 4, 5], [2, 4, 1, 8, 5])
axes[1, 0].set_title("Scatter Plot")

# Bottom-right: Histogram
axes[1, 1].hist([1, 1, 2, 2, 2, 3, 3, 4], bins=4)
axes[1, 1].set_title("Histogram")

plt.tight_layout()
plt.show()</code></pre>
<h3>Shared Axes</h3>
<pre><code># Share y-axis across subplots for easy comparison
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)</code></pre>
<h3>Unequal Sizes</h3>
<pre><code>import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(10, 4))
gs = gridspec.GridSpec(1, 3, width_ratios=[2, 1, 1])

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])
ax3 = fig.add_subplot(gs[2])</code></pre>'''
            }
        )
        self._add_quiz(l5_3_1, [
            ("What does plt.subplots(2, 2, figsize=(10, 8)) create?", [
                ("A single plot", False), ("A 2x2 grid of subplots", True),
                ("2 separate figures", False), ("A 4x4 grid", False)]),
            ("What does sharey=True do when creating subplots?", [
                ("Shares the x-axis across subplots", False),
                ("Shares the y-axis across subplots for easy comparison", True),
                ("Merges the subplots into one", False), ("Hides the y-axis", False)]),
            ("Which module allows creating subplots with unequal sizes using width_ratios?", [
                ("matplotlib.gridspec", True), ("matplotlib.axes", False),
                ("matplotlib.figure", False), ("matplotlib.style", False)]),
            ("In the lesson's 2x2 example, which chart type appears in the bottom-right subplot?", [
                ("Line plot", False), ("Bar chart", False), ("Scatter plot", False), ("Histogram", True)]),
        ])
        l5_3_2, _ = Lesson.objects.get_or_create(
            chapter=ch5_3,
            title='Scatter',
            defaults={
                'order': 2,
                'is_free': False,
                'content': '''<h2>Scatter Plot</h2>
<p>Scatter plots reveal relationships between two variables. Each point represents one observation - its position shows the values of both variables.</p>
<h3>Basic Scatter Plot</h3>
<pre><code>import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.normal(50, 15, 100)
y = x * 1.2 + np.random.normal(0, 10, 100)

plt.scatter(x, y, alpha=0.6, edgecolors="black", linewidths=0.5)
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.title("Study Hours vs Exam Performance")
plt.show()</code></pre>
<h3>Coloured by Category</h3>
<pre><code>categories = np.random.choice(["A", "B", "C"], 100)
colours = {"A": "#3b82f6", "B": "#ef4444", "C": "#10b981"}

for cat in ["A", "B", "C"]:
    mask = categories == cat
    plt.scatter(x[mask], y[mask], c=colours[cat], label=cat, alpha=0.6)

plt.legend()
plt.title("Scatter Plot by Category")
plt.show()</code></pre>
<h3>Bubble Chart (Size by Value)</h3>
<pre><code>sizes = np.random.uniform(20, 200, 100)
plt.scatter(x, y, s=sizes, alpha=0.4, c=y, cmap="viridis")
plt.colorbar(label="Score")
plt.show()</code></pre>
<p>Scatter plots are your go-to for exploring correlations and spotting outliers.</p>'''
            }
        )
        self._add_quiz(l5_3_2, [
            ("What does each point in a scatter plot represent?", [
                ("A category label", False), ("One observation, positioned by two variable values", True),
                ("The mean of the dataset", False), ("A regression line", False)]),
            ("In the bubble chart example, what does the s parameter control?", [
                ("The colour of points", False), ("The size of each point", True),
                ("The shape of markers", False), ("The transparency", False)]),
            ("What is a scatter plot most useful for, per the lesson?", [
                ("Showing proportions of a whole", False), ("Exploring correlations and spotting outliers", True),
                ("Displaying time-series trends only", False), ("Comparing categorical counts", False)]),
            ("In the \"coloured by category\" example, how many categories are used?", [
                ("2", False), ("3", True), ("4", False), ("5", False)]),
        ])
        l5_3_3, _ = Lesson.objects.get_or_create(
            chapter=ch5_3,
            title='Bars',
            defaults={
                'order': 3,
                'is_free': False,
                'content': '''<h2>Bar Charts</h2>
<p>Bar charts compare quantities across categories. They are one of the most intuitive and widely used chart types.</p>
<h3>Vertical Bar Chart</h3>
<pre><code>import matplotlib.pyplot as plt

languages = ["Python", "R", "SQL", "Julia", "Java"]
scores = [92, 78, 85, 45, 60]

plt.bar(languages, scores, color="#3b82f6", edgecolor="white")
plt.title("Language Popularity in Data Science")
plt.ylabel("Popularity Score")
plt.ylim(0, 100)
plt.show()</code></pre>
<h3>Horizontal Bar Chart</h3>
<pre><code>plt.barh(languages, scores, color="#3b82f6")
plt.title("Language Popularity")
plt.xlabel("Score")
plt.show()</code></pre>
<h3>Grouped Bar Chart</h3>
<pre><code>import numpy as np

x = np.arange(len(languages))
width = 0.35

plt.bar(x - width/2, scores, width, label="2024", color="#3b82f6")
plt.bar(x + width/2, [s+5 for s in scores], width, label="2025", color="#f59e0b")

plt.xticks(x, languages)
plt.legend()
plt.title("Year-over-Year Comparison")
plt.show()</code></pre>
<h3>Stacked Bar Chart</h3>
<pre><code>plt.bar(languages, [60, 40, 50, 20, 35], label="Beginner", color="#93c5fd")
plt.bar(languages, [32, 38, 35, 25, 25], bottom=[60, 40, 50, 20, 35],
        label="Advanced", color="#1d4ed8")
plt.legend()
plt.show()</code></pre>'''
            }
        )
        self._add_quiz(l5_3_3, [
            ("Which function creates a horizontal bar chart?", [
                ("plt.bar()", False), ("plt.barh()", True), ("plt.hbar()", False), ("plt.rowbar()", False)]),
            ("In a grouped bar chart, how are bars offset so they sit side by side?", [
                ("Using width and x - width/2 / x + width/2 offsets", True), ("Using alpha", False),
                ("Using bottom", False), ("Using edgecolor", False)]),
            ("Which parameter creates a stacked bar chart by placing one bar on top of another?", [
                ("width", False), ("bottom", True), ("stack=True", False), ("offset", False)]),
            ("What is the highest score in the lesson's language popularity bar chart example?", [
                ("Python at 92", True), ("R at 78", False), ("SQL at 85", False), ("Java at 60", False)]),
        ])
        l5_3_4, _ = Lesson.objects.get_or_create(
            chapter=ch5_3,
            title='Histograms',
            defaults={
                'order': 4,
                'is_free': False,
                'content': '''<h2>Histograms</h2>
<p>Histograms show the distribution of a single numeric variable. They divide the data into bins and count how many values fall into each bin.</p>
<h3>Basic Histogram</h3>
<pre><code>import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(100, 15, 1000)

plt.hist(data, bins=30, edgecolor="black", alpha=0.7)
plt.title("Distribution of Test Scores")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.show()</code></pre>
<h3>Adjusting Bins</h3>
<pre><code># Fewer bins = smoother, more bins = more detail
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.hist(data, bins=10, edgecolor="black", alpha=0.7)
ax1.set_title("10 Bins")

ax2.hist(data, bins=50, edgecolor="black", alpha=0.7)
ax2.set_title("50 Bins")

plt.tight_layout()
plt.show()</code></pre>
<h3>Overlapping Distributions</h3>
<pre><code>group_a = np.random.normal(100, 15, 500)
group_b = np.random.normal(115, 15, 500)

plt.hist(group_a, bins=30, alpha=0.5, label="Group A", color="#3b82f6")
plt.hist(group_b, bins=30, alpha=0.5, label="Group B", color="#ef4444")
plt.legend()
plt.title("Score Distribution by Group")
plt.show()</code></pre>
<p>Histograms are essential for understanding your data's shape: is it symmetric? Skewed? Are there gaps or outliers?</p>'''
            }
        )
        self._add_quiz(l5_3_4, [
            ("What does increasing the number of bins in a histogram generally do?", [
                ("Smooths the distribution", False), ("Shows more detail", True),
                ("Removes outliers", False), ("Changes the data values", False)]),
            ("Which parameter allows two overlapping histograms to both be visible?", [
                ("bins", False), ("alpha (transparency)", True), ("edgecolor", False), ("density", False)]),
            ("What three questions does the lesson say histograms help answer about data shape?", [
                ("Is it symmetric, skewed, and are there gaps or outliers", True),
                ("What is the mean, median, and mode", False),
                ("What is the sample size, source, and format", False),
                ("What colour, size, and shape to use", False)]),
            ("In the lesson's basic example, what distribution is used to generate the sample data?", [
                ("Uniform distribution", False), ("Normal distribution", True),
                ("Binomial distribution", False), ("Poisson distribution", False)]),
        ])
        l5_3_5, _ = Lesson.objects.get_or_create(
            chapter=ch5_3,
            title='Pie Charts',
            defaults={
                'order': 5,
                'is_free': False,
                'content': '''<h2>Pie Charts</h2>
<p>Pie charts show how a whole is divided into parts. Use them sparingly - they're best for showing proportions when you have a small number of categories (2-5).</p>
<h3>Basic Pie Chart</h3>
<pre><code>import matplotlib.pyplot as plt

categories = ["Python", "R", "SQL", "Julia", "Other"]
shares = [45, 20, 25, 5, 5]

plt.pie(shares, labels=categories, autopct="%1.1f%%")
plt.title("Language Market Share")
plt.show()</code></pre>
<h3>Styled Pie Chart</h3>
<pre><code>colours = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6"]
explode = [0.05, 0, 0, 0, 0]  # Slightly separate the first slice

plt.pie(shares,
    labels=categories,
    colors=colours,
    explode=explode,
    autopct="%1.1f%%",
    shadow=True,
    startangle=90
)
plt.title("Language Market Share")
plt.show()</code></pre>
<h3>Donut Chart</h3>
<pre><code>plt.pie(shares, labels=categories, colors=colours, autopct="%1.1f%%",
        pctdistance=0.85)

# Add a white circle in the centre
centre_circle = plt.Circle((0, 0), 0.60, fc="white")
plt.gca().add_artist(centre_circle)

plt.title("Language Market Share")
plt.show()</code></pre>
<p>Avoid pie charts when you have many categories or when categories have similar values - bar charts are easier to read in those cases.</p>'''
            }
        )
        self._add_quiz(l5_3_5, [
            ("What does the explode parameter do in a pie chart?", [
                ("Removes a slice", False), ("Slightly separates a slice from the rest", True),
                ("Changes slice colours", False), ("Adds a legend", False)]),
            ("How is a donut chart created from a pie chart, per the lesson?", [
                ("By adding a white circle in the centre", True), ("By using plt.donut()", False),
                ("By setting explode=1", False), ("By using bar charts instead", False)]),
            ("According to the lesson, when should pie charts be avoided?", [
                ("When there are many categories or similar values", True), ("When there are only 2 categories", False),
                ("Always", False), ("When using Matplotlib", False)]),
            ("What does autopct=\"%1.1f%%\" display on the pie chart?", [
                ("The category names only", False), ("The percentage value of each slice", True),
                ("The raw counts", False), ("The colour codes", False)]),
        ])

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Total chapters: {Chapter.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total lessons: {Lesson.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total quizzes: {Quiz.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total questions: {Question.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total choices: {Choice.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write(self.style.SUCCESS('  Instructor: instructor / instructor123'))
        self.stdout.write(self.style.SUCCESS('  Student: student / student123'))
