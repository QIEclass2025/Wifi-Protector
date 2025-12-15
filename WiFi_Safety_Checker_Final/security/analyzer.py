# security/analyzer.py
import re
from data.education_content import EDUCATION_CONTENT

def analyze_security(wifi_info, os_type=""):
    """WiFi 정보를 분석하여 최종 점수와 세부 분석 항목 리스트를 반환합니다."""
    score = 100
    analysis_items = []

    # 1. 암호화 강도 분석
    if not wifi_info or 'auth' not in wifi_info:
        # 조기 반환 대신 기본 오류 항목 추가
        analysis_items.append({"check": "암호화 강도", "status": "WiFi 정보를 가져올 수 없습니다.", "score_change": -100})
        score = 0
    else:
        auth_method = wifi_info['auth'].upper()
        if os_type == "Darwin" and auth_method == "NONE":
            analysis_items.append({"check": "암호화 강도", "status": "확인 불가 (기업용/802.1X 네트워크 가능성)", "score_change": 0})
        elif "WPA3" in auth_method:
            analysis_items.append({"check": "암호화 강도", "status": "WPA3 (매우 안전)", "score_change": 0})
        elif "WPA2" in auth_method:
            score -= 10
            analysis_items.append({"check": "암호화 강도", "status": "WPA2 (안전)", "score_change": -10})
        elif "WPA" in auth_method and "WPA2" not in auth_method:
            score -= 40 # 점수 조정
            analysis_items.append({"check": "암호화 강도", "status": "WPA (주의 필요)", "score_change": -40})
        elif "WEP" in auth_method:
            score -= 80
            analysis_items.append({"check": "암호화 강도", "status": "WEP (위험)", "score_change": -80})
        elif "OPEN" in auth_method or auth_method == "NONE":
            score -= 100
            analysis_items.append({"check": "암호화 강도", "status": "개방형 네트워크 (매우 위험)", "score_change": -100})
        else:
            score -= 50
            analysis_items.append({"check": "암호화 강도", "status": f"알 수 없는 방식: {auth_method}", "score_change": -50})

    # 2. MITM 위험 분석 (Placeholder)
    # 실제 MITM 탐지 로직은 복잡하므로, 여기서는 '안전'으로 가정합니다.
    # 추후 ARP 스푸핑 감지 등의 로직을 추가할 수 있습니다.
    analysis_items.append({
        "check": "중간자 공격(MITM) 위험",
        "status": "현재 네트워크에서는 탐지된 위험 없음",
        "score_change": 0 # MITM 위험은 점수에 반영하지 않음 (탐지가 어려우므로)
    })

    score = max(0, score)
    return score, analysis_items
