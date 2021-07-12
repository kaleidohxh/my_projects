import pandas as pd
import numpy as np

immersion_coding = pd.read_csv('Imported table-Grid view.csv', header=0, encoding='utf-8')
immersion_review = pd.read_csv('immersion_review0307-Grid view.csv', header=0, encoding='utf-8', usecols=['Key', 'Author', 'Title'])

def structure_title(df:pd.DataFrame):
    df['Title'] = df.loc[:, 'Title'].str.split().str.join(' ')
    return df

immersion_coding_title_structured = structure_title(immersion_coding)
immersion_review_title_structured = structure_title(immersion_review)

immersion_merge = immersion_coding_title_structured.merge(immersion_review_title_structured, how='left', on='Title')
immersion_merge.to_csv('merge2.csv')


