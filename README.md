<header>
    <h1 align="center">BalleAir Backend</h1>
</header>
<br>
<main>
    <div>
        <h2>💻 Technologies</h2>
        <ul>
            <li><a target="_blank" rel="noreferrer" href="https://www.djangoproject.com/">Django</a></li>
            <li><a target="_blank" rel="noreferrer" href="https://www.django-rest-framework.org/">Django Rest
                    Framework</a></li>
            <li><a target="_blank" rel="noreferrer"
                    href="https://django-rest-framework-simplejwt.readthedocs.io/en/latest/">Django SimpleJWT</a></li>
        </ul>
    </div>
    <br>
    <div>
        <h2>✏️ Project</h2>
        <p>BalleAir was a challenge proposed by the Ballerini Community. The project consisted of creating an API in
            which it was possible to list, book and cancel airline flights.</p>
    </div>
    <br>
    <div>
        <h2>✨ Extra</h2>
        <p>To improve the proposed challenge, I added a user registration with two types of users that are travelers and
            airline. Travelers can book and cancel flights. The airline can create and delete flights. One important
            thing is that anyone can create a traveler account, but only I with the superuser account can create airline
            accounts.</p>
        <h3>Airline accounts to test:</h3>
        <p>
            username = Latam <br>
            password = balleair-latam
            <br> <br>
            username = Azul <br>
            password = balleair-azul
            <br> <br>
            username = Gol <br>
            password = balleair-gol
        </p>
    </div>
    <br>
    <div>
        <h2>📝 Documentation</h2>
        <h3>Users</h3>
        <p>All users API functions are preceded by /users/ on the root url</p>
        <ul>
            <li>POST: register/traveler/</li>
            <p>Return all informations of the new travler.</p>
            body:
            <pre>
                {
                    owner: {
                        "username": string,
                        "email": string,
                        "password": string
                    }
                }
            </pre>
            <li>POST: token/</li>
            <p>Return access and refresh tokens of the user.</p>
            body:
            <pre>
                {
                    "username": string,
                    "password": string
                }
            </pre>
            <li>GET: info/</li>
            <p>Return all informations of the user.</p>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {accesstoken}'
                }
            </pre>
        </ul>
        <h3>Flights</h3>
        <p>All flights API functions are preceded by /flights/ on the root url</p>
        <ul>
            <li>POST: create/</li>
            <p>Return all informations of the new flight.</p>
            body:
            <pre>
                {
                    "pax": {
                        "available": number
                    },
                    "departure_airport": string,
                    "arrival_airport": string,
                    "flight_date": string (datetime -> 2022-06-07T10:30),
                    "aircraft": string
                }
            </pre>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {airline_accesstoken}'
                }
            </pre>
            <li>GET: list/</li>
            <p>Return all flights from the authenticated airline.</p>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {airline_accesstoken}'
                }
            </pre>
            <li>GET, PUT, PATCH, DELETE: detail/{flight_number}/</li>
            <p>Return specific flight from the authenticated airline and give you the access to handle this flight.</p>
            body:
            <pre>
                {
                    "pax": {
                        "available": number
                    },
                    "departure_airport": string,
                    "arrival_airport": string,
                    "flight_date": string (datetime -> 2022-06-07T10:30),
                    "aircraft": string
                }
            </pre>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {airline_accesstoken}'
                }
            </pre>
            <li>GET: retrieve/?</li>
            <p>Return specific flight from the authenticated airline based on some query parameters.</p>
            possible query parameters:
            <pre>
                airline = number -> airline_id,
                departure_airport = string,
                arrival_airport = string,
                flight_date = string (datetime -> 2022-06-07T10:30),
            </pre>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {airline_flight_owner_accesstoken}'
                }
            </pre>
            <li>GET: book/{flight_number}/</li>
            <p>Book a flight.</p>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {traveler_accesstoken}'
                }
            </pre>
            <li>GET: cancel/{flight_number}/</li>
            <p>Cancel a flight booked before.</p>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {traveler_accesstoken}'
                }
            </pre>
            <li>GET: airports/</li>
            <p>Return all airports available.</p>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {accesstoken}'
                }
            </pre>
            <li>GET: aircrafts/</li>
            <p>Return all aircrafts available.</p>
            headers:
            <pre>
                {
                    'Authorization': 'Bearer {accesstoken}'
                }
            </pre>
        </ul>
    </div>
    <br>
    <br>
    <div align="right">
        <hr>
        <p>Proposed by the <a target="_blank" rel="noreferrer" href="http://discord.gg/ballerini">Ballerini
                Community</a></p>
        <p>Developed by <a target="_blank" rel="noreferrer" href="https://www.linkedin.com/in/mateusvrs/">Mateus
                Vieira</a> 💛</p>
    </div>
</main>