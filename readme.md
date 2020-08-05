# Mini-project - Database as a service (DBaaS)

This mini-project consists in a simple API that communicates with a database to store user credentials and sentence.

**Software stack:**
- Flask
- MongoDB
- Docker.


**The API handles the following actions:**
- Register a new user (5 initial credits)
- Store a sentence in the database (cost: 1 credit)
- Retrieve a sentence in the database (cost: 1 credit)
- Save password hash in the database
- If a user runs out of credits, he will not be able to store or retrieve data anymore.


**Running the app:**
- ```docker-compose build```
- ```docker-compose up```
- Use Postman to send API post requests with the following body components:
  - **User registration (localhost:5000/register):** ```{'username': name, 'password': pwd}```
  - **Sentence storing (localhost:5000/store):** ```{'username': name, 'password': pwd, 'sentence': msg}```
  - **Sentence retrieving (localhost:5000/get):** ```{'username': name, 'password': pwd}```