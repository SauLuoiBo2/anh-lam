# B1 – Phân tích cấu trúc dữ liệu

## 1. Tổng quan

| Hạng mục | Giá trị |
|---|---|
| Phiên bản | Bộ data test MSB TM V1.28, bản hợp nhất 29/10/2026 (riêng watchlist cập nhật 02/11/2026) |
| Hệ quản trị | Oracle. Script dùng `INSERT ALL` theo lô 200 dòng, `COMMIT` sau mỗi lô, `PROMPT` để log tiến độ |
| Số bảng | 21 bảng STG, cộng 1 script UPDATE |
| Tổng số dòng | ≈ 137.700 |
| Hệ thống nguồn | `V_DATA_ORIGIN = 'MSB'` (riêng bảng PARTY_MASTER có KYC/EKYC/OTHERS) |
| Giá trị mặc định | `V_DATA_JURISDICTION = 'All'`, `V_BUSINESS_DOMAIN = 'A'`, `N_LOAD_RUN_ID = 1`, `V_GAAP_CODE = 'VNGAAP'` |

**FIC_MIS_DATE** (ngày dữ liệu) có mặt trong khóa chính của mọi bảng. Theo file mapping, giá trị này phải khớp `KDD_PRCSNG_BATCH_CONTROL.DATA_DUMP_DT` khi chạy batch.

## 2. Danh sách bảng (theo thứ tự chạy)

| # | Bảng | Nhóm | Số dòng | Khóa chính | Liên kết | Nội dung |
|---|---|---|---:|---|---|---|
| 01 | STG_PARTY_TYPE_MASTER | Danh mục | 54 | V_PARTY_TYPE_CODE, FIC | — | IND / ORG, lặp cho 27 ngày FIC |
| 02 | STG_COUNTRY_MASTER | Danh mục | 260 | V_COUNTRY_ID, FIC | — | Quốc gia và điểm rủi ro `N_COUNTRY_RISK_FACTOR` (10–100) |
| 03 | STG_WATCHLIST_MASTER | Danh mục | 2 | V_WATCH_LIST_ID, FIC | — | VRC (rủi ro rất cao, mức 9), HRC (rủi ro cao, mức 7) |
| 04 | STG_WATCHLIST_MEMBER_ENTRY | Danh mục | 39 | V_WATCHLIST_ID, MEMBER_ID | → 03, → 02 | VRC 5 QG, HRC 34 QG |
| 05 | STG_CUSTOMER_ACCT_ROLE_MASTER | Danh mục | 7 | ROLE_ID | — | OWNER, JOINT, POA, GUARDIAN, WDRWL, TRDNG, OBLIG |
| 06 | STG_PARTY_MASTER | Khách hàng | 471 | V_PARTY_ID, FIC | → 01 | **Bảng gốc KH (CIF)**. 335 KHCN, 136 KHTC |
| 07 | STG_PARTY_ROLE_MAP | Khách hàng | 471 | V_PARTY_ID, ROLE | → 06 | 1 KH : 1 dòng, CUSTOMER / A |
| 08 | STG_ADDRESS_MASTER | Khách hàng | 720 | V_ADDRESS_ID, FIC | — | Nội dung địa chỉ |
| 09 | STG_PARTY_ADDRESS_MAP | Khách hàng | 720 | PARTY, ADDRESS, PURPOSE | → 06, → 08 | 1 KH : 1–2 địa chỉ (L/M/B/P/A) |
| 10 | STG_PARTY_PHONE_MAP | Khách hàng | 708 | PARTY, PHONE_ID, PURPOSE | → 06 | 1 KH : 1–3 SĐT (M/B/F/H) |
| 11 | STG_PARTY_EMAIL_MAP | Khách hàng | 471 | PARTY, EMAIL, PURPOSE | → 06 | PRSNL / BUSS / PRIM |
| 12 | STG_CUSTOMER_IDENTIFCTN_DOC | Khách hàng | 545 | CUST_REF, DOC_TYPE, DOC_ID | → 06 | Giấy tờ định danh |
| 13 | STG_PARTY_PARTY_RELATIONSHIP | Khách hàng | 266 | PARTY, RELATED_PARTY, TYPE | → 06 (2 chiều) | REP / UBO / CACC / Other |
| 14 | STG_PARTY_MSB_DETAILS | Khách hàng | 471 | V_PARTY_ID, FIC | → 06 | Bảng custom của MSB: cờ FDI, cờ vượt ngưỡng, cờ có SP tiền gửi |
| 15 | STG_CORRESPONDENT_PROD_SERVED | Khách hàng | 1.010 | CORR_FIN_INST_ID, PROD | → 06 | SP KH đang dùng (PAYMENT, DEPOSIT, ...) |
| 16 | STG_CASA | Tài khoản | 497 | V_ACCOUNT_NUMBER, FIC | → 06 | 471 TK. TK ngủ đông có thêm 1 dòng status `D` |
| 17 | STG_PARTY_ACCOUNT_ROLE_MAP | Tài khoản | 471 | ACCT, PARTY, ROLE | → 16, → 06 | Chủ TK = OWNER |
| 18 | STG_ACCOUNT_ALT_CCY_VALUES | Tài khoản | 471 | ACCT, FIC | → 16 | Số dư quy đổi |
| 19 | STG_CASA_TXNS | Giao dịch | 21.765 | V_TXN_REF_NO, FIC | → 16 | **Bảng chính để kích hoạt rule** |
| 20 | STG_TXN_ALT_CCY_VALUES | Giao dịch | 21.765 | V_TXN_REF_NO, FIC | → 19 (1:1) | Số tiền VND quy đổi và tỷ giá |
| 21 | STG_FRONT_OFFICE_TXN_PARTY | Giao dịch | 84.401 | TXN_REF_NO, PARTY_ROLE | → 19 (1:n) | Các bên tham gia GD (2–4 dòng/GD) |
| 30 | UPDATE F_EWALLET_FLAG | Giao dịch | — | — | → 19 | Giai đoạn 2: set `F_EWALLET_FLAG = 'Y'` cho GD nạp ví (TH14) |

## 3. Sơ đồ quan hệ

```
STG_PARTY_TYPE_MASTER ─┐
                       ▼
                STG_PARTY_MASTER (V_PARTY_ID = CIF)
   ┌──────────┬──────────┬───────────┬──────────┬───────────┬─────────────┬──────────────┐
   ▼          ▼          ▼           ▼          ▼           ▼             ▼              ▼
ROLE_MAP  ADDRESS_MAP  PHONE_MAP  EMAIL_MAP  IDENT_DOC  PARTY_PARTY_REL  MSB_DETAILS  CORR_PROD_SERVED
              │
              ▼
       ADDRESS_MASTER

STG_PARTY_MASTER ──(V_CUST_REF_CODE)──► STG_CASA (V_ACCOUNT_NUMBER)
                                          ├── PARTY_ACCOUNT_ROLE_MAP
                                          ├── ACCOUNT_ALT_CCY_VALUES
                                          └── STG_CASA_TXNS (V_TXN_REF_NO)
                                                 ├── TXN_ALT_CCY_VALUES (1:1)
                                                 └── FRONT_OFFICE_TXN_PARTY (1:n)

COUNTRY_MASTER ◄── WATCHLIST_MEMBER_ENTRY ──► WATCHLIST_MASTER
     ▲
     └── V_TXN_ORIGIN_COUNTRY_ID / V_ISO_COUNTRY_CODE (giao dịch)
```

**Kết quả kiểm tra toàn vẹn (đã chạy):**

| Kiểm tra | Số dòng lỗi |
|---|---:|
| CASA → PARTY_MASTER | 0 |
| ACCOUNT_ROLE_MAP → CASA / PARTY | 0 / 0 |
| CASA_TXNS → CASA | 0 |
| TXN_ALT_CCY → CASA_TXNS | 0 |
| FRONT_OFFICE_TXN_PARTY → CASA_TXNS | 0 |
| ADDRESS_MAP → ADDRESS_MASTER | 0 |
| RELATIONSHIP.related_party → PARTY_MASTER | 0 |
| GD **không có** dòng FRONT_OFFICE_TXN_PARTY | 304 (chủ yếu GD nền BG: lãi, phí, ATM) |

## 4. Quy ước mã

| Đối tượng | Mẫu mã | Ví dụ | Ghi chú |
|---|---|---|---|
| KH bộ TC | `TCxx_nnn` | TC05_083 | xx = số TH. Số thứ tự nnn chạy liên tục qua các TH (001–160) |
| TK bộ TC | `ACTxx_nnn` | ACT05_083 | Cùng nnn với KH |
| KH / TK bộ A | `CIF_Axx_nnn` / `ACC_Axx_nnn` | CIF_A01_001 | 001–020 trong mỗi TH |
| KH / TK bộ WL | `CIF_WLxx_nnn` / `ACC_WLxx_nnn` | CIF_WL05_001 | 001 (TH09 có 2 KH) |
| KH / TK nền | `CIF_BG_nnn` / `ACC_BG_nnn` | CIF_BG_001 | 001–012 |
| KH / TK watchlist | `WLTnnn` / `WLAnnn` | WLT155 / WLA155 | 155–160 |
| Người thân TH09 bộ A | `CIF_A09_10nn` | CIF_A09_1001 | Mã 4 chữ số, không theo quy ước 3 chữ số |
| Giao dịch | `TXNnnnnnnn` | TXN0011291 | Lớn nhất hiện tại: **TXN0021825** |
| Địa chỉ | `ADR10xxxx`, `ADRBGxxxxxx` | ADRBG956195 | BG = sinh ngẫu nhiên |
| Điện thoại | `PH20xxxx`, `PHBGxxxxxx` | PHBG984368 | |
| Giấy tờ | `DOC30xxxx`, `DOCBGxxxxxx` | DOCBG939329 | |

## 5. Giá trị danh mục và codeset đang dùng

| Cột | Giá trị |
|---|---|
| V_PARTY_TYPE | IND (KHCN), ORG (KHTC) |
| N_KYC_RISK | 3 = thường; 7, 8 = rủi ro cao (TH02, một phần WLT) |
| V_GENDER | A, B |
| V_OCCUPATION_STATUS | EMP, SE, STU, HM, UE |
| V_ORG_CONSTITUENT_TYPE | TNHH, CP, DNTN, HTX, HKD |
| V_BUSS_SEGMENT (PARTY) | RBK (bán lẻ), CBK (doanh nghiệp) |
| V_BUSINESS_SEGMENT_CODE (CASA) | KHCN: IND, AFF, MAFF, HKD. KHTC: LC1, CIB, SSE, SME, MSME, SMC, LMC |
| V_MANTAS_ACCT_HOLDR_TYPE / V_OWNERSHIP_TYPE | CR / IND (KHCN), CI / CORP (KHTC) |
| V_ACCT_STATUS_CODE | A (hoạt động), D (ngủ đông) |
| V_DOC_TYPE_CODE | IDC (CCCD), IP (CMND), PP (hộ chiếu), VS (visa), BR (ĐKKD), IL (ĐK đầu tư) |
| V_RELATIONSHIP_TYPE_CODE | REP (người đại diện PL), UBO (chủ sở hữu hưởng lợi), CACC (kế toán trưởng), Other (người thân) |
| V_MANTAS_TXN_PROD_TYPE_CD | EFT-OTHER, EFT-SWIFT, CURRENCY, CHECK, DEBIT-CARD, ... (13 giá trị) |
| V_MANTAS_TXN_CHANNEL_CD | BRANCH-TELLER, ON-LINE, ATM, DEBIT-TERMINAL, MOBILE-PDA, INTERNAL-SYSTEM, RETAIL-OUTLET |
| V_PAYMENT_SETTL_SYSTEM_CODE | CITAD, NAPAS, SWIFT, INTERNAL |
| V_PARTY_ROLE (FO_TXN_PARTY) | ORG (người chuyển), BENE (người hưởng), SEND / RCV (NH gửi/nhận, BIC), CND (người thực hiện), LOC (địa điểm POS) |
| V_PARTY_ID_TYPE | IA (TK nội bộ MSB), XA (TK ngoài), BIC, CU, OT |
| Chi nhánh | VN0010001, VN0010002, VN0010003 |

## 6. Cấu trúc một giao dịch mẫu (TH01: nhận tiền từ Cuba)

**STG_CASA_TXNS** – TXN0011291:

| Cột | Giá trị |
|---|---|
| V_ACCOUNT_NUMBER | ACT01_001 |
| F_DRCR_INDICATOR | C |
| V_TXN_CCY_CODE / N_TXN_AMT | USD / 38.080,73 |
| V_MANTAS_TXN_PROD_TYPE_CD / CHANNEL | EFT-SWIFT / BRANCH-TELLER |
| V_PAYMENT_SETTL_SYSTEM_CODE | SWIFT |
| V_TXN_ORIGIN_COUNTRY_ID / F_CROSS_BORDER_TXN_FLAG | CU / Y |
| D_TRANSACTION_DATE / FIC_MIS_DATE | 2026-10-05 / 2026-10-15 |

**STG_TXN_ALT_CCY_VALUES:** N_TXN_AMOUNT_LCY = 1.000.000.000 VND, tỷ giá 26.260.

**STG_FRONT_OFFICE_TXN_PARTY** (4 dòng):

| Role | Tên | ID | Loại ID | QG |
|---|---|---|---|---|
| ORG | HAVANA GENERAL TRADING S.A. | CU4246177719138136 | XA | CU |
| SEND | MATANZAS TRADE BANK | MATBCULA | BIC | CU |
| RCV | NGAN HANG TMCP HANG HAI VIET NAM (MSB) | MCOBVNVX | BIC | VN |
| BENE | NGUYEN MY OANH | ACT01_001 | IA | VN |

> Quy tắc chung: GD chuyển khoản liên ngân hàng có 4 dòng party (ORG / SEND / RCV / BENE). GD nội bộ có 2 dòng. GD POS có 3 dòng (thêm LOC). GD tiền mặt có dòng CND.

## 7. Phân bố FIC_MIS_DATE

- **Khách hàng / tài khoản:** 2026-02-05 (phần lớn), 2026-03-08 (BG), 2026-03-25 (TC12), 2026-04-01 (TC03–05, A05, A12, WL05, WL12).
- **TK ngủ đông:** thêm dòng ở 2026-08-15 (TC06), 2026-09-15 (A06), 2026-09-30 (WL06).
- **Giao dịch:** 27 ngày từ 2026-02-05 đến 2027-02-28. Nhiều nhất ở **2026-10-15 (8.600 GD)** và 2026-10-19 (2.622 GD).
- Một FIC_MIS_DATE gom GD của nhiều ngày giao dịch. Ví dụ FIC 2026-10-15 chứa các GD từ 05/10 đến 14/10.
