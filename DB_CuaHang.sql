-- =============================================
-- DATABASE: YamahaDB - Yamaha E-Commerce Store
-- Version: 3.0 (Final)
-- Last Updated: November 2024
-- =============================================

-- 1. Tạo Database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'YamahaDB')
BEGIN
    CREATE DATABASE YamahaDB;
    PRINT N'✅ Database YamahaDB đã được tạo';
END
ELSE
BEGIN
    PRINT N'⚠️ Database YamahaDB đã tồn tại';
END
GO

-- 2. Sử dụng Database
USE YamahaDB;
GO

-- =============================================
-- 3. Tạo các bảng
-- =============================================

-- Bảng Người Dùng
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'NguoiDung')
BEGIN
    CREATE TABLE NguoiDung (
        id INT PRIMARY KEY IDENTITY(1,1),
        ten_dang_nhap VARCHAR(50) NOT NULL UNIQUE,
        mat_khau VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE,
        ho_ten NVARCHAR(100),
        sdt VARCHAR(15),
        vai_tro VARCHAR(20) NOT NULL DEFAULT 'khach_hang',
        ngay_tao DATETIME DEFAULT GETDATE()
    );
    PRINT N'✅ Bảng NguoiDung đã được tạo';
END
GO

-- Bảng Danh Mục
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'DanhMuc')
BEGIN
    CREATE TABLE DanhMuc (
        id INT PRIMARY KEY IDENTITY(1,1),
        ten_danh_muc NVARCHAR(100) NOT NULL UNIQUE,
        ngay_tao DATETIME DEFAULT GETDATE()
    );
    PRINT N'✅ Bảng DanhMuc đã được tạo';
END
GO

-- Bảng Sản Phẩm
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SanPham')
BEGIN
    CREATE TABLE SanPham (
        id INT PRIMARY KEY IDENTITY(1,1),
        ten_san_pham NVARCHAR(255) NOT NULL,
        gia DECIMAL(18, 2) NOT NULL,
        mo_ta NVARCHAR(MAX),
        thong_so_ky_thuat NVARCHAR(MAX),
        hinh_anh VARCHAR(255),
        noi_bat BIT DEFAULT 0,
        da_xoa BIT DEFAULT 0,
        so_luong INT NOT NULL DEFAULT 0,
        an BIT DEFAULT 0,
        ngay_tao DATETIME DEFAULT GETDATE()
    );
    PRINT N'✅ Bảng SanPham đã được tạo';
END
ELSE
BEGIN
    -- Thêm cột da_xoa nếu bảng đã tồn tại nhưng chưa có cột này
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('SanPham') AND name = 'da_xoa')
    BEGIN
        ALTER TABLE SanPham ADD da_xoa BIT DEFAULT 0;
        UPDATE SanPham SET da_xoa = 0 WHERE da_xoa IS NULL;
        PRINT N'✅ Đã thêm cột da_xoa vào bảng SanPham';
    END
    
    -- Thêm cột so_luong nếu chưa có
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('SanPham') AND name = 'so_luong')
    BEGIN
        ALTER TABLE SanPham ADD so_luong INT NOT NULL DEFAULT 0;
        PRINT N'✅ Đã thêm cột so_luong vào bảng SanPham';
    END
    
    -- Thêm cột an nếu chưa có
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('SanPham') AND name = 'an')
    BEGIN
        ALTER TABLE SanPham ADD an BIT DEFAULT 0;
        UPDATE SanPham SET an = 0 WHERE an IS NULL;
        PRINT N'✅ Đã thêm cột an vào bảng SanPham';
    END
END
GO

-- Bảng Hình Ảnh Sản Phẩm (Nhiều ảnh cho 1 sản phẩm)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'SanPham_HinhAnh')
BEGIN
    CREATE TABLE SanPham_HinhAnh (
        id INT PRIMARY KEY IDENTITY(1,1),
        san_pham_id INT NOT NULL,
        hinh_anh VARCHAR(255) NOT NULL,
        thu_tu INT DEFAULT 0,
        ngay_tao DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (san_pham_id) REFERENCES SanPham(id) ON DELETE CASCADE
    );
    PRINT N'✅ Bảng SanPham_HinhAnh đã được tạo';
END
GO

-- Bảng nối Nhiều-Nhiều giữa Danh Mục và Sản Phẩm
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Danhmuc_Sanpham')
BEGIN
    CREATE TABLE Danhmuc_Sanpham (
        san_pham_id INT NOT NULL,
        danh_muc_id INT NOT NULL,
        PRIMARY KEY (san_pham_id, danh_muc_id),
        FOREIGN KEY (san_pham_id) REFERENCES SanPham(id) ON DELETE CASCADE,
        FOREIGN KEY (danh_muc_id) REFERENCES DanhMuc(id) ON DELETE CASCADE
    );
    PRINT N'✅ Bảng Danhmuc_Sanpham đã được tạo';
END
GO

-- Bảng Giỏ Hàng
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'GioHang')
BEGIN
    CREATE TABLE GioHang (
        id INT PRIMARY KEY IDENTITY(1,1),
        ma_nguoi_dung INT NOT NULL UNIQUE,
        ngay_tao DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (ma_nguoi_dung) REFERENCES NguoiDung(id) ON DELETE CASCADE
    );
    PRINT N'✅ Bảng GioHang đã được tạo';
END
GO

-- Bảng Chi Tiết Giỏ Hàng
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ChiTietGioHang')
BEGIN
    CREATE TABLE ChiTietGioHang (
        id INT PRIMARY KEY IDENTITY(1,1),
        ma_gio_hang INT NOT NULL,
        ma_san_pham INT NOT NULL,
        so_luong INT NOT NULL DEFAULT 1,
        ngay_them DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (ma_gio_hang) REFERENCES GioHang(id) ON DELETE CASCADE,
        FOREIGN KEY (ma_san_pham) REFERENCES SanPham(id) ON DELETE CASCADE
    );
    PRINT N'✅ Bảng ChiTietGioHang đã được tạo';
END
GO

-- Bảng Đơn Hàng
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'DonHang')
BEGIN
    CREATE TABLE DonHang (
        id INT PRIMARY KEY IDENTITY(1,1),
        ma_nguoi_dung INT,
        ten_khach_hang NVARCHAR(100) NOT NULL,
        so_dien_thoai VARCHAR(15) NOT NULL,
        dia_chi NVARCHAR(255) NOT NULL,
        ngay_dat DATETIME DEFAULT GETDATE(),
        tong_gia DECIMAL(18, 2) NOT NULL,
        trang_thai NVARCHAR(50) DEFAULT N'Chờ xử lý',
        FOREIGN KEY (ma_nguoi_dung) REFERENCES NguoiDung(id)
    );
    PRINT N'✅ Bảng DonHang đã được tạo';
END
GO

-- Bảng Chi Tiết Đơn Hàng
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'ChiTietDonHang')
BEGIN
    CREATE TABLE ChiTietDonHang (
        id INT PRIMARY KEY IDENTITY(1,1),
        ma_don_hang INT NOT NULL,
        ma_san_pham INT NOT NULL,
        so_luong INT NOT NULL,
        don_gia DECIMAL(18, 2) NOT NULL,
        FOREIGN KEY (ma_don_hang) REFERENCES DonHang(id) ON DELETE CASCADE,
        FOREIGN KEY (ma_san_pham) REFERENCES SanPham(id) ON DELETE NO ACTION
    );
    PRINT N'✅ Bảng ChiTietDonHang đã được tạo';
END
GO

-- Bảng Tin Tức
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TinTuc')
BEGIN
    CREATE TABLE TinTuc (
        id INT PRIMARY KEY IDENTITY(1,1),
        tieu_de NVARCHAR(255) NOT NULL,
        noi_dung NVARCHAR(MAX),
        hinh_anh VARCHAR(255),
        noi_bat BIT DEFAULT 0,
        ngay_tao DATETIME DEFAULT GETDATE()
    );
    PRINT N'✅ Bảng TinTuc đã được tạo';
END
GO

-- Bảng Banner Quảng Cáo
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Banner')
BEGIN
    CREATE TABLE Banner (
        id INT PRIMARY KEY IDENTITY(1,1),
        tieu_de NVARCHAR(255),
        hinh_anh VARCHAR(255) NOT NULL,
        link VARCHAR(500),
        vi_tri INT NOT NULL,
        thu_tu INT DEFAULT 0,
        kich_hoat BIT DEFAULT 1,
        ngay_tao DATETIME DEFAULT GETDATE()
    );
    PRINT N'✅ Bảng Banner đã được tạo';
END
GO

-- =============================================
-- 4. Tạo Index để tăng hiệu suất
-- =============================================

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_SanPham_NoiBat')
    CREATE INDEX IX_SanPham_NoiBat ON SanPham(noi_bat);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_SanPham_DaXoa')
    CREATE INDEX IX_SanPham_DaXoa ON SanPham(da_xoa);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_SanPham_HinhAnh_SanPhamId')
    CREATE INDEX IX_SanPham_HinhAnh_SanPhamId ON SanPham_HinhAnh(san_pham_id, thu_tu);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_TinTuc_NoiBat')
    CREATE INDEX IX_TinTuc_NoiBat ON TinTuc(noi_bat);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Banner_ViTri')
    CREATE INDEX IX_Banner_ViTri ON Banner(vi_tri, kich_hoat, thu_tu);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_DonHang_TrangThai')
    CREATE INDEX IX_DonHang_TrangThai ON DonHang(trang_thai);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_DonHang_NgayDat')
    CREATE INDEX IX_DonHang_NgayDat ON DonHang(ngay_dat DESC);

PRINT N'✅ Indexes đã được tạo';
GO

-- =============================================
-- 6. Tạo Trigger để tự động cập nhật trường 'an' khi số lượng thay đổi
-- =============================================

-- Trigger cho INSERT và UPDATE
IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_SanPham_UpdateAn')
    DROP TRIGGER TR_SanPham_UpdateAn;
GO

CREATE TRIGGER TR_SanPham_UpdateAn
ON SanPham
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Cập nhật trường 'an' dựa trên số lượng
    UPDATE sp
    SET an = CASE 
        WHEN i.so_luong <= 0 THEN 1 
        ELSE 0 
    END
    FROM SanPham sp
    INNER JOIN inserted i ON sp.id = i.id;
END
GO

PRINT N'✅ Trigger TR_SanPham_UpdateAn đã được tạo';
GO
