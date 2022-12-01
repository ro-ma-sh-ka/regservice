from fastapi import FastAPI


app = FastAPI()


@app.post("/")
def test():
    return test


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
