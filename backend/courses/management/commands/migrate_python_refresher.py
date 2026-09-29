from django.core.management.base import BaseCommand
from courses.models import Course, Chapter, Lesson


class Command(BaseCommand):
    help = 'One-off migration to expand Python Refresher into a full chapter'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting Python Refresher migration...')

        # Get the course
        try:
            course1 = Course.objects.get(title='Introduction to Data Science')
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR('Course "Introduction to Data Science" not found'))
            return

        # Step 1: Find and remove the old thin Python Refresher lesson
        old_lesson = Lesson.objects.filter(
            chapter__course=course1,
            title='Python Refresher'
        ).first()

        if old_lesson:
            self.stdout.write(f'Found old Python Refresher lesson (id={old_lesson.id}). Deleting...')
            old_lesson.delete()
            self.stdout.write(self.style.SUCCESS('Deleted old Python Refresher lesson'))
        else:
            self.stdout.write('No old Python Refresher lesson found (may already be deleted)')

        # Step 2: Renumber existing Python for Data Science chapter from order=2 to order=3
        python_for_ds_chapter = Chapter.objects.filter(
            course=course1,
            title='Python for Data Science'
        ).first()

        if python_for_ds_chapter:
            self.stdout.write(f'Found Python for Data Science chapter (id={python_for_ds_chapter.id}). Updating order from {python_for_ds_chapter.order} to 3...')
            python_for_ds_chapter.order = 3
            python_for_ds_chapter.save()
            self.stdout.write(self.style.SUCCESS('Updated Python for Data Science chapter order to 3'))
        else:
            self.stdout.write(self.style.WARNING('Python for Data Science chapter not found'))

        # Step 3: Create new Python Refresher chapter with 10 lessons
        # Check if it already exists
        new_chapter = Chapter.objects.filter(
            course=course1,
            title='Python Refresher'
        ).first()

        if not new_chapter:
            self.stdout.write('Creating new Python Refresher chapter...')
            new_chapter = Chapter.objects.create(
                course=course1,
                title='Python Refresher',
                order=2,
                description='A full Python fundamentals pass for beginners'
            )
            self.stdout.write(self.style.SUCCESS(f'Created Python Refresher chapter (id={new_chapter.id})'))
        else:
            self.stdout.write(f'Python Refresher chapter already exists (id={new_chapter.id})')

        # Define the 10 lessons
        lessons_data = [
            {
                'title': 'Printing, Variables & Arithmetic',
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
            },
            {
                'title': 'Data Types, Type Casting & Checking Types',
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
            },
            {
                'title': 'Lists',
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
            },
            {
                'title': 'Tuples',
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
            },
            {
                'title': 'Dictionaries',
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
            },
            {
                'title': 'Conditional (If) Statements',
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
            },
            {
                'title': 'For-Loops',
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
            },
            {
                'title': 'While Loops',
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
            },
            {
                'title': 'Functions',
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
            },
            {
                'title': 'Functional Programming Concepts',
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
        ]

        # Create lessons
        for lesson_data in lessons_data:
            lesson, created = Lesson.objects.get_or_create(
                chapter=new_chapter,
                title=lesson_data['title'],
                defaults={
                    'order': lesson_data['order'],
                    'is_free': lesson_data['is_free'],
                    'content': lesson_data['content']
                }
            )
            if created:
                self.stdout.write(f'  Created lesson: {lesson_data["title"]}')
            else:
                self.stdout.write(f'  Lesson already exists: {lesson_data["title"]}')

        self.stdout.write(self.style.SUCCESS('Migration complete!'))
        self.stdout.write(f'Total chapters in course: {Chapter.objects.filter(course=course1).count()}')
        self.stdout.write(f'Total lessons in course: {Lesson.objects.filter(chapter__course=course1).count()}')
