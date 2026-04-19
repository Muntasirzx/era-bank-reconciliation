import pandas as pd
import random
from datetime import datetime, timedelta

def generate_era_data():
    print("Generating Synthetic ERA Summary and Claims Data...")
    
    summary_records = []
    claims_records = []
    
    check_start = 100100000
    payers = ['BLUE CROSS', 'AETNA', 'CIGNA', 'UNITED HEALTHCARE', 'MEDICARE']
    procedures = ['99213', '99214', '71045', '80053', '93000']
    
    start_date = datetime(2023, 1, 1)

    for i in range(50):
        check_num = check_start + i
        check_date = start_date + timedelta(days=random.randint(0, 180))
        payer = random.choice(payers)
        
        num_claims = random.randint(5, 20)
        
        check_billed = 0
        check_allowed = 0
        check_paid = 0
        check_adj = 0
        
        for j in range(num_claims):
            claim_id = f"CLM-{check_num}-{j+1}"
            proc = random.choice(procedures)
            
            billed = round(random.uniform(150.0, 800.0), 2)
            allowed = round(billed * random.uniform(0.4, 0.8), 2)
            adj = round(billed - allowed, 2)
            paid = allowed # Assuming fully paid by primary for simplicity
            
            claims_records.append({
                'Claim_ID': claim_id,
                'Check_EFT_Number': check_num,
                'Procedure_Code': proc,
                'Billed_Amount': billed,
                'Allowed_Amount': allowed,
                'Contractual_Adj': adj,
                'Provider_Paid': paid
            })
            
            check_billed += billed
            check_allowed += allowed
            check_paid += paid
            check_adj += adj
            
        summary_records.append({
            'Check_EFT_Number': check_num,
            'Check_Date': check_date.strftime('%m/%d/%y'),
            'Payer': payer,
            'Total_Claims': num_claims,
            'Total_Billed': round(check_billed, 2),
            'Total_Allowed': round(check_allowed, 2),
            'Gross_Provider_Paid': round(check_paid, 2),
            'Provider_Adjustment': round(check_adj, 2),
            'Expected_Bank_Deposit': round(check_paid, 2)
        })

    df_summary = pd.DataFrame(summary_records)
    df_claims = pd.DataFrame(claims_records)
    
    # Save to the data directory (assuming script is run from project root)
    df_summary.to_csv('data/era_summary_load.csv', index=False)
    df_claims.to_csv('data/era_claims_load.csv', index=False)
    
    print("Success! 'era_summary_load.csv' and 'era_claims_load.csv' generated in the /data folder.")

if __name__ == "__main__":
    generate_era_data()