from models import Product

from database import Base, SessionLocal, engine


def test_database_connection():
    print("1. Creating database tables in PostgreSQL...")
    # Creates tables in Postgres if they don't exist yet
    Base.metadata.create_all(bind=engine)
    print("   Tables created successfully!")

    # Open a new database session
    db = SessionLocal()

    try:
        print("\n2. Inserting a test product into 'product' table...")
        test_product = Product(
            name="Basil Plant 4in Pot",
            unit="each",
            cost_per_unit=1.75,
            price_per_unit=4.99,
            quantity_in_stock=40.0,
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        print(f"   Success! Product inserted with ID: {test_product.id}")

        print("\n3. Querying product back from database...")
        retrieved_product = (
            db.query(Product).filter(Product.id == test_product.id).first()
        )
        print(
            f"   Fetched item: {retrieved_product.name} | Stock: {retrieved_product.quantity_in_stock}"
        )

    except Exception as e:
        print(f"\n❌ Error connecting or performing query: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_database_connection()
