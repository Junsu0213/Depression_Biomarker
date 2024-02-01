# -*- coding:utf-8 -*-
"""
Created on Wed. Jul. 26 20:23:35 2023
@author: Jun-su Park
"""
import glob
import pickle
from Config.config import OpenDatasetConfig
import numpy as np
from mne_connectivity import spectral_connectivity_epochs


class DataAnalysis(object):
    def __init__(self, config: OpenDatasetConfig):
        self.config = config
        self.ch_list = config.ch_list
        self.band_freq = config.band_freq
        self.band = tuple(zip(*tuple(self.band_freq.values())))
        self.fc_method = config.fc_method
        self.psd_method = config.psd_method

    def fc_analysis(self, epoch):
        # Functional connectivity analysis
        con = spectral_connectivity_epochs(data=epoch, names=self.ch_list, method=self.fc_method,
                                           fmin=self.band[0], fmax=self.band[1], faverage=True,
                                           mt_adaptive=True, n_jobs=1)
        # Connectivity features (channel*channel, band frequency)
        conmat = con.get_data()
        # Adjacency matrix (channel, channel, band frequency)
        adj_mat = con.get_data(output='dense')
        return conmat, adj_mat

    def psd_analysis(self, epoch, relative=True):
        # Power spectral density analysis
        power = epoch.compute_psd(method=self.psd_method, fmin=min(self.band[0]), fmax=max(self.band[1]))
        # Average the spectra across epochs.
        power = power.average()
        # total power
        total_power = power.get_data().sum(axis=1)

        # band name
        band_name = self.band_freq.keys()

        # psd list
        nor_power = []
        for i in band_name:
            fmin, fmax = self.band_freq[i]
            # normalized psd
            if relative == True:
                nor_power_ = power.get_data(fmin=fmin, fmax=fmax).sum(axis=1)/total_power
            # raw psd
            elif relative == False:
                nor_power_ = power.get_data(fmin=fmin, fmax=fmax).sum(axis=1)
            nor_power.append(nor_power_)

        # psd (channel, band frequency)
        nor_power = np.array(nor_power).swapaxes(1, 0)
        return nor_power


if __name__ == '__main__':
    # analysis test (single case)
    config = OpenDatasetConfig()

    path = '.\\database\\KUMC\\epoch\\'
    flist = glob.glob(path+'*.pickle')

    with open(flist[0], 'rb') as f:
        epoch = pickle.load(f)

    analysis = DataAnalysis(config=config)
    _, adj_mat = analysis.fc_analysis(epoch=epoch)
    psd = analysis.psd_analysis(epoch=epoch)

    print(adj_mat.shape)
    print(psd.shape)