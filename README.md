This project uses Python and SQLAlchemy with SQLite to create and manage a simple shop database.

## The database contains three tables:

-User
-Product
-Order

## Relationships:

-A User can have many Orders.
-A Product can appear in many Orders.
-Each Order belongs to one User and one Product.

This project uses SQLite and creates a database file named:

-shop.db

## The program will:

-Create the database tables.
-Insert sample users, products, and orders.
-Display users and products.
-Display orders with customer names, product names, and quantities.
-Update a product price.
-Delete a user by ID.
-Display unshipped orders.
-Count the number of orders per user.