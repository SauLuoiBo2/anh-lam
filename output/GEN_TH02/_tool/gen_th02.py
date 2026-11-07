"""Sinh data test TH02 (KH rui ro cao, tien vao-ra luan phien) theo khuon bo TC02 V1.28."""
import random, sys, os, datetime as dt
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
rnd = random.Random(20261107)
HDR = 'Bo data test MSB TM - BO SUNG TH02 (gen 07/11/2026) | Khuon theo TC02 V1.28 | INSERT ALL theo lo 200 dong, COMMIT moi lo'
D = lambda s: None if s is None else ('DATE', s)

def lit(v):
    if v is None: return 'NULL'
    if isinstance(v, tuple):
        return f"TO_DATE('{v[1]}','YYYY-MM-DD HH24:MI:SS')" if len(v[1]) > 10 else f"TO_DATE('{v[1]}','YYYY-MM-DD')"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"

TABLES = {}
def add(t, row): TABLES.setdefault(t, []).append(row)

FIC_KH = '2026-02-05'
MSB = 'NGAN HANG TMCP HANG HAI VIET NAM (MSB)'
BANKS = [('ACB', 'ASCBVNVX'), ('VIETCOMBANK', 'BFTVVNVX'), ('VIETINBANK', 'ICBVVNVX'), ('BIDV', 'BIDVVNVX')]

# ---------------- Khach hang ----------------
# (id, loai, KYC, ky vong, ten, chi nhanh, tong tien vao/ra, doi tac)
CUS = [
 ('TC02_161', 'IND', 8, 'ALERT',    'TRINH VAN KHANH',                        'VN0010001', 2_000_000_000, 'CONG TY TNHH THUONG MAI MINH QUANG HA NOI'),
 ('TC02_162', 'IND', 7, 'ALERT',    'LUONG THI HOAI',                         'VN0010003', 2_400_000_000, 'CONG TY CO PHAN DAU TU BAO LONG'),
 ('TC02_163', 'ORG', 8, 'ALERT',    'CONG TY TNHH XUAT NHAP KHAU KIM PHAT',   'VN0010002', 5_000_000_000, 'CONG TY TNHH VAT LIEU XAY DUNG THANH DAT'),
 ('TC02_164', 'ORG', 7, 'ALERT',    'CONG TY CO PHAN THUONG MAI DAI THANH',   'VN0010002', 5_000_000_000, 'CONG TY TNHH NONG SAN PHU YEN XANH'),
 ('TC02_165', 'IND', 3, 'NO ALERT', 'MAC VAN TOAN',                           'VN0010001', 2_000_000_000, 'CONG TY TNHH THUONG MAI MINH QUANG HA NOI'),
]
IND_INFO = {
 'TC02_161': dict(dob='1985-03-14', g='A', prof='0003', emp='CONG TY CO PHAN DICH VU AN PHU', st='EMP', edu='DAI HOC', email='trinhvankhanh85@gmail.com', city=('SO 45 PHO HUE', 'PHUONG HAI BA TRUNG', 'HA NOI')),
 'TC02_162': dict(dob='1990-11-02', g='B', prof='0014', emp=None, st='SE', edu='CAO DANG', email='luongthihoai90@gmail.com', city=('SO 18 DUONG LE LOI', 'PHUONG BEN THANH', 'TP HO CHI MINH')),
 'TC02_165': dict(dob='1987-07-21', g='A', prof='0003', emp='CONG TY TNHH KY THUAT HUNG THINH', st='EMP', edu='DAI HOC', email='macvantoan87@gmail.com', city=('SO 9 PHO TRAN DUY HUNG', 'PHUONG CAU GIAY', 'HA NOI')),
}
ORG_INFO = {
 'TC02_163': dict(disp='KIM PHAT', full='KIM PHAT IMPORT EXPORT COMPANY LIMITED', ctype='TNHH', ind='46101', inc='2016-05-10', web='www.kimphat.com.vn', dom='kimphat.com.vn', seg='LC1', city=('SO 210 DUONG NGUYEN VAN LINH', 'PHUONG HAI CHAU', 'DA NANG'), rep='TC02_161'),
 'TC02_164': dict(disp='DAI THANH', full='DAI THANH TRADING JOINT STOCK COMPANY', ctype='CP', ind='46101', inc='2015-09-01', web='www.daithanh.com.vn', dom='daithanh.com.vn', seg='SME', city=('SO 77 DUONG LACH TRAY', 'PHUONG NGO QUYEN', 'HAI PHONG'), rep='TC02_162'),
}
used_phone, used_doc = set(), set()
def uniq(gen, used):
    while True:
        v = gen()
        if v not in used: used.add(v); return v
seq = {'ADR': 0, 'PH': 0, 'DOC': 0}
def nid(p): seq[p] += 1; return f'{p}GN{seq[p]:06d}'

for cid, typ, kyc, _, name, br, _, _ in CUS:
    acc = 'ACT02_' + cid.split('_')[1]
    if typ == 'IND':
        i = IND_INFO[cid]
        add('STG_PARTY_MASTER', dict(FIC_MIS_DATE=D(FIC_KH), V_DATA_JURISDICTION='All', V_BUSINESS_DOMAIN='A', V_PARTY_ID=cid, V_PARTY_NAME=name, V_DISPLAY_NM=name, V_PARTY_TYPE='IND', D_DATE_OF_BIRTH=D(i['dob']), V_GENDER=i['g'], V_NATIONALITY_COUNTRY='VN', V_DOMICILE_COUNTRY='VN', V_PROFESSION=i['prof'], V_ORG_CONSTITUENT_TYPE=None, V_INDUSTRY_CODE=None, D_INCORPORATION_DATE=None, V_PARTY_TAX_ID=None, V_BUSS_SEGMENT='RBK', N_KYC_RISK=kyc, D_START_DATE=D('2023-01-22'), V_DATA_ORIGIN='KYC', V_INCORPORATION_COUNTRY_CD=None, V_CITIZENSHIP_TYPE='Birth Citizenship', V_BENEFICIAL_OWNER_CATEGORY='Individual', V_EMP_COMPANY=i['emp'], V_OCCUPATION_STATUS=i['st'], V_EDUCATION=i['edu'], V_RESIDENCY_STATUS_INDICATOR='Y', V_ADDRESS_OFF_FAX_NO=None, V_WEBSITE=None, V_BRANCH_CODE=br, V_JOB_TITLE=i['prof'], V_PARTY_FULL_NAME=name, V_PARTY_ALIAS=None, V_SECONDARY_CITIZENSHIP=None, F_SAR_STR_FLAG='N'))
        addr, purp = i['city'], 'L'
        phones = [('M', uniq(lambda: '09' + str(rnd.randint(10**7, 10**8 - 1)), used_phone))]
        emails = [('PRSNL', i['email'])]
        docref = uniq(lambda: '0' + str(rnd.randint(10**10, 10**11 - 1)), used_doc)
        add('STG_CUSTOMER_IDENTIFCTN_DOC', dict(V_CUST_REF_CODE=cid, FIC_MIS_DATE=D(FIC_KH), V_DOCUMENT_ID=nid('DOC'), V_DOCUMENT_NAME='THE CAN CUOC CONG DAN', V_DATA_JURISDICTION='All', V_DOC_TYPE_CODE='IDC', V_DOC_REF_NO=docref, D_DOC_ISSUE_DATE=D('2021-04-20'), D_DOC_EXPIRY_DATE=D(str(int(i['dob'][:4]) + 40) + i['dob'][4:]), V_DOC_ISSUED_BY='CUC CANH SAT QLHC VE TTXH', V_ISO_COUNTRY_CODE='VN', V_DATA_ORIGIN='MSB'))
        holder, own, bseg, prods, depo = 'CR', 'IND', 'IND', ['PAYMENT', 'CREDIT/LENDING'], 'N'
    else:
        o = ORG_INFO[cid]
        tax = uniq(lambda: '0' + str(rnd.randint(10**8, 10**9 - 1)), used_doc)
        add('STG_PARTY_MASTER', dict(FIC_MIS_DATE=D(FIC_KH), V_DATA_JURISDICTION='All', V_BUSINESS_DOMAIN='A', V_PARTY_ID=cid, V_PARTY_NAME=name, V_DISPLAY_NM=o['disp'], V_PARTY_TYPE='ORG', D_DATE_OF_BIRTH=None, V_GENDER=None, V_NATIONALITY_COUNTRY='VN', V_DOMICILE_COUNTRY='VN', V_PROFESSION=None, V_ORG_CONSTITUENT_TYPE=o['ctype'], V_INDUSTRY_CODE=o['ind'], D_INCORPORATION_DATE=D(o['inc']), V_PARTY_TAX_ID=tax, V_BUSS_SEGMENT='CBK', N_KYC_RISK=kyc, D_START_DATE=D('2023-01-22'), V_DATA_ORIGIN='KYC', V_INCORPORATION_COUNTRY_CD='VN', V_CITIZENSHIP_TYPE=None, V_BENEFICIAL_OWNER_CATEGORY='Corporation', V_EMP_COMPANY=None, V_OCCUPATION_STATUS=None, V_EDUCATION=None, V_RESIDENCY_STATUS_INDICATOR='Y', V_ADDRESS_OFF_FAX_NO=None, V_WEBSITE=o['web'], V_BRANCH_CODE=br, V_JOB_TITLE=None, V_PARTY_FULL_NAME=o['full'], V_PARTY_ALIAS=o['disp'], V_SECONDARY_CITIZENSHIP=None, F_SAR_STR_FLAG='N'))
        addr, purp = o['city'], 'B'
        phones = [('B', uniq(lambda: '0236' + str(rnd.randint(10**6, 10**7 - 1)), used_phone)), ('M', uniq(lambda: '09' + str(rnd.randint(10**7, 10**8 - 1)), used_phone))]
        emails = [('BUSS', 'info@' + o['dom']), ('PRIM', 'ketoan@' + o['dom'])]
        add('STG_CUSTOMER_IDENTIFCTN_DOC', dict(V_CUST_REF_CODE=cid, FIC_MIS_DATE=D(FIC_KH), V_DOCUMENT_ID=nid('DOC'), V_DOCUMENT_NAME='GIAY CHUNG NHAN DANG KY DOANH NGHIEP', V_DATA_JURISDICTION='All', V_DOC_TYPE_CODE='BR', V_DOC_REF_NO=tax, D_DOC_ISSUE_DATE=D(o['inc']), D_DOC_EXPIRY_DATE=None, V_DOC_ISSUED_BY='SO TAI CHINH', V_ISO_COUNTRY_CODE='VN', V_DATA_ORIGIN='MSB'))
        for code, desc in [('REP', 'NGUOI DAI DIEN THEO PHAP LUAT'), ('UBO', 'CHU SO HUU HUONG LOI')]:
            add('STG_PARTY_PARTY_RELATIONSHIP', dict(V_PARTY_ID=cid, FIC_MIS_DATE=D(FIC_KH), V_RELATIONSHIP_DESC=desc, V_RELATED_PARTY_ID=o['rep'], V_RELATIONSHIP_TYPE_CODE=code, D_RELATIONSHIP_EFF_DATE=D(FIC_KH), V_DATA_ORIGIN='MSB'))
        holder, own, bseg, prods, depo = 'CI', 'CORP', o['seg'], ['PAYMENT', 'DEPOSIT'], 'Y'
    add('STG_PARTY_ROLE_MAP', dict(V_PARTY_ID=cid, V_PARTY_ROLE='CUSTOMER', FIC_MIS_DATE=D(FIC_KH), V_PARTY_STATUS='A', V_DATA_ORIGIN='MSB'))
    aid = nid('ADR')
    add('STG_ADDRESS_MASTER', dict(FIC_MIS_DATE=D(FIC_KH), V_ADDRESS_ID=aid, V_ADDRESS_LINE1=addr[0], V_ADDRESS_LINE2=addr[1], V_CITY=addr[2], V_COUNTRY_CODE='VN', V_DATA_ORIGIN='MSB'))
    add('STG_PARTY_ADDRESS_MAP', dict(FIC_MIS_DATE=D(FIC_KH), V_ADDRESS_ID=aid, V_ADDRESS_PURPOSE_TYPE_CD=purp, V_PARTY_ID=cid, N_SEQUENCE_NUMBER=1))
    for n, (pt, num) in enumerate(phones, 1):
        add('STG_PARTY_PHONE_MAP', dict(FIC_MIS_DATE=D(FIC_KH), V_PARTY_ID=cid, V_PHONE_ID=nid('PH'), V_PHONE_PURPOSE_TYPE_CD=pt, N_SEQUENCE_NUMBER=n, V_PHONE_NUMBER=num))
    for n, (et, em) in enumerate(emails, 1):
        add('STG_PARTY_EMAIL_MAP', dict(FIC_MIS_DATE=D(FIC_KH), V_EMAIL_PURPOSE_TYPE_CD=et, V_PARTY_ID=cid, N_SEQUENCE_NUMBER=n, V_EMAIL_ID=em))
    add('STG_PARTY_MSB_DETAILS', dict(V_PARTY_ID=cid, FIC_MIS_DATE=D(FIC_KH), V_CITIZENSHIP_3=None, V_CITIZENSHIP_4=None, V_CITIZENSHIP_5=None, F_FDI_FLAG='N', F_INTL_REMIT_THRESHOLD_FLAG='N', F_TRADE_FIN_THRESHOLD_FLAG='N', F_DOM_PAYMENT_THRESHOLD_FLAG='N', F_HAS_DEPOSIT_PROD_FLAG=depo, V_DATA_ORIGIN='MSB'))
    for p in prods:
        add('STG_CORRESPONDENT_PROD_SERVED', dict(FIC_MIS_DATE=D(FIC_KH), V_CORR_FIN_INST_ID=cid, V_PROD_CODE=p, V_DATA_ORIGIN='MSB'))
    # ---------------- Tai khoan ----------------
    bal = 1_000_000_000
    add('STG_CASA', dict(FIC_MIS_DATE=D(FIC_KH), N_LOAD_RUN_ID=1, V_GAAP_CODE='VNGAAP', V_MANTAS_ACCT_HOLDR_TYPE=holder, V_DATA_JURISDICTION='All', V_BUSINESS_DOMAIN='A', V_ACCOUNT_NUMBER=acc, V_CUST_REF_CODE=cid, V_ACCOUNT_TYPE_CODE='CASA', V_ACCT_DISPLAY_NAME=name, V_CCY_CODE='VND', D_ACCT_OPEN_DATE=D('2023-01-22'), V_ACCT_STATUS_CODE='A', D_ACCT_STATUS_DATE=D('2023-01-22'), D_LAST_ACTIVITY_DATE=None, V_ACCOUNT_PURPOSE='O', V_OWNERSHIP_TYPE=own, V_BRANCH_CODE=br, N_EOP_BAL=bal, V_DATA_ORIGIN='MSB', F_ESCROW_ACCOUNT_FLAG='N', N_ACCT_NET_WORTH=bal, V_BUSINESS_SEGMENT_CODE=bseg))
    add('STG_PARTY_ACCOUNT_ROLE_MAP', dict(FIC_MIS_DATE=D(FIC_KH), V_ACCOUNT_NUMBER=acc, V_PARTY_ID=cid, V_ACCT_PARTY_ROLE='CUSTOMER', D_ROLE_EFFECTIVE_DATE=D('2023-01-22'), V_ACCT_PARTY_OPERATN_ROLE_CD='OWNER', V_DATA_ORIGIN='MSB'))
    add('STG_ACCOUNT_ALT_CCY_VALUES', dict(FIC_MIS_DATE=D(FIC_KH), V_ACCOUNT_NUMBER=acc, V_RCY_CODE='VND', V_LCY_CODE='VND', N_ACCT_NET_WORTH_RCY=bal, N_ACCT_NET_WORTH_LCY=bal, N_EOP_BAL_RCY=bal, N_LEDGER_BAL_RCY=bal, N_CASH_BALANCE_RCY=bal, N_EOP_BAL_FCY=bal, N_ACCT_NET_WORTH_FCY=bal, V_FCY_CODE='VND', V_DATA_SOURCE_CODE='MSB'))

# ---------------- Giao dich ----------------
# Khuon TC02: 6 ngay luan phien No/Co, 3-3-3-2-2-2 GD. Tong ca 2 chieu = total.
PLAN = [('2026-10-05', 'D', 3), ('2026-10-07', 'C', 3), ('2026-10-09', 'D', 3), ('2026-10-12', 'C', 2), ('2026-10-14', 'D', 2), ('2026-10-16', 'C', 2)]
txn_no = 21825
EXPECT = []
for k, (cid, typ, kyc, exp, name, br, total, cp) in enumerate(CUS):
    acc = 'ACT02_' + cid.split('_')[1]
    bank, bic = BANKS[k % len(BANKS)]
    cp_acc = str(rnd.randint(10**9, 10**10 - 1))
    cp_addr = f'SO {rnd.randint(10, 400)} DUONG TRAN HUNG DAO, PHUONG CUA NAM, HA NOI'
    teller = 'GDV00' + br[-1]
    ntx = sum(n for _, _, n in PLAN)
    base = total // ntx; first = True  # nhu goc: tong ca 2 chieu = total, moi GD = total/15
    notes_d = ['CHUYEN KHOAN ' + cp, 'THANH TOAN TIEN HANG THEO HD SO {}/2026', 'CHUYEN TIEN GOP VON', 'TRA TIEN HANG DOT {}']
    notes_c = [cp + ' CHUYEN TIEN', 'HOAN UNG ' + cp, 'THANH TOAN TIEN HANG THEO HD SO {}/2026', 'TRA TIEN HANG DOT {}']
    sums = {'D': 0, 'C': 0}; cnt = 0
    for day, drcr, n in PLAN:
        t = dt.datetime.fromisoformat(day + ' 08:00:00')
        for _ in range(n):
            txn_no += 1; ref = f'TXN{txn_no:07d}'
            amt = base + (total - base * ntx if first else 0); first = False
            sums[drcr] += amt; cnt += 1
            t += dt.timedelta(minutes=rnd.randint(15, 55), seconds=rnd.randint(0, 59))
            fic = '2026-10-15' if day <= '2026-10-14' else '2026-10-19'
            note = rnd.choice(notes_d if drcr == 'D' else notes_c).format(rnd.randint(1, 999) if drcr == 'D' else rnd.randint(1, 5))
            add('STG_CASA_TXNS', dict(FIC_MIS_DATE=D(fic), V_MANTAS_TXN_ASSET_CLASS_CD='FUNDS', V_TXN_REF_NO=ref, V_ACCOUNT_NUMBER=acc, F_DRCR_INDICATOR=drcr, N_TXN_AMT=amt, V_TXN_CCY_CODE='VND', D_TXN_VALUE_DATE=D(day), D_EXECUTION_TIME=D(t.strftime('%Y-%m-%d %H:%M:%S')), V_MANTAS_TXN_PROD_TYPE_CD='EFT-OTHER', V_MANTAS_TXN_PURPOSE_CD='GENERAL', V_MANTAS_TXN_CHANNEL_CD='BRANCH-TELLER', V_DATA_ORIGIN='MSB', F_CROSS_BORDER_TXN_FLAG='N', V_ORIGNTR_TO_BENFCRY_INSTRCTNS=note, V_TXN_TELLER_ID=f'{teller}{rnd.randint(1, 12):02d}', V_BRANCH_CODE=br, D_TXN_POSTING_DATE=D(day), V_ON_US_OFF_US_IND=None, V_PAYMENT_SETTL_SYSTEM_CODE='CITAD', V_TXN_ORIGIN_COUNTRY_ID='VN', F_PASS_THROUGH_FLAG='N', V_ORIGINAL_TXN_REF_NO=None, F_CANCELING_INDICATOR='N', F_EWALLET_FLAG='N', N_TXN_AMOUNT_NCY=amt, D_TRANSACTION_DATE=D(day), V_TXN_ACY_CODE='VND', V_CARD_NO=None, V_TXN_TERMINAL_ID=None, V_TXN_MERCHANT_POS_ID=None, V_MERCHANT_CATEGORY_CODE=None, F_TXN_CARD_NOT_PRESENTED_FLAG=None, V_TXN_CHANNEL_LOCATION_ID=None, V_TXN_CHANNEL_LOCATION_NAME=None, V_PAYMNT_INSTRUMENT_NUMBER=None, V_PAYMNT_INSTRUMENT_ROUTING_CD=None, D_DEPOSITING_DATE=None, V_TXN_DEVICE_ID=None, V_TXN_DEVICE_TYPE=None, V_TXN_GEO_LOCATION=None))
            add('STG_TXN_ALT_CCY_VALUES', dict(FIC_MIS_DATE=D(fic), V_TXN_REF_NO=ref, V_RCY_CODE='VND', V_LCY_CODE='VND', N_TXN_AMOUNT_RCY=amt, N_TXN_AMOUNT_LCY=amt, N_TXN_AMOUNT_FCY=amt, V_TXN_FCY_CODE='VND', N_TXN_CCY_TO_RCY_RATE=1, V_DATA_SOURCE_CODE='MSB'))
            me = dict(V_PARTY_NAME=name, V_PARTY_ID=acc, V_PARTY_ID_TYPE='IA', V_PARTY_ID_ISSUER=MSB, V_ISO_COUNTRY_CODE='VN', V_ADDRESS_LINE_1=None, F_INTERNAL_ACCOUNT_FLAG='Y')
            other = dict(V_PARTY_NAME=cp, V_PARTY_ID=cp_acc, V_PARTY_ID_TYPE='XA', V_PARTY_ID_ISSUER=bank, V_ISO_COUNTRY_CODE='VN', V_ADDRESS_LINE_1=cp_addr, F_INTERNAL_ACCOUNT_FLAG='N')
            msb = dict(V_PARTY_NAME=MSB, V_PARTY_ID='MCOBVNVX', V_PARTY_ID_TYPE='BIC', V_PARTY_ID_ISSUER='SWIFT', V_ISO_COUNTRY_CODE='VN', V_ADDRESS_LINE_1=None, F_INTERNAL_ACCOUNT_FLAG='N')
            ob = dict(V_PARTY_NAME=bank, V_PARTY_ID=bic, V_PARTY_ID_TYPE='BIC', V_PARTY_ID_ISSUER='SWIFT', V_ISO_COUNTRY_CODE='VN', V_ADDRESS_LINE_1=None, F_INTERNAL_ACCOUNT_FLAG='N')
            roles = [('ORG', me), ('SEND', msb), ('RCV', ob), ('BENE', other)] if drcr == 'D' else [('ORG', other), ('SEND', ob), ('RCV', msb), ('BENE', me)]
            for role, p in roles:
                add('STG_FRONT_OFFICE_TXN_PARTY', dict(V_TXN_REF_NO=ref, FIC_MIS_DATE=D(fic), V_PARTY_ROLE=role, **p, V_DATA_ORIGIN='MSB', N_CNDTR_REF_ID=0))
    EXPECT.append((cid, acc, typ, kyc, name, cnt, sums['C'], sums['D'], exp))

# ---------------- Ghi file ----------------
ORDER = [('06', 'STG_PARTY_MASTER'), ('07', 'STG_PARTY_ROLE_MAP'), ('08', 'STG_ADDRESS_MASTER'), ('09', 'STG_PARTY_ADDRESS_MAP'), ('10', 'STG_PARTY_PHONE_MAP'), ('11', 'STG_PARTY_EMAIL_MAP'), ('12', 'STG_CUSTOMER_IDENTIFCTN_DOC'), ('13', 'STG_PARTY_PARTY_RELATIONSHIP'), ('14', 'STG_PARTY_MSB_DETAILS'), ('15', 'STG_CORRESPONDENT_PROD_SERVED'), ('16', 'STG_CASA'), ('17', 'STG_PARTY_ACCOUNT_ROLE_MAP'), ('18', 'STG_ACCOUNT_ALT_CCY_VALUES'), ('19', 'STG_CASA_TXNS'), ('20', 'STG_TXN_ALT_CCY_VALUES'), ('21', 'STG_FRONT_OFFICE_TXN_PARTY')]
for no, t in ORDER:
    rows = TABLES[t]
    with open(os.path.join(OUT, f'{no}_{t}.sql'), 'w', encoding='ascii') as f:
        f.write(f'-- {t} | {HDR}\nSET DEFINE OFF\nPROMPT Loading {t} ...\n')
        for i in range(0, len(rows), 200):
            f.write('INSERT ALL\n')
            for r in rows[i:i + 200]:
                f.write(f"  INTO {t} ({', '.join(r)}) VALUES ({', '.join(lit(v) for v in r.values())})\n")
            f.write('SELECT 1 FROM DUAL;\nCOMMIT;\n')
        f.write(f'PROMPT {t}: {len(rows)} rows\n')
    print(no, t, len(rows))

with open(os.path.join(OUT, '00_RUN_ALL.sql'), 'w') as f:
    f.write('-- Chay toan bo data bo sung TH02 theo dung thu tu (SQL*Plus / SQL Developer: F5)\nSET DEFINE OFF\nWHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK\n')
    for no, t in ORDER: f.write(f'@@{no}_{t}.sql\n')
    f.write('@@98_CHECK.sql\n')

ids = "'" + "','".join(c[0] for c in CUS) + "'"
accs = "'" + "','".join('ACT02_' + c[0].split('_')[1] for c in CUS) + "'"
with open(os.path.join(OUT, '98_CHECK.sql'), 'w') as f:
    f.write(f"""-- Kiem tra sau khi nap data bo sung TH02
SET PAGESIZE 100 LINESIZE 200
PROMPT === So dong da nap theo bang (ky vong: PARTY 5, CASA 5, TXN 75, ALT 75, FO_PARTY 300)
SELECT 'STG_PARTY_MASTER' T, COUNT(*) N FROM STG_PARTY_MASTER WHERE V_PARTY_ID IN ({ids})
UNION ALL SELECT 'STG_CASA', COUNT(*) FROM STG_CASA WHERE V_ACCOUNT_NUMBER IN ({accs})
UNION ALL SELECT 'STG_CASA_TXNS', COUNT(*) FROM STG_CASA_TXNS WHERE V_ACCOUNT_NUMBER IN ({accs})
UNION ALL SELECT 'STG_TXN_ALT_CCY_VALUES', COUNT(*) FROM STG_TXN_ALT_CCY_VALUES WHERE V_TXN_REF_NO IN (SELECT V_TXN_REF_NO FROM STG_CASA_TXNS WHERE V_ACCOUNT_NUMBER IN ({accs}))
UNION ALL SELECT 'STG_FRONT_OFFICE_TXN_PARTY', COUNT(*) FROM STG_FRONT_OFFICE_TXN_PARTY WHERE V_TXN_REF_NO IN (SELECT V_TXN_REF_NO FROM STG_CASA_TXNS WHERE V_ACCOUNT_NUMBER IN ({accs}));

PROMPT === Tong hop GD theo KH (doi chieu voi file KICH_BAN_TH02.md)
SELECT p.V_PARTY_ID, p.V_PARTY_TYPE, p.N_KYC_RISK, COUNT(t.V_TXN_REF_NO) SO_GD,
       SUM(CASE WHEN t.F_DRCR_INDICATOR='C' THEN t.N_TXN_AMT END) TONG_CO,
       SUM(CASE WHEN t.F_DRCR_INDICATOR='D' THEN t.N_TXN_AMT END) TONG_NO,
       MIN(t.D_TRANSACTION_DATE) TU_NGAY, MAX(t.D_TRANSACTION_DATE) DEN_NGAY
FROM STG_PARTY_MASTER p JOIN STG_CASA c ON c.V_CUST_REF_CODE=p.V_PARTY_ID
LEFT JOIN STG_CASA_TXNS t ON t.V_ACCOUNT_NUMBER=c.V_ACCOUNT_NUMBER
WHERE p.V_PARTY_ID IN ({ids}) GROUP BY p.V_PARTY_ID, p.V_PARTY_TYPE, p.N_KYC_RISK ORDER BY 1;
""")
with open(os.path.join(OUT, '99_ROLLBACK_XOA_DATA.sql'), 'w') as f:
    f.write(f"""-- XOA toan bo data bo sung TH02 (chi chay khi can lam lai). Xoa theo thu tu nguoc.
SET DEFINE OFF
DELETE FROM STG_FRONT_OFFICE_TXN_PARTY WHERE V_TXN_REF_NO IN (SELECT V_TXN_REF_NO FROM STG_CASA_TXNS WHERE V_ACCOUNT_NUMBER IN ({accs}));
DELETE FROM STG_TXN_ALT_CCY_VALUES WHERE V_TXN_REF_NO IN (SELECT V_TXN_REF_NO FROM STG_CASA_TXNS WHERE V_ACCOUNT_NUMBER IN ({accs}));
DELETE FROM STG_CASA_TXNS WHERE V_ACCOUNT_NUMBER IN ({accs});
DELETE FROM STG_ACCOUNT_ALT_CCY_VALUES WHERE V_ACCOUNT_NUMBER IN ({accs});
DELETE FROM STG_PARTY_ACCOUNT_ROLE_MAP WHERE V_ACCOUNT_NUMBER IN ({accs});
DELETE FROM STG_CASA WHERE V_ACCOUNT_NUMBER IN ({accs});
DELETE FROM STG_CORRESPONDENT_PROD_SERVED WHERE V_CORR_FIN_INST_ID IN ({ids});
DELETE FROM STG_PARTY_MSB_DETAILS WHERE V_PARTY_ID IN ({ids});
DELETE FROM STG_PARTY_PARTY_RELATIONSHIP WHERE V_PARTY_ID IN ({ids});
DELETE FROM STG_CUSTOMER_IDENTIFCTN_DOC WHERE V_CUST_REF_CODE IN ({ids});
DELETE FROM STG_PARTY_EMAIL_MAP WHERE V_PARTY_ID IN ({ids});
DELETE FROM STG_PARTY_PHONE_MAP WHERE V_PARTY_ID IN ({ids});
DELETE FROM STG_ADDRESS_MASTER WHERE V_ADDRESS_ID IN (SELECT V_ADDRESS_ID FROM STG_PARTY_ADDRESS_MAP WHERE V_PARTY_ID IN ({ids}));
DELETE FROM STG_PARTY_ADDRESS_MAP WHERE V_PARTY_ID IN ({ids});
DELETE FROM STG_PARTY_ROLE_MAP WHERE V_PARTY_ID IN ({ids});
DELETE FROM STG_PARTY_MASTER WHERE V_PARTY_ID IN ({ids});
COMMIT;
""")
import json; json.dump(EXPECT, open(os.path.join(OUT, '.expect.json'), 'w'))
print('TXN', 'TXN0021826 ->', f'TXN{txn_no:07d}')
for e in EXPECT: print(e)
