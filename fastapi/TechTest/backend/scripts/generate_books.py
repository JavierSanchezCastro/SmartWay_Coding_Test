import sys
import os
import random
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

#Add the backend directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from db.session import SessionLocal, engine
from db.models.Book import Book, Book_Status
from db.models.User import User
from db.models.Loan import Loan
from db.models.Base import Base

#Create the database if it doesn't exist
Base.metadata.create_all(bind=engine)

def generate_books():
    db: Session = SessionLocal()
    mean_rating = 3.5
    std_dev_rating = 1.0

    for i in range(100):
        rating = max(0, min(5, np.random.normal(mean_rating, std_dev_rating)))
        book = Book(
            title=f"Book {i+1}",
            author=f"Author {random.randint(1, 10)}",
            publish_date=datetime(random.randint(1900, 2023), 1, 1),
            status=Book_Status.Available,  #All books init as "Available"
            pages=random.randint(80, 1000),
            goodread_rating=round(rating, 2)
        )
        db.add(book)

    db.commit()
    print("✅ 100 books inserted into the database.")

def generate_users_and_loans():
    db: Session = SessionLocal()

    DAYS_PER_PAGE = 0.05  # Duración base por página (en días)
    STD_DEV_PERCENTAGE = 0.2  # 20% de la duración media como desviación estándar

    #Create 5 users
    users = []
    for i in range(1, 6):
        user = User(name=f"User {i}", email=f"user{i}@example.com")
        db.add(user)
        users.append(user)

    db.commit()

    for user in users:
        num_loans = random.randint(3, 10)

        #Get all books
        books = db.query(Book).all()

        if not books:
            print("⚠ No books in the database.")
            break

        loaned_books = random.sample(books, min(num_loans, len(books)))

        for book in loaned_books:
            max_attempts = 10  #Attempts to find a valid date without overlap
            valid_loan = False

            mean_loan_days = DAYS_PER_PAGE * book.pages
            std_dev_loan_days = mean_loan_days * STD_DEV_PERCENTAGE

            for _ in range(max_attempts):
                loan_duration = max(1, int(np.random.normal(mean_loan_days, std_dev_loan_days)))
                loan_date = datetime.now() - timedelta(days=random.randint(1, 30))
                return_date = loan_date + timedelta(days=loan_duration)

                #Check if the book is already loaned during this period
                overlapping_loan = db.query(Loan).filter(
                    Loan.book_id == book.id,
                    Loan.loan_date < return_date, #It overlaps if the loan_date is within the period
                    Loan.return_date > loan_date
                ).first()

                if not overlapping_loan:
                    valid_loan = True
                    break  #A valid date was found, exiting the loop

            if not valid_loan:
                print(f"⚠ No valid date found for book {book.id}, skipping loan.")
                continue  #Skip this loan if no valid dates are found

            #Create the loan
            loan = Loan(
                user_id=user.id,
                book_id=book.id,
                loan_date=loan_date,
                return_date=return_date
            )
            db.add(loan)

            #If the loan is still active (return_date has not passed), mark the book as "Borrowed"
            if return_date > datetime.now():
                book.status = Book_Status.Borrowed
            else:
                book.status = Book_Status.Available

    db.commit()
    db.close()
    print("✅ 5 users created and loans generated without overlaps.")


if __name__ == "__main__":
    print("FastAPI script")
    generate_books()
    generate_users_and_loans()
