## Hexagonal Architecture Implementation (Django)
 
This Application is a basic implementation of Hexangonal architecture in Django. This is a very simple application that takes a user name , email and stores them in **In-memory storage**.

## Overview

This application provides a simple service: it accepts a username and email and stores them in **In-Memory storage**. 

* **Logic:** If the user doesn't exist, they are added.
* **Validation:** If the user already exists, the system throws a clear error.

## Why ?? 

The main reason behind this application is to learn about hexangonal architecture. While studying about hexagonal architecture i learnt that it is very easy to test applications written using this design pattern. I am currently exploring about testing and would love to add some test here soon😀.

## Getting Started

**Clone the Repository**

```bash 
git clone https://github.com/Ayushsingla1/interneers-lab
```
**Create a Virtual Environment and activate it**
```bash 
cd backend/python
python -m venv venv
source venv/bin/activate
```

**Install the Dependencies**
```bash
pip install -r requirements.txt
```

**Run Server**
```bash
python manage.py runserver
```

# Further Reading
I also tried Writing a Article on hexagonal Architecture you can check it out here [medium article](https://medium.com/@ayushsingla1122/hexagonal-architecture-169730958ef5)