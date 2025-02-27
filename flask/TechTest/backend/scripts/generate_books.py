import sys
import os
import random
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

#from db.session import SessionLocal, engine
from db.models import Book, Loan, User
from db.session import db

#Base.metadata.create_all(bind=engine)

def generate_books():
    #db: Session = SessionLocal()
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
        db.add(book)

    db.commit()
    print("✅ 100 libros insertados en la base de datos.")

def generate_users_and_loans():
    #db: Session = SessionLocal()

    # Crear 5 usuarios
    users = []
    for i in range(1, 6):
        user = User(name=f"User {i}", email=f"user{i}@example.com")
        db.add(user)
        users.append(user)

    db.commit()

    for user in users:
        num_loans = random.randint(3, 10)

        # Obtener todos los libros
        books = db.query(Book).all()

        if not books:
            print("⚠ No hay libros en la base de datos.")
            break

        loaned_books = random.sample(books, min(num_loans, len(books)))

        for book in loaned_books:
            max_attempts = 10  # Intentos para encontrar una fecha válida sin solapamiento
            valid_loan = False

            for _ in range(max_attempts):
                loan_date = datetime.now() - timedelta(days=random.randint(1, 30))
                return_date = loan_date + timedelta(days=random.randint(5, 30))

                # Comprobar si el libro ya está prestado en este período
                overlapping_loan = db.query(Loan).filter(
                    Loan.book_id == book.id,
                    Loan.loan_date < return_date,  # Se solapa si el loan_date está dentro del período
                    Loan.return_date > loan_date
                ).first()

                if not overlapping_loan:
                    valid_loan = True
                    break  # Se encontró una fecha válida, salimos del bucle

            if not valid_loan:
                print(f"⚠ No se encontró una fecha válida para el libro {book.id}, omitiendo préstamo.")
                continue  # Saltamos este préstamo si no encontramos fechas válidas

            # Crear el préstamo
            loan = Loan(
                user_id=user.id,
                book_id=book.id,
                loan_date=loan_date,
                return_date=return_date
            )
            db.add(loan)

            # Si el préstamo sigue activo (aún no ha pasado la return_date), marcar libro como "Borrowed"
            if return_date > datetime.now():
                book.status = Book_Status.Borrowed
            else:
                book.status = Book_Status.Available

    db.commit()
    db.close()
    print("✅ 5 usuarios creados y préstamos generados sin solapamientos.")

from app import create_app
from app.db.session import db
from app.db.models import Base
def create_tables():
    with app.app_context():
        # Solo crea las tablas si no existen en la base de datos
        Base.metadata.create_all(bind=db.engine, checkfirst=True)  # checkfirst=True previene crear tablas existentes


from app import create_app
if __name__ == "__main__":
    app = create_app()
    create_tables()
    with app.app_context():
        generate_books()
        generate_users_and_loans()