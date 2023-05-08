# Backend of Image management and compression service (Picky Assignment)

The purpose of this subdirectory is to separate the frontend from the backend code and have separate git repositories. I generally like separating files and code based on their purpose and where they will run. 
In this case the backend can be hosted on a completely different server than the frontend.

## Steps and thought process
1. Create a virtual environment in python where I can install and explore FastAPI and its depedencies (especially uvicorn for runninng the server).
2. Create basic endpoints for CRUD operations using FastAPI annotations.
3. Create a test.py file that makes HTTP requests to test the APIs. I also created a Postman collection that does the same thing. UPDATE: Postman is much better for testing image upload so it's the preferred testing method. 
4. Now that the add image, delete image, get image by id, and get all images APIs are implemented, I will handle the large image. 
5. I use the image handling library pillow to take care of resizing the image to about 500x500 pixels. I use the functions Image.thumbnail() to keep the aspect ratio of the image. 
6. I had to add CORS middleware in order to receive request from cross-origin.

## API Documentation
- GET "/"
    - Function: query_all_images()
    - Get all image records from DB.
    - Request body: NA
    - Response body: list of image objects
    ```
    {
        'images': [
            {
                "_id": "27e9a05e39db4fb4855ba49da888b9db",
                "createdDate": 1383866752,
                "filename": "cat1.jpeg",
                "contentType": "image/jpeg"
            }
        ]
    }
    ```

- GET "/image"
    - Function: query_image_by_parameter(
        filename: Optional[str] = None,
        contentType: Optional[str] = None,
        createdDate: Optional[int] = None,
    )
    - Return image records with maching parameters. Can be used like a search.
    - Request example
    ```
    /image?filename=cat1.jpeg
    ```
    - Response body: list of image objects
    ```
    {   
        'query_result': [
            {
                "_id": "27e9a05e39db4fb4855ba49da888b9db",
                "createdDate": 1383866752,
                "filename": "cat1.jpeg",
                "contentType": "image/jpeg"
            }
        ]
    }
    ```

- GET "/image/{image_id}"
    - Function: get_image_by_id(image_id: str)
    - Return image with maching ID. If ID is not found, raise a HTTPException.
    - Request example
    ```
    /image/27e9a05e39db4fb4855ba49da888b9db
    ```
    - Response body: FileResponse which is received as a ReadableStream containing the image data.

- POST "/"
    - Function: add_image(file: Annotated[UploadFile, File()])
    - Add new image to DB and file storage. Compress the image and return it.
    - Request body: FormData with one key:value pair
        - Key: 'file'
        - Value: image file data
    - Response body: FileResponse which is received as a ReadableStream containing the image data.

- DELETE "/image/{image_id}"
    - Function: delete_image(image_id: str)
    - Delete image with maching ID from the DB and storage. If ID is not found, raise a HTTPException.
    - Request example
    ```
    /image/27e9a05e39db4fb4855ba49da888b9db
    ```
    - Response body: 
    ```
    {"status": "success", "delete_image": imageObj}
    ```

## How to run
### Locally:
```
uvicorn app.main:app --reload
```

### Docker
Build image
```
docker build -t image-compression-backend .
```
Run image
```
docker run -d --name mycontainer -p 8000:8000 image-compression-backend
```

## TODO:
1. Unit test
1. Update python to 3.10+ in order to use simplified Optional/Union syntax, ie: str | None = None