import pandas as pd
from sqlalchemy import create_engine

# Database connection
# Replace with your database URI
DATABASE_URI = "postgresql://Biswanathdas:Papun$1996@post-db-ai.postgres.database.azure.com/azure-sales-data"
engine = create_engine(DATABASE_URI)

# Fetch all table names
table_names = engine.table_names()

# Join all tables
if table_names:
    first_table = table_names[0]
    df = pd.read_sql(f"SELECT * FROM {first_table}", engine)

    for table in table_names[1:]:
        temp_df = pd.read_sql(f"SELECT * FROM {table}", engine)
        # Replace 'common_column' with the column you want to join on
        df = pd.merge(df, temp_df, how='outer',
                      left_on='common_column', right_on='common_column')

# Save to CSV
df.to_csv("output.csv", index=False)
