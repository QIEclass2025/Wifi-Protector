# 🛡️ WiFi Safety Checker

**WiFi Safety Checker**는 현재 연결된 WiFi 네트워크의 보안 상태를 분석하고, 안전 점수를 계산하며, 점검 이력을 지도에 시각화하여 보여주는 파이썬 기반의 GUI 애플리케이션입니다.

사용자가 연결한 네트워크가 개방형(Open)인지, 혹은 강력한 암호화(WPA2/WPA3)를 사용하는지 판별하여 해킹 위협으로부터 보호할 수 있도록 돕습니다.

## ✨ 주요 기능

  * **🔍 실시간 보안 점검**: 현재 연결된 WiFi의 SSID, BSSID, 암호화 방식(Auth/Encryption)을 분석합니다.
  * **💯 보안 점수 산정**: 암호화 강도에 따라 0점\~100점까지 보안 점수를 부여합니다 (WPA3/WPA2는 안전, WEP/Open은 위험).
  * **📚 보안 가이드 제공**: 분석 결과에 따라 구체적인 위험 요소와 해결책(교육용 콘텐츠)을 제공합니다.
  * **🗺️ 점검 기록 시각화 (지도)**: 점검 당시의 대략적인 위치(IP 기반)를 저장하고, 지도 탭에서 과거 점검 이력과 안전도를 마커 색상(초록/노랑/빨강)으로 확인할 수 있습니다.
  * **💻 크로스 플랫폼 지원**: Windows 및 macOS 환경을 모두 지원합니다 (macOS의 경우 `wdutil` 사용을 위해 관리자 권한 필요).

## 🛠️ 기술 스택

  * **Language**: Python 3.x
  * **GUI**: CustomTkinter
  * **Map**: TkinterMapView
  * **Database**: SQLite3
  * **Location**: Geocoder
  * **OS Interface**: Subprocess (netsh, wdutil)

## 📂 프로젝트 구조

```bash
Wifi-Protector/
├── main.py                  # 프로그램 실행 진입점
├── requirements.txt         # 필요 라이브러리 목록
├── gui/
│   ├── app.py               # GUI 구성 및 이벤트 처리 (메인 윈도우, 탭, 지도)
│   └── __init__.py
├── utils/
│   ├── system_info.py       # OS별 WiFi 정보 수집 및 위치 정보 파싱
│   └── __init__.py
├── security/
│   ├── analyzer.py          # 보안 점수 계산 및 취약점 분석 로직
│   └── __init__.py
└── data/
    ├── database.py          # SQLite DB 연동 (기록 저장 및 조회)
    ├── education_content.py # 보안 피드백 텍스트 데이터
    └── __init__.py
```

## 🚀 설치 및 실행 방법

### 1\. 저장소 복제 (Clone)

```bash
git clone https://github.com/QIEclass2025/Wifi-Protector.git
cd Wifi-Protector
```

### 2\. 필수 라이브러리 설치

제공된 `requirements.txt`를 사용하여 의존성 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

*주요 라이브러리: `customtkinter`, `tkintermapview`, `geocoder`, `Pillow` 등*

### 3\. 프로그램 실행

```bash
python main.py
```

프로그램이 시작되면 자동으로 데이터베이스(`wifi_history.db`)가 초기화되고 GUI 창이 열립니다.

## ⚠️ OS별 주의사항

### Windows

  * 별도의 권한 없이 `netsh` 명령어를 통해 정보를 수집합니다.

### macOS

  * macOS는 보안 정책상 WiFi 상세 정보를 얻기 위해 관리자 권한(`sudo`)이 필요합니다.
  * 점검 시작 시 **관리자 암호 입력 창**이 뜨면 맥북 잠금 해제 암호를 입력해주세요.
  * 입력된 암호는 `wdutil` 명령어를 실행하는 데에만 사용되며 저장되지 않습니다.

## 📊 보안 점수 기준

| 암호화 방식 | 점수 | 상태 | 설명 |
| :--- | :--- | :--- | :--- |
| **WPA3** | 100점 | ✅ 매우 안전 | 최신 보안 표준 사용 중 |
| **WPA2** | 90점 | ✅ 안전 | 일반적인 가정/기업용 보안 표준 |
| **WPA** | 40점 | ⚠️ 주의 | 오래된 방식, 업그레이드 권장 |
| **WEP** | 20점 | 🚨 위험 | 매우 쉽게 해킹 가능 |
| **OPEN** | 0점 | 🚨 매우 위험 | 비밀번호 없음, 데이터 도청 위험 |

## 📝 라이선스

This project is for educational purposes.
