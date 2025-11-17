from flask import Blueprint, request, jsonify
from library.donhang.don_hang_access import DonHangRepository

# Tạo blueprint cho đơn hàng
don_hang = Blueprint("don_hang", __name__)
dh_repo = DonHangRepository()

# Lấy tất cả đơn hàng
@don_hang.route("/donhang", methods=["GET"])
def lay_tat_ca():
    """Lấy danh sách tất cả đơn hàng."""
    ds_don_hang = dh_repo.lay_tat_ca()
    
    if ds_don_hang is None:
        return jsonify({"error": "Không thể lấy danh sách đơn hàng"}), 500
    
    return jsonify(ds_don_hang), 200

# Lấy đơn hàng theo ID
@don_hang.route("/donhang/<int:ma_don_hang>", methods=["GET"])
def lay_theo_id(ma_don_hang):
    """Lấy chi tiết đơn hàng theo ID."""
    don_hang = dh_repo.lay_theo_id(ma_don_hang)
    
    if don_hang is None:
        return jsonify({"error": "Không tìm thấy đơn hàng"}), 404
    
    return jsonify(don_hang), 200

# Lấy đơn hàng theo người dùng
@don_hang.route("/donhang/nguoidung/<int:ma_nguoi_dung>", methods=["GET"])
def lay_theo_nguoi_dung(ma_nguoi_dung):
    """Lấy danh sách đơn hàng của người dùng."""
    ds_don_hang = dh_repo.lay_theo_nguoi_dung(ma_nguoi_dung)
    
    if ds_don_hang is None:
        return jsonify({"error": "Không thể lấy đơn hàng"}), 500
    
    return jsonify(ds_don_hang), 200

# Tạo đơn hàng mới
@don_hang.route("/donhang", methods=["POST"])
def tao_don_hang():
    """Tạo đơn hàng mới."""
    data = request.get_json()
    
    ma_nguoi_dung = data.get("ma_nguoi_dung")
    ten_khach_hang = data.get("ten_khach_hang")
    so_dien_thoai = data.get("so_dien_thoai")
    dia_chi = data.get("dia_chi")
    chi_tiet_san_pham = data.get("chi_tiet_san_pham", [])
    
    # Validate dữ liệu
    if not ten_khach_hang or not so_dien_thoai or not dia_chi:
        return jsonify({"error": "Thiếu thông tin khách hàng"}), 400
    
    if not chi_tiet_san_pham:
        return jsonify({"error": "Đơn hàng phải có ít nhất 1 sản phẩm"}), 400
    
    ma_don_hang = dh_repo.tao_don_hang(
        ma_nguoi_dung, 
        ten_khach_hang, 
        so_dien_thoai, 
        dia_chi, 
        chi_tiet_san_pham
    )
    
    if ma_don_hang:
        return jsonify({
            "message": "Tạo đơn hàng thành công",
            "ma_don_hang": ma_don_hang
        }), 201
    else:
        return jsonify({"error": "Không thể tạo đơn hàng"}), 500

# Cập nhật trạng thái đơn hàng
@don_hang.route("/donhang/<int:ma_don_hang>/trangthai", methods=["PUT"])
def cap_nhat_trang_thai(ma_don_hang):
    """Cập nhật trạng thái đơn hàng."""
    data = request.get_json()
    trang_thai = data.get("trang_thai")
    
    if not trang_thai:
        return jsonify({"error": "Thiếu trạng thái"}), 400
    
    if dh_repo.cap_nhat_trang_thai(ma_don_hang, trang_thai):
        return jsonify({"message": "Cập nhật trạng thái thành công"}), 200
    else:
        return jsonify({"error": "Không thể cập nhật trạng thái"}), 404

# Xóa đơn hàng
@don_hang.route("/donhang/<int:ma_don_hang>", methods=["DELETE"])
def xoa_don_hang(ma_don_hang):
    """Xóa đơn hàng."""
    if dh_repo.xoa_don_hang(ma_don_hang):
        return jsonify({"message": "Xóa đơn hàng thành công"}), 200
    else:
        return jsonify({"error": "Không thể xóa đơn hàng"}), 404
