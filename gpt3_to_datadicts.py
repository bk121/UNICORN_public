import json
import pandas as pd 
import time
import openai
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")


openai.api_key = api_key

def call_gpt3(filepath, filename, column, dtypes, prompt):
    df = pd.read_csv(filepath + filename, dtype=dtypes)
    values = df[column].unique()

    with open('gpt_responses/'+filename[:-4]+'/'+column+'.txt', 'w') as f:
        for value in values:
            try:
                response = openai.Completion.create(
                    model="text-davinci-002",
                    prompt=prompt+str(value)+'\nOutput:',
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
                    prompt=prompt+str(value)+'\nOutput:',
                    temperature=0,
                    max_tokens=64,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                )
            text = str(value)+': '+response['choices'][0]['text']
            f.write(text+'\n')
            f.flush()
            print(text)




# call_gpt3('output/Consolidated/','MEDICAL HISTORY.csv', 'AGE OF ONSET', {'AGE OF ONSET':str}, prompts.months)

# call_gpt3('output/Consolidated/','MEDICAL HISTORY.csv', 'AGE AT DIAGNOSIS', {'AGE AT DIAGNOSIS':str}, prompts.months)

# call_gpt3('output/Consolidated/','MEDICAL HISTORY.csv', 'PATTERN', {'PATTERN':str}, prompts.pattern)










def processgpt3(filepath, filename):
    with open('gpt_responses/'+filepath+filename, 'r') as f:
        text=f.read().strip().split('\n')


    text = list(map(lambda x: x.split(':'), text))
    text = [[a, b.strip()] for a, b in text]


    gpt_dict = dict()

    for value, key in text:
        if key not in gpt_dict:
            gpt_dict[key]=[value]
        else:
            gpt_dict[key].append(value)

    print(gpt_dict)

    with open('gpt_responses/'+filepath+filename[:-4]+' DICT.json', 'w') as f:
        json.dump(gpt_dict, f, ensure_ascii=False, indent=4)

    with open('data_dicts/'+filepath[:-1]+'.json', 'r+') as f:
        property_values=json.load(f)
        property_values[filename[:-4]]=json.loads(json.dumps(gpt_dict))
        f.seek(0)
        f.truncate()
        json.dump(property_values, f, indent=4, ensure_ascii=False)


# process('MEDICAL HISTORY/','AGE OF ONSET.txt')
# process('MEDICAL HISTORY/','AGE AT DIAGNOSIS.txt')


