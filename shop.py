#Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, select, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship, mapped_column, Mapped
from typing import List

#Create an engine and base
engine = create_engine('sqlite:///shop.db')
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

#Create a User table
class User(Base):
    __tablename__= "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    
    #One-to-Many: User -> List of Order objects
    orders: Mapped[List["Order"]] = relationship(back_populates="customer", cascade="all, delete-orphan")

#Create a Product table    
class Product(Base):
    __tablename__= "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    
    #One-to-Many: Product -> List of Order objects
    orders: Mapped[List["Order"]] = relationship(back_populates="product")

#Create an Order table    
class Order(Base):
    __tablename__= "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    
    #Many-to-One: Order -> User
    customer: Mapped["User"] = relationship(back_populates="orders")
    #Many-to-One: Order -> Product
    product: Mapped["Product"] = relationship(back_populates="orders")

#Create tables in the SQLite database
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

#Creating new objects
session = Session()

customer1 = User(name="Alice", email="alice1@email.com")
customer2 = User(name="Alex", email="alex2@email.com")

product1 = Product(name="Vitamin C", price=20)
product2 = Product(name="Vitamin D", price=25)
product3 = Product(name="Magnesium", price=28)

order1 = Order(
    customer=customer1,
    product=product2,
    quantity=2,
    status=False
)

order2 = Order(
    customer=customer2,
    product=product2,
    quantity=1,
    status=True
)

order3 = Order(
    customer=customer1,
    product=product3,
    quantity=1,
    status=True
)

order4 = Order(
    customer=customer2,
    product=product1,
    quantity=6,
    status=True
)

#Adding all new objects to the session
session.add_all([
    customer1,
    customer2,
    product1,
    product2,
    product3,
    order1,
    order2,
    order3,
    order4
])

session.commit()

#Retrieve all users and print their information
query = select(User)
users = session.execute(query).scalars().all()

for number, user in enumerate(users, start=1):
    print(f"User: {number}")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")

#Retrieve all products and print their name and price
query = select(Product)
products = session.execute(query).scalars().all()

for product in products:
    print(f"Product's name: {product.name}")
    print(f"Product's price: {product.price}")

#Retrieve all orders, showing the user’s name, product name, and quantity
query = select(Order)
orders = session.execute(query).scalars().all()

for order in orders:
    print(
        f"User: {order.customer.name}, "
        f"Product: {order.product.name}, "
        f"Quantity: {order.quantity}"
    )

#Update a product’s price
query = select(Product).where(Product.id == 1)
product = session.execute(query).scalar_one()

product.price = 22
session.commit()

#Delete a user by ID
query = select(User).where(User.id == 2)
user = session.execute(query).scalar_one()

session.delete(user)
session.commit()

#Query all orders that are not shipped
query = select(Order).where(Order.status == False)

orders = session.execute(query).scalars().all()

for order in orders:
    print(
        order.customer.name,
        order.product.name,
        order.quantity
    )
    
#Count the total number of orders per user
query = select(User.name, func.count(Order.id)).join(Order).group_by(User.id)

results = session.execute(query).all()

for name, count in results:
    print(f"{name}: {count} orders")