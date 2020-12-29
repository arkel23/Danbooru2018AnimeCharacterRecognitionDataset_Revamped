import os, sys, glob
import pandas as pd
import numpy as np
from PIL import Image

def make_data_dic(data_folder):
    
    types = ('*.jpg', '*.jpeg', '*.png') # the tuple of file types
    files_all = []
    for file_type in types:
        # files_all is the list of files
        path = os.path.join(data_folder, '**', file_type)
        files_curr_type = glob.glob(path, recursive=True)
        files_all.extend(files_curr_type)

        print(file_type, len(files_curr_type))    
    print('Total image files pre-filtering', len(files_all))

    class_name_list = []      # holds classes names and is also relative path
    filename_classid_dic = {} # filename and classid pairs
    classid_classname_dic = {}    # id and class name/rel path as dict
    
    idx = -1
    for file_path in files_all:
        # verify the image is RGB
        im = Image.open(file_path)
        if im.mode == 'RGB':
            abs_path, filename = os.path.split(file_path)
            _, class_name = os.path.split(abs_path)
            rel_path = os.path.join(class_name, filename)

            if class_name not in class_name_list:
                idx += 1
                class_name_list.append(class_name)
                classid_classname_dic[idx] = class_name 

            filename_classid_dic[rel_path] = idx
    
    no_classes = idx + 1
    print('Total number of classes: ', no_classes)
    print('Total images files post-filtering (RGB only): ', len(filename_classid_dic))

    # save dataframe to hold the class IDs and the relative paths of the files
    df = pd.DataFrame.from_dict(filename_classid_dic, orient='index', columns=['class_id'])
    idx_col = np.arange(0, len(df), 1)
    df['idx_col'] = idx_col
    df['file_rel_path'] = df.index
    df.set_index('idx_col', inplace=True)
    print(df.head())    
    dataset_name = os.path.basename(os.path.normpath(data_folder))
    df_name = dataset_name + '.csv'
    df.to_csv(df_name, sep=',', header=False, index=False)

    # save dataframe to hold the class IDs and their respective names
    df_classid_classname = pd.DataFrame.from_dict(classid_classname_dic, orient='index', columns=['class_id'])
    idx_col = np.arange(0, len(df_classid_classname), 1)
    df_classid_classname['idx_col'] = idx_col
    df_classid_classname['class_name'] = df_classid_classname.index
    df_classid_classname.set_index('idx_col', inplace=True)
    print(df_classid_classname.head())    
    df_classid_classname_name = 'classid_classname' + '.csv'
    df_classid_classname.to_csv(df_classid_classname_name, sep=',', header=False, index=False)


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
            img_path = os.path.join('danbooru2018_animefacecropdataset', rel_path)
            img = Image.open(img_path)
            if img.mode == 'RGB':
                verified_image.append(idx)
    print('Total number of images (prefiltering): ', len(df))
    print('Total number of images with high confidence (85%): ', len(high_confidence))
    print('Total number of images post RGB only filter: ', len(verified_image))

    new_df = df[['dir', 'id']].iloc[verified_image]
    print(new_df.head())
    no_classes_pre = df['id'].nunique()
    no_classes_post = new_df['id'].nunique()
    print('Number of classes pre / post filtering (85% + RGB only): {} / {}'.format(
    no_classes_pre, no_classes_post))

    new_df_name = 'danbooru2018_faces_85.csv'
    new_df.to_csv(new_df_name, sep=',', header=False, index=False)


def main():
    '''
    input is the path to the Danbooru2018CharacterRecognitionDataset
    '''
    try:
        data_folder = os.path.abspath(sys.argv[1])
    except:
        data_folder = 'faces.tsv'
    reduced_dic(data_folder)

main()

