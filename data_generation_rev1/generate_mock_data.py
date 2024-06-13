import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()

# Number of mock customers
num_customers = 1000

# Generate mock data
data = {
    'customer_id': [fake.uuid4() for _ in range(num_customers)],
    'name': [fake.name() for _ in range(num_customers)],
    'email': [fake.email() for _ in range(num_customers)],
    'usage_frequency': np.random.poisson(lam=5, size=num_customers),  # Simulated usage frequency
    'support_tickets': np.random.poisson(lam=2, size=num_customers),  # Simulated support ticket count
    'nps_score': np.random.randint(0, 10, size=num_customers)  # Simulated Net Promoter Score
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('customer_data.csv', index=False)

print("Mock customer data generated and saved to customer_data.csv")
