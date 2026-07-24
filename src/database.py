from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Update with your team's credentials
DATABASE_URL = "postgresql://root:root@127.0.0.1:5432/gardendb"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

temp_storage = []
