# main.py
from gui.app import App
from data.database import init_db

if __name__ == "__main__":
    # 프로그램 시작 시 데이터베이스 초기화
    init_db()
    
    # GUI 앱 실행
    app = App()
    app.mainloop()
