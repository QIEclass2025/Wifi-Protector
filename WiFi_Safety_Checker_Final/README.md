# WiFi Safety Checker

현재 연결된 WiFi 네트워크의 보안 상태를 점검하고, 취약점을 분석하여 사용자에게 알려주는 데스크탑 애플리케이션입니다.

## 주요 기능

- **WiFi 보안 점수:** 현재 네트워크의 암호화 방식, 잠재적 위협 등을 분석하여 100점 만점으로 점수를 매깁니다.
- **상세 분석:** WPA3, WPA2, WEP 등 사용 중인 보안 프로토콜을 탐지하고 위험성을 알려줍니다.
- **보안 가이드:** 분석 결과에 따른 보안 강화 조치 사항을 안내합니다. (기능 구현 예정)
- **점검 기록 지도:** 과거에 점검했던 WiFi 네트워크의 위치와 보안 점수를 지도에 표시하여 시각적으로 확인합니다. (macOS에서 완벽 지원, Windows는 기능 개발 중)

---

## 요구 사항

- Python 3.8 이상
- `uv` (초고속 Python 패키지 설치 및 관리 도구)

`uv`가 설치되어 있지 않다면, 아래 명령어로 설치할 수 있습니다:
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 설치 및 실행 방법

1.  **Git 리포지토리 복제**

    ```bash
    git clone <your-repository-url>
    cd WiFi_Safety_Checker_Final
    ```

2.  **필요한 라이브러리 설치**

    프로젝트 폴더 내에서 `uv`를 사용하여 필요한 모든 라이브러리를 설치합니다.

    ```bash
    uv pip install -r requirements.txt
    ```

3.  **애플리케이션 실행**

    아래 명령어를 사용하여 프로그램을 실행합니다.

    ```bash
    uv run main.py
    ```
    
    **참고:** 정확한 WiFi 정보 스캔을 위해 최초 실행 시 **관리자(sudo) 암호**를 요구할 수 있습니다. 이는 시스템 네트워크 유틸리티에 접근하기 위한 정상적인 절차입니다.

## 프로젝트 구조

```
WiFi_Safety_Checker_Final/
│
├── data/              # 데이터베이스 및 교육 콘텐츠 관련 모듈
├── gui/               # PyQt6 기반의 GUI 컴포넌트 및 UI 로직
├── security/          # WiFi 보안 분석 로직
├── utils/             # OS별 정보 수집 등 유틸리티 함수
│
├── main.py            # 애플리케이션 메인 실행 스크립트 (OS 자동 감지)
├── requirements.txt   # 프로젝트 실행에 필요한 라이브러리 목록
├── .gitignore         # Git 버전 관리에서 제외할 파일/폴더 목록
└── README.md          # 프로젝트 설명서
```
