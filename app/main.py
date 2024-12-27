from typing import Union

from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from routers import upload_test, download_test, presigned_test
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Allow only the Next.js frontend origin
origins = [
    "http://localhost:3000",  # Your Next.js frontend
    "http://127.0.0.1:3000",  # Localhost alternative
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow specific methods (GET for downloads)
    allow_headers=["*"],  # Allow all headers
)

#Include Routers
app.include_router(upload_test.router)
app.include_router(download_test.router,prefix="/download-test",tags=["download-test"])
app.include_router(presigned_test.router,prefix="/presigned-test",tags=["presigned-test"])
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
