import can
import time

# 使用するバスの選択（"VN1640A" または "VIRTUAL"）
USE_VN1640A = False  # True にすると VN1640A を使用
LOOPBACK_MODE = True  # True にするとループバックを有効化（VN1640A のみ）

if USE_VN1640A:
    print("VN1640A で動作中...")
    bus = can.interface.Bus(
        bustype='vector', channel=0, bitrate=500000, receive_own_messages=LOOPBACK_MODE
    )
else:
    print("仮想CANバスで動作中...")
    bus = can.interface.Bus(bustype='virtual', channel='1')

try:
    while True:
        # CAN メッセージ作成
        msg = can.Message(
            arbitration_id=0x123, data=[1, 2, 3, 4, 5, 6, 7, 8], is_extended_id=False
        )
        
        # メッセージ送信
        bus.send(msg)
        print(f"送信: {msg}")

        # ループバックが有効な場合のみ受信
        if USE_VN1640A and LOOPBACK_MODE:
            received_msg = bus.recv(timeout=1.0)
            if received_msg:
                print(f"受信: {received_msg}")

        time.sleep(1)  # 1秒間隔で送信

except KeyboardInterrupt:
    print("CANテスト終了")
finally:
    bus.shutdown()