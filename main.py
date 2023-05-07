import os
import uuid
import aiofiles
from PIL import Image
from typing import Union, Optional, Annotated
from datetime import datetime
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import db_utils as db

IMG_BASE_PATH = "./image/"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# I understand that pydantic is very useful to create and manage the data models,
# however I decided to use only basic python objects and data types as the purpose
# of this assignment is not to test my ability using pydantic.


# Index route returns a list of all image objects
@app.get("/")
def query_all_images() -> dict[str, list]:
    images = db.read()
    return {"images": images}


# Query images by parameters included in the url. These are optional parameters.
# Example: /image?filename=cat1.jpeg
# TODO: Update python to 3.10+ in order to use simplified Optional/Union syntax, ie: str | None = None
@app.get("/image")
def query_image_by_parameter(
    filename: Optional[str] = None,
    contentType: Optional[str] = None,
    createdDate: Optional[int] = None,
) -> dict[str, list]:
    def check_image(image: dict):
        return all(
            (
                filename is None or image["filename"] == filename,
                contentType is None or image["contentType"] == contentType,
                createdDate is None or image["createdDate"] == createdDate,
            )
        )

    images_list = db.read()
    selection = [image for image in images_list if check_image(image)]
    return {"query_result": selection}


# API to get image by image_id. Returns image file.
@app.get("/image/{image_id}")
def get_image_by_id(image_id: str) -> FileResponse:
    images_list = db.read()
    images = db.list_to_dict(images_list)
    if image_id not in images:
        raise HTTPException(
            status_code=404, detail=f"Image with ID {image_id} does not exist"
        )

    return FileResponse(IMG_BASE_PATH + images[image_id]["filename"])


# Endpoint to add an image to storage and DB. Returns the downsized image file.
@app.post("/")
async def add_image(file: Annotated[UploadFile, File()]) -> FileResponse:
    if not file.filename or file.size < 1:
        raise HTTPException(status_code=404, detail=f"Invalid or missing file")

    # Save image to 'image' directory using buffer
    out_file_path = IMG_BASE_PATH + file.filename
    async with aiofiles.open(out_file_path, "wb") as out_file:
        while content := await file.read(5 * 1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    # If image is larger than 1MB, downsize it and overwrite the original image
    img = Image.open(out_file_path)
    if img.width > 500 or img.height > 500:
        img.thumbnail((500, 500))
    img.save(IMG_BASE_PATH + file.filename)

    images_list = db.read()
    for img in images_list:
        if file.filename == img["filename"]:
            # Image with same name already exists, update existing entry
            db.update_entry(img)
            return FileResponse(IMG_BASE_PATH + file.filename)

    # Store image entry in DB
    new_image = {
        "_id": uuid.uuid1().hex,
        "createdDate": int(datetime.now().timestamp()),
        "filename": file.filename,
        "contentType": file.content_type,
    }
    result = db.add_image(new_image)
    return FileResponse(IMG_BASE_PATH + file.filename)


# TODO: Implement patching function for completeness
# @app.put("/images/{image_id}")


# Delete image data from DB and image file.
@app.delete("/image/{image_id}")
def delete_image(image_id: str):
    images_list = db.read()
    images = db.list_to_dict(images_list)
    if image_id not in images:
        raise HTTPException(
            status_code=404, detail=f"Image with id {image_id} does not exist"
        )

    # Delete image entry from DB
    image = db.remove_image(image_id)

    # Delete image file from 'image' directory
    os.remove(IMG_BASE_PATH + image["filename"])

    return {"status": "success", "delete_image": image}
