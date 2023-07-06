import re
import sqlite3
from pathlib import Path
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from .prompts import *


QUERY_FAILED = '<query_failed>'

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def query_database(db_path, query, max_rows=20):
    
    try:
        with sqlite3.connect(db_path) as connection:

            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchmany(max_rows)   # limit rows
            columns = tuple([x[0] for x in cursor.description])
            
            return pd.DataFrame(rows, columns=columns)
    
    except:
        return QUERY_FAILED
    
    
def get_schema(db_path, table_name):
    
    command = f"PRAGMA table_info('{table_name}')"
    
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(command)
        rows = [row[1:3] for row in cursor.fetchall()]
        
    return rows
    

def extract_code(text):
    pattern = r'```(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    
    return match.group(1).strip().strip('python').strip() if match else None

sql_generator = LLMChain(
    llm=ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.1, max_tokens=2048), 
    prompt=generate_sql_prompt
)

sql_rewriter = LLMChain(
    llm=ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.1, max_tokens=2048), 
    prompt=sql_rewriter_prompt
)

summarizer = LLMChain(
    llm=ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5, max_tokens=2048), 
    prompt=summarizer_prompt
)


def answer_question(question, path_to_db, table_name):

    schema = str(get_schema(path_to_db, table_name))
    df_samples = query_database(path_to_db, 'SELECT * FROM {table_name} LIMIT 3;')
    samples = str([tuple(df_samples.columns.tolist())] + [row[1:] for row in df_samples.to_records().tolist()])
    
    # generate the initial query
    sql_query = sql_generator.run({
        'question': question, 
        'columns': schema, 
        'samples': samples, 
        'table_name': table_name
    })

    # run the query against the database
    db_response = query_database(path_to_db, sql_query)

    # fix the query if necessary
    if str(db_response) == QUERY_FAILED:
        answer_raw = sql_rewriter.run({
            'question': question, 
            'columns': schema, 
            'samples': samples, 
            'table_name': table_name,
            'query': sql_query
        })
        
        sql_query = extract_code(answer_raw)
        answer = query_database(path_to_db, sql_query)
    else:
        answer = db_response
        
    # generate a summary of the result and the methodology
    summarized_response = summarizer.run({
        'question': question, 
        'query': sql_query, 
        'answer': answer
    })

    return {
        'summary': summarized_response,
        'sql_query': sql_query,
        'answer': answer
    }

if __name__ == '__main__':

    question = 'What year had the highest rated games on average?'
    table_name = 'steam_games'
    path_to_db = Path.cwd() / '..' / 'tests' / 'datasets' / 'steam_games.db'

    results = answer_question(
        question=question,
        path_to_db=path_to_db, 
        table_name=table_name 
    )

    print(results)