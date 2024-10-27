### INF601 - Advanced Programming in Python
### Damian Rios
### Mini Project 3


# Mini Project 3 - BookNest


## Description
**BookNest** is a web application developed using Flask that allows users 
to manage their personal book library. Users can register an account where they will be able to
add, update, remove books, and track their reading status.

The app features a user-friendly interface built with Bootstrap, ensuring a responsive design across different devices.


## Getting Started
To set up the project locally, follow the instructions below.

### Prerequisites
- Python 3.x installed on your machine.
- A virtual environment (recommended) to manage dependencies.

### Dependencies
Make sure all required libraries are installed by running:
```
pip install -r requirements.txt
```

### Executing the Program
1. **Clone the repository:**
https://github.com/Damian-Rios/miniproject3DamianRios.git

2. **Create a virtual environment:**
python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate

3. **Install the dependencies:**

4. **Initialize the database:**
```
flask init-db
```

5. **Run the application:**
```
flask --app bookNest run
```

6. **Access the application:**
Click on link in terminal or open your web browser and navigate to
`http://127.0.0.1:5000` to use the BookNest application.

   
### Output
The application provides a clean interface to view and manage your book library. Users can:
- View dashboard with books added from different users
- Add books to the dashboard with details such as title, author, and status.
- Add books to personal library
- Update the reading status of each book.
- Remove books from the library through a confirmation modal.


## Authors
Damian Rios


## Acknowledgments
Inspiration, code snippets, etc.
* [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
* [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
* [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
* [ChatGPT - For assistance with coding and project ideas](https://chatgpt.com/share/671ea8a1-5b98-800f-a1b5-106f8e777e96)