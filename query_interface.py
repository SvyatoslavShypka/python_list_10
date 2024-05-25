from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import sys
from create_database import Base, Station, Rental

def query_interface(database_name):
    engine = create_engine(f'sqlite:///{database_name}.sqlite3')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    stations = session.query(Station).all()
    print("Available stations:")
    for station in stations:
        print(station.name)

    selected_station_name = input("Enter the station name: ")
    selected_station = session.query(Station).filter_by(name=selected_station_name).first()

    if selected_station:
        avg_duration_start = session.query(func.avg(Rental.duration)).filter_by(start_station=selected_station).scalar()
        avg_duration_end = session.query(func.avg(Rental.duration)).filter_by(end_station=selected_station).scalar()
        unique_bikes_count = session.query(func.count(func.distinct(Rental.bike_number))).filter_by(end_station=selected_station).scalar()

        print(f"Average duration of rentals starting at {selected_station.name}: {avg_duration_start:.2f} minutes")
        print(f"Average duration of rentals ending at {selected_station.name}: {avg_duration_end:.2f} minutes")
        print(f"Number of unique bikes parked at {selected_station.name}: {unique_bikes_count}")

        # Custom query example:
        total_rentals_start = session.query(func.count(Rental.id)).filter_by(start_station=selected_station).scalar()
        print(f"Total number of rentals starting at {selected_station.name}: {total_rentals_start}")
    else:
        print("Station not found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python query_interface.py <database_name>")
    else:
        query_interface(sys.argv[1])

#  TEST lab_10_3 interface: python query_interface.py database_rowery