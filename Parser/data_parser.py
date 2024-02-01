# -*- coding:utf-8 -*-
"""
Created on Wed. Jul. 26 17:10:22 2023
@author: Jun-su Park
"""
import glob
import pickle
import mne
import scipy.io as sio
import numpy as np
from Config.config import OpenDatasetConfig


class OpenDataParser(object):
    def __init__(self, config: OpenDatasetConfig):
        self.config = config
        self.data_path = config.data_path
        self.ch_list = config.ch_list
        self.sfreq = config.sfreq

    def epoch_data_save(self):
        flist = glob.glob(r'A:\DataBase\MDD_open_data\raw\*.mat')

        # data epoch
        for sub in flist:

            # subject name
            sub_name = sub.split("\\")[-1].split("_")[0]

            # load data
            raw_data = sio.loadmat(sub)

            # event
            event = raw_data["EEG"]["event"]
            event_len = event[0][0][0].shape[0]

            # event list
            event_ec_1 = []
            event_ec_end_1 = []
            event_ec_2 = []
            event_ec_end_2 = []
            event_ec_3 = []
            event_ec_end_3 = []
            for j in range(event_len):
                if str(event[0][0][0][j][0][0]) == '11':
                    event_ec_1.append(int(event[0][0][0][j][1][0][0]))
                elif str(event[0][0][0][j][0][0]) == '1':
                    event_ec_end_1.append(int(event[0][0][0][j][1][0][0]))
                elif str(event[0][0][0][j][0][0]) == '13':
                    event_ec_2.append(int(event[0][0][0][j][1][0][0]))
                elif str(event[0][0][0][j][0][0]) == '3':
                    event_ec_end_2.append(int(event[0][0][0][j][1][0][0]))
                elif str(event[0][0][0][j][0][0]) == '15':
                    event_ec_3.append(int(event[0][0][0][j][1][0][0]))
                elif str(event[0][0][0][j][0][0]) == '5':
                    event_ec_end_3.append(int(event[0][0][0][j][1][0][0]))
            try:
                event_close_start_1 = event_ec_1[0]
                event_close_end_1 = event_ec_end_1[-1]
                event_close_start_2 = event_ec_2[0]
                event_close_end_2 = event_ec_end_2[-1]
                event_close_start_3 = event_ec_3[0]
                event_close_end_3 = event_ec_end_3[-1]
            except IndexError:
                for j in range(event_len):
                    if event[0][0][0][j][0][0] == 11:
                        event_ec_1.append(int(event[0][0][0][j][1][0][0]))
                    elif event[0][0][0][j][0][0] == 1:
                        event_ec_end_1.append(int(event[0][0][0][j][1][0][0]))
                    elif event[0][0][0][j][0][0] == 13:
                        event_ec_2.append(int(event[0][0][0][j][1][0][0]))
                    elif event[0][0][0][j][0][0] == 3:
                        event_ec_end_2.append(int(event[0][0][0][j][1][0][0]))
                    elif event[0][0][0][j][0][0] == 15:
                        event_ec_3.append(int(event[0][0][0][j][1][0][0]))
                    elif event[0][0][0][j][0][0] == 5:
                        event_ec_end_3.append(int(event[0][0][0][j][1][0][0]))
                event_close_start_1 = event_ec_1[0]
                event_close_end_1 = event_ec_end_1[-1]
                event_close_start_2 = event_ec_2[0]
                event_close_end_2 = event_ec_end_2[-1]
                event_close_start_3 = event_ec_3[0]
                event_close_end_3 = event_ec_end_3[-1]

            # load data
            raw_ = raw_data['EEG']['data'][0][0][:64, :]
            raw_ = np.delete(raw_, (32, 42, 59, 63), axis=0)

            # preprocessing
            eeg_info = mne.create_info(ch_names=self.ch_list, sfreq=self.sfreq, ch_types="eeg")
            data = mne.io.RawArray(raw_, info=eeg_info)

            # filtering
            data = data.filter(l_freq=0.5, h_freq=40)
            filtered_data = data.get_data()

            # epochs setting
            ec_data_1 = filtered_data[:, event_close_start_1:event_close_end_1]
            ec_data_1 = mne.io.RawArray(ec_data_1, info=eeg_info)
            ec_data_2 = filtered_data[:, event_close_start_2:event_close_end_2]
            ec_data_2 = mne.io.RawArray(ec_data_2, info=eeg_info)
            ec_data_3 = filtered_data[:, event_close_start_3:event_close_end_3]
            ec_data_3 = mne.io.RawArray(ec_data_3, info=eeg_info)

            ec_1 = mne.make_fixed_length_epochs(raw=ec_data_1, overlap=.0, duration=2.0)
            ec_2 = mne.make_fixed_length_epochs(raw=ec_data_2, overlap=.0, duration=2.0)
            ec_3 = mne.make_fixed_length_epochs(raw=ec_data_3, overlap=.0, duration=2.0)

            # epoch concatenate
            ec_data = mne.concatenate_epochs([ec_1, ec_2, ec_3])

            # pickle 파일로 저장
            with open(rf'A:\DataBase\MDD_open_data\epoch\{sub_name}.pickle', 'wb') as file:
                pickle.dump(ec_data, file)


if __name__ == '__main__':
    config = OpenDatasetConfig()
    OpenDataParser(config=config).epoch_data_save()