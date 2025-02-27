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
    
    
    #🚨 User with more loans
    today = datetime.now(timezone.utc)
    most_loans_user = db.query(User.name, func.count(Loan.id).label("active_loans"))\
                          .join(Loan, Loan.user_id == User.id)\
                          .join(Book, Loan.book_id == Book.id)\
                          .filter(Loan.return_date > today, Book.status == "Borrowed")\
                          .group_by(User.name)\
                          .order_by(desc("active_loans"))\
                          .first()
    print(f"User with more loans actually: {most_loans_user}")

    

    #Alias to compare two loans from same user
    LoanAlias1 = aliased(Loan)
    LoanAlias2 = aliased(Loan)

    #Look for the historic loans for the user
    most_loans_user = db.query(
        User.name,
        func.count().label("simultaneous_loans")
    ).join(LoanAlias1, LoanAlias1.user_id == User.id)\
    .join(Book, LoanAlias1.book_id == Book.id)\
    .join(LoanAlias2, LoanAlias2.user_id == User.id)\
    .filter(
        LoanAlias1.book_id != LoanAlias2.book_id,
        and_(
            LoanAlias1.loan_date <= LoanAlias2.return_date,  #Loan A before Loan b
            LoanAlias1.return_date >= LoanAlias2.loan_date  #Loan A finished after Loan b starts
        )
    ).group_by(User.name)\
    .order_by(func.count().desc())\
    .first()

    print(f"User with more simultaneous loans in the historical: {most_loans_user}")
    
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
    loans = db.query(Book.pages, func.julianday(Loan.return_date) - func.julianday(Loan.loan_date))\
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
    #generate_plots()
