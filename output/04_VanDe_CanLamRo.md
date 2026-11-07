# Vấn đề phát hiện và câu hỏi cần làm rõ

## A. Điểm bất thường trong data

| # | Vấn đề | Chi tiết | Ảnh hưởng / Đề xuất |
|---|---|---|---|
| A1 | **`N_TXN_AMOUNT_NCY` chứa số nguyên tệ, trong khi `V_TXN_ACY_CODE = 'VND'`** | 480 GD ngoại tệ. Ví dụ TXN0011291: `N_TXN_AMOUNT_NCY = 38.080,73` (USD) nhưng mã tiền tệ đi kèm là VND. Số VND đúng (1 tỷ) chỉ có ở `STG_TXN_ALT_CCY_VALUES.N_TXN_AMOUNT_LCY` | Nếu rule đọc số tiền từ cột NCY thì sẽ hiểu GD 1 tỷ thành khoảng 38 nghìn VND, và TH01, 10–13 có thể **không ra alert**. Cần xác nhận rule đọc cột nào |
| A2 | **TH03 và TH04 trùng khớp số liệu** | Cùng 120 GD, cùng min / TB / max, cùng khoảng ngày, ở cả 3 bộ TC / A / WL | Xác nhận 2 TH này khác nhau ở điểm nào (rule, ngưỡng, loại KH) |
| A3 | 304 GD không có dòng trong STG_FRONT_OFFICE_TXN_PARTY | Chủ yếu là GD nền BG (lãi, phí, ATM) | Có thể đúng theo thiết kế. Cần xác nhận OFSAA không loại các GD này |
| A4 | Mã KH người thân TH09 không theo quy ước | `CIF_A09_1001` – `CIF_A09_1012` (4 chữ số) | Không gây lỗi, chỉ cần lưu ý khi lọc theo mẫu mã |
| A5 | Cột `F_EWALLET_FLAG` chưa có trong DDL chuẩn | Script 30 ghi rõ chỉ chạy sau khi FIS thêm cột | Xác nhận DDL môi trường test đã có cột này chưa |
| A6 | Ba cờ vượt ngưỡng trong STG_PARTY_MSB_DETAILS đều = `N` | `F_INTL_REMIT / TRADE_FIN / DOM_PAYMENT_THRESHOLD_FLAG` | Mapping đang chờ MSB định nghĩa ngưỡng (Action Tracker AT-05) |
| A7 | `V_CITIZENSHIP_3/4/5` đều rỗng | — | Chưa có case KH nhiều quốc tịch (AT-05) |
| A8 | `STG_PARTY_MSB_LOGIN` có trong mapping nhưng **không có script data** | Phiên đăng nhập IB/MB, phục vụ AML-08 / 09 | Nếu cần test rule đăng nhập thì phải sinh thêm bảng này (AT-06) |
| A9 | `D_LAST_ACTIVITY_DATE` chỉ có 27/497 dòng CASA | Chỉ ở TK ngủ đông và một vài TK khác | Bình thường theo thiết kế TH06 |

## B. Câu hỏi về cách tổ chức bộ test

1. **Bộ A và bộ WL khác nhau thế nào?** Pattern GD trên từng TK giống hệt nhau. WL là whitelist (KH được loại trừ, kỳ vọng **không** ra alert) hay chỉ là bộ thu nhỏ?
2. **Kỳ vọng alert của bộ TC và bộ A** là gì? Cả hai đều là case dương, hay bộ A có cả case sát ngưỡng?
3. **Nhóm WLT** test rule nào: watchlist quốc gia (giống TH01) hay đối chiếu tên với danh sách cấm vận?
4. Có tài liệu **danh sách rule AML** (mã AML-xx, ngưỡng, khoảng thời gian quét) không, để đối chiếu với 14 TH?

## C. Mục còn mở trong file mapping (Action Tracker)

File Excel mapping có 14 mục cần MSB làm rõ, trong đó 7 mục ưu tiên Cao. Các mục liên quan trực tiếp tới data test:

| Mã | Nội dung |
|---|---|
| AT-01 | Quy tắc tách số điện thoại / email thành nhiều dòng, sinh V_PHONE_ID |
| AT-02 | Trường ngày dữ liệu cho FIC_MIS_DATE và dấu hiệu bản ghi mới / cập nhật (Daily delta) |
| AT-03 | Nguồn cho V_MANTAS_ACCT_HOLDR_TYPE (data test đang dùng CR / CI) |
| AT-04 | Nguồn cho V_MANTAS_TXN_ASSET_CLASS_CD (data test đang dùng FUNDS) |
| AT-05 | Cờ FDI, cờ vượt ngưỡng, quốc tịch 3–5 |
| AT-06 | Bảng STG_PARTY_MSB_LOGIN |
| AT-08 | Bảng điểm rủi ro quốc gia (N_COUNTRY_RISK_FACTOR) |
