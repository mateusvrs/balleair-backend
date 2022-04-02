def airport_choices():
    airport_file = open('flights/static/assets/airports_icao.txt')
    airport_lines = airport_file.readlines()
    airport_choices = []

    for airport in airport_lines:
        array = airport.split('\t')
        choice = (array[1].strip(), array[3].strip())
        airport_choices.append(choice)

    airport_choices = sorted(airport_choices, key=lambda x: x[1])
    return airport_choices

def aircraft_choices():
    aircraft_file = open('flights/static/assets/aircrafts_icao.txt')
    aircraft_lines = aircraft_file.readlines()
    aircraft_choices = []

    for aircraft in aircraft_lines:
        array = aircraft.split('\t')
        choice = (array[0].strip(), array[0].strip())
        aircraft_choices.append(choice)
    
    return aircraft_choices
