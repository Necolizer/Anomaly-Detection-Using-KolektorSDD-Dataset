# Anomaly-Detection-Using-KolektorSDD-Dataset
 Reorganize KolektorSDD dataset as MVTecAD dataset's format. Report SOTA anomaly detection models' results in KolektorSDD.

## 0. Table of Contents
* [1. Purpose](#1-purpose)
* [2. Usage](#2-usage)
* [3. Illustrations of KolektorSDD Preprocessing](#3-illustrations-of-kolektorsdd-preprocessing)
* [4. Experimental Results](#4-experimental-results)
* [5. Sample Visualizations](#5-sample-visualizations)
* [6. Change Log](#6-change-log)
* [7. License](#7-license)

## 1. Purpose

### CN
这是本仓库作者在实习期间完成的代码，主要内容是拿KolektorSDD数据集去跑部分SOTA工业缺陷检测模型（主要取自[MVTecAD的排行榜](https://paperswithcode.com/sota/anomaly-detection-on-mvtec-ad)）。由于各种限制，这里只公布了KolektorSDD的预处理代码和复现出的结果。通过KolektorSDD的预处理代码，可以快速将KolektorSDD数据集的格式转换为MVTecAD数据集的格式，这样就可以直接套用SOTA开源代码或者[Anomalib库](https://github.com/openvinotoolkit/anomalib)，快速的进行训练和测试。完整复现应该不困难。

### EN
This repository contains code for preprocessing KolektorSDD dataset so that we could train/test some SOTA anomaly detection models in [MVTecAD leaderboard](https://paperswithcode.com/sota/anomaly-detection-on-mvtec-ad). Due to various restrictions, I do NOT upload the modified training/testing code for those SOTA models. But I believe with the KolektorSDD dataset after preprocessing, you could reproduce the results in a very short time, just with slight modifications to SOTA codes/[Anomalib](https://github.com/openvinotoolkit/anomalib) using **MVTecAD configurations**. I also report the results I reproduce for comparisons.


## 2. Usage

1. Download KolektorSDD Dataset with fine annotations in https://www.vicos.si/resources/kolektorsdd/
    - Please cite according to their requirements
2. Unzip the KolektorSDD file
3. git clone this repo
4. Modify the path in `KolektorSDD_Preprocess.py`
```
# Args that you need to change: 
# @ read_base : Path to the downloaded KolektorSDD dataset
# @ save_base : Path to the repository you wanna save
read_base = r'.\KolektorSDD'
save_base = r'.\KolektorSDD1'
```
5. Run the script
```
python KolektorSDD_Preprocess.py
```
6. Your final directory tree of reorganized KolektorSDD should look like this:

```
save_base
└── metal
    ├── ground_truth
    |    └── defect
    |         ├── 000_mask.png
    |         ├── 001_mask.png
    |         ├── ...
    ├── test
    |    ├── defect
    |    |    ├── 000.png
    |    |    ├── 001.png
    |    |    ├── ...
    |    └── good
    |         ├── 000.png
    |         ├── 001.png
    |         ├── ...
    └── train
         └── good
             ├── 000.png
             ├── 001.png
             ├── ...
```
7. Modify the code configurations and run your training and testing scripts
    - See **Section 4** to get the open source code for SOTA models in my experiment
    - With the KolektorSDD dataset after preprocessing, you could reproduce the results in a very short time, just with slight modifications to SOTA codes/[Anomalib](https://github.com/openvinotoolkit/anomalib) using **MVTecAD configurations**.

## 3. Illustrations of KolektorSDD Preprocessing

### CN
总体思路：处理成接近MVTecAD数据集的样式

步骤：
1. Jpg和Bmp转Png
2. Resize到统一的尺寸：500x1240
3. 划分训练和测试
    - 训练：295张正常
    - 测试：52张正常+52张异常

> 这里需要注意：
> - 本仓库作者采取的手段是直接Resize到统一的尺寸，这可能会导致某些小缺陷的mask变形，如果有时间，可以换成crop的形式，把有缺陷的部分crop出一个正方形区域出来。
> - 本仓库作者采取的划分方式是直接划分训练和测试，没有留验证集。同时，在代码中已经规定了测试时的正常和异常样本数量相等。如果需要。可以自行修改代码，取合理的划分。
> - 因为random.shuffle没有固定种子，每次运行会得到具体样本不同的划分结果。

### EN

To take use of SOTA codes / [Anomalib](https://github.com/openvinotoolkit/anomalib) using **MVTecAD configurations**, we should reorganize KolektorSDD dataset in MVTecAD dataset's format.

Steps:
1. JPG/BMP to PNG
2. Resize to the same size (500x1240)
3. Train-Test Split
    - Train
        - Flawless samples for training: 295
    - Test
        - Flawless samples for testing: 52
        - Anomalies for testing: 52

> ATTENTION:
> - I resize all the images to the same size (500x1240), which might result in defect distortions.
> - Because of the small number of samples, I do NOT reserve a validation set. I sampled the same number of flawless samples as anomalies for testing. This setting could be changed as you want.
> - Seed for random.shuffle() is NOT fixed. So each run of this preprocessing script will result in different splitting results.

## 4. Experimental Results

SOTA models that chosen to train/test (Also as Acknowledgements):
- PatchCore (backbone: wide_resnet50_2)
    - [Official Code Ver.](https://github.com/amazon-science/patchcore-inspection)
    - [Anomalib Ver.](https://github.com/openvinotoolkit/anomalib/tree/main/anomalib/models/patchcore)
- FastFlow (backbone: resnet18 / cait_m48_448)
    - [Anomalib Ver.](https://github.com/openvinotoolkit/anomalib/tree/main/anomalib/models/fastflow)
    - [Unofficial Code Ver.](https://github.com/RistoranteRist/FastFlow)
- CFA (backbone: wrn50_2)
    - [Official Code Ver.](https://github.com/sungwool/CFA_for_anomaly_localization)
- Cflow-AD (backbone: wide_resnet50_2)
    - [Official Code Ver.](https://github.com/gudovskiy/cflow-ad)
    - [Anomalib Ver.](https://github.com/openvinotoolkit/anomalib/tree/main/anomalib/models/cflow)

<table>
    <tr>
        <td>Version</td> 
        <td>Methods</td> 
        <td>Backbone</td> 
        <td>Avg DET AUC (image ROCAUC)</td> 
        <td>Avg SEG AUC (pixel ROCAUC)</td> 
        <td>pixel PROAUC</td> 
    </tr>
    <tr>
        <td rowspan="3">Official Code</td>    
        <td >PatchCore</td>  
        <td >wide_resnet50_2</td> 
        <td >0.909</td> 
        <td >0.941</td> 
        <td >/</td> 
    </tr>
    <tr>
        <td >FastFlow</td> 
        <td >cait_m48_448</td> 
        <td >0.955</td> 
        <td >0.960</td> 
        <td >/</td> 
    </tr>
    <tr>
        <td >Cflow-AD</td> 
        <td >wide_resnet50_2</td> 
        <td >0.801</td> 
        <td >0.891</td> 
        <td >0.497</td> 
    </tr>
    <tr>
        <td >Unofficial Code</td> 
        <td >CFA</td> 
        <td >wrn50_2</td> 
        <td >0.939</td> 
        <td >0.939</td> 
        <td >0.823</td> 
    </tr>
    <tr>
        <td rowspan="4">Anomalib</td> 
        <td >PatchCore</td>  
        <td >wide_resnet50_2</td> 
        <td >0.863</td> 
        <td >0.840</td> 
        <td >/</td> 
    </tr>
    <tr>
        <td rowspan="2">FastFlow</td> 
        <td >resnet18</td> 
        <td >0.807</td> 
        <td >0.883</td> 
        <td >/</td> 
    </tr>
    <tr>
        <td >cait_m48_448</td> 
        <td >0.914</td> 
        <td >0.963</td> 
        <td >/</td> 
    </tr>
    <tr>
        <td >Cflow-AD</td> 
        <td >wide_resnet50_2</td> 
        <td >0.850</td> 
        <td >0.847</td> 
        <td >/</td> 
    </tr>
</table>
<style>
	table {
   	 margin: auto;
	}
</style>

## 5. Sample Visualizations

- PatchCore (wide_resnet50_2)
![PatchCore](./imgs/patchcore/013.png "PatchCore (wide_resnet50_2)")
- FastFlow (cait_m48_448)
![FastFlow](./imgs/fastflow/013.png "FastFlow (cait_m48_448)")
- Cflow-AD (wide_resnet50_2)
![Cflow-AD](./imgs/cflow/013.png "Cflow-AD (wide_resnet50_2)")
- CFA (wrn50_2)
![CFA](./imgs/cfa/metal_20.png "CFA (wrn50_2)")


## 6. Change Log

- [2022/12/28] Create repository and release preprocessing script. 

## 7. License

[MIT](https://github.com/Necolizer/Anomaly-Detection-Using-KolektorSDD-Dataset/blob/main/LICENSE)