from flask import Flask, send_from_directory
import os
import socket
import webbrowser

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_ip():
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
    return send_from_directory(BASE_DIR, filename)


if __name__ == '__main__':
    local_ip = get_ip()

    print(f"\n🚀 PosAnatomy 主控台啟動中...")
    # 【關鍵修正】：這裡全部改用 local_ip，確保產生的 QR Code 網址是正確的區域網路 IP
    print(f"💻 電腦端主控台: https://{local_ip}:5000")
    print(f"📱 區網參考 IP: {local_ip} (手機端請以網頁產生的 QR Code 為準)\n")

    # 讓電腦自動打開本機主控台 (使用真實區域網路 IP)
    webbrowser.open(f"https://{local_ip}:5000")

    # 啟動 Flask 伺服器，使用 adhoc 產生臨時 HTTPS 憑證
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc', debug=False)