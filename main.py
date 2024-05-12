from fastapi import FastAPI
from database import engine, Base
from routers import auth, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/healthy')
async def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(users.router)