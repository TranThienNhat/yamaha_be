from library.db_connection import get_db
import pyodbc

class BannerRepository:
    
    def lay_tat_ca(self):
        """Lấy tất cả banner."""
        db = get_db()
        if db is None: return []
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, tieu_de, hinh_anh, link, vi_tri, thu_tu, kich_hoat, ngay_tao 
                FROM Banner 
                ORDER BY thu_tu ASC, ngay_tao DESC
            """)
            ket_qua = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            banners = []
            for row in ket_qua:
                banner = dict(zip(columns, row))
                # Map kich_hoat -> trang_thai cho frontend
                banner['trang_thai'] = banner.pop('kich_hoat', False)
                if banner.get('hinh_anh'):
                    banner['hinh_anh_url'] = f"http://localhost:5000/uploads/{banner['hinh_anh']}"
                banners.append(banner)
            return banners
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy banner: {e}")
            return []
        finally:
            cursor.close()
    
    def lay_theo_vi_tri(self, vi_tri):
        """Lấy banner theo vị trí."""
        db = get_db()
        if db is None: return []
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, tieu_de, hinh_anh, link, vi_tri, thu_tu, kich_hoat
                FROM Banner 
                WHERE vi_tri = ? AND kich_hoat = 1
                ORDER BY thu_tu ASC
            """, (vi_tri,))
            ket_qua = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            banners = []
            for row in ket_qua:
                banner = dict(zip(columns, row))
                # Map kich_hoat -> trang_thai cho frontend
                banner['trang_thai'] = banner.pop('kich_hoat', False)
                if banner.get('hinh_anh'):
                    banner['hinh_anh_url'] = f"http://localhost:5000/uploads/{banner['hinh_anh']}"
                banners.append(banner)
            return banners
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy banner: {e}")
            return []
        finally:
            cursor.close()
    
    def them(self, tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai=True):
        """Thêm banner mới."""
        db = get_db()
        if db is None: return None
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO Banner (tieu_de, hinh_anh, link, vi_tri, thu_tu, kich_hoat)
                OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)
            """, (tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai))
            new_id = cursor.fetchone()[0]
            db.commit()
            return new_id
        except pyodbc.Error as e:
            db.rollback()
            print(f"Lỗi khi thêm banner: {e}")
            return None
        finally:
            cursor.close()
    
    def sua(self, id, tieu_de, hinh_anh, link, vi_tri, thu_tu, kich_hoat):
        """Cập nhật banner."""
        db = get_db()
        if db is None: return False
        
        try:
            cursor = db.cursor()
            if hinh_anh:
                cursor.execute("""
                    UPDATE Banner 
                    SET tieu_de = ?, hinh_anh = ?, link = ?, vi_tri = ?, thu_tu = ?, kich_hoat = ?
                    WHERE id = ?
                """, (tieu_de, hinh_anh, link, vi_tri, thu_tu, kich_hoat, id))
            else:
                cursor.execute("""
                    UPDATE Banner 
                    SET tieu_de = ?, link = ?, vi_tri = ?, thu_tu = ?, kich_hoat = ?
                    WHERE id = ?
                """, (tieu_de, link, vi_tri, thu_tu, kich_hoat, id))
            db.commit()
            return cursor.rowcount > 0
        except pyodbc.Error as e:
            db.rollback()
            print(f"Lỗi khi sửa banner: {e}")
            return False
        finally:
            cursor.close()
    
    def cap_nhat_trang_thai(self, id, trang_thai):
        """Cập nhật trạng thái banner."""
        db = get_db()
        if db is None: return False
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE Banner 
                SET kich_hoat = ?
                WHERE id = ?
            """, (trang_thai, id))
            db.commit()
            return cursor.rowcount > 0
        except pyodbc.Error as e:
            db.rollback()
            print(f"Lỗi khi cập nhật trạng thái banner: {e}")
            return False
        finally:
            cursor.close()
    
    def lay_theo_id(self, id):
        """Lấy banner theo ID."""
        db = get_db()
        if db is None: return None
        
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT id, tieu_de, hinh_anh, link, vi_tri, thu_tu, kich_hoat, ngay_tao 
                FROM Banner 
                WHERE id = ?
            """, (id,))
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                banner = dict(zip(columns, row))
                # Map kich_hoat -> trang_thai cho frontend
                banner['trang_thai'] = banner.pop('kich_hoat', False)
                if banner.get('hinh_anh'):
                    banner['hinh_anh_url'] = f"http://localhost:5000/uploads/{banner['hinh_anh']}"
                return banner
            return None
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy banner: {e}")
            return None
        finally:
            cursor.close()
    
    def xoa(self, id):
        """Xóa banner."""
        db = get_db()
        if db is None: return False
        
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM Banner WHERE id = ?", (id,))
            db.commit()
            return cursor.rowcount > 0
        except pyodbc.Error as e:
            db.rollback()
            print(f"Lỗi khi xóa banner: {e}")
            return False
        finally:
            cursor.close()
