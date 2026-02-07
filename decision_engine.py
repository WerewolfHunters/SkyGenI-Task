import pandas as pd
import numpy as np

# Data Preparation
df = pd.read_csv('data/skygeni_sales_data.csv')

# Clean outcome
df['outcome_clean'] = df['outcome'].astype(str).str.strip().str.lower()
df['is_won'] = (df['outcome_clean'] == 'won').astype(int)

# Dates
df['created_date'] = pd.to_datetime(df['created_date'])
df['closed_date'] = pd.to_datetime(df['closed_date'])

# Sales cycle
df['sales_cycle_days'] = (df['closed_date'] - df['created_date']).dt.days


# Decision Engine Implementation
def deal_risk_engine(
    data,
    cycle_weight=0.4,
    stagnation_weight=0.3,
    stage_weight=0.3,
    stagnation_threshold=None,
    top_n=10
):
    """
    Interactive Deal Risk Scoring Engine
    """

    df = data.copy()

    # --- Normalize sales cycle risk ---
    df['cycle_risk'] = (
        df['sales_cycle_days'] - df['sales_cycle_days'].min()
    ) / (
        df['sales_cycle_days'].max() - df['sales_cycle_days'].min()
    )

    # --- Stagnation threshold ---
    if stagnation_threshold is None:
        stagnation_threshold = df['sales_cycle_days'].median()

    df['stagnation_risk'] = (df['sales_cycle_days'] > stagnation_threshold).astype(int)

    # --- Stage-level risk ---
    stage_loss_rate = (
        df.groupby('deal_stage')['is_won']
        .apply(lambda x: 1 - x.mean())
    )

    df['stage_risk'] = df['deal_stage'].map(stage_loss_rate)

    # --- Final risk score ---
    df['deal_risk_score'] = (
        cycle_weight * df['cycle_risk'] +
        stagnation_weight * df['stagnation_risk'] +
        stage_weight * df['stage_risk']
    )

    # --- Sort & return actionable output ---
    result = df.sort_values(by='deal_risk_score', ascending=False)

    return result[[
        'deal_id',
        'deal_stage',
        'sales_cycle_days',
        'deal_amount',
        'deal_risk_score'
    ]].head(top_n)



if __name__=="__main__":

#     result = deal_risk_engine(
#     df,                         
#     cycle_weight=0.6,           
#     stagnation_weight=0.2,
#     stage_weight=0.2
# )
    result = deal_risk_engine(
    df,
    stagnation_threshold=30,
    top_n=15
)

    
    print(result)