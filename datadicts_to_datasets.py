import json
import pandas as pd
import numpy as np
import subprocess


def process(input_file, output_file, data_dict):
    df = pd.read_csv(input_file, low_memory=False)
    with open(data_dict) as f:
        property_values=json.load(f)
    for property in property_values.keys():
        for key in property_values[property]:
            for value in property_values[property][key]:
                df.loc[df[property]==value, property]=key
        # df.loc[pd.isna(df[property]), property] = 'unknown'
    df.to_csv(output_file, index=False)
    print('finished '+output_file[10:])



for file in subprocess.check_output(['ls', 'output/Consolidated']).decode('utf-8').split('\n'):
    if file[-3:]=='csv':
        print('processing '+file)
        process('output/Consolidated/'+file, 'processed/'+file, 'data_dicts/'+file[:-4]+'.json')


