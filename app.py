from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'p2p_signal_2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# 网络池字典：key=池名称，value=池内所有玩家sid和公网地址
network_pools = {}

@socketio.on('join_pool')
def handle_join_pool(data):
    pool_name = data['pool_name']
    public_addr = data['public_addr']  # 客户端上传自己的公网IP:端口
    sid = request.sid

    if pool_name not in network_pools:
        network_pools[pool_name] = {}
    # 存入当前玩家信息
    network_pools[pool_name][sid] = public_addr
    # 把池内全部玩家列表广播给池里所有人
    emit('pool_member_list', {
        "pool": pool_name,
        "members": network_pools[pool_name]
    }, room=pool_name)

@socketio.on('leave_pool')
def handle_leave_pool(data):
    pool_name = data['pool_name']
    sid = request.sid
    if pool_name in network_pools and sid in network_pools[pool_name]:
        del network_pools[pool_name][sid]
        # 没人就删掉这个池
        if len(network_pools[pool_name]) == 0:
            del network_pools[pool_name]
        else:
            emit('pool_member_list', {
                "pool": pool_name,
                "members": network_pools[pool_name]
            }, room=pool_name)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
