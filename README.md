# SmartWay Coding Test

## Overview

This project is a library management system implemented in both **FastAPI** and **Flask**. It allows users to manage books, users, and loans, and provides statistics about the library's usage. The system is containerized using Docker and uses MySQL as the database.

The project is divided into two versions:
1. **FastAPI**: A modern, asynchronous web framework with built-in data validation and middleware for error handling.
2. **Flask**: A lightweight, synchronous web framework with a simpler structure.

Both versions share the same core functionality but differ in implementation details, such as middleware, data validation, and error handling.

---

## Features

### Core Features
- **Book Management**:
  - View all books.
  - Filter books by status (Available/Borrowed).
  - View details of a specific book by UUID.
- **User Management**:
  - View all users.
  - View details of a specific user by UUID or email.
  - View a user's loan history.
- **Loan Management**:
  - Track active and returned loans for each user.
  - Automatically mark books as "Borrowed" or "Available" based on loan dates.
- **Statistics**:
  - Generate and display library statistics, including:
    - Author with the most books.
    - Most borrowed author.
    - Most borrowed book.
    - User with the most active loans.
  - Visualize data with plots (e.g., Goodreads ratings distribution, pages vs. loan duration).

### Additional Features
- **Error Handling**:
  - Custom error pages for invalid routes or missing resources.
  - Middleware for request validation and error responses (FastAPI only).
- **Dynamic Data Generation**:
  - Scripts to generate books, users, and loans for testing.
- **Dockerized Environment**:
  - Easy setup with Docker Compose.
  - Includes MySQL database and Adminer for database management.

---

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Steps to Run the Project

#### 1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

#### 2. **Set Up Environment Variables**:
   - Ensure the `.env` files in both `fastapi` and `flask` directories are correctly configured with your MySQL credentials.

#### 3. **Choose a Backend (FastAPI or Flask)**:
   - The project is designed to run **either FastAPI or Flask at a time**, but not both simultaneously. This is to avoid port conflicts and ensure a clean development environment.

   - To switch between FastAPI and Flask, you will need to stop one backend before starting the other.

#### 4. **Start the Docker Containers**:
   - Navigate to the directory of the backend you want to run (`fastapi` or `flask`):
     ```bash
     cd fastapi/Techtest  # or cd flask/TechTest
     ```
   - Start the Docker containers:
     ```bash
     docker compose up -d
     ```

#### 5. **Generate Sample Data**:
   - Run the `generate_books.py` script to populate the database with books, users, and loans:
     ```bash
     docker compose run --rm backend generate_books
     ```

#### 6. **Generate Statistics and Plots**:
   - Run the `statistics.py` script to generate statistics and plots:
     ```bash
     docker compose run --rm backend statistics
     ```

#### 7. **Access the Application**:
   - Open your browser and navigate to:
     `http://localhost:8000`

#### 8. **Switching Between FastAPI and Flask**:
   - To switch to the other backend, first stop the currently running containers:
     ```bash
     docker compose down
     ```
   - Then navigate to the other backend's directory and start its containers:
     ```bash
     cd ../../flask/TechTest  # or cd ../../fastapi/TechTest
     docker compose up -d
     ```
   - Run the `generate_books.py` script to populate the database with books, users, and loans:
     ```bash
     docker compose run --rm backend generate_books
     ```
   - Run the `statistics.py` script to generate statistics and plots:
     ```bash
     docker compose run --rm backend statistics
     ```

    (Yes, each framework has its own mysql volume)
---

## Technical Highlights

### Database Models
- **Books**: Stores book details like title, author, publish date, status, and Goodreads rating.
- **Users**: Stores user details like name and email.
- **Loans**: Tracks loans with loan and return dates, linking users and books.

### Scripts
- **`generate_books.py`**:
  - Generates 100 books with random titles, authors, and ratings.
  - Creates 5 users with random loans.
  - Ensures loans do not overlap for the same book.
- **`statistics.py`**:
  - Calculates library statistics (e.g., most borrowed book, user with the most loans).
  - Generates plots for Goodreads ratings and loan duration vs. pages.

### Templates
- **Jinja2 Templates**: Used for rendering HTML pages in both FastAPI and Flask.
- **Dynamic Content**: Pages dynamically display data from the database (e.g., book lists, user details).

### Docker
- **Multi-container Setup**: Includes MySQL, Adminer, and the backend service.
- **Volume for Data Persistence**: Database data is persisted in a Docker volume.

---

## Interesting Observations

1. **Loan Duration Calculation**:
   - The loan duration is calculated based on the number of pages in the book, with some randomness added to simulate real-world behavior.

2. **Data Validation**:
   - FastAPI automatically validates request data using Pydantic, while Flask requires manual validation.

3. **Error Handling**:
   - FastAPI provides a more structured approach to error handling with middleware, whereas Flask relies on custom error handlers.

4. **Dynamic Data Generation**:
   - The `generate_books.py` script ensures that loans do not overlap, simulating a real-world library system.

5. **Visualizations**:
   - The `statistics.py` script generates plots using Matplotlib, providing insights into the library's usage patterns.

---

## Future Improvements

- **User Authentication**: Add login and registration functionality.
