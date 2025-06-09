from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models import Base


DATABASE_URL ="sqlite:///gym_membership.db"


engine = create_engine(DATABASE_URL, echo=False, future=True)

#creating all tables if they do not exist
Base.metadata.create_all(engine)

#creating the session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@contextmanager
def get_session():
    """
    Provide a transactional scope around a series of operations,
    using context management for safe commit/rollback/close.
    
    Usage:
        with get_session() as session:
            # perform database operations with session
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

