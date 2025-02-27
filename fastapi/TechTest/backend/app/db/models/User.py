from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from db.models.Base import Base
#from db.models.Info_Ranking import Info_Ranking
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
#from db.models.Loan import Loan

class User(Base):
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True)


    loans: Mapped[list["Loan"]] = relationship("Loan", back_populates="user")