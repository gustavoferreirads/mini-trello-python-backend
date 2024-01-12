# Backend for Trello Clone Project

This is the backend component of a Trello clone project, a task management application similar to Trello. 

It is built using Flask in conjunction with Graphene for GraphQL support, Flask, and DynamoDB for scalable and flexible data storage. Docker is used to encapsulate the environment and run a local instance of DynamoDB.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python that's easy to get started with but powerful enough for production use.
- **Graphene**: A Python library for building GraphQL APIs, making it simple to define the data schema and resolve queries.
- **DynamoDB**: A NoSQL database offered by Amazon Web Services that provides quick and predictable performance with seamless scalability.
- **Docker**: A platform for developing, shipping, and running applications in isolated containers, allowing for easy deployment and scaling.

### Advantages for a Task Manager Application

- **Scalability**: DynamoDB's scalability ensures that as the number of tasks and users grows, the database can handle the increased load without significant changes to the backend.
- **Performance**: FastAPI and Flask provide a robust and efficient backend, capable of handling numerous requests simultaneously which is crucial for real-time task management.
- **Real-time updates**: Graphene with subscriptions can provide real-time updates to the frontend, allowing users to see changes immediately, which is essential for collaborative task management.
- **Interactivity**: Docker enables consistent development environments and easy deployment, making it simpler to manage application delivery and environment configurations.

## Project Structure


## Project Structure

- `db`: Contains modules to configure and interact with DynamoDB.
  - `migration`: Scripts for database migrations.
  - `dynamodb_config.py`: Configuration settings for DynamoDB.
  - `dynamodb_utils.py`: Utility functions for DynamoDB operations.
  - `init_dynamodb.py`: Script to initialize the DynamoDB tables.
- `inputs`: GraphQL input types for API operations.
  - `board_input.py`: Input types related to board operations.
  - `card_input.py`: Input types related to card operations.
  - `column_input.py`: Input types related to column operations.
- `model`: Python classes that represent the data models.
  - `board.py`: Data model for boards.
  - `card.py`: Data model for cards.
  - `column.py`: Data model for columns.
- `resolvers`: GraphQL resolvers for handling queries and mutations.
  - `board_resolver.py`: Resolvers for board-related operations.
  - `card_resolver.py`: Resolvers for card-related operations.
  - `column_resolver.py`: Resolvers for column-related operations.
  - `schema.py`: The GraphQL schema definition.
- `service`: Business logic layer for handling application operations.
  - `board_service.py`: Services for board operations.
  - `card_service.py`: Services for card operations.
  - `column_service.py`: Services for column operations.
- `venv`: Virtual environment for Python packages.
- `docker-compose.yml`: Docker Compose configuration for local DynamoDB.
- `Dockerfile`: Dockerfile for creating the application container.
- `main.py`: Entry point for the Flask application.
- `requirements.txt`: List of Python package dependencies.

## Setup

1. Ensure you have Docker and Python installed on your system.

2. Install Python dependencies within a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # For Unix-like systems
   .\venv\Scripts\activate  # For Windows
   pip install -r requirements.txt
   

### Running the Services

1. **Start the Services:**
   To start the DynamoDB Local navigate to the root directory of the project and run:

   ```sh
   docker-compose up --build
   
  
### Database Initialization and Migrations

The `init_dynamodb.py` script within the `db` directory is designed to set up the necessary tables in the DynamoDB database. This script acts as a migration manager, ensuring that your database schema is initialized correctly and can also be used to apply incremental changes or rollbacks to the database schema.

To create the tables in your DynamoDB instance, run the following command:


## Contributing

Please read the contributing guidelines (CONTRIBUTING.md) to understand the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
