import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
from create_database import Baza, Stacja, Wynajem


def load_data(file_csv, nazwa_bazy_danych):
    engine = create_engine(f'sqlite:///{nazwa_bazy_danych}.sqlite3')
    Baza.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    with open(file_csv, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for wiersz in reader:
            stacja_wynajmu = session.query(Stacja).filter_by(nazwa=wiersz['Stacja wynajmu']).first()
            if not stacja_wynajmu:
                stacja_wynajmu = Stacja(nazwa=wiersz['Stacja wynajmu'])
                session.add(stacja_wynajmu)
                session.commit()

            stacja_zwrotu = session.query(Stacja).filter_by(nazwa=wiersz['Stacja zwrotu']).first()
            if not stacja_zwrotu:
                stacja_zwrotu = Stacja(nazwa=wiersz['Stacja zwrotu'])
                session.add(stacja_zwrotu)
                session.commit()

            wynajem = Wynajem(
                numer_roweru=wiersz['Numer roweru'],
                data_wynajmu=datetime.strptime(wiersz['Data wynajmu'], '%Y-%m-%d %H:%M:%S'),
                data_zwrotu=datetime.strptime(wiersz['Data zwrotu'], '%Y-%m-%d %H:%M:%S'),
                czas_trwania=float(wiersz['Czas trwania']),
                stacja_wynajmu=stacja_wynajmu,
                stacja_zwrotu=stacja_zwrotu
            )
            session.add(wynajem)
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
