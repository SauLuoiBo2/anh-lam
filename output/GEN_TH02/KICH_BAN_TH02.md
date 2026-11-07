# Data bổ sung TH02 – KH rủi ro cao, tiền vào – ra luân phiên

Bộ data này sinh theo **đúng khuôn của bộ TC02 trong V1.28**: cùng số GD, cùng lịch ngày, cùng cách chia tiền, cùng kênh và hệ thống thanh toán. Chỉ đổi KH, TK, số tiền và đối tác.

## 1. Danh sách case và kỳ vọng

| CIF | Số TK | Loại | KYC risk | Tên | Số GD | Tổng Có | Tổng Nợ | Tổng 2 chiều | **Kỳ vọng** |
|---|---|---|:-:|---|:-:|--:|--:|--:|:-:|
| TC02_161 | ACT02_161 | KHCN | **8** | TRINH VAN KHANH | 15 | 933.333.331 | 1.066.666.669 | 2,0 tỷ | **ALERT** |
| TC02_162 | ACT02_162 | KHCN | **7** | LUONG THI HOAI | 15 | 1.120.000.000 | 1.280.000.000 | 2,4 tỷ | **ALERT** |
| TC02_163 | ACT02_163 | KHTC | **8** | CONG TY TNHH XUAT NHAP KHAU KIM PHAT | 15 | 2.333.333.331 | 2.666.666.669 | 5,0 tỷ | **ALERT** |
| TC02_164 | ACT02_164 | KHTC | **7** | CONG TY CO PHAN THUONG MAI DAI THANH | 15 | 2.333.333.331 | 2.666.666.669 | 5,0 tỷ | **ALERT** |
| TC02_165 | ACT02_165 | KHCN | 3 | MAC VAN TOAN | 15 | 933.333.331 | 1.066.666.669 | 2,0 tỷ | **NO ALERT** (đối chứng) |

- TC02_161–164 là **case dương**: KH rủi ro cao giao dịch giá trị lớn.
- TC02_165 là **case đối chứng**: giao dịch **giống hệt** TC02_161, chỉ khác KYC = 3 (rủi ro thường). Nếu case này ra alert thì rule đang không lọc theo mức rủi ro KH.

## 2. Pattern giao dịch (mỗi TK)

| Ngày GD | Chiều | Số GD | FIC_MIS_DATE |
|---|:-:|:-:|---|
| 05/10/2026 | Nợ (chuyển đi) | 3 | 2026-10-15 |
| 07/10/2026 | Có (nhận về) | 3 | 2026-10-15 |
| 09/10/2026 | Nợ | 3 | 2026-10-15 |
| 12/10/2026 | Có | 2 | 2026-10-15 |
| 14/10/2026 | Nợ | 2 | 2026-10-15 |
| 16/10/2026 | Có | 2 | 2026-10-19 |

- Mỗi GD = tổng / 15. KHCN khoảng 133–160 triệu/GD, KHTC khoảng 333 triệu/GD.
- Thuộc tính GD: `EFT-OTHER`, `BRANCH-TELLER`, `CITAD`, VND, trong nước, `GENERAL`.
- Mỗi TK giao dịch qua lại với **1 đối tác cố định** ở ngân hàng khác (ACB, VCB, VietinBank, BIDV).
- Mỗi GD có 4 dòng FRONT_OFFICE_TXN_PARTY: ORG / SEND / RCV / BENE.

## 3. Thông tin khác

- FIC_MIS_DATE của KH và TK là **2026-02-05**. Các FIC 2026-10-15 và 2026-10-19 đã có trong bộ V1.28, nên **không cần** thêm STG_PARTY_TYPE_MASTER.
- KHTC có quan hệ REP + UBO: TC02_163 → TC02_161, TC02_164 → TC02_162.
- Mã mới, không trùng bộ V1.28 (đã kiểm tra):
  - KH `TC02_161`–`165`, TK `ACT02_161`–`165`
  - GD `TXN0021826`–`TXN0021900`
  - Địa chỉ `ADRGN000001`–`005`, SĐT `PHGN000001`–`007`, giấy tờ `DOCGN000001`–`005`
- Số SĐT, số giấy tờ và MST đều không trùng với data cũ.

## 4. Số dòng theo bảng

| Bảng | Dòng | Bảng | Dòng |
|---|--:|---|--:|
| 06 PARTY_MASTER | 5 | 14 PARTY_MSB_DETAILS | 5 |
| 07 PARTY_ROLE_MAP | 5 | 15 CORRESPONDENT_PROD_SERVED | 10 |
| 08 ADDRESS_MASTER | 5 | 16 CASA | 5 |
| 09 PARTY_ADDRESS_MAP | 5 | 17 PARTY_ACCOUNT_ROLE_MAP | 5 |
| 10 PARTY_PHONE_MAP | 7 | 18 ACCOUNT_ALT_CCY_VALUES | 5 |
| 11 PARTY_EMAIL_MAP | 7 | 19 CASA_TXNS | 75 |
| 12 CUSTOMER_IDENTIFCTN_DOC | 5 | 20 TXN_ALT_CCY_VALUES | 75 |
| 13 PARTY_PARTY_RELATIONSHIP | 4 | 21 FRONT_OFFICE_TXN_PARTY | 300 |

## 5. Cách chạy

1. **Điều kiện:** bộ V1.28 đã được nạp, vì data mới dùng chung danh mục và FIC.
2. Mở `00_RUN_ALL.sql` trong SQL Developer và chạy bằng **F5** (Run Script), hoặc chạy bằng SQL*Plus: `@00_RUN_ALL.sql` trong thư mục này. Script chạy lần lượt các file 06 → 21, sau đó chạy `98_CHECK.sql`.
3. Đối chiếu kết quả của `98_CHECK.sql` với bảng ở mục 1.
4. Chạy batch OFSAA cho FIC 2026-10-15 và 2026-10-19, rồi kiểm tra alert theo CIF.
5. Nếu cần làm lại thì chạy `99_ROLLBACK_XOA_DATA.sql`. Script này chỉ xóa đúng 5 KH mới.

## 6. Lưu ý

- Kỳ vọng ALERT / NO ALERT dựa trên **giả định** rằng rule TH02 = "KH rủi ro cao (KYC 7/8) có GD giá trị lớn". Ngưỡng chính xác của rule chưa có. Bộ data dùng cùng mức tiền với TC02 gốc, nên nếu TC02 gốc ra alert thì bộ này cũng sẽ ra.
- Muốn sinh lại hoặc đổi số lượng, số tiền: sửa danh sách `CUS` trong `_tool/gen_th02.py`, rồi chạy `python3 _tool/gen_th02.py <thư mục output>`.
