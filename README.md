# Accuknox Django Trainee Assignment

## Overview

This repository contains solutions for the Django Trainee assignment provided by Accuknox. The assignment demonstrates the behavior of Django signals and implements a custom iterable `Rectangle` class in Python.

---

# Project Structure

```text
Accuknox_Assignment/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── Accuknox_Assignment/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── signal_assignment/
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── migrations/
│   └── management/
│       └── commands/
│           └── demonstrate_signals.py
│
└── rectangle_assignment/
    └── rectangle.py
```

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Accuknox_Assignment
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Topic 1: Django Signals

The assignment investigates three properties of Django signals:

## Question 1

### Are Django signals executed synchronously or asynchronously by default?

### Answer

**Django signals are synchronous by default.**

### Proof

A `post_save` signal handler introduces a delay using `time.sleep(2)`. Execution returns to the caller only after the signal handler completes.

Example output:

```text
Before save
Signal started
Signal finished
After save
Elapsed time: 2.00 seconds
```

### Conclusion

The caller waits for the signal to finish execution, demonstrating synchronous behavior.

---

## Question 2

### Do Django signals run in the same thread as the caller?

### Answer

**Yes. Django signals execute in the same thread by default.**

### Proof

Thread IDs are printed inside both the caller and the signal handler.

Example output:

```text
Caller thread ID: 140589673545472
Signal thread ID: 140589673545472
```

### Conclusion

Since both thread IDs are identical, signals run in the same thread as the caller.

---

## Question 3

### Do Django signals run in the same database transaction as the caller?

### Answer

**Yes. By default, signals execute within the same database transaction as the caller.**

### Proof

A record is created inside the signal handler and an exception is intentionally raised.

Example result:

```text
Transaction rolled back
```

Checking the database:

```python
TestModel.objects.count()
LogModel.objects.count()
```

Output:

```text
0
0
```

### Conclusion

Both database operations are rolled back together, proving that signals participate in the same transaction.

---

# Running the Demonstration

Execute the custom management command:

```bash
python manage.py demonstrate_signals
```

This command demonstrates:

* Synchronous execution of signals.
* Signal execution within the same thread.
* Signal participation in the same database transaction.

---

# Topic 2: Custom Python Class

## Rectangle Class

### Requirements

* Initialize with:

```python
length: int
width: int
```

* The object should be iterable.
* Iteration should first return:

```python
{'length': value}
```

followed by:

```python
{'width': value}
```

---

## Example

```python
from rectangle_assignment.rectangle import Rectangle

rect = Rectangle(10, 5)

for item in rect:
    print(item)
```

Output:

```python
{'length': 10}
{'width': 5}
```

---

# Technologies Used

* Python 3.x
* Django
* SQLite3

---

# Author

Submitted as part of the Django Trainee Assignment for Accuknox.
