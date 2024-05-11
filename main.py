from fastapi import FastAPI
from database import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/healthy')
async def health_check():
    return {'status': 'Healthy'}