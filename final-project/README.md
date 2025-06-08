# Task Manager Web App
#### Video Demo: [https://youtu.be/KIJIDr3ZFAY]
#### Description:

My final project for CS50 is a **Task Manager Web Application**, a user-friendly platform where users can register for an account, log in securely, and manage their personal to-do list. This app empowers users to create, view, and delete tasks with deadlines, allowing them to stay organized and productive as they manage their daily responsibilities and work.

## Overview

This project is built using **Python** and the **Flask** web framework, with **SQLite** as the database engine. It implements secure user authentication, session management, and basic CRUD (Create, Read, Update, Delete) operations for tasks. The application’s design prioritizes simplicity and ease of use, enabling users to quickly register and begin managing their tasks effectively. The use of Flask’s templating system (Jinja2) allows for dynamic and interactive content rendering, ensuring a seamless user experience.

## Features

- **User Registration and Login**: Users can register by providing a unique username and a password, which is securely hashed before being stored in the database. After registration, users can log in using their credentials, and their session is managed securely using Flask-Session.

- **Task Management**: Authenticated users can add tasks with a title, description, and due date. Users can view their list of tasks on the homepage and delete tasks once they are completed or no longer relevant. This functionality ensures that users can manage their workload effectively and stay organized.

- **Responsive UI**: The app uses a combination of HTML, CSS, and the Bootstrap framework to create a clean and responsive user interface that adapts well to various screen sizes. This makes the app accessible and user-friendly on both desktop and mobile devices.

- **Data Persistence**: All data, including users and their tasks, is stored in an SQLite database (`tasks.db`). This ensures that data persists across user sessions, even if the server is restarted.

## Project Structure

- `app.py`: The main Flask application file that defines routes and handles the logic for user registration, login, logout, adding tasks, viewing tasks, and deleting tasks. It also manages session handling and error messages using Flask’s features.

- `requirements.txt`: A text file that lists the Python packages required to run the application, including Flask, Flask-Session, and Werkzeug.

- `templates/`: A folder containing HTML templates that define the structure and layout of the app’s web pages.
  - `layout.html`: The base layout containing the navbar and links that all other templates extend from.
  - `index.html`: The main dashboard that displays the list of tasks and provides a form for adding new tasks.
  - `login.html`: Contains the login form that allows existing users to authenticate.
  - `register.html`: Contains the registration form for new users to create an account.
  - `apology.html`: A simple template that displays error messages to the user in case of invalid inputs or other issues.

- `static/styles.css`: A custom CSS file that enhances the look and feel of the application with styles that complement Bootstrap’s default theme.

- `tasks.db`: The SQLite database that stores user information and tasks. It consists of two tables: `users` and `tasks`.

## Implementation Details

**User Authentication**: Passwords are hashed using Werkzeug’s security functions before being stored in the database, ensuring that user credentials remain secure. Flask-Session is used to maintain login status and manage sessions, preventing unauthorized access to user data.

**Task Management**: Each task is linked to a user through a foreign key relationship in the `tasks` table. This ensures that users only see their own tasks and cannot access tasks created by other users.

**Database Design**: I chose SQLite for its ease of use and seamless integration with Flask. It’s ideal for small projects like this one and doesn’t require a separate database server. The `users` table stores each user’s unique username and hashed password, while the `tasks` table contains details about each task, including its title, description, due date, and associated user ID.

## Design Choices

I chose to build this project using Flask because it aligns with the Python skills I developed throughout CS50 and allows for rapid prototyping. Jinja2 templates make it easy to render dynamic HTML pages, and Bootstrap enables me to create a polished and responsive interface with minimal effort. I also decided to prioritize core functionality—such as secure registration, login, and task management—over more advanced features due to time constraints. However, I made sure to design the code in a way that makes it easy to expand in the future.

## Future Enhancements

- **Task Editing**: Add the ability for users to edit existing tasks to accommodate changing deadlines and task details.
- **Task Categories/Tags**: Implement a system to categorize tasks or add tags, enabling users to better organize and filter their tasks.
- **Notifications**: Send email or SMS reminders to users for upcoming due dates, helping them stay on top of their to-do list.
- **Search and Filtering**: Provide search functionality and filtering options to allow users to easily find and manage tasks as their lists grow.

## Conclusion

This project reflects the skills and knowledge I’ve gained throughout CS50 and showcases my ability to build a full-stack web application from scratch. I’m proud of the functionality I implemented and the clean user interface I created. I look forward to building on this project in the future by adding more advanced features, and I hope this application helps users stay organized and productive. Thank you for taking the time to learn about my project!
