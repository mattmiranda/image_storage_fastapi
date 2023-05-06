from datetime import datetime
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Image(BaseModel):
    _id: str
    createdDate: int
    filename: str
    contentType: str

images = {
    "0": Image(_id="0", createdDate=123098123, filename="cat1.jpeg", contentType="image/jpeg"),
    "1": Image(_id="1", createdDate=123098124, filename="cat2.jpeg", contentType="image/jpeg"),
    "2": Image(_id="2", createdDate=123098125, filename="cat3.jpeg", contentType="image/jpeg"),
    "3": Image(_id="3", createdDate=123098126, filename="cat4.jpeg", contentType="image/jpeg")
}

@app.get("/")
def index():
    return {"images": images}


@app.get("/image/{image_id}")
def query_image_by_id(image_id: str):
    if image_id not in images:
        raise HTTPException(status_code=404, detail=f"Image with ID {image_id} does not exist")
    else:
        return images[image_id]

# Problem with the typing Union operator in python 3.9
@app.get("/image")
def query_image_by_parameter(
        filename: str
        # contentType: Optional[str],
        # createdDate: Optional[int]
):
    def check_image(image: Image):
        return filename is None or image.filename == filename
        # return all(
        #     (
        #         filename is None or image.filename == filename
        #         contentType is None or image.contentType == contentType,
        #         createdDate is None or image.createdDate == createdDate
        #     )
        # )
    selection = [image for image in images.values() if check_image(image)]
    return {
        "query": {"filename": filename},
        "selection": selection
    }

@app.post("/")
def add_image(image: Image):
    for img in images:
        if image.filename == img:
            HTTPException(status_code=400, detail=f"Image with id {image._id} already exists")

    images[image._id] = image
    return {"status": "success", "added_image": image}
    
# @app.put("/images/{image_id}")
    
@app.delete("/image/{image_id}")
def delete_image(image_id: str):
    if image_id not in images:
        raise HTTPException(status_code=404, detail=f"Image with id {image_id} does not exist")
    
    image = images.pop(image_id)
    return {"status": "success", "delete_image": image}