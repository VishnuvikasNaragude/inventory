## Inventory Management API

### Setup Instructions:
1. Clone the repository.
2. Set up a virtual environment and install the dependencies.
3. Set up PostgreSQL and Redis.
4. Run `python manage.py migrate` to apply migrations.
5. Use `python manage.py runserver` to start the server.

### API Endpoints:
- `POST /api/items/`: Create a new item.
- `GET /api/items/{item_id}/`: Retrieve item details.
- `PUT /api/items/{item_id}/`: Update item details.
- `DELETE /api/items/{item_id}/`: Delete an item.
