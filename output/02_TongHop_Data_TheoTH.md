# B2 – Tổng hợp dữ liệu theo trường hợp (TH)

> Ý nghĩa từng TH được **suy luận từ dữ liệu giao dịch** (số tiền, chiều, quốc gia, kênh, nội dung chuyển tiền), vì không có tài liệu mô tả rule. Cần đối chiếu với danh sách kịch bản AML chính thức.
> Mọi số tiền dưới đây là **VND quy đổi** (`STG_TXN_ALT_CCY_VALUES.N_TXN_AMOUNT_LCY`).

## 1. Cách tổ chức các bộ dữ liệu

| Bộ | Mã KH / TK | Quy mô | Đặc điểm |
|---|---|---|---|
| **TC** | `TCxx_nnn` / `ACTxx_nnn` | 4–28 KH/TH, 151 KH | Bộ gốc. GD tập trung trong khoảng 01–28/10/2026 (TH03, TH04 trải dài 05→11/2026) |
| **A** | `CIF_Axx_nnn` / `ACC_Axx_nnn` | 20 KH/TH (TH09: 24), 284 KH | Mỗi TK có **GD nền nhỏ** (20–50 triệu, vào 09/2026 và 01–02/2027) cộng **1 sự kiện kích hoạt** quanh 05–16/10/2026 |
| **WL** | `CIF_WLxx_nnn` / `ACC_WLxx_nnn` | 1 KH/TH (TH09: 2), 15 KH | Pattern **giống hệt bộ A trên từng TK** (cùng số GD/TK). Chưa rõ vai trò, xem file 04 |
| **BG** | `CIF_BG_nnn` / `ACC_BG_nnn` | 12 KH, 1.810 GD | GD thông thường đa kênh: tiền mặt, ATM, POS, séc, lãi, phí, lương. Dùng làm nhiễu, không kỳ vọng cảnh báo |
| **WLT** | `WLTnnn` / `WLAnnn` | 6 KH, 21 GD | Nhận tiền từ đối tác Cuba (HAVANA GENERAL TRADING) |

## 2. Diễn giải 14 kịch bản

| TH | Diễn giải (suy luận) | Dấu hiệu nhận biết trong data |
|---|---|---|
| **01** | GD với quốc gia rủi ro cao / rất cao (VRC / HRC) | EFT-SWIFT, `V_TXN_ORIGIN_COUNTRY_ID` ∈ watchlist (CU, AF, IR, KP, SY, MM...), F_CROSS_BORDER = Y, 0,3–2,5 tỷ |
| **02** | KH rủi ro cao giao dịch giá trị lớn | `N_KYC_RISK` = 7 / 8. Tiền vào – ra luân phiên, tổng khoảng 2–2,6 tỷ/TK trong 2 tuần |
| **03** | GD giá trị lớn đột biến so với lịch sử | 05→09/2026 mỗi tháng 1 GD 1 tỷ, tháng 10 tăng lên khoảng 5 tỷ |
| **04** | Giống TH03 | Số liệu **trùng khớp hoàn toàn** với TH03 (cùng số GD, cùng min/TB/max). Có thể là cùng pattern nhưng khác rule hoặc ngưỡng |
| **05** | Tần suất cao, nhiều GD nhỏ (chia nhỏ) | Khoảng 100 GD Có + 100 GD Nợ, mỗi GD khoảng 7 triệu, trong 12 ngày. Tối đa 74 GD/TK/ngày |
| **06** | TK ngủ đông hoạt động trở lại | CASA có thêm dòng `V_ACCT_STATUS_CODE = 'D'`. 02/2026 có 1 GD, sau đó 8 tháng không có GD, rồi 10/2026 có GD 400 triệu |
| **07** | Nhiều đối tác (fan-in / fan-out) | 1 TK nhận khoảng 150 GD từ khoảng 26 đối tác khác nhau trong 01–28/10 |
| **08** | Tiền vào lớn rồi ra nhanh (pass-through), kênh online | Nhận khoảng 2 tỷ qua ON-LINE, sau 2 ngày chuyển đi 1,8–2 tỷ |
| **09** | Giao dịch qua lại với người thân | RELATIONSHIP type `Other` (NGUOI THAN). Chuyển qua lại khoảng 500 triệu, ON-LINE / INTERNAL |
| **10** | Nhận tiền quốc tế từ Mỹ | SWIFT USD từ US (khoảng 500 triệu), sau đó chi ra trong nước |
| **11** | KH nước ngoài / FDI: tiền quốc tế vào rồi ra | KHCN quốc tịch US, KHTC có `F_FDI_FLAG = 'Y'`. Nhận USD từ US rồi chuyển đi SG |
| **12** | Chuyển tiền đi Singapore liên tục | Chỉ Nợ, SWIFT USD, khoảng 2 tỷ/GD, 5–6 GD cách nhau 2 ngày. Chủ yếu KHTC |
| **13** | Chuyển tiền đi Hong Kong liên tục | Chỉ Nợ, SWIFT HKD, khoảng 0,6–9,7 tỷ/GD |
| **14** | Nạp ví điện tử nhiều lần | NAPAS, "NAP TIEN VI DIEN TU MOMO / ZALOPAY / VNPAY / SHOPEEPAY", khoảng 10 triệu/lần, khoảng 20 lần/TK/ngày. `F_EWALLET_FLAG = 'Y'` |

## 3. Bảng số liệu theo TH × bộ

| TH | Bộ | KH | KHCN | KHTC | Số GD | Khoảng ngày GD | Tiền min | Tiền TB | Tiền max | Tiền tệ | Quốc gia |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| 01 | TC | 15 | 15 | 0 | 30 | 05/10–19/10/26 | 300tr | 903tr | 2,5 tỷ | USD,VND | CU,AF,VN |
| 01 | A | 20 | 20 | 0 | 166 | 14/09/26–11/02/27 | 20tr | 258tr | 1,2 tỷ | USD,VND | 18 QG watchlist |
| 01 | WL | 1 | 1 | 0 | 7 | 14/09/26–11/02/27 | 20tr | 201tr | 1,2 tỷ | USD,VND | IR,VN |
| 02 | TC | 10 | 6 | 4 | 149 | 05/10–19/10/26 | 127tr | 252tr | 464tr | VND | VN |
| 02 | A | 20 | 10 | 10 | 440 | 14/09/26–11/02/27 | 20tr | 200tr | 375tr | VND | VN |
| 02 | WL | 1 | 1 | 0 | 22 | 14/09/26–11/02/27 | 20tr | 119tr | 150tr | VND | VN |
| 03 | TC | 16 | 8 | 8 | 120 | 15/05–15/11/26 | 200tr | 888tr | 2,5 tỷ | VND | VN |
| 03 | A | 20 | 10 | 10 | 280 | 11/04/26–21/02/27 | 20tr | 508tr | 2,17 tỷ | VND | VN |
| 03 | WL | 1 | 1 | 0 | 14 | 11/04/26–21/02/27 | 20tr | 836tr | 2,17 tỷ | VND | VN |
| 04 | TC | 16 | 8 | 8 | 120 | 15/05–15/11/26 | 200tr | 888tr | 2,5 tỷ | VND | VN |
| 04 | A | 20 | 10 | 10 | 280 | 11/04/26–21/02/27 | 20tr | 508tr | 2,17 tỷ | VND | VN |
| 04 | WL | 1 | 1 | 0 | 14 | 11/04/26–21/02/27 | 20tr | 836tr | 2,17 tỷ | VND | VN |
| 05 | TC | 28 | 15 | 13 | 5.914 | 05/10–19/10/26 | 6,4tr | 58,7tr | 224tr | VND | VN |
| 05 | A | 20 | 20 | 0 | 4.520 | 14/09/26–17/02/27 | 6,6tr | 7,9tr | 50tr | VND | VN |
| 05 | WL | 1 | 1 | 0 | 236 | 14/09/26–11/02/27 | 6,6tr | 7,5tr | 50tr | VND | VN |
| 06 | TC | 6 | 6 | 0 | 13 | 05/02–19/10/26 | 50tr | 255tr | 450tr | VND | VN |
| 06 | A | 20 | 20 | 0 | 120 | 05/02/26–11/02/27 | 20tr | 104tr | 450tr | VND | VN |
| 06 | WL | 1 | 1 | 0 | 6 | 05/02/26–11/02/27 | 20tr | 107tr | 450tr | VND | VN |
| 07 | TC | 14 | 6 | 8 | 2.097 | 01/10–28/10/26 | 9,3tr | 26,8tr | 43,6tr | VND | VN |
| 07 | A | 20 | 10 | 10 | 3.220 | 11/09/26–21/02/27 | 11,6tr | 25,5tr | 50tr | VND | VN |
| 07 | WL | 1 | 1 | 0 | 161 | 11/09/26–21/02/27 | 11,6tr | 12,4tr | 50tr | VND | VN |
| 08 | TC | 6 | 6 | 0 | 13 | 05/10–19/10/26 | 1,8 tỷ | 2,05 tỷ | 2,6 tỷ | VND | VN |
| 08 | A | 20 | 20 | 0 | 160 | 14/09/26–11/02/27 | 20tr | 539tr | 2,1 tỷ | VND | VN |
| 08 | WL | 1 | 1 | 0 | 8 | 14/09/26–11/02/27 | 20tr | 541tr | 2,1 tỷ | VND | VN |
| 09 | TC | 12 | 12 | 0 | 12 | 07/10–19/10/26 | 400tr | 515tr | 600tr | VND | VN |
| 09 | A | 24 | 24 | 0 | 192 | 14/09/26–11/02/27 | 20tr | 174tr | 600tr | VND | VN |
| 09 | WL | 2 | 2 | 0 | 16 | 14/09/26–11/02/27 | 20tr | 174tr | 600tr | VND | VN |
| 10 | TC | 6 | 6 | 0 | 11 | 05/10–19/10/26 | 20tr | 437tr | 750tr | USD,VND | US,VN |
| 10 | A | 20 | 20 | 0 | 160 | 14/09/26–11/02/27 | 20tr | 108tr | 600tr | USD,VND | US,VN |
| 10 | WL | 1 | 1 | 0 | 8 | 14/09/26–11/02/27 | 20tr | 105tr | 600tr | USD,VND | US,VN |
| 11 | TC | 7 | 5 | 2 | 15 | 05/10–19/10/26 | 900tr | 1,36 tỷ | 2 tỷ | USD,SGD | US,SG |
| 11 | A | 20 | 10 | 10 | 160 | 14/09/26–11/02/27 | 20tr | 458tr | 2,4 tỷ | USD,SGD,VND | US,SG,VN |
| 11 | WL | 1 | 0 | 1 | 8 | 14/09/26–11/02/27 | 20tr | 604tr | 2,4 tỷ | USD,SGD,VND | US,SG,VN |
| 12 | TC | 7 | 0 | 7 | 35 | 05/10–19/10/26 | 1,98 tỷ | 2,51 tỷ | 3,25 tỷ | USD | SG |
| 12 | A | 20 | 0 | 20 | 240 | 14/09/26–11/02/27 | 20tr | 1,14 tỷ | 2,88 tỷ | USD,VND | SG,VN |
| 12 | WL | 1 | 0 | 1 | 12 | 14/09/26–11/02/27 | 20tr | 974tr | 1,92 tỷ | USD,VND | SG,VN |
| 13 | TC | 7 | 5 | 2 | 34 | 05/10–19/10/26 | 580tr | 2,54 tỷ | 9,75 tỷ | HKD | HK |
| 13 | A | 20 | 12 | 8 | 240 | 14/09/26–11/02/27 | 20tr | 1,34 tỷ | 5,75 tỷ | HKD,VND | HK,VN |
| 13 | WL | 1 | 1 | 0 | 12 | 14/09/26–11/02/27 | 20tr | 307tr | 575tr | HKD,VND | HK,VN |
| 14 | TC | 4 | 4 | 0 | 81 | 18/10/26 | 9,5tr | 10,1tr | 11,1tr | VND | VN |
| 14 | A | 20 | 20 | 0 | 560 | 27/09/26–11/02/27 | 9,5tr | 15tr | 50tr | VND | VN |
| 14 | WL | 1 | 1 | 0 | 28 | 27/09/26–11/02/27 | 9,5tr | 14,3tr | 50tr | VND | VN |
| BG | — | 12 | 8 | 4 | 1.810 | 08/03/26–21/02/27 | 11 nghìn | 8,6tr | 80tr | VND | VN |
| WLT | — | 6 | 6 | 0 | 21 | 05/10–16/10/26 | 173tr | 467tr | 1,2 tỷ | USD,VND | CU,VN |

## 4. Đặc điểm theo bảng khách hàng

| Hạng mục | Ghi nhận |
|---|---|
| Quốc tịch | Hầu hết VN. **US**: CIF_A11 (10 KHCN), TC11_054–056. 3 KH có quốc tịch phụ (V_SECONDARY_CITIZENSHIP = VN) |
| KYC risk | 3 với mọi TH, trừ **TH02** (7 / 8), CIF_WL02 (8) và một số WLT (8) |
| Cờ FDI | CIF_A11 KHTC (10), TC11_149–150, CIF_WL11, 2 KH BG |
| Quan hệ | Tập trung ở KHTC của TH02, 03, 04, 05, 07, 11, 12, 13: người đại diện (REP), chủ sở hữu hưởng lợi (UBO), kế toán trưởng (CACC). TH09: người thân (Other) |
| Giấy tờ | KHCN: CCCD / CMND (+ hộ chiếu, visa với KH US). KHTC: ĐKKD (+ ĐK đầu tư với FDI) |

## 5. Chi tiết

Số liệu từng tài khoản (471 TK: CIF, tên, loại KH, KYC, số dư, số GD, tổng Có / Nợ VND) nằm trong sheet **B2_ChiTiet_TK** của file [B1_B2_TongHop_Data_TheoTH.xlsx](B1_B2_TongHop_Data_TheoTH.xlsx).
