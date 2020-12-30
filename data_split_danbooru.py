import os, sys, glob
import pandas as pd
import numpy as np

def data_split(data_dic_path):
    '''
    splits data into training and val (0.7, 0.1) and testing (0.2)   
    only keeps the images if the class has at least CLASS_THRESHOLD images
    '''
    SPLIT = [0.7, 0.1, 0.2]
    CLASS_THRESHHOLD = 20

    df = pd.read_csv(data_dic_path[0], sep=',', names=['dir', 'class_id_og'])
    print('Original df: ', len(df))
    print(df.head())
    
    samples_per_class_df = df.groupby('class_id_og', as_index=True).count()
    print(samples_per_class_df.head())
        
    df_list_train = []
    df_list_val = []
    df_list_test = []
    total_samples_pre = 0
    total_samples_post = 0
    total_classes_pre = 0
    total_classes_post = 0

    df_classid_classname_og = pd.read_csv(data_dic_path[1], sep='\t', names=['class_name', 'class_id_og'])
    print(df_classid_classname_og.head())
    classid_list = [] # append new classes after filtering to this
    classid_classname_dic = {}    # id and class_name as dict
    
    idx = -1
    for class_id_og in samples_per_class_df.index:
        total_samples_class = samples_per_class_df.loc[class_id_og, 'dir']
        if total_samples_class >= CLASS_THRESHHOLD:
            if class_id_og not in classid_list:
                idx += 1
                classid_list.append(idx)
                class_name = df_classid_classname_og.loc[df_classid_classname_og['class_id_og']==class_id_og, 'class_name'].values
                classid_classname_dic[idx] = class_name
                
            train_val_samples_class = int(total_samples_class*(SPLIT[0] + SPLIT[1]))
            test_samples_class = total_samples_class - train_val_samples_class
            assert(train_val_samples_class + test_samples_class == total_samples_class)
            train_val_subset_class = df.loc[df['class_id_og']==class_id_og].groupby('class_id_og').head(train_val_samples_class)
            test_subset_class = df.loc[df['class_id_og']==class_id_og].groupby('class_id_og').tail(test_samples_class)

            train_samples_class = int(total_samples_class*SPLIT[0])
            val_samples_class = train_val_samples_class - train_samples_class
            assert(train_samples_class + val_samples_class == train_val_samples_class)
            assert(train_samples_class + val_samples_class + test_samples_class == total_samples_class)
            train_subset_class = train_val_subset_class.head(train_samples_class)
            val_subset_class = train_val_subset_class.tail(val_samples_class)

            train_subset_class.insert(1, 'class_id', idx)
            val_subset_class.insert(1, 'class_id', idx)
            test_subset_class.insert(1, 'class_id', idx)

            train_subset_class = train_subset_class.drop(columns=['class_id_og'])
            val_subset_class = val_subset_class.drop(columns=['class_id_og'])
            test_subset_class = test_subset_class.drop(columns=['class_id_og'])
            
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

    # save dataframe to hold the class IDs and their respective names
    print('Length of classid_classname_dic: {} and one sample: {}.'.format(len(classid_classname_dic), classid_classname_dic[0]))
    df_classid_classname = pd.DataFrame.from_dict(classid_classname_dic, orient='index', columns=['class_name'])
    idx_col = np.arange(0, len(df_classid_classname), 1)
    df_classid_classname['idx_col'] = idx_col
    df_classid_classname['class_id'] = df_classid_classname.index
    df_classid_classname.set_index('idx_col', inplace=True)
    cols = df_classid_classname.columns.tolist()
    cols = cols[-1:] + cols[:-1] # reordering the columns
    df_classid_classname = df_classid_classname[cols]
    print(df_classid_classname.head())    
    df_classid_classname_name = 'classid_classname' + '.csv'
    df_classid_classname.to_csv(df_classid_classname_name, sep=',', header=False, index=False)
    print('Finished saving classid_classname dictionary.')
    
def main():
    
    try:
        data_dic_path = os.path.abspath(sys.argv[1])
    except:
        data_dic_path = ["danbooru2018_faces_85.csv", "tagIds.tsv"]
    
    data_split(data_dic_path)

main()