from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Get the link for the database
# If it's not in the environment, use the default one
db_link = os.getenv("DATABASE_URL")
if db_link == None:
    db_link = "mysql+pymysql://iotuser:iotpassword@db:3306/iotdb"

# Setting up the connection
my_engine = create_engine(
    db_link,
    pool_pre_ping=True,
    pool_recycle=3600
)

# This is for making sessions later
SessionMakerObject = sessionmaker(autocommit=False, autoflush=False, bind=my_engine)

# The base class for the tables
MyBase = declarative_base()

class SensorReading(MyBase):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    raw_json = Column(Text, nullable=True)
    # Use datetime.utcnow as the default
    received_at = Column(DateTime, default=datetime.utcnow)

class Alert(MyBase):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False)
    violated_keys = Column(Text, nullable=False)
    actual_values = Column(Text, nullable=False)
    threshold_values = Column(Text, nullable=False)
    severity = Column(String(50), default="WARNING")
    created_at = Column(DateTime, default=datetime.utcnow)

def create_tables():
    print("Now starting to create the tables...")
    # This creates all the tables we defined above
    MyBase.metadata.create_all(bind=my_engine)
    print("Done creating tables.")

def get_db():
    # Make a new session
    database_session = SessionMakerObject()
    try:
        yield database_session
    finally:
        # Close it when the work is finished
        database_session.close()