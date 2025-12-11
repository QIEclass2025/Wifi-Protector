# security/analyzer.py
import re
from data.education_content import EDUCATION_CONTENT

def analyze_security(wifi_info, os_type=""):
    """WiFi 정보를 분석하여 최종 점수와 세부 분석 항목 리스트를 반환합니다."""
    score = 100
    analysis_items = []  # 각 항목의 점검 결과를 담을 리스트

    if not wifi_info or 'auth' not in wifi_info:
        return 0, [{"check": "오류", "status": "WiFi 정보를 가져올 수 없습니다.", "score_change": -100}]

    auth_method = wifi_info['auth'].upper()

    # macOS에서 기업용 네트워크 등이 'None'으로 표시되는 경우를 위한 특별 처리
    if os_type == "Darwin" and auth_method == "NONE":
        analysis_items.append({
            "check": "암호화 강도",
            "status": "확인 불가 (기업용/802.1X 네트워크 가능성)",
            "score_change": 0
        })
    elif "WPA3" in auth_method:
        analysis_items.append({"check": "암호화 강도", "status": "WPA3 (매우 안전)", "score_change": 0})
    elif "WPA2" in auth_method:
        score -= 10
        analysis_items.append({"check": "암호화 강도", "status": "WPA2 (안전)", "score_change": -10})
    elif "WPA" in auth_method and "WPA2" not in auth_method:
        score -= 60
        analysis_items.append({"check": "암호화 강도", "status": "WPA (주의 필요)", "score_change": -60})
    elif "WEP" in auth_method:
        score -= 80
        analysis_items.append({"check": "암호화 강도", "status": "WEP (위험)", "score_change": -80})
    elif "OPEN" in auth_method or auth_method == "NONE":
        score -= 100
        analysis_items.append({"check": "암호화 강도", "status": "개방형 네트워크 (매우 위험)", "score_change": -100})
    else:
        score -= 100
        analysis_items.append({"check": "암호화 강도", "status": "알 수 없음 (오류)", "score_change": -100})

    score = max(0, score)
    return score, analysis_items
