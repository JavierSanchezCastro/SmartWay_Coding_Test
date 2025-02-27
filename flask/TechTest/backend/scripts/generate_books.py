import sys
import os
import random
import numpy as np
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.db.models.Book import Book, Book_Status
from app.db.models.User import User
from app.db.models.Loan import Loan
from app import create_app
from app.db.session import db

def generate_books():
    mean_rating = 3.5
    std_dev_rating = 1.0

    for i in range(100):
        rating = max(0, min(5, np.random.normal(mean_rating, std_dev_rating)))
        book = Book(
            title=f"Book {i+1}",
            author=f"Author {random.randint(1, 10)}",
            publish_date=datetime(random.randint(1900, 2023), 1, 1),
            status=Book_Status.Available,
            pages=random.randint(80, 1000),
            goodread_rating=round(rating, 2)
        )
        db.session.add(book)

    db.session.commit()
    print("✅ 100 books inserted into the database.")

def generate_users_and_loans():
    # Create 5 users
    users = []
    for i in range(1, 6):
        user = User(name=f"User {i}", email=f"user{i}@example.com")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    for user in users:
        num_loans = random.randint(3, 10)

        # Get all books
        books = Book.query.all()

        if not books:
            print("⚠ No books in the database.")
            break

        loaned_books = random.sample(books, min(num_loans, len(books)))

        for book in loaned_books:
            max_attempts = 10
            valid_loan = False

            for _ in range(max_attempts):
                loan_date = datetime.now() - timedelta(days=random.randint(1, 30))
                return_date = loan_date + timedelta(days=random.randint(5, 30))

                # Check if book is already loaned in this period
                overlapping_loan = Loan.query.filter(
                    Loan.book_id == book.id,
                    Loan.loan_date < return_date,
                    Loan.return_date > loan_date
                ).first()

                if not overlapping_loan:
                    valid_loan = True
                    break

            if not valid_loan:
                print(f"⚠ No valid date found for book {book.id}, skipping loan.")
                continue

            # Create the loan
            loan = Loan(
                user_id=user.id,
                book_id=book.id,
                loan_date=loan_date,
                return_date=return_date
            )
            db.session.add(loan)

            # If loan is still active, mark book as "Borrowed"
            if return_date > datetime.now():
                book.status = Book_Status.Borrowed
            else:
                book.status = Book_Status.Available

    db.session.commit()
    print("✅ 5 users created and loans generated without overlaps.")

if __name__ == "__main__":
    print("Flask script")
    app = create_app()
    with app.app_context():
        db.create_all()
        generate_books()
        generate_users_and_loans()