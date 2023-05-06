import os
import uuid
import aiofiles
from typing import Optional, Annotated
from datetime import datetime
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import db_utils as db

app = FastAPI()

# I understand that pydantic is very useful to create the data models. 
# I will try using it for data validation later.
# class Image(BaseModel):
#     _id: str
#     createdDate: int
#     filename: str
#     contentType: str

@app.get("/")
def index():
    images = db.read()
    return {"images": images}


@app.get("/image/{image_id}")
def query_image_by_id(image_id: str):
    images_list = db.read()
    images = db.list_to_dict(images_list)
    if image_id not in images:
        raise HTTPException(status_code=404, detail=f"Image with ID {image_id} does not exist")
    else:
        return images[image_id]

# Problem with the typing Union operator in python 3.9
@app.get("/image")
def query_image_by_parameter(
        filename: Optional[str] = None,
        contentType: Optional[str] = None,
        createdDate: Optional[int] = None
):
    def check_image(image: dict): #(image: Image)
        return all(
            (
                filename is None or image['filename'] == filename,
                contentType is None or image['contentType'] == contentType,
                createdDate is None or image['createdDate'] == createdDate
            )
        )
    images_list = db.read()
    selection = [image for image in images_list if check_image(image)]
    return {
        "query": {"filename": filename, "contentType": contentType, "createdDate": createdDate},
        "selection": selection
    }

@app.post("/")
async def add_image(
    file: Annotated[UploadFile, File()]
): #(image: Image)
    print("filename: ", file.filename)
    print("fileb_content_type: ", file.content_type)
    images_list = db.read()
    for img in images_list:
        if file.filename == img["filename"]:
            HTTPException(status_code=400, detail=f"Image with same name already exists")

    # Save image to 'image' directory using buffer
    out_file_path = './image/' + file.filename
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    # Store image entry to DB
    new_image = {
        "_id": uuid.uuid1().hex,
        "filename": file.filename,
        "contentType": file.content_type,
        "createdDate": int(datetime.now().timestamp())
    }
    result = db.add_image(new_image)
    return {"status": "success", "added_image": new_image}
    
# # @app.put("/images/{image_id}")
    
@app.delete("/image/{image_id}")
def delete_image(image_id: str):
    images_list = db.read()
    images = db.list_to_dict(images_list)
    if image_id not in images:
        raise HTTPException(status_code=404, detail=f"Image with id {image_id} does not exist")

    # Delete image entry from DB
    image = db.remove_image(image_id)

    # Delete image file from 'image' directory
    os.remove('./image/'+image['filename'])

    return {"status": "success", "delete_image": image}