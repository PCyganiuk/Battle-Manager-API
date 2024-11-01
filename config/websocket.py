from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        self.active_connections[websocket] = game_id

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def broadcast(self, message: dict, game_id: str):
        for connection, conn_game_id in self.active_connections.items():
            if conn_game_id == game_id:
                await connection.send_json(message)