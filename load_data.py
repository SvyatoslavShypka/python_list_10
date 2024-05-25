import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
from create_database import Base, Station, Rental


def load_data(csv_file, nazwa_bazy_danych):
    engine = create_engine(f'sqlite:///{nazwa_bazy_danych}.sqlite3')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_station = session.query(Station).filter_by(name=row['Stacja wynajmu']).first()
            if not start_station:
                start_station = Station(name=row['Stacja wynajmu'])
                session.add(start_station)
                session.commit()

            end_station = session.query(Station).filter_by(name=row['Stacja zwrotu']).first()
            if not end_station:
                end_station = Station(name=row['Stacja zwrotu'])
                session.add(end_station)
                session.commit()

            rental = Rental(
                bike_number=row['Numer roweru'],
                start_time=datetime.strptime(row['Data wynajmu'], '%Y-%m-%d %H:%M:%S'),
                end_time=datetime.strptime(row['Data zwrotu'], '%Y-%m-%d %H:%M:%S'),
                duration=float(row['Czas trwania']),
                start_station=start_station,
                end_station=end_station
            )
            session.add(rental)
        session.commit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Używaj: python load_data.py <file_csv> <nazwa_bazy_danych>")
    else:
        load_data(sys.argv[1], sys.argv[2])

# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-01.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-02.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-03.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-04.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-05.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-06.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-07.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-08.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-09.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-10.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-11.csv database_rowery
# TEST lab_10_2 load data: python load_data.py historia_przejazdow_2021-12.csv database_rowery
