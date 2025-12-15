# gui/app.py
import sys
import random
import platform
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QFrame, QInputDialog, QLineEdit, QDialog)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF, QPointF, QUrl

# --- PyInstaller 경로 문제 해결 함수 ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

try:
    from security.analyzer import analyze_security
    from data.database import add_record, get_all_records
    from utils import system_info
except ImportError:
    print("Warning: Backend modules not found. Using dummy functions.")
    def analyze_security(wifi_info, os_type):
        score = random.randint(0, 100)
        items = [{"check": "암호화 강도", "status": "WPA2 (안전)", "score_change": -10 if score < 71 else 0},
                 {"check": "중간자 공격(MITM) 위험", "status": "탐지된 위험 없음", "score_change": 0}]
        if score < 31: items[0]['status'], items[1]['status'] = "WEP / 개방형 (취약)", "탐지됨"
        elif score < 71: items[0]['status'] = "WPA2 (양호)"
        else: items[0]['status'] = "WPA3 (매우 강력)"
        return score, items
    def add_record(ssid, bssid, score, lat, lon): print(f"DB Record Added: {ssid}, {score}")
    def get_all_records(): return [{'ssid': 'Test1', 'bssid': '0A', 'score': 90, 'latitude': 37.56, 'longitude': 126.97}]
    class DummySystemInfo:
        def get_wifi_info(self, password=None): return {'auth': 'WPA2', 'bssid': '00:11:22:33:44:55', 'ssid': 'Test_WiFi'}
        def get_location(self): return {"lat": 37.5665, "lon": 126.9780}
    system_info = DummySystemInfo()

BG_COLOR = "#F5F7FA"
FONT_FAMILY = "Malgun Gothic" if platform.system() == "Windows" else "AppleSDGothicNeo"
COLOR_RED = "#dc3545"; COLOR_YELLOW = "#ffc107"; COLOR_GREEN = "#28a745"

class GaugeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.score = 0; self.status_text = ""; self.gauge_color = QColor(COLOR_GREEN)
        self.setMinimumSize(250, 200)

    def set_score(self, score):
        self.score = score
        if 71 <= score <= 100: self.gauge_color, self.status_text = QColor(COLOR_GREEN), "안전함"
        elif 31 <= score <= 70: self.gauge_color, self.status_text = QColor(COLOR_YELLOW), "주의 필요"
        else: self.gauge_color, self.status_text = QColor(COLOR_RED), "위험함"
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect, center, radius, pen_width = self.rect(), QPointF(self.rect().center()), min(self.rect().width(), self.rect().height()) / 2.5, 22
        bbox_rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        start_angle, span_angle = 225 * 16, -270 * 16
        pen = QPen(QColor("#EAEAEA"), pen_width); pen.setCapStyle(Qt.PenCapStyle.RoundCap); painter.setPen(pen)
        painter.drawArc(bbox_rect, start_angle, span_angle)
        score_span = int((self.score / 100.0) * span_angle); pen.setColor(self.gauge_color); painter.setPen(pen)
        painter.drawArc(bbox_rect, start_angle, score_span)
        painter.setPen(QColor("#000000")); font = QFont(FONT_FAMILY, 48, QFont.Weight.Bold); painter.setFont(font)
        painter.drawText(bbox_rect, Qt.AlignmentFlag.AlignCenter, f"{self.score}점")
        painter.setPen(self.gauge_color); font.setPointSize(16); painter.setFont(font)
        painter.drawText(QRectF(bbox_rect.x(), bbox_rect.y() + 40, bbox_rect.width(), bbox_rect.height()), Qt.AlignmentFlag.AlignCenter, self.status_text)

class ResultView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.main_window = parent
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card = QFrame(self); card.setObjectName("MainCard"); card.setStyleSheet("background-color: white; border-radius: 12px;"); card.setFixedSize(600, 450)
        card_layout = QVBoxLayout(card); card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gauge = GaugeWidget(); card_layout.addWidget(self.gauge)
        info_layout = QHBoxLayout(); info_layout.setSpacing(20)
        self.card_left_value, self.card_right_value = QLabel("WPA2-PSK"), QLabel("없음")
        info_layout.addWidget(self._create_info_card("🔒 암호화 강도", self.card_left_value)); info_layout.addWidget(self._create_info_card("⚠️ MITM 위험", self.card_right_value))
        card_layout.addLayout(info_layout)
        recheck_button = QPushButton("↻ 다시 점검하기"); recheck_button.setStyleSheet("color: #000000; border-radius: 8px; padding: 5px;")
        recheck_button.clicked.connect(lambda: self.main_window.select_tab("check"))
        card_layout.addWidget(recheck_button, 0, Qt.AlignmentFlag.AlignCenter); layout.addWidget(card)

    def _create_info_card(self, title, value_label):
        card = QFrame(); card.setFixedSize(250, 80); card.setStyleSheet("background-color: #F7F9FC; border-radius: 10px;")
        layout = QVBoxLayout(card); title_label = QLabel(title); title_label.setFont(QFont(FONT_FAMILY, 14)); title_label.setStyleSheet("color: #333;")
        value_label.setFont(QFont(FONT_FAMILY, 16, QFont.Weight.Bold)); value_label.setStyleSheet("color: #000000;")
        layout.addWidget(title_label); layout.addWidget(value_label)
        return card

    def update_ui(self, score, analysis_items):
        self.gauge.set_score(score)
        if analysis_items: self.card_left_value.setText(analysis_items[0]['status']); self.card_right_value.setText(analysis_items[1]['status'])

class PasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sudo Password")
        self.setStyleSheet("QDialog { background-color: white; }")

        layout = QVBoxLayout(self)
        self.label = QLabel("macOS 관리자 암호를 입력하세요:")
        self.label.setStyleSheet("color: black;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("color: black; background-color: #f0f0f0;")

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("color: black; background-color: lightgray;")
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("color: black; background-color: lightgray;")

        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addLayout(button_layout)

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

    def get_password(self):
        return self.password_input.text()

class StartView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.main_window = parent
        layout = QVBoxLayout(self); layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card = QFrame(self); card.setObjectName("MainCard"); card.setStyleSheet("background-color: white; border-radius: 12px;"); card.setFixedSize(600, 450)
        card_layout = QVBoxLayout(card); card_layout.setContentsMargins(50, 30, 50, 30); card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QLabel("🛜"); icon.setFont(QFont(FONT_FAMILY, 100)); icon.setStyleSheet("color: #AECBFA;")
        card_layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        self.ssid_label = QLabel(f"현재 연결된 네트워크: N/A"); self.ssid_label.setFont(QFont(FONT_FAMILY, 18, QFont.Weight.Bold)); self.ssid_label.setStyleSheet("color: #000000;")
        self.ssid_label.hide() # 처음에는 숨김
        card_layout.addWidget(self.ssid_label, 0, Qt.AlignmentFlag.AlignCenter)
        start_button = QPushButton("WiFi 점검 시작"); start_button.setFixedSize(250, 50)
        start_button.setObjectName("StartButton")
        start_button.setStyleSheet("#StartButton { background-color: #1A73E8; color: white; border-radius: 8px; font-size: 16px; font-weight: bold; } #StartButton:hover { background-color: #1558B4; }")
        start_button.clicked.connect(self.run_check)
        card_layout.addWidget(start_button, 0, Qt.AlignmentFlag.AlignCenter); layout.addWidget(card); self.refresh_ssid()

    def run_check(self):
        self.ssid_label.show()
        password = None
        if platform.system() == "Darwin":
            dialog = PasswordDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                password = dialog.get_password()
            else:
                return # User cancelled
        
        wifi_info = system_info.get_wifi_info(password=password)
        if not wifi_info: wifi_info = {'auth': 'WPA2', 'bssid': '00:11:22:33:44:55', 'ssid': 'Test_WiFi'}
        self.ssid_label.setText(f"현재 연결된 네트워크: {wifi_info.get('ssid', 'N/A')}")
        score, items = analyze_security(wifi_info, platform.system())
        location = system_info.get_location()
        add_record(wifi_info.get('ssid', 'N/A'), wifi_info.get('bssid', 'N/A'), score, location['lat'], location['lon'])
        self.main_window.show_result_view(score, items)

    def refresh_ssid(self): pass

class MapView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.page_loaded = False
        layout = QVBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        self.web_view = QWebEngineView()
        map_path = resource_path('gui/map.html')
        self.web_view.setUrl(QUrl.fromLocalFile(map_path))
        self.web_view.loadFinished.connect(self.on_load_finished)
        layout.addWidget(self.web_view)

    def on_load_finished(self, success):
        if success: self.page_loaded = True; self.load_map_markers()

    def load_map_markers(self):
        if not self.page_loaded: return
        self.web_view.page().runJavaScript("clearMarkers();")
        records = get_all_records()
        if records:
            for record in records:
                js_code = f"addMarker({record['latitude']}, {record['longitude']}, '<b>SSID:</b> {record['ssid']}<br><b>점수:</b> {record['score']}');"
                self.web_view.page().runJavaScript(js_code)
            js_code = f"setView({records[-1]['latitude']}, {records[-1]['longitude']}, 13);"
            self.web_view.page().runJavaScript(js_code)
        else: self.web_view.page().runJavaScript("setView(37.5665, 126.9780, 10);")

class App(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("WiFi Safety Checker"); self.setFixedSize(800, 600)
        central_widget = QWidget(); self.setCentralWidget(central_widget); central_widget.setStyleSheet(f"background-color: {BG_COLOR};")
        main_layout = QVBoxLayout(central_widget); self.stacked_widget = QStackedWidget()
        self._create_header(); main_layout.addWidget(self.header); main_layout.addWidget(self.stacked_widget)
        self.start_view, self.result_view, self.map_view = StartView(self), ResultView(self), MapView(self)
        self.stacked_widget.addWidget(self.start_view); self.stacked_widget.addWidget(self.result_view); self.stacked_widget.addWidget(self.map_view)
        self.select_tab("check")

    def _create_header(self):
        self.header = QFrame(); self.header.setFixedHeight(50)
        header_layout = QHBoxLayout(self.header); header_layout.setContentsMargins(20, 0, 20, 0); header_layout.setSpacing(30)
        title = QLabel("WiFi Safety Checker"); title.setFont(QFont(FONT_FAMILY, 22, QFont.Weight.Bold)); title.setStyleSheet("color: #000000;")
        header_layout.addWidget(title); header_layout.addStretch(1)
        self.tabs = {}
        for name, text in [("check", "보안점검"), ("map", "점검 기록 지도")]:
            tab = QPushButton(text); tab.setFont(QFont(FONT_FAMILY, 16)); tab.setCheckable(True); tab.setFlat(True)
            tab.setStyleSheet("QPushButton { border: none; border-radius: 8px; padding: 5px; color: #000000; } QPushButton:checked { font-weight: bold; }")
            tab.clicked.connect(lambda _, n=name: self.select_tab(n)); header_layout.addWidget(tab); self.tabs[name] = tab
    
    def select_tab(self, name):
        for tab_name, tab_button in self.tabs.items(): tab_button.setChecked(tab_name == name)
        if name == "check": self.stacked_widget.setCurrentWidget(self.start_view)
        else: self.stacked_widget.setCurrentWidget(self.map_view); self.map_view.load_map_markers()

    def show_result_view(self, score, items):
        self.result_view.update_ui(score, items)
        self.stacked_widget.setCurrentWidget(self.result_view)
