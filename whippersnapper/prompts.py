from langchain.prompts import PromptTemplate

generate_sql_prompt = PromptTemplate(
    input_variables=['question', 'columns', 'samples', 'table_name'],
    template='''
# Context
Your job is to write a sql query that answers the following question:
{question}

Below is a list of columns and their datatypes. Your query should only use the data contained in the table. The table name is `{table_name}`.

# Columns
{columns}

# Samples
{samples}

If the question is not a question or is answerable with the given columns, respond to the best of your ability or say the question can't be answered.
Do not use columns that aren't in the table.
Ensure that the query runs and returns the correct output.

# Query:
'''
)

sql_rewriter_prompt = PromptTemplate(
    input_variables=['question', 'columns', 'samples', 'table_name', 'query'],
    template='''
# Context
Your job is to identify why a segment of a query produced an error, then rewrite it to make it work.
If the question cannot be answered with the given dataset, say that the question cannot be answered and briefly explain why.
Wrap the query in triple backticks, like markdown.

#### EXAMPLE ####
The query didn't work because you used the column "name", which doesn't exist. It should use the column "first_name" instead.
The query also is missing a semi-colon at the end. Here's a working version

```
SELECT
  first_name,
  SUM(1) AS total_people
FROM people
GROUP BY
  first_name
LIMIT 10;
```
#################


# Initial question
{question}

# Table name
{table_name}

# Columns
{columns}

# Samples
{samples}

# Original query
{query}

# Rewritten code
'''
)

summarizer_prompt = PromptTemplate(
    input_variables=['question', 'query', 'answer'],
    template='''
# Context
Your job is to summarize the answer to a data question and give a brief explanation of the methodology/approach.
Be concise and call out any caveats.


# Question
{question}

# Query
{query}

# Answer
{answer}

# Summary and methodology
'''
)