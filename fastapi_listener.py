from fastapi import FastAPI
import asyncio
import pika
app = FastAPI()

x = [1]           # a global variable x


@app.get("/")
def hello():
    return {"message": "hello", "x": x}


async def periodic():
    while True:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='rpc_queue')

        connection.close()
        # code to run periodically starts here
        x[0] += 1
        print(f"x is now {x}")
        # code to run periodically ends here
        # sleep for 3 seconds after running above code
        await asyncio.sleep(3)


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
