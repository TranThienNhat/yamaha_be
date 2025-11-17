from flask import g
import pyodbc
import os

# --- Cấu hình Kết nối ---
# Đọc cấu hình từ biến môi trường
SERVER = os.environ.get('DB_SERVER', 'localhost')
DATABASE = os.environ.get('DB_DATABASE', 'YamahaShop')
DRIVER = '{ODBC Driver 17 for SQL Server}' # Đảm bảo đã cài driver này

# Thêm timeout settings để tránh lỗi timeout
CONNECTION_STRING = (
    f'DRIVER={DRIVER};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    f'Trusted_Connection=yes;'
    f'Connection Timeout=30;'
    f'Command Timeout=30;'
)
# --- Quản lý Kết nối ---

def get_db():
    """Tạo hoặc trả về kết nối DB đã tồn tại trong ngữ cảnh request (g)."""
    if 'db' not in g:
        try:
            g.db = pyodbc.connect(CONNECTION_STRING)
        except pyodbc.Error as ex:
            # Xử lý lỗi kết nối
            print(f"LỖI KẾT NỐI DB: {ex}")
            g.db = None
    return g.db

def close_db(e=None):
    """Đóng kết nối DB sau khi request hoàn tất."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- Hàm tiện ích cho kết quả truy vấn ---
def row_to_dict(cursor, row):
    """Chuyển đổi pyodbc.Row sang Dictionary."""
    columns = [column[0] for column in cursor.description]
    return dict(zip(columns, row))

def get_results(cursor):
    """Lấy tất cả kết quả và chuyển đổi sang List of Dicts."""
    results = []
    if cursor.description:
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
    return results