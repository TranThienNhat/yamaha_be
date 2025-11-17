# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

#Import các Blueprint(route) từ library
from library.sanpham.san_pham import san_pham
from library.danhmuc.danh_muc import danh_muc
from library.giohang.gio_hang import gio_hang
from library.donhang.don_hang import don_hang
from library.tintuc.tin_tuc import tin_tuc
from library.nguoidung.nguoi_dung import nguoi_dung
from library.upload.upload import upload_bp
from library.banner.banner import banner_bp

#Import hàm đóng DB
from library.db_connection import close_db
# 1. Tải các biến từ file .env vào môi trường hệ thống
load_dotenv() 

app = Flask(__name__, static_url_path="/uploads", static_folder="uploads")
# Cấu hình CORS để cho phép frontend truy cập
CORS(app, resources={r"/*": {"origins": "*"}})
# Đảm bảo kết nối DB luôn được đóng sau mỗi request
app.teardown_appcontext(close_db) 
# Đăng ký route cho file:
app.register_blueprint(san_pham)
app.register_blueprint(danh_muc)
app.register_blueprint(gio_hang)
app.register_blueprint(don_hang)
app.register_blueprint(tin_tuc)
app.register_blueprint(nguoi_dung)
app.register_blueprint(upload_bp)
app.register_blueprint(banner_bp)
if __name__ == '__main__':
    # Chạy ứng dụng. 
    # Mặc định Flask chạy trên http://127.0.0.1:5000
    app.run(debug=True)