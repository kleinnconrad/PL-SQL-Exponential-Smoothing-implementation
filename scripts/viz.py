import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Setup & Generate Mock Data (Simulating the 'source_table')
np.random.seed(42)
dates = pd.date_range(start='2026-04-01', periods=30, freq='D')

# Simulated churn numbers with a slight trend and noise
base_trend = np.linspace(30, 80, 30)
noise = np.random.normal(0, 15, 30)
churners_raw = np.maximum(0, base_trend + noise).astype(int)

df = pd.DataFrame({'Date': dates, 'Churners': churners_raw})

# 2. Apply Exponential Smoothing (Equivalent to the PL/SQL logic)
# alpha = 0.2 as defined in the original PL/SQL script
alpha_val = 0.2
df['Smoothed_Alpha_0.2'] = df['Churners'].ewm(alpha=alpha_val, adjust=False).mean()

# 3. Concise and appealing visualization
sns.set_theme(style="whitegrid", context="talk")
plt.figure(figsize=(14, 7))

# Raw data as a subtle bar chart in the background
plt.bar(df['Date'], df['Churners'], 
        color='#9CB4D4', alpha=0.6, label='Actual Churners (Raw Data)')

# Smoothed values as a prominent line in the foreground
plt.plot(df['Date'], df['Smoothed_Alpha_0.2'], 
         color='#D9381E', linewidth=3.5, marker='o', markersize=8,
         label=f'Exponential Smoothing (α={alpha_val})')

# Chart formatting
plt.title('Effect of Exponential Smoothing on Churn Rates', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Date', fontsize=14, labelpad=10)
plt.ylabel('Number of Churners', fontsize=14, labelpad=10)
plt.xticks(rotation=45)

# Optimize legend and layout
plt.legend(loc='upper left', frameon=True, shadow=True)
plt.tight_layout()

# Save the plot as a PNG file in the same folder as your script
plt.savefig('exponential_smoothing_chart.png', dpi=300, bbox_inches='tight')
print("Chart successfully saved as 'exponential_smoothing_chart.png'")

