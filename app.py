from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# 网络池：key=池名, value={玩家地址: 最后心跳时间}
pools = {}

@app.route('/join', methods=['POST'])
def join():
    data = request.get_json()
    pool_name = data['pool']
    addr = data['addr']  # 格式：ip:port
    if pool_name not in pools:
        pools[pool_name] = {}
    pools[pool_name][addr] = time.time()
    return jsonify({"members": list(pools[pool_name].keys())})

@app.route('/list', methods=['GET'])
def list_members():
    pool_name = request.args.get('pool')
    if pool_name not in pools:
        return jsonify({"members": []})
    # 自动清理超过60秒没心跳的掉线玩家
    now = time.time()
    pools[pool_name] = {a: t for a, t in pools[pool_name].items() if now - t < 60}
    return jsonify({"members": list(pools[pool_name].keys())})

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json()
    pool_name = data['pool']
    addr = data['addr']
    if pool_name in pools and addr in pools[pool_name]:
        pools[pool_name][addr] = time.time()
    return jsonify({"ok": True})

@app.route('/leave', methods=['POST'])
def leave():
    data = request.get_json()
    pool_name = data['pool']
    addr = data['addr']
    if pool_name in pools and addr in pools[pool_name]:
        del pools[pool_name][addr]
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
