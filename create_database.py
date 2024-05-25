from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sys

Baza = declarative_base()


class Stacja(Baza):
    __tablename__ = 'stacji'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String, unique=True, nullable=False)
    wynajem_z = relationship('Wynajem', back_populates='stacja_wynajmu', foreign_keys='Wynajem.stacja_wynajmu_id')
    wynajem_do = relationship('Wynajem', back_populates='stacja_zwrotu', foreign_keys='Wynajem.stacja_zwrotu_id')


class Wynajem(Baza):
    __tablename__ = 'wynajmy'
    id = Column(Integer, primary_key=True)
    numer_roweru = Column(String, nullable=False)
    data_wynajmu = Column(DateTime, nullable=False)
    data_zwrotu = Column(DateTime, nullable=False)
    czas_trwania = Column(Float, nullable=False)
    stacja_wynajmu_id = Column(Integer, ForeignKey('stacji.id'), nullable=False)
    stacja_zwrotu_id = Column(Integer, ForeignKey('stacji.id'), nullable=False)
    stacja_wynajmu = relationship('Stacja', foreign_keys=[stacja_wynajmu_id], back_populates='wynajem_z')
    stacja_zwrotu = relationship('Stacja', foreign_keys=[stacja_zwrotu_id], back_populates='wynajem_do')


def main(nazwa_bazy_danych):
    engine = create_engine(f'sqlite:///{nazwa_bazy_danych}.sqlite3')
    Baza.metadata.create_all(engine)
    print(f"Baza danych '{nazwa_bazy_danych}.sqlite3' została stworzona pomyślnie.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Używaj: python create_database.py <nazwa_bazy_danych>")
    else:
        main(sys.argv[1])

# TEST lab_10_1 creating database: python create_database.py database_rowery
