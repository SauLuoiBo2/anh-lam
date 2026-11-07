# B3 – Hướng dẫn sinh data mới (chuẩn bị)

Tài liệu này ghi lại quy tắc để sinh data mới **cùng định dạng và nhất quán** với bộ V1.28. Yêu cầu cụ thể của bước 3 (TH nào, số lượng bao nhiêu, kỳ vọng cảnh báo hay không, ngưỡng rule) **chưa có**, cần sếp xác nhận.

## 1. Sinh một thực thể thì phải insert những bảng nào

### Một khách hàng mới

| Bảng | Bắt buộc | Số dòng | Ghi chú |
|---|---|---|---|
| 06 STG_PARTY_MASTER | ✔ | 1 | KHCN: ngày sinh, giới tính, nghề nghiệp... KHTC: mã số thuế, ngày thành lập, ngành nghề, loại hình |
| 07 STG_PARTY_ROLE_MAP | ✔ | 1 | `CUSTOMER`, `A` |
| 08 STG_ADDRESS_MASTER | ✔ | 1–2 | |
| 09 STG_PARTY_ADDRESS_MAP | ✔ | 1–2 | `N_SEQUENCE_NUMBER` = 1, 2 |
| 10 STG_PARTY_PHONE_MAP | ✔ | 1–3 | M (di động), B (công ty), F (fax), H (nhà) |
| 11 STG_PARTY_EMAIL_MAP | ✔ | 1 | |
| 12 STG_CUSTOMER_IDENTIFCTN_DOC | ✔ | 1–2 | KHCN: IDC / IP (+ PP / VS nếu là người nước ngoài). KHTC: BR (+ IL nếu FDI) |
| 14 STG_PARTY_MSB_DETAILS | ✔ | 1 | Cờ FDI, cờ có SP tiền gửi |
| 15 STG_CORRESPONDENT_PROD_SERVED | ✔ | 1–n | SP KH đang dùng |
| 13 STG_PARTY_PARTY_RELATIONSHIP | tùy | n | KHTC: REP / UBO / CACC. TH09: Other. KH liên quan phải có trong bảng 06 |
| 01 STG_PARTY_TYPE_MASTER | ⚠ | — | Nếu dùng **FIC_MIS_DATE mới** thì thêm 2 dòng IND / ORG cho ngày đó |

### Một tài khoản mới

| Bảng | Số dòng | Ghi chú |
|---|---|---|
| 16 STG_CASA | 1 (TK ngủ đông: 2) | `V_CUST_REF_CODE` = CIF. KHCN: CR / IND. KHTC: CI / CORP |
| 17 STG_PARTY_ACCOUNT_ROLE_MAP | 1 | `CUSTOMER` / `OWNER` |
| 18 STG_ACCOUNT_ALT_CCY_VALUES | 1 | Số dư = `N_EOP_BAL` |

### Một giao dịch mới

| Bảng | Số dòng | Ghi chú |
|---|---|---|
| 19 STG_CASA_TXNS | 1 | `N_TXN_AMT` / `N_TXN_AMOUNT_NCY` = số tiền **nguyên tệ** |
| 20 STG_TXN_ALT_CCY_VALUES | 1 | `N_TXN_AMOUNT_LCY` = **VND quy đổi**, kèm tỷ giá |
| 21 STG_FRONT_OFFICE_TXN_PARTY | 2–4 | Liên NH: ORG, SEND, RCV, BENE. Nội bộ: ORG, BENE |
| 30 UPDATE F_EWALLET_FLAG | — | Chỉ cho GD nạp ví (nếu cột chưa có trong DDL) |

## 2. Mã tiếp theo (tránh trùng khóa)

| Đối tượng | Đang dùng tới | Mã mới đề xuất |
|---|---|---|
| KH bộ TC | TC01…TC14 dùng nnn 001–154, WLT dùng 155–160 | `TCxx_161` trở đi |
| KH bộ A | CIF_Axx_020 (A09: 1012) | `CIF_Axx_021` trở đi, hoặc bộ mới `CIF_Bxx_001` |
| KH bộ WL | CIF_WLxx_001 / 002 | `CIF_WLxx_002` / `003` trở đi |
| Giao dịch | **TXN0021825** | `TXN0021826` trở đi |
| Địa chỉ / SĐT / giấy tờ | ADRBG…, PHBG…, DOCBG… | Đề xuất tiền tố mới `ADRGN`, `PHGN`, `DOCGN` + số thứ tự |
| Số tham chiếu giấy tờ, MST, SĐT | — | Phải **duy nhất** (`V_DOC_REF_NO`, `V_PARTY_TAX_ID` và `V_PHONE_NUMBER` hiện đều không trùng) |

## 3. Quy tắc giá trị

1. **FIC_MIS_DATE của giao dịch:** ≥ ngày giao dịch. Bộ cũ gom GD vào các mốc như 15 hằng tháng, cuối tháng, 19/10, 26/10...
2. **FIC của KH / TK** phải ≤ FIC của GD đầu tiên. Ngày mở TK (`D_ACCT_OPEN_DATE`) phải trước ngày GD.
3. **Ngoại tệ:** tỷ giá dùng trong bộ cũ là USD = 26.260, SGD = 20.400 và HKD = 3.370. Quy tắc: `N_TXN_AMOUNT_LCY = N_TXN_AMT × N_TXN_CCY_TO_RCY_RATE`.
4. **GD quốc tế:** `V_MANTAS_TXN_PROD_TYPE_CD = 'EFT-SWIFT'`, `V_PAYMENT_SETTL_SYSTEM_CODE = 'SWIFT'`, `F_CROSS_BORDER_TXN_FLAG = 'Y'`, `V_TXN_ORIGIN_COUNTRY_ID` = QG đối tác. Bảng FO_TXN_PARTY cần BIC của NH nước ngoài.
5. **GD trong nước:** `EFT-OTHER` + `CITAD` (liên NH) hoặc `INTERNAL`. Nạp ví dùng `NAPAS`.
6. **QG rủi ro:** lấy từ bảng 04. VRC gồm CU, IR, KP, MM, SY. HRC gồm 34 QG (AF, RU, UA, VE...).
7. **TK ngủ đông:** dòng 1 status `A` ở FIC đầu. Dòng 2 status `D`, có `D_ACCT_STATUS_DATE` và `D_LAST_ACTIVITY_DATE` = ngày GD cuối trước khi ngủ đông.
8. **Giá trị cố định:** `V_DATA_ORIGIN = 'MSB'`, `V_DATA_JURISDICTION = 'All'`, `V_BUSINESS_DOMAIN = 'A'`, `N_LOAD_RUN_ID = 1`, `V_GAAP_CODE = 'VNGAAP'`, `V_MANTAS_TXN_ASSET_CLASS_CD = 'FUNDS'`, `V_CCY_CODE (CASA) = 'VND'`.
9. **Tên tiếng Việt viết không dấu, in hoa**, giống bộ cũ.

## 4. Mẫu theo kịch bản (khi sinh thêm KH cho TH đã có)

Bộ A cung cấp khuôn mẫu ổn định. Mỗi TK gồm:
- **GD nền:** 3 GD nhỏ 30 / 40 / 50 triệu vào 14 / 21 / 28 tháng 9, và 3 GD 20 / 30 / 40 triệu vào 28/01, 04/02, 11/02 năm sau.
- **Sự kiện kích hoạt** quanh 05–16/10, theo pattern của TH (xem bảng mục 2 trong file 02).

Khi sinh case **âm (không được cảnh báo)**, giữ nguyên cấu trúc và chỉ hạ số tiền, số lần hoặc số đối tác xuống **dưới ngưỡng rule**. Việc này cần biết ngưỡng chính xác.

## 5. Checklist trước khi bàn giao script

- [ ] Không trùng khóa chính với bộ V1.28 (chạy SELECT kiểm tra trên DB đích)
- [ ] Mọi khóa ngoại tồn tại: TK → KH, GD → TK, ALT / FO_PARTY → GD, địa chỉ map → địa chỉ master
- [ ] Mỗi GD có 1 dòng ALT_CCY, có từ 2 dòng FO_TXN_PARTY trở lên
- [ ] FIC_MIS_DATE mới có trong STG_PARTY_TYPE_MASTER
- [ ] Số tiền LCY khớp nguyên tệ × tỷ giá
- [ ] Định dạng script: `INSERT ALL` theo lô 200 dòng, `COMMIT` mỗi lô, `SET DEFINE OFF`, đánh số file theo thứ tự 01–21
- [ ] Kèm bảng mapping **CIF / TK → TH → kỳ vọng (Alert / No alert)** để tester đối chiếu kết quả

## 6. Thông tin cần sếp cung cấp để làm B3

1. Gen cho **TH nào**: thêm TH mới hay bổ sung TH đã có?
2. **Kỳ vọng**: case dương (phải có alert) hay case âm (sát ngưỡng, không có alert)?
3. **Ngưỡng rule** của từng TH: số tiền, số lần, khoảng thời gian, số đối tác.
4. **Số lượng** KH / TK / GD và **FIC_MIS_DATE** cần dùng.
5. Tài liệu kịch bản AML chính thức, để chốt lại phần diễn giải ở file 02.
