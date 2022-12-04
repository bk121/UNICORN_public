import pandas as pd
import openai
import time
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")


openai.api_key = api_key

def merge_dfs(original_df, modified_df, prop):
    study_series = original_df['STUDYID']
    subject_series = original_df['SUBJID']
    original_values = original_df[prop]
    new_values = modified_df[prop]
    new_df = pd.DataFrame({'STUDYID':study_series, 'SUBJID':subject_series, prop+'_ORIGINAL':original_values, prop+'_MODIFIED':new_values})
    return new_df


def gen_gpt3_df(original_df, prop, prompt):
    gpt3_df = original_df.copy()
    prop_vals = gpt3_df[prop].copy()
    unique_prop_values = gpt3_df[prop].unique()
    data_dict = {}
    for unique_prop_val in unique_prop_values:
        unique_prop_val=str(unique_prop_val)
        try:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt+unique_prop_val+'\nOutput: ',
                temperature=0,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
        except: 
            print('waiting one minute')
            time.sleep(61)
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt+unique_prop_val+'\nOutput: ',
                temperature=0,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
        new_val = response['choices'][0]['text'].strip()
        print('old val: ' + unique_prop_val+'   new val: '+new_val)
        data_dict[unique_prop_val] = new_val
    for idx, prop_val in enumerate(prop_vals):
        if (not pd.isnull(prop_val)):
            prop_vals[idx] = data_dict[prop_val]
    gpt3_df[prop]=prop_vals
    return gpt3_df