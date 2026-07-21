from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}