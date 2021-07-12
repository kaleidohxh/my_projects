import numpy as np
import pandas as pd

def MergeAttentionData(eyetrackingfile, qualtricsfile):
    """
    This function eyetracking output file with qualtrics output file so eye tracking data (e.g. fixation count)
    can be mapped onto the qualtrics output per participant, per repetition condition.
    :param eyetrackingfile: eye tracking output csv file (from iMotions)
    :param qualtricsfile: online questionnaire output csv file (from Qualtrics)
    :return: merged csv file
    """

    #first read the eyetracking data csv file, with specified variables
    column_name = ['Respondent Name', 'Label', 'Time spent-G (ms)', 'TTFF-F (ms)', 'Time spent-F (ms)', 'Fixations Count']
    df = pd.read_csv(eyetrackingfile, header=0, usecols=column_name)
    all_data = df.dropna(subset=['Fixations Count'])

    #next read the qualtrics csv file
    qualtrics_df = pd.read_csv(qualtricsfile, header=0)
    qualtrics_df['random_order'] = qualtrics_df.loc[:, 'random_order'].str.split('|')
    qualtrics_order = qualtrics_df[['random_order', 'participant']]

    #the random_order column contains lists of stimuli repetition order for each participant
    #expand the lists so for every participant, each repetition represents a row
    qualtrics_order = qualtrics_order.explode('random_order').reset_index()

    qualtrics_order = qualtrics_order.rename_axis('myindex').sort_values(by=['participant', 'myindex'], ascending=[False, True])
    qualtrics_order_sort = qualtrics_order.reset_index().drop(['myindex', 'index'], axis=1)
    all_data = all_data.reset_index()

    #merge the two files based on reset index
    merge_data = all_data.merge(qualtrics_order_sort, how='left', left_index=True, right_index=True)
    fixation_data = merge_data.loc[:, ['Respondent Name', 'TTFF-F (ms)', 'Time spent-F (ms)', 'Fixations Count', 'random_order']]
    output = fixation_data.set_index(['Respondent Name', 'random_order']).unstack(['random_order'])

    return output

# if '__name__' == '__main__':
    # output_p = MergeAttentionData('p_n=17_p3-27.csv', 'ad choice study_personalization _July 12, 2021_12.01.csv')
    # output_p.to_csv('output_p.csv')

