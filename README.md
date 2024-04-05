# Policy Issuer App

[![Test CI](https://github.com/tbaiguzhinov/policy_issuer/actions/workflows/test_and_deploy.yml/badge.svg?branch=main)](https://github.com/tbaiguzhinov/policy_issuer/actions/workflows/test_and_deploy.yml)

This repository contains a Dockerized Django application built to fulfill the requirements of the API coding test. The application provides endpoints to create customers, generate insurance quotes, and manage policies.

Live API version of the app is deployed to an AWS EC2 server at [http://18.135.45.9/](http://18.135.45.9/). Access to API requires login to Django admin (username: _democrance_, password: _democrance_).

Tech Stack: Django, PostgreSQL (Sqlite for local dev), Docker, AWS EC2.

## Setup (Docker version)

To run this Django application locally using Docker, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/tbaiguzhinov/policy_issuer.git
   ```

2. Navigate into the project directory:

   ```bash
   cd policy_issuer
   ```

3. Build and run the Docker image:

   ```bash
   docker-compose up -d --build
   ```

4. Access the Django development server at [http://localhost:8000](http://localhost:8000)

## Setup (Simple version)

To run this Django application locally without Docker, follow these steps (steps 1 and 2 are the same):

3. Create a virtual environment and install dependencies:

   ```bash
   virtualenv venv
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

4. Create a database file using migrations and run server:

   ```bash
   python3 manage.py migrate
   python3 manage.py runserver 0.0.0.0:8000
   ```

5. Access the Django development server at [http://localhost:8000](http://localhost:8000)

## Create superuser

To be able to access the admin site, you need to create a superuser profile:

On a running Docker:

```bash
docker exec -it issuer python3 manage.py createsuperuser
```

Without Docker:

```bash
python3 manage.py createsuperuser
```

## Endpoints

### 1. Create Customer

- Endpoint: `http://localhost:8000/api/v1/create_customer/`
- Method: POST
- Description: Create a new customer in the database.

#### Request Example:

```json
{
  "first_name": "Ben",
  "last_name": "Stokes",
  "dob": "25-06-1991"
}
```

### 2. Create Insurance Quote

- Endpoint: `http://localhost:8000/api/v1/quote/`
- Method: POST
- Description: Create an insurance quote for the customer.

#### Request Example:

```json
{
  "type": "personal-accident",
  "premium": 200,
  "cover": 200000,
  "customer_id": 1
}
```

### 3. List Policies

- Endpoint: `http://localhost:8000/api/v1/policies/`
- Method: GET
- Description: Return a list of policies for a given customer.

### 4. Policy Details

- Endpoint: `http://localhost:8000/api/v1/policies/{id}`
- Method: GET
- Description: Return detailed information about a given policy.

### 5. Policy History

- Endpoint: `http://localhost:8000/api/v1/policies/{id}/history`
- Method: GET
- Description: Return detailed history of 'state' field change of a given policy.

### 6. Update Policy State

- Endpoint: `http://localhost:8000/api/v1/quote/`
- Method: PATCH
- Description: Update 'state' of a policy.

### Search Customers/Policies

Search functionality is implemented within the Django admin panel. Customers can be searched by first name, last name, date of birth, type of policies. Policies can be searched by customer name and types.

### Authentication Implementation

My suggestion is to keep authentication for users (insurance companies) via Django's built-in authentication system, logging in through django admin interface.
The authentication for customers (i.e. clients who wish to purchase an insurance) should be done with JWT or OAuth2. Both are easy to be integrated into Django app and provide reliable and secure way to manage authentication.

### Additional functionality

1. **PEP8 compliance**: all code is tested against PEP8 requirements.
2. **Security**: code is checked by bandit framework for any potential security vulnerabilities.
3. **CI/CD**: a pipeline consisting of build and test created and successfully implemented with Github Actions.
4. **API documentation**: a swagger with examples and details is accessible at /api/v1/swagger and /api/v1/redoc.
5. **Docker**: the app is dockerized, with creation of 2 containers: a PostgreSQL database and main Django container.
6. **Dev deployment**: the code is successfully deployed for demonstration on AWS EC2 machine.
7. **Testing**: tests created with 100% coverage.

### Additional Notes

Ensure Docker and Docker Compose are installed on your machine before running the application.  
For any questions or clarifications, feel free to reach out.  
Thank you for considering my submission!
