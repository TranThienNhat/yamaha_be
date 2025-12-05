from library.db_connection import get_db
from library.config import get_image_url
import pyodbc

class BannerRepository:
    def lay_tat_ca(self):
        """Lấy tất cả banner."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai 
            FROM banner 
            ORDER BY vi_tri, thu_tu
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": row.id,
            "tieu_de": row.tieu_de,
            "hinh_anh": get_image_url(row.hinh_anh),
            "link": row.link,
            "vi_tri": row.vi_tri,
            "thu_tu": row.thu_tu,
            "trang_thai": row.trang_thai
        } for row in rows]
    
    def lay_theo_vi_tri(self, vi_tri):
        """Lấy banner theo vị trí (chỉ banner active)."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai 
            FROM banner 
            WHERE vi_tri = ? AND trang_thai = 1
            ORDER BY thu_tu
        """, (vi_tri,))
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            "id": row.id,
            "tieu_de": row.tieu_de,
            "hinh_anh": get_image_url(row.hinh_anh),
            "link": row.link,
            "vi_tri": row.vi_tri,
            "thu_tu": row.thu_tu,
            "trang_thai": row.trang_thai
        } for row in rows]
    
    def lay_theo_id(self, id):
        """Lấy chi tiết banner theo ID."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai 
            FROM banner 
            WHERE id = ?
        """, (id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row.id,
                "tieu_de": row.tieu_de,
                "hinh_anh": get_image_url(row.hinh_anh),
                "link": row.link,
                "vi_tri": row.vi_tri,
                "thu_tu": row.thu_tu,
                "trang_thai": row.trang_thai
            }
        return None
    
    def them(self, tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai):
        """Thêm banner mới."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO banner (tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai))
            conn.commit()
            cursor.execute("SELECT @@IDENTITY")
            new_id = cursor.fetchone()[0]
            conn.close()
            return new_id
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def sua(self, id, tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai):
        """Cập nhật banner."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            if hinh_anh:
                cursor.execute("""
                    UPDATE banner 
                    SET tieu_de = ?, hinh_anh = ?, link = ?, vi_tri = ?, thu_tu = ?, trang_thai = ?
                    WHERE id = ?
                """, (tieu_de, hinh_anh, link, vi_tri, thu_tu, trang_thai, id))
            else:
                cursor.execute("""
                    UPDATE banner 
                    SET tieu_de = ?, link = ?, vi_tri = ?, thu_tu = ?, trang_thai = ?
                    WHERE id = ?
                """, (tieu_de, link, vi_tri, thu_tu, trang_thai, id))
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return affected > 0
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def cap_nhat_trang_thai(self, id, trang_thai):
        """Cập nhật trạng thái banner."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE banner 
                SET trang_thai = ?
                WHERE id = ?
            """, (trang_thai, id))
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return affected > 0
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    def xoa(self, id):
        """Xóa banner."""
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM banner WHERE id = ?", (id,))
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return affected > 0
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e