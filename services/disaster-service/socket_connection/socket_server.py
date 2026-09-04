import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)


@sio.event
async def connect(sid, environ, auth):
    print("🔥 SOCKET CONNECTED:", sid)


@sio.event
async def disconnect(sid):
    print("🔥 SOCKET DISCONNECTED:", sid)