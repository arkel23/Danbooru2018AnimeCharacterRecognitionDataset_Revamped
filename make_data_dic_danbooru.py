import os, sys, glob
import pandas as pd
import numpy as np
from PIL import Image

def reduced_dic(file_name):
    '''
    makes a text dictionary based on the original faces.tsv
    only extract images with a confidence above 85%
    also verifies the image is RGB
    '''
    df = pd.read_csv(file_name, sep='\t', header=None, names=['dir', 'id', 'coords'])
    df['dir'].replace(to_replace=r'\\', value=r'/', inplace=True, regex=True)
    # if change the name of the danbooru2018_animefacecropdataset folders to 4 digits it's not needed 
    #df['dir'] = df['dir'].str.slice(start=1)
    print(df.head())
    
    high_confidence = []
    verified_image = []
    for idx in df.index:
        confidence = float(df.iloc[idx]['coords'][-8:])
        if confidence >= 0.85:
            high_confidence.append(idx)
            rel_path = df.iloc[idx]['dir']
            img_path = os.path.join('data', rel_path)
            img = Image.open(img_path)
            if img.mode == 'RGB':
                verified_image.append(idx)
    print('Total number of images (prefiltering): ', len(df))
    print('Total number of images with high confidence (85%): ', len(high_confidence))
    print('Total number of images post RGB only filter: ', len(verified_image))

    new_df = df[['id', 'dir']].iloc[verified_image]
    print(new_df.head())
    no_classes_pre = df['id'].nunique()
    no_classes_post = new_df['id'].nunique()
    print('Number of classes pre / post filtering (85% + RGB only): {} / {}'.format(
    no_classes_pre, no_classes_post))

    new_df_name = 'danbooru2018_faces_85.csv'
    new_df.to_csv(new_df_name, sep=',', header=False, index=False)


def main():
    '''
    input is the path to the Danbooru2018CharacterRecognitionDataset faces.tsv file
    it then checks for the data/rel_path from the faces.tsv file
    '''
    try:
        data_folder = os.path.abspath(sys.argv[1])
    except:
        data_folder = 'faces.tsv'
    reduced_dic(data_folder)

main()

