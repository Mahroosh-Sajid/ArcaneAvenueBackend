from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from routes.auth_routes import auth_router
# entire application
app = FastAPI()

# allows front end to communicate to backened 
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)


# testing end point
@app.get("/")
def read_root():
    return {"Hello": "World"}

