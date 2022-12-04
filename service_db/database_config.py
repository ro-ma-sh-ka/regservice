from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///service_db/appeals_registration.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
