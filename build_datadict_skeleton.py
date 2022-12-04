import subprocess
import pandas as pd



def build_skeleton(project):
    consolidated_datasets = project + '/'+'output/Consolidated'
    for file in subprocess.check_output(['ls', consolidated_datasets]).decode('utf-8').split('\n'):
        if file[-3:]=='csv':
            df=pd.read_csv(consolidated_datasets + file)
            cols = df.columns.tolist()
            print(cols)
            with open(project+'/data_dicts_skeleton/'+file[:-4]+'.json', 'w') as f:
                f.write('{\n')
                for index, col in enumerate(cols):
                    f.write('   "'+col+'": {\n')
                    f.write('   }')
                    if index+1!=len(cols):
                        f.write(',\n')
                    else: 
                        f.write('\n')
                f.write('}\n')
    