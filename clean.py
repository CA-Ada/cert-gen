import os
import pandas as pd
import yaml
from os import listdir
from os.path import isfile, join
from pathlib import Path


# get the name of csv


def getNameCsv(path):
    onlyfiles = [f for f in listdir(path)
                 if isfile(join(path, f))]
    return onlyfiles


def readYAML(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

# clean  multiple csv from google meets


def cleanCert(hours):
    config_file = readYAML('config.yaml')
    input_name = config_file['input_name']
    output = pd.DataFrame(columns=['NAME', 'HOURS'])
    output.to_csv(input_name, index=False)
    csvs = getNameCsv('csv')
    csvs.sort()
    try:
        for csv, hour in zip(csvs, hours):
            print(csv)
            print(hour)
            df2 = pd.read_csv('output.csv', sep=',')
            p = Path('csv/' + csv)
            df = pd.read_csv(p, sep=',')
            try:
                df['Nome'] = df['Nome'] + ' ' + df['Sobrenome']
            except:
                print("Column %s was not found in %s" % 'Sobrenome', csv)
            try:
                df.drop(df.loc[:, df.columns != "Nome"], inplace=True, axis=1)
                df.rename(columns={'Nome': 'NAME'}, inplace=True)
                df['HOURS'] = hour
                df = df.merge(df2, on='NAME', how='outer').fillna(0)
                df['HOURS'] = df['HOURS_x'] + df['HOURS_y']
                df.drop(columns=['HOURS_x', 'HOURS_y'], inplace=True)
                df.to_csv(input_name, index=False)
            except:
                print("Unable to clean %s", csv)
    except:
        print("No cvs found")


if __name__ == '__main__':
    config_file = readYAML('config.yaml')
    cleanCert(config_file['cleaner_hours'])
