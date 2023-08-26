import os
from langchain import SQLDatabase
from langchain.llms import AzureOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts.prompt import PromptTemplate

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["OPENAI_API_BASE"] = "https://soumenopenai.openai.azure.com"
os.environ["OPENAI_API_KEY"] = "3a5a6eba4d2546558d3fa749ef9fb5ce"


_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the table foobar, they really mean the employee table.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)


# input_db = SQLDatabase.from_uri(
#     'postgresql://Biswanathdas:Papun$1996@post-db-ai.postgres.database.azure.com/azure-sales-data')
# print(input_db)
# llm_1 = AzureOpenAI(deployment_name="gpt-35-turbo",
#                     model_name="gpt-35-turbo",)
# db_agent = SQLDatabaseChain(llm=llm_1,
#                             database=input_db,
#                             verbose=True)
# result = db_agent.run(
#     "what is the total order value of Holmes? ")
# print(result)

def connect(dbUri):

    input_db = SQLDatabase.from_uri(dbUri)
    return input_db


def searchInDB(dbUri, question):
    db = connect(dbUri)
    llm_1 = AzureOpenAI(deployment_name="gpt-35-turbo",
                        model_name="gpt-35-turbo",)

    db_agent = SQLDatabaseChain(llm=llm_1,
                                database=db,
                                verbose=False,
                                # prompt=PROMPT
                                )

    result = db_agent.run(question)
    return result
