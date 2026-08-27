from flask import Flask, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gns_signal_2026'
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

@socketio.on("join_room")
def handle_join(data):
    room_id = data["room"]
    sid = request.sid
    if room_id not in rooms:
        rooms[room_id] = []
    if sid not in rooms[room_id]:
        rooms[room_id].append(sid)
    client_addr = data["addr"]
    if len(rooms[room_id]) == 2:
        p1, p2 = rooms[room_id]
        socketio.emit("peer_info", {"peer": client_addr}, to=p1)
        socketio.emit("peer_info", {"peer": client_addr}, to=p2)
        del rooms[room_id]

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
