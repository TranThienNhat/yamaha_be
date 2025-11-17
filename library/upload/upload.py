from flask import Blueprint, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Upload ảnh đơn
@upload_bp.route("/upload/image", methods=["POST"])
def upload_image():
    """Upload ảnh lên server và trả về URL."""
    if 'file' not in request.files:
        return jsonify({"error": "Không có file"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Không có file được chọn"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Định dạng file không hợp lệ. Chỉ chấp nhận: png, jpg, jpeg, gif, webp"}), 400
    
    try:
        # Tạo tên file unique với timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_filename = secure_filename(file.filename)
        name, ext = os.path.splitext(original_filename)
        filename = f"{name}_{timestamp}{ext}"
        
        # Tạo thư mục nếu chưa có
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Lưu file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Tạo URL
        file_url = url_for('san_pham.uploaded_file', filename=filename, _external=True)
        
        return jsonify({
            "message": "Upload thành công",
            "filename": filename,
            "url": file_url
        }), 200
        
    except Exception as e:
        print(f"Lỗi khi upload: {e}")
        return jsonify({"error": "Lỗi khi upload file"}), 500

# Upload nhiều ảnh
@upload_bp.route("/upload/images", methods=["POST"])
def upload_images():
    """Upload nhiều ảnh cùng lúc."""
    if 'files' not in request.files:
        return jsonify({"error": "Không có file"}), 400
    
    files = request.files.getlist('files')
    
    if not files or len(files) == 0:
        return jsonify({"error": "Không có file được chọn"}), 400
    
    uploaded_files = []
    errors = []
    
    for file in files:
        if file.filename == '':
            continue
            
        if not allowed_file(file.filename):
            errors.append(f"{file.filename}: Định dạng không hợp lệ")
            continue
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            original_filename = secure_filename(file.filename)
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{timestamp}{ext}"
            
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            file_url = url_for('san_pham.uploaded_file', filename=filename, _external=True)
            
            uploaded_files.append({
                "filename": filename,
                "url": file_url,
                "original_name": original_filename
            })
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
    
    return jsonify({
        "message": f"Upload thành công {len(uploaded_files)} file",
        "files": uploaded_files,
        "errors": errors if errors else None
    }), 200

# Lấy danh sách ảnh đã upload
@upload_bp.route("/upload/images", methods=["GET"])
def get_uploaded_images():
    """Lấy danh sách tất cả ảnh đã upload."""
    try:
        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({"images": []}), 200
        
        files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            if allowed_file(filename):
                file_url = url_for('san_pham.uploaded_file', filename=filename, _external=True)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file_stat = os.stat(filepath)
                
                files.append({
                    "filename": filename,
                    "url": file_url,
                    "size": file_stat.st_size,
                    "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                })
        
        # Sắp xếp theo thời gian tạo, mới nhất trước
        files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({"images": files}), 200
        
    except Exception as e:
        print(f"Lỗi khi lấy danh sách ảnh: {e}")
        return jsonify({"error": "Lỗi khi lấy danh sách ảnh"}), 500
