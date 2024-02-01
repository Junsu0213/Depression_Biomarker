# -*- coding:utf-8 -*-
"""
Created on Wed. Jul. 26 16:14:23 2023
@author: Jun-su Park

** PRED + CT (http://predict.cs.unm.edu/) **
Project Name: Depression Rest

S01-S121 (control: 75, MDD: 46)

channels: ['Fp1', 'Fpz', 'Fp2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'Fz',
           'F2', 'F4', 'F6', 'F8', 'FT7', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2',
           'FC4', 'FC6', 'FT8', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4',
           'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6',
           'TP8', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'PO7',
           'PO5', 'PO3', 'POz', 'PO4', 'PO6', 'PO8', 'O1', 'Oz', 'O2']
data length: 6 min
sfreq: 500 Hz
"""


class OpenDatasetConfig(object):
    def __init__(
            self,
            data_path=r'C:\Users\User\Desktop\PyCharm Projects\MDD_biomarker',
            fc_method='wpli',
            psd_method='welch',
            sfreq=500,
            ch_list=None,
            band_freq=None
    ):
        if ch_list is None:
            ch_list = ['Fp1', 'Fpz', 'Fp2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'Fz',
                       'F2', 'F4', 'F6', 'F8', 'FT7', 'FC5', 'FC3', 'FC1', 'FCz', 'FC2',
                       'FC4', 'FC6', 'FT8', 'T7', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4',
                       'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPz', 'CP2', 'CP4', 'CP6',
                       'TP8', 'P7', 'P5', 'P3', 'P1', 'Pz', 'P2', 'P4', 'P6', 'P8', 'PO7',
                       'PO5', 'PO3', 'POz', 'PO4', 'PO6', 'PO8', 'O1', 'Oz', 'O2']
        if band_freq is None:
            band_freq = {'Low alpha': (8, 11)}
        self.data_path = data_path
        self.fc_method = fc_method
        self.psd_method = psd_method
        self.sfreq = sfreq
        self.ch_list = ch_list
        self.band_freq = band_freq