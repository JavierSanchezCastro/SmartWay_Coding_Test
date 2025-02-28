import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from datetime import datetime, timezone

#Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from db.session import SessionLocal
from db.models.Book import Book
from db.models.User import User
from db.models.Loan import Loan
from sqlalchemy import func, desc, and_, select, outerjoin

from sqlalchemy.orm import aliased

#Static images folder
IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/static/images"))
os.makedirs(IMAGE_PATH, exist_ok=True)

def get_statistics():
    db: Session = SessionLocal()
    
    #📊 Author with the most books in the catalog
    most_books_author = db.query(Book.author, func.count(Book.id).label("total"))\
                            .group_by(Book.author)\
                            .order_by(desc("total"))\
                            .first()
    print(f"Author with more books: {most_books_author}")
    
    #📚 Most loaned author
    most_borrowed_author = db.query(Book.author, func.count(Loan.id).label("total"))\
                                .join(Loan, Loan.book_id == Book.id)\
                                .group_by(Book.author)\
                                .order_by(desc("total"))\
                                .first()
    print(f"Most loaned author: {most_borrowed_author}")
    
    #📖 Most loaned author by user (compatible with MySQL)
    #Create a subquery to count the loans of each book by user
    loan_counts = db.query(
        User.name,
        Book.author,
        func.count(Loan.id).label("loan_count")
    ).join(Loan, Loan.user_id == User.id)\
    .join(Book, Loan.book_id == Book.id)\
    .group_by(User.name, Book.author)\
    .subquery()

    #Subquery to get a row number for each author by user, ordered by the number of loans
    row_number_subquery = db.query(
        loan_counts.c.name,
        loan_counts.c.author,
        func.row_number().over(
            partition_by=loan_counts.c.name, 
            order_by=loan_counts.c.loan_count.desc()
        ).label('row_num')
    ).subquery()

    #Now we only select the results with row_num = 1 (the most loaned author by user)
    user_top_author = db.query(
        row_number_subquery.c.name,
        row_number_subquery.c.author
    ).filter(
        row_number_subquery.c.row_num == 1
    ).all()

    #Print the results
    print("Most loaned author by user:")
    for user, author in user_top_author:
        print(f"  {user}: {author}")

    
    #📌 Most Borrowed Book
    most_borrowed_book = db.query(Book.title, func.count(Loan.id).label("total"))\
                              .join(Loan, Loan.book_id == Book.id)\
                              .group_by(Book.title)\
                              .order_by(desc("total"))\
                              .first()
    print(f"Most borrowed book: {most_borrowed_book}")
    
    
    # 🚨 User with more loans
    today = datetime.now(timezone.utc)
    most_active_user = db.query(User.name, func.count(Loan.id).label("active_loans"))\
                                 .join(Loan, Loan.user_id == User.id)\
                                 .filter(Loan.return_date > today)\
                                 .group_by(User.id)\
                                 .order_by(func.count(Loan.id).desc())\
                                 .first()
    if most_active_user:
        user_name, active_loans = most_active_user
        print(f"User with the most active loans: {user_name}")
        print(f"Number of active loans: {active_loans}")
    else:
        print("No active loans found.")
    db.close()

def generate_plots():
    db: Session = SessionLocal()
    
    #📈 Ratings Density
    ratings = [book.goodread_rating for book in db.query(Book).all()]
    plt.figure()
    plt.hist(ratings, bins=10, density=True, alpha=0.6, color='g')
    plt.title("Distribución de Goodreads Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Densidad")
    plt.savefig(os.path.join(IMAGE_PATH, "goodreads_density.png"))
    print("Plot 'goodreads_density.png' saved in static/images.")
    
    #📉 Relation between pages and time of the loan
    loans = db.query(Book.pages, func.datediff(Loan.return_date, Loan.loan_date))\
                  .join(Loan, Loan.book_id == Book.id)\
                  .filter(Loan.return_date != None)\
                  .all()
    pages, durations = zip(*loans)
    plt.figure()
    plt.scatter(pages, durations, alpha=0.5)
    plt.title("Páginas vs. Duración del Préstamo")
    plt.xlabel("Número de Páginas")
    plt.ylabel("Días Prestado")
    plt.savefig(os.path.join(IMAGE_PATH, "pages_vs_duration.png"))
    print("Plot 'pages_vs_duration.png' saved in static/images.")
    
    db.close()

if __name__ == "__main__":
    get_statistics()
    generate_plots()
