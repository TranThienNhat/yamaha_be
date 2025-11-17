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
        ngay_tao DATETIME DEFAULT GETDATE()
    );
    PRINT N'✅ Bảng SanPham đã được tạo';
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
        FOREIGN KEY (ma_san_pham) REFERENCES SanPham(id)
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
-- 5. Thêm dữ liệu mẫu
-- =============================================

-- Thêm Admin mặc định
IF NOT EXISTS (SELECT * FROM NguoiDung WHERE ten_dang_nhap = 'admin')
BEGIN
    INSERT INTO NguoiDung (ten_dang_nhap, mat_khau, email, ho_ten, vai_tro) 
    VALUES ('admin', 'admin123', 'admin@yamaha.vn', N'Quản trị viên', 'admin');
    PRINT N'✅ Tài khoản admin đã được tạo';
END

-- Thêm User mẫu
IF NOT EXISTS (SELECT * FROM NguoiDung WHERE ten_dang_nhap = 'user')
BEGIN
    INSERT INTO NguoiDung (ten_dang_nhap, mat_khau, email, ho_ten, vai_tro) 
    VALUES ('user', 'user123', 'user@example.com', N'Nguyễn Văn A', 'khach_hang');
    PRINT N'✅ Tài khoản user mẫu đã được tạo';
END
GO

-- Thêm danh mục mẫu
IF NOT EXISTS (SELECT * FROM DanhMuc WHERE ten_danh_muc = N'Xe côn tay')
BEGIN
    INSERT INTO DanhMuc (ten_danh_muc) VALUES 
    (N'Xe côn tay'),
    (N'Xe tay ga'),
    (N'Xe số'),
    (N'Phụ kiện');
    PRINT N'✅ Danh mục mẫu đã được tạo';
END
GO

-- Thêm sản phẩm mẫu
IF NOT EXISTS (SELECT * FROM SanPham WHERE ten_san_pham = N'Yamaha Exciter 155')
BEGIN
    INSERT INTO SanPham (ten_san_pham, gia, mo_ta, thong_so_ky_thuat, noi_bat) VALUES
    (N'Yamaha Exciter 155', 52990000, N'Xe côn tay thể thao hàng đầu Việt Nam', N'Động cơ: 155cc, Công suất: 15PS, Mô-men xoắn: 14.2Nm', 1),
    (N'Yamaha NVX 155', 52990000, N'Xe tay ga thể thao cao cấp', N'Động cơ: 155cc, Công suất: 15.4PS, Mô-men xoắn: 13.8Nm', 1),
    (N'Yamaha Sirius', 21990000, N'Xe số tiết kiệm nhiên liệu', N'Động cơ: 110cc, Công suất: 7.8PS, Tiêu hao nhiên liệu: 1.5L/100km', 0),
    (N'Yamaha Grande', 45990000, N'Xe tay ga cao cấp sang trọng', N'Động cơ: 125cc, Công suất: 9.3PS, Hệ thống khởi động thông minh', 1),
    (N'Yamaha Janus', 32990000, N'Xe tay ga thời trang cho phái đẹp', N'Động cơ: 125cc, Công suất: 9.3PS, Thiết kế nhỏ gọn', 0);
    PRINT N'✅ Sản phẩm mẫu đã được tạo';
END
GO

-- Liên kết sản phẩm với danh mục
IF NOT EXISTS (SELECT * FROM Danhmuc_Sanpham WHERE san_pham_id = 1)
BEGIN
    INSERT INTO Danhmuc_Sanpham (san_pham_id, danh_muc_id) VALUES
    (1, 1), -- Exciter - Xe côn tay
    (2, 2), -- NVX - Xe tay ga
    (3, 3), -- Sirius - Xe số
    (4, 2), -- Grande - Xe tay ga
    (5, 2); -- Janus - Xe tay ga
    PRINT N'✅ Liên kết sản phẩm-danh mục đã được tạo';
END
GO

-- Thêm tin tức mẫu
IF NOT EXISTS (SELECT * FROM TinTuc WHERE tieu_de LIKE N'%Exciter 155%')
BEGIN
    INSERT INTO TinTuc (tieu_de, noi_dung, noi_bat) VALUES
    (N'Ra mắt Yamaha Exciter 155 VVA 2024', N'<h2>Yamaha Exciter 155 VVA 2024 - Đột phá mới</h2><p>Yamaha Motor Việt Nam chính thức giới thiệu Exciter 155 VVA phiên bản 2024 với nhiều cải tiến vượt trội về thiết kế và công nghệ.</p>', 1),
    (N'Khuyến mãi tháng 11 - Giảm giá sốc', N'<h2>Chương trình khuyến mãi lớn</h2><p>Giảm giá đến 5 triệu đồng cho các dòng xe tay ga. Tặng kèm phụ kiện chính hãng trị giá 2 triệu đồng.</p>', 1),
    (N'Hướng dẫn bảo dưỡng xe định kỳ', N'<h2>Bảo dưỡng xe Yamaha đúng cách</h2><p>Hướng dẫn chi tiết cách bảo dưỡng xe Yamaha để xe luôn hoạt động tốt nhất.</p>', 0);
    PRINT N'✅ Tin tức mẫu đã được tạo';
END
GO

-- =============================================
-- 6. Thông báo hoàn thành
-- =============================================

PRINT N'';
PRINT N'========================================';
PRINT N'✅ DATABASE YAMAHADB ĐÃ SẴN SÀNG!';
PRINT N'========================================';
PRINT N'';
PRINT N'📊 Các bảng đã tạo:';
PRINT N'  • NguoiDung (Quản lý tài khoản)';
PRINT N'  • DanhMuc (Danh mục sản phẩm)';
PRINT N'  • SanPham (Sản phẩm)';
PRINT N'  • SanPham_HinhAnh (Nhiều ảnh/sản phẩm)';
PRINT N'  • Danhmuc_Sanpham (Liên kết nhiều-nhiều)';
PRINT N'  • GioHang (Giỏ hàng)';
PRINT N'  • ChiTietGioHang (Chi tiết giỏ hàng)';
PRINT N'  • DonHang (Đơn hàng)';
PRINT N'  • ChiTietDonHang (Chi tiết đơn hàng)';
PRINT N'  • TinTuc (Tin tức & khuyến mãi)';
PRINT N'  • Banner (Banner quảng cáo)';
PRINT N'';
PRINT N'🔐 Tài khoản mặc định:';
PRINT N'  Admin:';
PRINT N'    Username: admin';
PRINT N'    Password: admin123';
PRINT N'  User:';
PRINT N'    Username: user';
PRINT N'    Password: user123';
PRINT N'';
PRINT N'✨ Tính năng:';
PRINT N'  • Quản lý sản phẩm với nhiều ảnh';
PRINT N'  • Danh mục nhiều-nhiều';
PRINT N'  • Giỏ hàng & đơn hàng';
PRINT N'  • Tin tức với HTML editor';
PRINT N'  • Banner quảng cáo đa vị trí';
PRINT N'  • Đánh dấu nổi bật';
PRINT N'  • Upload ảnh';
PRINT N'';
PRINT N'🚀 Bước tiếp theo:';
PRINT N'  1. Chạy backend: python app.py';
PRINT N'  2. Chạy frontend: cd yamaha_fe && npm run dev';
PRINT N'  3. Truy cập: http://localhost:3000';
PRINT N'========================================';
GO
