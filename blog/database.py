from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


sql_alchemy_database = 'sqlite:///./blog.db'
engine = create_engine(sql_alchemy_database, connect_args={"check_same_thread": False}) 

Base = declarative_base()
Sessionlocal =sessionmaker(bind=engine, autocommit=False, autoflush=False)


