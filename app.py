from flask import Flask, send_from_directory
import os
import socket
import webbrowser
import threading

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_ip():
    """獲取本機的區域網路 IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 連線到一個外部 IP 來強制獲取本機的 LAN IP
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


@app.route('/')
def index():
    # 電腦端：主控台 (負責算圖與顯示模型)
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/phone')
def phone():
    # 手機端：純鏡頭畫面
    return send_from_directory(BASE_DIR, 'phone.html')


@app.route('/<path:filename>')
def serve_static(filename):
    # 負責提供模型檔 (.glb) 或其他靜態資源
    return send_from_directory(BASE_DIR, filename)


def open_browser(ip):
    """打開本機瀏覽器"""
    webbrowser.open(f"https://{ip}:5000")


if __name__ == '__main__':
    local_ip = get_ip()

    print(f"\n🚀 PosAnatomy 主控台啟動中...")
    print(f"💻 電腦端主控台: https://{local_ip}:5000")
    print(f"📱 區網參考 IP: {local_ip} (手機端請以網頁產生的 QR Code 為準)\n")

    # 延遲 1 秒打開瀏覽器，確保 Flask 伺服器已經完全啟動，避免出現「無法連線」的畫面
    threading.Timer(1.0, open_browser, args=[local_ip]).start()

    # 啟動 Flask 伺服器
    # ⚠️ 注意：ssl_context='adhoc' 需要安裝 pyopenssl，如果報錯請在終端機執行：pip install pyopenssl
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc', debug=False)