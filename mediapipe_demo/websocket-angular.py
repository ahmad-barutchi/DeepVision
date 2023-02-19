import cv2
import json
import asyncio
import websockets


async def process_video(websocket, path):
    cap = cv2.VideoCapture()
    fourcc = cv2.VideoWriter_fourcc(*'VP80')
    out = cv2.VideoWriter('output.webm', fourcc, 30.0, (640, 480))

    while True:
        data = await websocket.recv()
        if not data:
            break
        out.write(data)
        ret, frame = cap.read()
        if not ret:
            break
        # Your computer vision processing code here
        result = {'x': 10, 'y': 20, 'width': 30, 'height': 40}
        await websocket.send(json.dumps(result))


async def main():
    async with websockets.serve(process_video, "localhost", 8000):
        print("Listening to localhost:8000")
        await asyncio.Future()  # run forever


asyncio.run(main())
