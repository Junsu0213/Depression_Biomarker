# -*- coding:utf-8 -*-
"""
Created on Thu. Aug. 01 17:24:20 2023
@author: Jun-su Park
"""
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from brainflow.data_filter import DataFilter
import mne
from mne.preprocessing import ICA
from mne_connectivity import spectral_connectivity_epochs


class Parameter(object):
    def __init__(
            self,
            data_path=None,
            file_name=None,
            sub_name=None,
            fc_method='wpli',
            sfreq=125,
            ch_list=None,
            band_freq=None,
            roi=None
    ):
        if ch_list is None:
            ch_list = ['Fp1', 'F7', 'F3', 'T3', 'C3', 'Cz', 'P3', 'O1',
                       'Fp2', 'F4', 'F8', 'C4', 'T4', 'P4', 'O2']
        if band_freq is None:
            band_freq = {'Low alpha': (7, 10)}
            if roi is None:
                roi = {'L-C': [4], 'L-P': [6]}
        self.data_path = data_path
        self.file_name = file_name
        self.sub_name = sub_name
        self.fc_method = fc_method
        self.sfreq = sfreq
        self.ch_list = ch_list
        self.band_freq = band_freq
        self.roi = roi


class MDDAnalysis(object):
    def __init__(self, config: Parameter):
        self.config = config
        self.file_name = config.file_name
        self.sub_name = config.sub_name
        self.data_path = config.data_path
        self.ch_list = config.ch_list
        self.sfreq = config.sfreq
        self.band_freq = config.band_freq
        self.band = tuple(zip(*tuple(self.band_freq.values())))
        self.fc_method = config.fc_method
        self.band_freq = config.band_freq
        self.roi = config.roi

    def data_preprocessing(self):
        try:
            data = DataFilter.read_file(fr'.\DataBase\{self.file_name}.csv')
        except:
            data = pd.read_csv(fr'.\DataBase\{self.file_name}.csv')
            data = np.array(data).transpose()

        # EEG data (1 minute)
        eeg_data = data[1:16, self.sfreq * 60 * 1:self.sfreq * 60 * 2] / 1e6

        # creat EEG information
        eeg_info = mne.create_info(ch_names=self.ch_list, sfreq=self.sfreq, ch_types="eeg")
        data_ = mne.io.RawArray(eeg_data, info=eeg_info)

        # filtering
        filt_data = data_.copy().filter(l_freq=1., h_freq=40.)

        # set montage
        montage = mne.channels.make_standard_montage('standard_1020')
        filt_data.set_montage(montage)

        # independent component analysis (artifact remove)
        ica = ICA(n_components=15, max_iter='auto', random_state=7)
        ica.fit(filt_data)

        # muscle artifacts removing
        muscle_idx_auto, scores = ica.find_bads_muscle(filt_data)

        # muscle artifacts ICA scoring plot
        print('Automatically found muscle artifact ICA components: '
              f'{muscle_idx_auto}')

        # epoch
        epoch_data = mne.make_fixed_length_epochs(raw=filt_data, duration=2.)
        return epoch_data

    def biomarker_fc_analysis(self, epoch):
        # Functional connectivity analysis
        con = spectral_connectivity_epochs(data=epoch, names=self.ch_list, method=self.fc_method,
                                           fmin=self.band[0], fmax=self.band[1], faverage=True,
                                           mt_adaptive=True, n_jobs=1)
        # Adjacency matrix (channel, channel, band frequency)
        adj_mat = con.get_data(output='dense')
        biomarker = self.roi_conn(adj_mat=adj_mat)
        return biomarker

    def roi_conn(self, adj_mat):
        # ROI connectivity mean

        # frequency band information
        band_names = list(self.band_freq.keys())

        # ROI information
        roi_dic = self.roi
        roi_chlist = list(self.roi.keys())

        flat_mat = []
        for band, band_num in zip(band_names, range(len(band_names))):
            # data transpose
            conn = self.transpose(adj_mat[:, :, band_num])
            a = []
            for i in roi_chlist:
                for j in roi_chlist:
                    # roi 별 mean 값
                    num_conn = len(roi_dic[i]) * len(roi_dic[j])
                    if j == i:
                        conn_ = conn[roi_dic[i], :]
                        roi_conn = np.array(np.sum(conn_[:, roi_dic[j]]) / (num_conn - (len(roi_dic[j])))).reshape(1, 1)
                        a = np.append(a, roi_conn)
                    else:
                        conn_ = conn[roi_dic[i], :]
                        roi_conn = np.array(np.sum(conn_[:, roi_dic[j]]) / (num_conn)).reshape(1, 1)
                        a = np.append(a, roi_conn)
            flat_mat = np.append(flat_mat, a)
            # print(flat_mat.shape) # --> (roi_num*roi_num*band) ex. (2*2*2)
        return flat_mat[1]

    @staticmethod
    # transpose sum
    def transpose(con_data):
        tr_data = np.transpose(con_data)
        conn_data = con_data + tr_data
        return conn_data

    def biomarker_figure(self, biomarker_value):
        with open(r'.\open_dataset_biomarker.pickle', 'rb')as f:

            mdd, control = pickle.load(f)

            ax = sns.boxplot(data=[control, mdd], palette='pastel')
            plt.xticks(range(2), ['Control', 'MDD'])
            plt.title("MDD classification (LHCx)")
            if biomarker_value > 0.395:
                # 외부 데이터 포인트 생성
                plt.scatter(x=0, y=biomarker_value, c='Blue')
                plt.text(.05, biomarker_value - 0.014, "subject (Control)")
            else:
                plt.scatter(x=1, y=biomarker_value, c='Red')
                plt.text(1.05, biomarker_value - 0.014, "subject (MDD)")
        plt.savefig(rf'.\Figure\{self.sub_name}.png', dpi=300)
        plt.show()


if __name__ == '__main__':
    file_name = '2023-07-26-1447'
    sub_name = 'TEST'

    # parameter setting
    config = Parameter(file_name=file_name, sub_name=sub_name)

    # biomarker class load
    biomarker_analysis = MDDAnalysis(config=config)

    # preprocessing (BPF, Epoch)
    epoch_data = biomarker_analysis.data_preprocessing()

    # Biomarker value extraction (FC analysis)
    LHCx_score = biomarker_analysis.biomarker_fc_analysis(epoch=epoch_data)

    # figure plot
    biomarker_analysis.biomarker_figure(biomarker_value=LHCx_score)