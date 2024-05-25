from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sys

Base = declarative_base()


class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    rentals_start = relationship('Rental', back_populates='start_station', foreign_keys='Rental.start_station_id')
    rentals_end = relationship('Rental', back_populates='end_station', foreign_keys='Rental.end_station_id')


class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True)
    bike_number = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=False)
    start_station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    end_station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)
    start_station = relationship('Station', foreign_keys=[start_station_id], back_populates='rentals_start')
    end_station = relationship('Station', foreign_keys=[end_station_id], back_populates='rentals_end')


def main(nazwa_bazy_danych):
    engine = create_engine(f'sqlite:///{nazwa_bazy_danych}.sqlite3')
    Base.metadata.create_all(engine)
    print(f"Baza danych '{nazwa_bazy_danych}.sqlite3' została stworzona pomyślnie.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Używaj: python create_database.py <nazwa_bazy_danych>")
    else:
        main(sys.argv[1])

# TEST lab_10_1 creating database: python create_database.py database_rowery
