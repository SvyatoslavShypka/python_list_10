from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import sys
from create_database import Baza, Stacja, Wynajem


def interfejs(nazwa_bazy_danych):
    engine = create_engine(f'sqlite:///{nazwa_bazy_danych}.sqlite3')
    Baza.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    stacji = session.query(Stacja).all()
    print("Dostępne stacji:")
    for station in stacji:
        print(station.nazwa)

    nazwa_wybranej_stacji = input("Wprowadź stacje dla raportu: ")
    wybrana_stacja = session.query(Stacja).filter_by(nazwa=nazwa_wybranej_stacji).first()

    if wybrana_stacja:
        sredni_czas_z = session.query(func.avg(Wynajem.czas_trwania))\
            .filter_by(stacja_wynajmu=wybrana_stacja).scalar()
        sredni_czas_do = session.query(func.avg(Wynajem.czas_trwania))\
            .filter_by(stacja_zwrotu=wybrana_stacja).scalar()
        liczba_roznych_rowerow = session.query(func.count(func.distinct(Wynajem.numer_roweru)))\
            .filter_by(stacja_zwrotu=wybrana_stacja).scalar()

        print(f"średni czas trwania przejazdu rozpoczynanego z danej stacji {wybrana_stacja.nazwa}"
              f": {sredni_czas_z:.2f} minut")
        print(f"średni czas trwania przejazdu kończonego na danej stacji {wybrana_stacja.nazwa}"
              f": {sredni_czas_do:.2f} minut")
        print(f"liczbę różnych rowerów parkowanych na danej stacji {wybrana_stacja.nazwa}: {liczba_roznych_rowerow}")

        # Liczba całkowita wynajmów ze stacji:
        liczba_calkowita_z = session.query(func.count(Wynajem.id)).filter_by(stacja_wynajmu=wybrana_stacja).scalar()
        print(f"Liczba całkowita wynajmów ze stacji {wybrana_stacja.nazwa}: {liczba_calkowita_z}")

        # Napopularniejszy kierunek z tej stacji
        napopularniejszy_kierunek = session.query(
            Wynajem.stacja_zwrotu_id,
            func.count(Wynajem.id).label('ilosc_kierunkow')
        ).filter(
            Wynajem.stacja_wynajmu == wybrana_stacja
        ).group_by(
            Wynajem.stacja_zwrotu_id
        ).order_by(
            func.count(Wynajem.id).desc()
        ).first()

        if napopularniejszy_kierunek:
            napopularniejszy_kierunek_do = session.query(Stacja).filter_by(id=napopularniejszy_kierunek.stacja_zwrotu_id).first()
            print(
                f"Napopularniejszy kierunek z tej stacji {wybrana_stacja.nazwa} jest do stacji "
                f"{napopularniejszy_kierunek_do.nazwa}. Wynajmów było: {napopularniejszy_kierunek.ilosc_kierunkow}")
        else:
            print("Z tej stacji nie było wynajmów.")

    else:
        print("Takiej stacji nie ma")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Używaj: python query_interface.py <nazwa_bazy_danych>")
    else:
        interfejs(sys.argv[1])

#  TEST lab_10_3 interfejs: python query_interface.py database_rowery