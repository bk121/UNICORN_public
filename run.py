from flask import Flask, request, send_file
import tempfile
import pandas as pd
from construct import merge_dfs, gen_gpt3_df
app = Flask(__name__)


@app.route('/')
def index():
    return '<p> working </p>'
  
  
@app.route('/plain', methods=['GET'])
def plain_request():
    project = request.args['project']
    dataset = request.args['dataset']
    column_parser = request.args['column parser']
    prop = request.args['property']
    original_df = pd.read_csv('datasets/'+project+'/output/Consolidated/'+dataset+'.csv', dtype={prop:str})
    modified_df = pd.read_csv('datasets/'+project+'/processed/'+dataset+'.csv', dtype={prop:str})
    new_df = merge_dfs(original_df, modified_df, prop)
    
    with tempfile.NamedTemporaryFile() as temp:
        print(temp.name)
        new_df.to_csv(temp.name)
        return send_file(temp.name, download_name='file.csv', as_attachment=True)
    

@app.route('/prompt', methods=['GET'])
def prompt_request():
    project = request.args['project']
    dataset = request.args['dataset']
    column_parser = request.args['column parser']
    prop = request.args['property']
    prompt = request.args['prompt']
    original_df = pd.read_csv('datasets/'+project+'/output/Consolidated/'+dataset+'.csv', dtype={prop:str})
    gpt3_df = gen_gpt3_df(original_df, prop, prompt)    
    new_df = merge_dfs(original_df, gpt3_df, prop)

    with tempfile.NamedTemporaryFile() as temp:
        new_df.to_csv(temp.name)
        return send_file(temp.name, download_name='file.csv', as_attachment=True)
