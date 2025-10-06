# FastAPI MongoDB Project

A simple FastAPI application with MongoDB integration featuring CRUD operations for managing items.

## Features

- ✅ FastAPI framework with async support
- ✅ MongoDB integration using Motor (async MongoDB driver)
- ✅ Environment variable configuration
- ✅ Pydantic models for data validation
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Automatic API documentation with Swagger UI
- ✅ Error handling and HTTP status codes

## Project Structure

```
fastapi-mongo-project/
├── main.py              # FastAPI application and routes
├── models.py            # Pydantic models for data validation
├── database.py          # MongoDB connection configuration
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create from .env.example)
└── README.md           # This file
```

## Prerequisites

- Python 3.8+
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package installer)

## Installation

1. **Clone or navigate to the project directory:**

   ```bash
   cd fastapi-mongo-project
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   - Update the `.env` file with your MongoDB connection details:

   ```env
   MONGODB_URI=mongodb://localhost:27017
   DATABASE_NAME=fastapi_demo
   PORT=8000
   HOST=0.0.0.0
   ENVIRONMENT=development
   ```

   **For MongoDB Atlas (cloud):**

   ```env
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=fastapi_demo
   ```

5. **Ensure MongoDB is running:**
   - **Local MongoDB:** Start MongoDB service on your system
   - **MongoDB Atlas:** Make sure your cluster is running and accessible

## Running the Application

1. **Start the FastAPI server:**

   ```bash
   python main.py
   ```

   Or use uvicorn directly:

   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Access the application:**
   - **API Base URL:** http://127.0.0.1:8000
   - **Interactive API Docs (Swagger):** http://127.0.0.1:8000/docs
   - **Alternative API Docs (ReDoc):** http://127.0.0.1:8000/redoc

## API Endpoints

### Health Check

- **GET /** - Health check endpoint

### Items Management

- **GET /items** - Get all items
- **GET /items/{item_id}** - Get a specific item by ID
- **POST /items** - Create a new item
- **PUT /items/{item_id}** - Update an existing item
- **DELETE /items/{item_id}** - Delete an item

## Example API Usage

### Create a new item (POST /items)

```json
{
  "name": "Laptop",
  "description": "High-performance gaming laptop",
  "price": 1299.99,
  "category": "Electronics"
}
```

### Response:

```json
{
  "id": "64f8a123b456c789d012e345",
  "name": "Laptop",
  "description": "High-performance gaming laptop",
  "price": 1299.99,
  "category": "Electronics",
  "created_at": "2024-01-15T10:30:00.000Z"
}
```

### Get all items (GET /items)

Returns an array of all items in the database.

### Get item by ID (GET /items/{item_id})

Replace `{item_id}` with the actual MongoDB ObjectId.

## Testing the API

You can test the API using:

1. **FastAPI Interactive Docs:** Visit http://127.0.0.1:8000/docs
2. **curl commands:**

   ```bash
   # Health check
   curl http://127.0.0.1:8000/

   # Get all items
   curl http://127.0.0.1:8000/items

   # Create a new item
   curl -X POST "http://127.0.0.1:8000/items" \
        -H "Content-Type: application/json" \
        -d '{"name": "Test Item", "description": "A test item", "price": 29.99}'
   ```

3. **Python requests:**

   ```python
   import requests

   # Create an item
   response = requests.post("http://127.0.0.1:8000/items", json={
       "name": "Test Item",
       "description": "A test item",
       "price": 29.99,
       "category": "Test"
   })
   print(response.json())
   ```

## MongoDB Collections

The application creates a collection called `items` in your specified database. Each item document has the following structure:

```json
{
  "_id": "ObjectId",
  "name": "string",
  "description": "string (optional)",
  "price": "number (optional)",
  "category": "string (optional)",
  "created_at": "datetime"
}
```

## Development

### Adding New Features

1. **Models:** Add new Pydantic models in `models.py`
2. **Routes:** Add new endpoints in `main.py`
3. **Database:** Modify database operations in `database.py` if needed

### Common Issues

1. **MongoDB Connection Error:**

   - Ensure MongoDB is running
   - Check your `MONGODB_URI` in `.env`
   - Verify network connectivity for MongoDB Atlas

2. **Import Errors:**

   - Make sure virtual environment is activated
   - Install dependencies: `pip install -r requirements.txt`

3. **Port Already in Use:**
   - Change the `PORT` in `.env` file
   - Or kill the process using the port

## Dependencies

- **FastAPI:** Modern, fast web framework for building APIs
- **Motor:** Async MongoDB driver for Python
- **Pydantic:** Data validation using Python type annotations
- **python-dotenv:** Load environment variables from .env file
- **uvicorn:** ASGI server for running FastAPI

## Next Steps

- Add authentication and authorization
- Implement pagination for large datasets
- Add data relationships between collections
- Set up logging and monitoring
- Add unit and integration tests
- Containerize with Docker

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is open source and available under the [MIT License](LICENSE).
