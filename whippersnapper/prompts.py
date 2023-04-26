from langchain.prompts import PromptTemplate

generate_code_prompt = PromptTemplate(
    input_variables=['question', 'sample_rows', 'columns', 'df_name'],
    template='''
# Context
Your job is to write python code to answers the following question:
{question}

Use the sample below and columns to understand the data in the table and the column names. 
Your query should only use the columns contained in the table. 


# Columns
{columns}

# Sample rows
{sample_rows}

If the question is not a question or is answerable with the given columns, say you can't answer the question.
Do not use columns that aren't in the table.
Ensure that the code runs and returns the correct output.
Wrap the code in a function that accepts the dataframe as an argument and prints the result. Call the function on the dataframe `{df_name}`.

# Code:
'''
)

code_rewriter_prompt = PromptTemplate(
    input_variables=['question', 'code', 'error', 'df_name'],
    template='''
# Context
Your job is to identify why a segment of code produced an error, then rewrite it to make it work.
If the code inticates that the question cannot be answered, say that the question cannot be answered and why
Wrap the code in a function that accepts the dataframe as an argument and prints the result. Call the function on the dataframe `{df_name}`.
Wrap all code in triple backticks, like markdown.

#### EXAMPLE ####
The code didn't work because it uses a plus sign instead of a minus sign. Here's the updated code:


```
a = 1
b = 2

print(a + b)
```


# Initial question
{question}

# Code
{code}

# Error
{error}

# Rewritten code
'''
)