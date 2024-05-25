from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import sys
from create_database import Base, Station, Rental


def query_interface(nazwa_bazy_danych):
    engine = create_engine(f'sqlite:///{nazwa_bazy_danych}.sqlite3')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    stations = session.query(Station).all()
    print("Dostępne stacji:")
    for station in stations:
        print(station.name)

    selected_station_name = input("Wprowadź stacje dla raportu: ")
    selected_station = session.query(Station).filter_by(name=selected_station_name).first()

    if selected_station:
        avg_duration_start = session.query(func.avg(Rental.duration)).filter_by(start_station=selected_station).scalar()
        avg_duration_end = session.query(func.avg(Rental.duration)).filter_by(end_station=selected_station).scalar()
        unique_bikes_count = session.query(func.count(func.distinct(Rental.bike_number))).filter_by(end_station=selected_station).scalar()

        print(f"średni czas trwania przejazdu rozpoczynanego na danej stacji {selected_station.name}: {avg_duration_start:.2f} minut")
        print(f"średni czas trwania przejazdu kończonego na danej stacji {selected_station.name}: {avg_duration_end:.2f} minut")
        print(f"liczbę różnych rowerów parkowanych na danej stacji {selected_station.name}: {unique_bikes_count}")

        # Liczba całkowita wynajmów ze stacji:
        total_rentals_start = session.query(func.count(Rental.id)).filter_by(start_station=selected_station).scalar()
        print(f"Liczba całkowita wynajmów ze stacji {selected_station.name}: {total_rentals_start}")

        # Most frequent route from the selected station
        most_frequent_route = session.query(
            Rental.end_station_id,
            func.count(Rental.id).label('route_count')
        ).filter(
            Rental.start_station == selected_station
        ).group_by(
            Rental.end_station_id
        ).order_by(
            func.count(Rental.id).desc()
        ).first()

        if most_frequent_route:
            most_frequent_end_station = session.query(Station).filter_by(id=most_frequent_route.end_station_id).first()
            print(
                f"Najczęśtszy wynajem z tej stacji {selected_station.name} jest do stacji {most_frequent_end_station.name} z {most_frequent_route.route_count} wynajmów.")
        else:
            print("Z tej stacji nie było wynajmów.")

    else:
        print("Takiej stacji nie ma")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Używaj: python query_interface.py <nazwa_bazy_danych>")
    else:
        query_interface(sys.argv[1])

#  TEST lab_10_3 interface: python query_interface.py database_rowery