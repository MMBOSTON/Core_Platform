import pandas as pd

# Load the mock data
df = pd.read_csv('customer_data.csv')

# Define key metrics for customer health
def calculate_health_score(row):
    usage_score = row['usage_frequency']
    support_score = 10 - row['support_tickets']  # Assuming more tickets is bad
    nps_score = row['nps_score']
    health_score = (usage_score + support_score + nps_score) / 3
    return health_score

df['health_score'] = df.apply(calculate_health_score, axis=1)

# Save the updated DataFrame
df.to_csv('customer_health_data.csv', index=False)

print("Customer health scores calculated and saved to customer_health_data.csv")
