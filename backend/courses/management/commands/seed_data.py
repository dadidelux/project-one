from django.core.management.base import BaseCommand
from accounts.models import User
from courses.models import Course, Chapter, Lesson


class Command(BaseCommand):
    help = 'Seed the database with sample Data Science courses'

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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 2: Python Refresher
        ch1_2, _ = Chapter.objects.get_or_create(
            course=course1,
            title='Python Refresher',
            defaults={'order': 2, 'description': 'A full Python fundamentals pass for beginners'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 3: Python for Data Science
        ch1_3, _ = Chapter.objects.get_or_create(
            course=course1,
            title='Python for Data Science',
            defaults={'order': 3, 'description': 'Essential Python skills for working with data'}
        )
        Lesson.objects.get_or_create(
            chapter=ch1_3,
            title='Classes and Dataclasses',
            defaults={
                'order': 1,
                'is_free': True,
                'content': '''<h2>Classes and Dataclasses</h2>
<p>Classes are the building blocks of object-oriented programming in Python. They let you bundle data and behaviour into a single, reusable unit — essential when your data science projects grow beyond simple scripts.</p>
<h3>Why Classes Matter in Data Science</h3>
<ul>
<li><strong>Organise related data and functions</strong> — a <code>DataPipeline</code> class can hold config, cleaning steps, and output in one place</li>
<li><strong>Reusable components</strong> — build a <code>Model</code> base class and extend it for different algorithms</li>
<li><strong>Cleaner APIs</strong> — scikit-learn's fit/predict interface is built on classes</li>
</ul>
<h3>Defining a Class</h3>
<pre><code>class Student:
    def __init__(self, name: str, grade: float):
        self.name = name
        self.grade = grade

    def is_passing(self) -> bool:
        return self.grade >= 50

    def __repr__(self) -> str:
        return f"Student(name='{self.name}', grade={self.grade})"

s = Student("Alice", 88)
print(s.is_passing())  # True
print(s)               # Student(name='Alice', grade=88)</code></pre>
<h3>Instance vs Class Attributes</h3>
<pre><code>class Counter:
    count = 0                       # class attribute — shared

    def __init__(self):
        Counter.count += 1          # modifies the class attribute
        self.id = Counter.count     # instance attribute — unique

a = Counter()
b = Counter()
print(a.id, b.id)        # 1 2
print(Counter.count)     # 2</code></pre>
<h3>Inheritance</h3>
<p>Create specialised versions of an existing class:</p>
<pre><code>class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

for animal in [Dog(), Cat()]:
    print(animal.speak())
# Woof!
# Meow!</code></pre>
<h3>Introducing Dataclasses (Python 3.7+)</h3>
<p>When a class mainly holds data, <code>@dataclass</code> eliminates boilerplate by auto-generating <code>__init__</code>, <code>__repr__</code>, and <code>__eq__</code>:</p>
<pre><code>from dataclasses import dataclass

@dataclass
class DataPoint:
    label: str
    value: float
    timestamp: str

dp = DataPoint("temperature", 23.5, "2025-01-15")
print(dp)  # DataPoint(label='temperature', value=23.5, timestamp='2025-01-15')</code></pre>
<h3>Dataclass Features</h3>
<pre><code>from dataclasses import dataclass, field

@dataclass
class Experiment:
    name: str
    trials: int = 0                        # default value
    results: list = field(default_factory=list)  # mutable default

    def run(self, result: float):
        self.results.append(result)
        self.trials += 1

    @property
    def average(self) -> float:
        return sum(self.results) / self.trials if self.trials else 0.0

exp = Experiment("A/B Test")
exp.run(0.42)
exp.run(0.38)
print(exp.average)  # 0.4</code></pre>
<h3>Regular Classes vs Dataclasses</h3>
<table>
<thead><tr><th>Feature</th><th>Regular Class</th><th>Dataclass</th></tr></thead>
<tbody>
<tr><td><code>__init__</code></td><td>Write it yourself</td><td>Auto-generated</td></tr>
<tr><td><code>__repr__</code></td><td>Write it yourself</td><td>Auto-generated</td></tr>
<tr><td><code>__eq__</code></td><td>Write it yourself</td><td>Auto-generated (compares all fields)</td></tr>
<tr><td>Mutable defaults</td><td>Tricky (shared references)</td><td><code>field(default_factory=...)</code></td></tr>
<tr><td>Validation</td><td>In <code>__init__</code></td><td><code>__post_init__</code></td></tr>
<tr><td>Best for</td><td>Complex logic, inheritance</td><td>Data containers, config, DTOs</td></tr>
</tbody>
</table>
<h3>When to Use What</h3>
<ul>
<li><strong>Dataclass</strong> — storing data with minimal behaviour (config objects, API responses, record types)</li>
<li><strong>Regular class</strong> — complex methods, inheritance hierarchies, custom initialisation logic</li>
<li><strong>Named tuple</strong> — immutable, lightweight alternative when you don't need mutation</li>
</ul>
<p>In data science workflows, dataclasses are perfect for structuring experiment configs, pipeline steps, and model parameters — anywhere you want clear, typed data without boilerplate.</p>'''
            }
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 2: Statistics Fundamentals
        ch2_2, _ = Chapter.objects.get_or_create(
            course=course2,
            title='Statistics Fundamentals',
            defaults={'order': 2, 'description': 'Statistical concepts for analysing and interpreting data'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 2: Working with Data
        ch4_2, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Working with Data',
            defaults={'order': 2, 'description': 'Reading, analysing, and summarising data'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 3: Data Cleaning
        ch4_3, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Data Cleaning',
            defaults={'order': 3, 'description': 'Handling messy real-world data'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 4: Analysis & Visualization
        ch4_4, _ = Chapter.objects.get_or_create(
            course=course4,
            title='Analysis & Visualization',
            defaults={'order': 4, 'description': 'Finding patterns and visualising data'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 2: Styling Plots
        ch5_2, _ = Chapter.objects.get_or_create(
            course=course5,
            title='Styling Plots',
            defaults={'order': 2, 'description': 'Customising the look of your charts'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        # Chapter 3: Chart Types
        ch5_3, _ = Chapter.objects.get_or_create(
            course=course5,
            title='Chart Types',
            defaults={'order': 3, 'description': 'Different chart types for different data'}
        )
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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
        Lesson.objects.get_or_create(
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Total chapters: {Chapter.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total lessons: {Lesson.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write(self.style.SUCCESS('  Instructor: instructor / instructor123'))
        self.stdout.write(self.style.SUCCESS('  Student: student / student123'))
        self.stdout.write(self.style.SUCCESS(f'Total chapters: {Chapter.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total lessons: {Lesson.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\nLogin credentials:'))
        self.stdout.write(self.style.SUCCESS('  Instructor: instructor / instructor123'))
        self.stdout.write(self.style.SUCCESS('  Student: student / student123'))
