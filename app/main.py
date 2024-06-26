from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from redis import Redis

app = FastAPI()
redis = Redis(host='localhost', port=6379, db=0)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def get():
    with open("app/static/index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            redis.rpush("chat", data)
            await websocket.send_text(f"Message received: {data}")
        except WebSocketDisconnect:
            print("Client disconnected")
            break
