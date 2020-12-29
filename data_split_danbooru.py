import os, sys, glob
import pandas as pd
import numpy as np

def data_split(data_dic_path):
    '''
    splits data into training and val (0.7, 0.1) and testing (0.2)   
    only keeps the images if the class has at least 10 images
    needs to reindex the classes since probably there's going 
    to be many less classes
    rename class_id col to class_id_og and create a new
    class_id col that holds an ID if the class_id_col is not in
    class_name_list 
    '''
    
    SPLIT = [0.7, 0.1, 0.2]
    CLASS_THRESHHOLD = 20

    # class_name_list = [] # append new classes after filtering to this

    df = pd.read_csv(data_dic_path, sep=',', names=['dir', 'class_id'])
    print('Original df: ', len(df))
    print(df.head())
    
    samples_per_class_df = df.groupby('class_id', as_index=True).count()
    print(samples_per_class_df.head())
    
    
    df_list_train = []
    df_list_val = []
    df_list_test = []
    total_samples_pre = 0
    total_samples_post = 0
    total_classes_pre = 0
    total_classes_post = 0

    for class_id in samples_per_class_df.index:
        total_samples_class = samples_per_class_df.loc[class_id, 'dir']
        if total_samples_class >= CLASS_THRESHHOLD:
            train_val_samples_class = int(total_samples_class*(SPLIT[0] + SPLIT[1]))
            test_samples_class = total_samples_class - train_val_samples_class
            assert(train_val_samples_class + test_samples_class == total_samples_class)
            train_val_subset_class = df.loc[df['class_id']==class_id].groupby('class_id').head(train_val_samples_class)
            test_subset_class = df.loc[df['class_id']==class_id].groupby('class_id').tail(test_samples_class)

            train_samples_class = int(total_samples_class*SPLIT[0])
            val_samples_class = train_val_samples_class - train_samples_class
            assert(train_samples_class + val_samples_class == train_val_samples_class)
            assert(train_samples_class + val_samples_class + test_samples_class == total_samples_class)
            train_subset_class = train_val_subset_class.head(train_samples_class)
            val_subset_class = train_val_subset_class.tail(val_samples_class)

            df_list_train.append(train_subset_class)
            df_list_val.append(val_subset_class)
            df_list_test.append(test_subset_class)

            total_samples_post += total_samples_class
            total_classes_post += 1
        total_samples_pre += total_samples_class
        total_classes_pre += 1

    print('Total number of samples pre/post filtering: {} / {}'.format(total_samples_pre, total_samples_post))
    print('Total number of classes pre/post filtering: {} / {}'.format(total_classes_pre, total_classes_post))

    df_train = pd.concat(df_list_train)
    df_val = pd.concat(df_list_val)
    df_test = pd.concat(df_list_test)

    print('Train df: ')
    print(df_train.head())
    print(df_train.shape)
    print('Val df: ')
    print(df_val.head())
    print(df_val.shape)
    print('Test df: ')
    print(df_test.head())
    print(df_test.shape)
    
    print('No of classes in train/val/test sets: {} / {} / {}'.format(
    df_train['class_id'].nunique(), df_val['class_id'].nunique(), df_test['class_id'].nunique()))

    df_train.to_csv('train.csv', sep=',', header=False, index=False)
    df_val.to_csv('val.csv', sep=',', header=False, index=False)
    df_test.to_csv('test.csv', sep=',', header=False, index=False)
    print('Finished saving train, val and test split dictionaries.')
    
def main():
    
    try:
        data_dic_path = os.path.abspath(sys.argv[1])
    except:
        data_dic_path = "danbooru2018_faces_85.csv"
    
    data_split(data_dic_path)

main()