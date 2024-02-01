# -*- coding:utf-8 -*-
"""
Created on Wed. Jul. 26 17:03:42 2023
@author: Jun-su Park
"""
import glob
import pickle
import pandas as pd
import numpy as np

from Analysis.data_analysis import DataAnalysis
from Config.config import OpenDatasetConfig


class FcAnalysis(object):
    def __init__(self, config: OpenDatasetConfig):
        self.config = config
        self.flist = glob.glob(fr'A:\DataBase\MDD_open_data\epoch\*')
        self.severity_range = {'normal': (0, 7), 'mdd': (13, 63)}
        self.analysis = DataAnalysis(config=config)

    def fc_analysis(self):
        # open csv file
        data_info_df = pd.read_excel(rf'A:\DataBase\MDD_open_data\bdi_score.xlsx', engine='openpyxl')

        # BDI score
        bdi_score = data_info_df['BDI'].values

        # label score
        labels = self.label_bdi_scores(bdi_scores=bdi_score, severity_ranges=self.severity_range)

        all_feature = {}
        for fpath, bdi, label in zip(self.flist, bdi_score, labels):
            sub_name = fpath.split('\\')[-1].split('.')[0]

            # open pickle file
            with open(fpath, 'rb') as f:
                epoch_data = pickle.load(f)

            # FC analysis
            _, adj_mat = self.analysis.fc_analysis(epoch=epoch_data)

            data = {'fc': adj_mat, 'label': label}
            all_feature[sub_name] = data
        with open(rf'A:\DataBase\MDD_open_data\fc_matrix\fc_data.pickle', 'wb') as f:
            pickle.dump(all_feature, f)

    @staticmethod
    def label_bdi_scores(bdi_scores, severity_ranges):
        labels = []
        keys = severity_ranges.keys()
        for score in bdi_scores:
            label = np.NaN
            for label_score, score_range in zip(range(len(keys)), severity_ranges.values()):
                if score >= score_range[0] and score <= score_range[1]:
                    label = label_score
                    break
            labels.append(label)
        return labels


if __name__ == '__main__':
    config = OpenDatasetConfig()
    FcAnalysis(config=config).fc_analysis()