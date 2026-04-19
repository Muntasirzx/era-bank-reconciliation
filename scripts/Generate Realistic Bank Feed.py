import pandas as pd
import random
from datetime import datetime, timedelta

def generate_realistic_bank():
    print("Reading Expected ERA Summary Data...")
    
    try:
        df_era = pd.read_csv("data/era_summary_load.csv")
    except FileNotFoundError:
        print("Error: Could not find data/era_summary_load.csv.")
        return

    # Clean data if it contains formatting
    if df_era['Expected_Bank_Deposit'].dtype == 'object':
        df_era['Expected_Bank_Deposit'] = df_era['Expected_Bank_Deposit'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
    
    df_era['Check_Date'] = pd.to_datetime(df_era['Check_Date'], format='%m/%d/%y')

    bank_records = []
    txn_counter = 500100

    total_checks = len(df_era)
    match_target = int(total_checks * 0.65)  # 65% Perfect Matches
    short_target = int(total_checks * 0.20)  # 20% Underpayments (Bank Fees)

    checks = df_era.to_dict('records')
    random.shuffle(checks)

    print(f"Generating Bank Feed: {match_target} Matches, {short_target} Short Pays, and {total_checks - match_target - short_target} Missing...")

    for i, check in enumerate(checks):
        if i < match_target:
            deposit_amt = check['Expected_Bank_Deposit']
        elif i < (match_target + short_target):
            fee = round(check['Expected_Bank_Deposit'] * random.uniform(0.01, 0.03), 2)
            deposit_amt = round(check['Expected_Bank_Deposit'] - fee, 2)
        else:
            continue

        dep_date = check['Check_Date'] + timedelta(days=random.randint(1, 2))

        bank_records.append({
            'Bank_Txn_ID': f"TXN-{txn_counter}",
            'Deposit_Date': dep_date.strftime("%Y-%m-%d"),
            'Check_EFT_Number': str(check['Check_EFT_Number']),
            'Payer_Name': check['Payer'],
            'Deposit_Amount': deposit_amt,
            'Transaction_Type': "ACH CREDIT",
            'Status': "CLEARED"
        })
        txn_counter += 1

    # Inject Noise Transactions
    for _ in range(150):
        noise_date = df_era['Check_Date'].min() + timedelta(days=random.randint(0, 30))
        bank_records.append({
            'Bank_Txn_ID': f"TXN-{txn_counter}",
            'Deposit_Date': noise_date.strftime("%Y-%m-%d"),
            'Check_EFT_Number': str(random.randint(200000000, 999999999)),
            'Payer_Name': random.choice(['BLUE CROSS', 'AETNA', 'CIGNA', 'UNITED HEALTHCARE', 'CASH PAY']),
            'Deposit_Amount': round(random.uniform(500.0, 15000.0), 2),
            'Transaction_Type': "WIRE TRANSFER",
            'Status': "CLEARED"
        })
        txn_counter += 1

    df_bank = pd.DataFrame(bank_records)
    df_bank = df_bank.sample(frac=1).reset_index(drop=True)
    
    df_bank.to_csv("data/bank_feed_load.csv", index=False)
    print("Success! 'bank_feed_load.csv' generated.")

if __name__ == "__main__":
    generate_realistic_bank()