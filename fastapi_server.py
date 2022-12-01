from fastapi import FastAPI


app = FastAPI()


@app.post("/send")
def test():
    print('test')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
