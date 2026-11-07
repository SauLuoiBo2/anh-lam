# Phân tích bộ data test MSB TM V1.28

Thư mục này chứa kết quả phân tích bộ script nạp dữ liệu test cho hệ thống giám sát giao dịch (AML/TM, Oracle OFSAA) của MSB.

**Đầu vào:**
- `input/Insert DATA/*.sql`: 22 script nạp 21 bảng STG, tổng khoảng 137 nghìn dòng.
- `input/Phu luc 1_MSB_TM_DataMapping_STG_Batch_V1.0.xlsx`: mapping cột cho từng bảng STG.

## Danh sách tài liệu

| File | Nội dung | Bước |
|---|---|---|
| [01_PhanTich_CauTruc_DuLieu.md](01_PhanTich_CauTruc_DuLieu.md) | Các bảng, khóa chính, quan hệ giữa các bảng, quy ước mã, giá trị cố định | B1 |
| [02_TongHop_Data_TheoTH.md](02_TongHop_Data_TheoTH.md) | Tổng hợp dữ liệu theo 14 kịch bản (TH) và 3 bộ TC / A / WL | B2 |
| [03_HuongDan_Gen_Data.md](03_HuongDan_Gen_Data.md) | Quy tắc sinh data mới cho bước 3: các bảng cần insert, mã tiếp theo, checklist | B3 (chuẩn bị) |
| [04_VanDe_CanLamRo.md](04_VanDe_CanLamRo.md) | Điểm bất thường phát hiện trong data và câu hỏi cần xác nhận | — |
| [B1_B2_TongHop_Data_TheoTH.xlsx](B1_B2_TongHop_Data_TheoTH.xlsx) | Số liệu chi tiết: cấu trúc bảng, profile từng cột, tổng hợp theo TH, chi tiết 471 tài khoản | B1 + B2 |

## Tóm tắt

- Dữ liệu chia thành 4 lớp: **Danh mục** (01–05), **Khách hàng** (06–15), **Tài khoản** (16–18) và **Giao dịch** (19–21). File 30 là bản cập nhật cờ ví điện tử ở giai đoạn 2.
- Có **14 kịch bản (TH01–TH14)**. Mỗi kịch bản có 3 bộ dữ liệu: **TC** (bộ gốc), **A** (20 KH/TH) và **WL** (1–2 KH/TH). Ngoài ra có nhóm **BG** (giao dịch nền, làm nhiễu) và **WLT** (test watchlist).
- Mã KH và mã TK chứa luôn số TH. Ví dụ `TC05_083`, `CIF_A05_001` và `ACC_WL05_001` đều thuộc TH05.
- Liên kết khóa ngoại giữa các bảng khớp 100%.
- **Lưu ý:** ý nghĩa các TH là **suy luận từ dữ liệu**, vì không có tài liệu nào mô tả rule. Cần đối chiếu với tài liệu kịch bản AML chính thức (xem file 04).
