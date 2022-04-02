from .models import Flight

def create_new_flight_number(airline):
    last_airline_flight = Flight.objects.filter(airline=airline).last()

    if last_airline_flight:
        last_flight_number_array = last_airline_flight.flight_number.split('-')
        last_flight_number_array[1] = str(int(last_flight_number_array[1]) + 1).zfill(4)
        new_flight_number = '-'.join(last_flight_number_array)
    else:
        new_flight_number_array = [airline.acronym, ''.zfill(4)]
        new_flight_number = '-'.join(new_flight_number_array) 

    return new_flight_number
