# utils/system_info_windows.py
import pywifi
from pywifi import const
import geocoder
import time

def get_wifi_info_windows():
    """
    현재 연결된 WiFi의 상세 정보(SSID, BSSID, 인증/암호화 방식 등)를 수집합니다.
    Windows OS에서 pywifi 라이브러리를 사용합니다.
    """
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0] # 첫 번째 무선랜카드 선택

        if iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
            return None

        profile = iface.scan_results()[0] # 현재 연결된 프로파일 정보 (가장 신호가 강한 SSID 기준)
        
        # 인증 방식과 암호화 방식을 문자열로 변환
        auth_str = "N/A"
        if profile.akm:
            if const.AKM_TYPE_WPA2PSK in profile.akm:
                auth_str = "WPA2"
            elif const.AKM_TYPE_WPAPSK in profile.akm:
                auth_str = "WPA"
            elif const.AKM_TYPE_WPA2 in profile.akm:
                auth_str = "WPA2-ENTERPRISE"
            elif const.AKM_TYPE_WPA in profile.akm:
                auth_str = "WPA-ENTERPRISE"
            elif const.AKM_TYPE_OPEN in profile.akm:
                auth_str = "OPEN"
        
        cipher_str = "N/A"
        if profile.cipher:
            if const.CIPHER_TYPE_CCMP in profile.cipher:
                cipher_str = "CCMP" # WPA2에서 주로 사용
            elif const.CIPHER_TYPE_TKIP in profile.cipher:
                cipher_str = "TKIP" # WPA에서 주로 사용
            elif const.CIPHER_TYPE_WEP in profile.cipher:
                cipher_str = "WEP"
            elif const.CIPHER_TYPE_NONE in profile.cipher:
                cipher_str = "NONE"

        wifi_data = {
            "ssid": profile.ssid,
            "bssid": profile.bssid,
            "auth": auth_str,
            "encryption": cipher_str,
            "signal": f"{profile.signal}%"
        }
        return wifi_data

    except Exception as e:
        print(f"pywifi를 사용하여 WiFi 정보 수집 중 오류: {e}")
        return None

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

    return {"lat": 37.5665, "lon": 126.9780}
