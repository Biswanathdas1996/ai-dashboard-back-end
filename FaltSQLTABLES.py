import pandas as pd
from sqlalchemy import create_engine, inspect

# Database connection
# Replace with your database URI
DATABASE_URI = "postgresql://Biswanathdas:Papun$1996@post-db-ai.postgres.database.azure.com/azure-sales-data"
engine = create_engine(DATABASE_URI)

inspector = inspect(engine)
table_names = inspector.get_table_names()


print(table_names)

dfs = [pd.read_sql(f"SELECT * FROM {table}", engine) for table in table_names]
df = pd.concat(dfs, ignore_index=True)

for table in table_names[1:]:
    temp_df = pd.read_sql(f"SELECT * FROM {table}", engine)

    # Convert columns to the same data type
    common_columns = df.columns.intersection(temp_df.columns).tolist()
    for col in common_columns:
        if df[col].dtype != temp_df[col].dtype:
            df[col] = df[col].astype(str)
            temp_df[col] = temp_df[col].astype(str)

    df = pd.merge(df, temp_df, how='outer', on=common_columns)

df.to_csv("concatenated_output.csv", index=False)
