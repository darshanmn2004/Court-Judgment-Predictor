from database import engine, Base
from models import PredictionHistory

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully")
