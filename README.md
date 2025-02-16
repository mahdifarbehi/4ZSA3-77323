
# Restaurant Booking System

This project implements a booking system for a restaurant using FastAPI, PostgreSQL, and Docker Compose. The system allows customers to book tables based on their party size, following the business rules outlined below. Users must be authenticated to make a reservation or cancel a reservation.

## Business Specification

1. The restaurant has a total of `N = 10` tables.
2. Each table has `M` seats, where `4 <= M <= 10`.
3. Customers can book tables based on the number of individuals, and the system will offer the cheapest available option.
4. Odd-numbered bookings are not allowed unless it exactly matches the table's seat count. For example, if a customer wants to book for 3 people, the system will assign them 4 seats and calculate the cost based on those 4 seats.
5. Each seat costs `X` amount. Booking an entire table costs `(M - 1) * X`.
6. Users must be authenticated to book or cancel a reservation.

## API Endpoints

### 1. `POST /book`
- **Description**: Allows authenticated users to book a table.
- **Request body**:
  ```json
  {
    "people_count": 5
  }
  ```
- **Response**:
  ```json
  {
  "id": 1,
  "table": "table1",
  "seat_count": 5,
  "total_price": 200,
  "created_by": "user"
  }
  ```

### 2. `DELETE /cancel/{reservation_id}`
- **Description**: Allows authenticated users to cancel a reservation.
- **Request body**: None.
- **Response**:
  ```json
  {
    "message": "Reservation canceled successfully"
  }
  ```

## Technical Specifications

1. **Web Framework**: FastAPI
2. **Database**: PostgreSQL
3. **ORM**: SQLAlchemy
4. **Authentication**: JWT-based user authentication
5. **Testing**: Unit tests written with `pytest`
6. **OpenAPI Specification**: Automatically generated from FastAPI
7. **Deployment**: Docker Compose for containerized deployment

## Setup and Installation

### Prerequisites

Before running the project, ensure that you have the following installed:

- Docker and Docker Compose
- Python 3.8+ (optional, Docker container will handle the environment)
- PostgreSQL (handled by Docker Compose)

### Steps to Set Up

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mahdifarbehi/4ZSA3-77323.git restaurant-booking
   cd restaurant-booking
   ```

2. **Build and start the containers** using Docker Compose:
   ```bash
   make all
   ```

3. **Run the tests**:
   If you want to run the tests in your Docker environment, use the following command:
   ```bash
   make test
   ```

4. **Access the API**:
   Once the containers are up and running, you can access the API on `http://localhost:8000`.

5. **OpenAPI Documentation**:
   FastAPI provides automatic documentation of the API. You can view it at:
   - [Swagger UI](http://localhost:8000/docs)

### Environment Variables

You can set the following environment variables in docker-compose file to customize the system:

- `DATABASE_URL`: URL for connecting to the PostgreSQL database (default is `postgresql://username:password@db:5432/mydb`).
- `SEAT_PRICE`: Price per seat (default is `50`).
- `TABLE_COUNT`: Total number of tables (default is `10`).
- `SEAT_COUNT`: Number of seats per table (default is `5`).

### Stopping and Removing Containers

To stop and remove the containers, you can run:

```bash
make down
```

## Contributing

Feel free to fork this project, submit issues, and send pull requests. If you have any suggestions for improvements, feel free to create an issue.
