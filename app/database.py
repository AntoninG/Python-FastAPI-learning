from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./article.db'

engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Create DB schemas
Base.metadata.create_all(engine)
