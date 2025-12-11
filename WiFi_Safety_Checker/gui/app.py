# gui/app.py
import customtkinter as ctk
import platform
from tkintermapview import TkinterMapView
from utils import system_info
from security import analyzer
from data import database

# customtkinter 테마 설정
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WiFi Safety Checker")
        self.geometry("800x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 탭 뷰 생성
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tab_view.add("🔍 보안 점검")
        self.tab_view.add("🗺️ 점검 기록 지도")

        # 각 탭의 컨텐츠 설정
        self.setup_home_tab()
        self.setup_map_tab()

    def setup_home_tab(self):
        home_tab = self.tab_view.tab("🔍 보안 점검")
        home_tab.grid_columnconfigure(0, weight=1)

        # 점검 시작 버튼
        self.check_button = ctk.CTkButton(home_tab, text="현재 WiFi 보안 점검 시작", command=self.run_check)
        self.check_button.grid(row=0, column=0, padx=20, pady=20)

        # 점수 표시 라벨
        self.score_label = ctk.CTkLabel(home_tab, text="점수를 기다리는 중...", font=ctk.CTkFont(size=40, weight="bold"))
        self.score_label.grid(row=1, column=0, padx=20, pady=10)

        # 보안 피드백 스크롤 프레임
        self.feedback_frame = ctk.CTkScrollableFrame(home_tab, label_text="분석 결과")
        self.feedback_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        home_tab.grid_rowconfigure(2, weight=1)

    def setup_map_tab(self):
        map_tab = self.tab_view.tab("🗺️ 점검 기록 지도")
        map_tab.grid_columnconfigure(0, weight=1)
        map_tab.grid_rowconfigure(0, weight=1)

        self.map_widget = TkinterMapView(map_tab, width=700, height=500, corner_radius=0)
        self.map_widget.grid(row=0, column=0, sticky="nsew")
        self.map_widget.set_position(37.5665, 126.9780) # 초기 위치: 서울 시청
        self.map_widget.set_zoom(12)
        
        # 지도 로딩 버튼 추가
        self.load_map_button = ctk.CTkButton(map_tab, text="기록 불러오기", command=self.load_map_markers)
        self.load_map_button.place(relx=0.02, rely=0.02, anchor="nw")


    def run_check(self):
        self.score_label.configure(text="점검 중...", text_color="white")
        self.check_button.configure(state="disabled")

        for widget in self.feedback_frame.winfo_children():
            widget.destroy()

        password = None
        if platform.system() == "Darwin":
            dialog = PasswordDialog(self)
            self.wait_window(dialog) # 다이얼로그가 닫힐 때까지 기다림
            password = dialog.password

            if password is None: # 사용자가 창을 그냥 닫은 경우
                self.score_label.configure(text="점검 취소", text_color="gray")
                self.check_button.configure(state="normal")
                return

        wifi_info = system_info.get_wifi_info(password=password)
        if not wifi_info:
            self.score_label.configure(text="연결 정보 없음", text_color="orange")
            
            # 이전 메시지 삭제
            for widget in self.feedback_frame.winfo_children():
                widget.destroy()

            ctk.CTkLabel(self.feedback_frame, text="WiFi에 연결되어 있지 않거나 정보를 가져올 수 없습니다.").pack(pady=5, padx=5)
            
            # macOS 사용자를 위한 추가 안내
            if platform.system() == "Darwin":
                mac_msg = (
                    "macOS에서는 Wi-Fi 정보를 얻기 위해 sudo 암호가 필요합니다.\n"
                    "암호를 정확히 입력했는지 확인하고 다시 시도해주세요.\n\n"
                    "만약 Wi-Fi에 연결되어 있는데도 이 메시지가 계속 표시된다면,\n"
                    "시스템 보안 설정으로 인해 정보 수집이 차단되었을 수 있습니다."
                )
                ctk.CTkLabel(self.feedback_frame, text=mac_msg, justify="left").pack(pady=10, padx=5, anchor="w")

            self.check_button.configure(state="normal")
            return
            
        location = system_info.get_location()

        # 상세 분석 결과 리스트를 받도록 수정
        score, analysis_items = analyzer.analyze_security(wifi_info, platform.system())

        color = "green"
        if score < 50: color = "red"
        elif score < 80: color = "orange"
        self.score_label.configure(text=f"{score}점", text_color=color)

        # 상세 분석 결과를 표 형태로 표시
        for item in analysis_items:
            item_frame = ctk.CTkFrame(self.feedback_frame)
            item_frame.pack(fill="x", padx=5, pady=3)
            item_frame.grid_columnconfigure(0, weight=2)
            item_frame.grid_columnconfigure(1, weight=3)
            item_frame.grid_columnconfigure(2, weight=1)

            ctk.CTkLabel(item_frame, text=item['check'], anchor="w").grid(row=0, column=0, sticky="w", padx=10)
            ctk.CTkLabel(item_frame, text=item['status'], anchor="w").grid(row=0, column=1, sticky="w", padx=10)

            score_change = item['score_change']
            color = "#66DE93" # Green
            if score_change < 0:
                color = "#F4A9A8" # Red/Orange
            
            score_text = f"{score_change}"
            if score_change >= 0:
                score_text = f"+{score_change}"

            ctk.CTkLabel(item_frame, text=score_text, text_color=color, anchor="e", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="e", padx=10)

        database.add_record(wifi_info['ssid'], wifi_info['bssid'], score, location['lat'], location['lon'])
        
        self.load_map_markers()
        self.check_button.configure(state="normal")

    def load_map_markers(self):
        self.map_widget.delete_all_marker()
        records = database.get_all_records()
        
        for record in records:
            score = record['score']
            color = "green"
            if score < 50: color = "red"
            elif score < 80: color = "yellow"

            text = f"SSID: {record['ssid']}\nScore: {score}\nDate: {record['checked_at'][:10]}"
            self.map_widget.set_marker(
                record['latitude'], 
                record['longitude'], 
                text=text,
                marker_color_circle=color,
                marker_color_outside="gray40"
            )
        
        # 가장 최근 기록으로 지도 위치 이동
        if records:
            latest_record = records[0]
            self.map_widget.set_position(latest_record['latitude'], latest_record['longitude'])

class PasswordDialog(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Sudo Password")
        self.geometry("300x150")
        self.password = None

        # 창을 항상 위에 표시
        self.attributes("-topmost", True)

        self.label = ctk.CTkLabel(self, text="macOS 관리자 암호를 입력하세요:")
        self.label.pack(padx=20, pady=10)

        self.entry = ctk.CTkEntry(self, show="*")
        self.entry.pack(padx=20, pady=5, fill="x")
        self.entry.focus() # 바로 입력할 수 있도록 포커스 설정

        self.ok_button = ctk.CTkButton(self, text="확인", command=self.on_ok)
        self.ok_button.pack(pady=10)

        # Enter 키를 눌렀을 때도 on_ok 함수가 호출되도록 바인딩
        self.entry.bind("<Return>", self.on_ok)


    def on_ok(self, event=None):
        self.password = self.entry.get()
        self.destroy()