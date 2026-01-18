from flask import Blueprint, request, jsonify
from library.giohang.gio_hang_access import GioHangRepository

# Tạo blueprint cho giỏ hàng
gio_hang = Blueprint("gio_hang", __name__)
gh_repo = GioHangRepository()

# Lấy giỏ hàng của người dùng
@gio_hang.route("/giohang/<int:ma_nguoi_dung>", methods=["GET"])
def lay_gio_hang(ma_nguoi_dung):
    """Lấy giỏ hàng của người dùng."""
    gio_hang = gh_repo.lay_gio_hang_theo_nguoi_dung(ma_nguoi_dung)
    
    if gio_hang is None:
        return jsonify({"error": "Không thể lấy giỏ hàng"}), 500
    
    return jsonify(gio_hang), 200

# Thêm sản phẩm vào giỏ hàng
@gio_hang.route("/giohang/<int:ma_nguoi_dung>/them", methods=["POST"])
def them_san_pham(ma_nguoi_dung):
    """Thêm sản phẩm vào giỏ hàng."""
    data = request.get_json()
    ma_san_pham = data.get("ma_san_pham")
    so_luong = data.get("so_luong", 1)
    
    if not ma_san_pham:
        return jsonify({"error": "Thiếu mã sản phẩm"}), 400
    
    try:
        if gh_repo.them_san_pham_vao_gio(ma_nguoi_dung, ma_san_pham, so_luong):
            return jsonify({"message": "Thêm sản phẩm vào giỏ hàng thành công"}), 201
        else:
            return jsonify({"error": "Không thể thêm sản phẩm vào giỏ hàng"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Cập nhật số lượng sản phẩm trong giỏ
@gio_hang.route("/giohang/chitiet/<int:ma_chi_tiet>", methods=["PUT"])
def cap_nhat_so_luong(ma_chi_tiet):
    """Cập nhật số lượng sản phẩm trong giỏ hàng."""
    data = request.get_json()
    so_luong = data.get("so_luong")
    
    if so_luong is None:
        return jsonify({"error": "Thiếu số lượng"}), 400
    
    if gh_repo.cap_nhat_so_luong(ma_chi_tiet, so_luong):
        return jsonify({"message": "Cập nhật số lượng thành công"}), 200
    else:
        return jsonify({"error": "Không thể cập nhật số lượng"}), 404

# Xóa sản phẩm khỏi giỏ hàng
@gio_hang.route("/giohang/chitiet/<int:ma_chi_tiet>", methods=["DELETE"])
def xoa_san_pham(ma_chi_tiet):
    """Xóa sản phẩm khỏi giỏ hàng."""
    if gh_repo.xoa_san_pham_khoi_gio(ma_chi_tiet):
        return jsonify({"message": "Xóa sản phẩm khỏi giỏ hàng thành công"}), 200
    else:
        return jsonify({"error": "Không thể xóa sản phẩm"}), 404

# Xóa toàn bộ giỏ hàng
@gio_hang.route("/giohang/<int:ma_nguoi_dung>", methods=["DELETE"])
def xoa_gio_hang(ma_nguoi_dung):
    """Xóa toàn bộ giỏ hàng của người dùng."""
    if gh_repo.xoa_gio_hang(ma_nguoi_dung):
        return jsonify({"message": "Xóa giỏ hàng thành công"}), 200
    else:
        return jsonify({"error": "Không thể xóa giỏ hàng"}), 404
