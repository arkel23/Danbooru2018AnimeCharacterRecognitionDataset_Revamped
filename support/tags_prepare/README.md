To organize danbooru metadata, combine into single dataframe files, filter and clean:
1. `python organize_metadata_raw.py DIR_TO_RAW_METADATA`
2. `mv DIR_TO_RAW_METADATA/*.csv NEW_DIR_ORGANIZED_METADATA`
3. `python combine_metadata.py NEW_DIR_ORGANIZED_METADATA`
4. `python filter_bool_ratings_exist_rgb_emptytags.py db2020_metadata_condensed_v1.csv`
5. `python remove_symbols.py db2020_metadata_condensed_v2.csv`
6. `python remove_lessthan.py db2020_metadata_condensed_v2_symbolsremoved.csv`
7. `python remove_profanities.py db2020_metadata_condensed_v2_symbolsremoved_minlen2_minapp2.csv profanity_list.txt`
8. `python fill_empty.py db2020_metadata_condensed_v2_symbolsremoved_minlen2_minapp2_profsremoved.txt`
