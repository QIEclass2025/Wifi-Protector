# utils/system_info.py
import platform
import subprocess
import re
import geocoder

def get_wifi_info(password=None):
    """
    현재 연결된 WiFi의 상세 정보(SSID, BSSID, 인증/암호화 방식 등)를 수집합니다.
    OS에 따라 다른 명령어를 사용하며, 정보 수집 실패 시에도 안전하게 처리합니다.
    macOS의 경우 sudo 암호를 인자로 받아 처리할 수 있습니다.
    """
    os_type = platform.system()
    wifi_data = {}

    try:
        if os_type == "Windows":
            # ... (기존 Windows 코드와 동일)
            def safe_extract(pattern, text):
                match = re.search(pattern, text, re.MULTILINE)
                if match and match.group(1):
                    value = match.group(1).strip()
                    if value:
                        return value
                return "N/A"
            output = subprocess.check_output(
                "netsh wlan show interfaces",
                shell=True,
                text=True,
                encoding="cp949",
                errors="ignore"
            )
            if ("There is no wireless interface on the system" in output or
                "not connected" in output or
                "무선 인터페이스가 시스템에 없습니다" in output or
                "연결되어 있지 않습니다" in output):
                return None
            wifi_data["ssid"] = safe_extract(r"SSID\s*:\s*(.*)", output)
            if wifi_data["ssid"] == "N/A":
                return None
            wifi_data["bssid"] = safe_extract(r"BSSID\s*:\s*(.*)", output)
            wifi_data["auth"] = safe_extract(r"(?:Authentication|인증)\s*:\s*(.*)", output)
            wifi_data["encryption"] = safe_extract(r"(?:Cipher|암호화)\s*:\s*(.*)", output)
            signal = safe_extract(r"(?:Signal|신호)\s*:\s*(\d+)", output)
            wifi_data["signal"] = f"{signal}%" if signal != "N/A" else "N/A"

        elif os_type == "Darwin":  # macOS
            try:
                command = "sudo -S wdutil info"
                
                process = subprocess.Popen(
                    command, # command is now a single string
                    shell=True, # shell=True is added
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    errors="ignore"
                )
                
                output, stderr = process.communicate(input=password + "\n" if password else None)

                # sudo 암호가 틀렸거나 다른 sudo 관련 오류 확인
                if "incorrect password attempt" in stderr or "sudo: a password is required" in stderr:
                    print(f"Sudo error: {stderr.strip()}")
                    return None

                def safe_extract(pattern, text):
                    match = re.search(pattern, text, re.MULTILINE)
                    if match and match.group(1):
                        value = match.group(1).strip()
                        if value:
                            return value
                    return "N/A"

                wifi_data["ssid"] = safe_extract(r"SSID\s*:\s*(.*)", output)
                if wifi_data["ssid"] == "N/A":
                    print("Could not find SSID in wdutil output.")
                    return None

                wifi_data["bssid"] = safe_extract(r"BSSID\s*:\s*(.*)", output)
                auth = safe_extract(r"Security\s*:\s*(.*)", output)
                wifi_data["auth"] = auth.upper() if auth != "N/A" else "NONE"
                wifi_data["encryption"] = wifi_data["auth"]
                
                rssi = safe_extract(r"RSSI\s*:\s*(-\d+)", output)
                wifi_data["signal"] = f"{rssi} dBm" if rssi != "N/A" else "N/A"

            except Exception as e:
                print(f"An unexpected error occurred while getting WiFi info with wdutil: {e}")
                return None
        
        else:  # Linux 등
            return None

    except Exception as e:
        print(f"WiFi 정보 수집 중 예기치 않은 오류: {e}")
        return None

    return wifi_data


# 이미 쓰고 있던 함수가 있을 테니, 없다면 참고용으로 같이 써도 됨
def get_location():
    """
    현재 대략적인 위치(위도/경도)를 반환합니다.
    실패 시 기본값(서울 시청)을 반환합니다.
    """
    try:
        g = geocoder.ip("me")
        if g.ok and g.latlng:
            lat, lon = g.latlng
            return {"lat": float(lat), "lon": float(lon)}
    except Exception:
        pass

    # 실패 시 기본값: 서울 시청
    return {"lat": 37.5665, "lon": 126.9780}