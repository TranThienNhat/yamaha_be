from flask import Blueprint, request, jsonify
from library.nguoidung.nguoi_dung_access import NguoiDungRepository

nguoi_dung = Blueprint("nguoi_dung", __name__)
nd_repo = NguoiDungRepository()

# Đăng ký
@nguoi_dung.route("/nguoidung/dangky", methods=["POST"])
def dang_ky():
    """Đăng ký người dùng mới."""
    data = request.get_json()
    
    ten_dang_nhap = data.get("ten_dang_nhap")
    mat_khau = data.get("mat_khau")
    email = data.get("email")
    ho_ten = data.get("ho_ten")
    sdt = data.get("sdt")
    vai_tro = data.get("vai_tro", "khach_hang")
    
    if not ten_dang_nhap or not mat_khau:
        return jsonify({"error": "Thiếu tên đăng nhập hoặc mật khẩu"}), 400
    
    ket_qua = nd_repo.dang_ky(ten_dang_nhap, mat_khau, email, ho_ten, sdt, vai_tro)
    
    if ket_qua is None:
        return jsonify({"error": "Không thể đăng ký"}), 500
    
    if "error" in ket_qua:
        return jsonify(ket_qua), 400
    
    return jsonify(ket_qua), 201

# Đăng nhập
@nguoi_dung.route("/nguoidung/dangnhap", methods=["POST"])
def dang_nhap():
    """Đăng nhập người dùng."""
    data = request.get_json()
    
    ten_dang_nhap = data.get("ten_dang_nhap")
    mat_khau = data.get("mat_khau")
    
    if not ten_dang_nhap or not mat_khau:
        return jsonify({"error": "Thiếu tên đăng nhập hoặc mật khẩu"}), 400
    
    ket_qua = nd_repo.dang_nhap(ten_dang_nhap, mat_khau)
    
    if ket_qua is None:
        return jsonify({"error": "Không thể đăng nhập"}), 500
    
    if "error" in ket_qua:
        return jsonify(ket_qua), 401
    
    return jsonify({
        "message": "Đăng nhập thành công",
        "nguoi_dung": ket_qua
    }), 200

# Lấy thông tin người dùng
@nguoi_dung.route("/nguoidung/<int:ma_nguoi_dung>", methods=["GET"])
def lay_thong_tin(ma_nguoi_dung):
    """Lấy thông tin người dùng theo ID."""
    nguoi_dung_info = nd_repo.lay_thong_tin(ma_nguoi_dung)
    
    if nguoi_dung_info is None:
        return jsonify({"error": "Không tìm thấy người dùng"}), 404
    
    return jsonify(nguoi_dung_info), 200

# Lấy danh sách tất cả người dùng
@nguoi_dung.route("/nguoidung", methods=["GET"])
def lay_tat_ca():
    """Lấy danh sách tất cả người dùng."""
    ds_nguoi_dung = nd_repo.lay_tat_ca()
    
    if ds_nguoi_dung is None:
        return jsonify({"error": "Không thể lấy danh sách người dùng"}), 500
    
    return jsonify(ds_nguoi_dung), 200

# Cập nhật thông tin người dùng
@nguoi_dung.route("/nguoidung/<int:ma_nguoi_dung>", methods=["PUT"])
def cap_nhat_thong_tin(ma_nguoi_dung):
    """Cập nhật thông tin người dùng."""
    data = request.get_json()
    
    email = data.get("email")
    ho_ten = data.get("ho_ten")
    sdt = data.get("sdt")
    
    if nd_repo.cap_nhat_thong_tin(ma_nguoi_dung, email, ho_ten, sdt):
        return jsonify({"message": "Cập nhật thông tin thành công"}), 200
    else:
        return jsonify({"error": "Không thể cập nhật thông tin"}), 404

# Đổi mật khẩu
@nguoi_dung.route("/nguoidung/<int:ma_nguoi_dung>/doimatkhau", methods=["PUT"])
def doi_mat_khau(ma_nguoi_dung):
    """Đổi mật khẩu người dùng."""
    data = request.get_json()
    
    mat_khau_cu = data.get("mat_khau_cu")
    mat_khau_moi = data.get("mat_khau_moi")
    
    if not mat_khau_cu or not mat_khau_moi:
        return jsonify({"error": "Thiếu mật khẩu cũ hoặc mật khẩu mới"}), 400
    
    ket_qua = nd_repo.doi_mat_khau(ma_nguoi_dung, mat_khau_cu, mat_khau_moi)
    
    if ket_qua is None:
        return jsonify({"error": "Không thể đổi mật khẩu"}), 500
    
    if "error" in ket_qua:
        return jsonify(ket_qua), 400
    
    return jsonify(ket_qua), 200

# Xóa người dùng
@nguoi_dung.route("/nguoidung/<int:ma_nguoi_dung>", methods=["DELETE"])
def xoa_nguoi_dung(ma_nguoi_dung):
    """Xóa người dùng."""
    if nd_repo.xoa_nguoi_dung(ma_nguoi_dung):
        return jsonify({"message": "Xóa người dùng thành công"}), 200
    else:
        return jsonify({"error": "Không thể xóa người dùng"}), 404
