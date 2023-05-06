# Backend of Image management and compression service (Picky Assignment)

The purpose of this subdirectory is to separate the frontend from the backend code and have separate git repositories. I generally like separating files and code based on their purpose and where they will run. 
In this case the backend can be hosted on a completely different server than the frontend.

## Steps and thought process
1. Create a virtual environment in python where I can install and explore FastAPI and its depedencies (especially uvicorn for runninng the server).
2. Create basic endpoints for CRUD operations using FastAPI annotations.
3. Create a test.py file that makes HTTP requests to test the APIs. I also created a Postman collection that does the same thing. UPDATE: Postman is much better for testing image upload. 
4. Now that the add image, delete image, get image by id, and get all images APIs are implemented, I will handle the large image. 


## TODO:
1. Add return types to every function

