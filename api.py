from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
def say_hello():
    return {"message": "안녕하세요"}

