# Depression Biomarker

Here is a simple repo for deriving the MDD biomarker, LHCx, through Resting-state EEG signals.

<div align=center>

![LHCx index](https://github.com/Junsu0213/Depression_Biomarker/assets/128777619/543e650a-fc7a-423f-90f5-e610d3bf7f99)

The average connectivity between statistically significant channels as determined by the independent sample t-test of MDD and control groups

##### [Novel Biomarker Based on Hemispheric Differences in Brain Connectivity for Diagnosis of Depression](https://ieeexplore.ieee.org/abstract/document/9954764?casa_token=h4JNQwpbwTcAAAAA:xqsk_gMjWYUeT8ewn4leD6UGmjs2CqABEJxZRFV-JrtGdm7ehkpRRiaKkayGUrSF-G8hUlI)

</div>

## 1. Abstract
> Biomarkers using EEG could be used to detect and analyze various mental diseases. Many researchers are working on biomarkers that are mostly based on spectral analysis, resulting in poor reproducibility so restricted to being used in a clinical environment. In this study, we proposed LHCx, a potential biomarker for MDD using resting state EEG and EEG connectivity algorithm. To develop LHCx, the PRED+CT dataset consisting of 43 MDD patients and 73 healthy control was used. PLI connectivity for the low alpha band was acquired from 60 EEG channels. An independent sample t-test was conducted, and only statistically significant connectivity (p < 0.001) was selected among the connectivity. As a result, there was the biggest difference in connectivity between CPz and left hemisphere connectivity among MDD patients and healthy control. A decrease in connectivity between the central parietal region and frontal/temporal region located in the left hemisphere of MDD patients is also confirmed. LHCx could be utilized in a diagnosis of MDD, and we expect it to be used in a clinical environment.


## 2. Installation

#### Environment
* Python == 2.8.2
* MNE == 1.1.0
* mne-connectivity == 0.3


## 3. Directory structure
```bash
├── Analysis
│   └── data_analysis.py
├── Evaluation
│   └── model_evaluation.py
├── Config
│   └── config.py
├── LHCx
│   ├── Figure
│   │   └── test.png
│   └── sw_code.py
├── Parser
│   ├── data_fc_analysis.py
│   └── data_parser.py
└── requirements.txt
```

## 4. Dataset

#### [PRED+CT MDD dataset](http://predict.cs.unm.edu/)
* 116 subjects (MDD: 73, Healthy control: 43)
* Resting state EEG data: eyes open (EO), eyes closed (EC)

## 5. Left hemisphere connectivity index (LHCx)
LHCx is a new biomarker for diagnosis of depression proposed by this study. LHCx is the sum of connectivity between the CPz channel and channels connected with it in the low alpha band. By defining left hemisphere channels {LHC: Fp1, AF3, F1, F3, F5, F7, FT7, FC5, T7, TP7, P7} connected with CPz as region of interest, LHCx is defined as the sum of connectivity between the LHC and CPz:

<div align=center>

![LHCx 수식](https://github.com/Junsu0213/Depression_Biomarker/assets/128777619/8ba8f95c-263f-4e05-b63f-348ee6c18238)

</div>
