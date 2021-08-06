#nohup rsync --verbose --files-from=val_512jpg.txt rsync://78.46.86.149:873/danbooru2020/512px/ 512px/ >> download_dafresplit_512px.out 
#nohup rsync --verbose --files-from=test_512jpg.txt rsync://78.46.86.149:873/danbooru2020/512px/ 512px/ >> download_dafresplit_512px.out 
#nohup rsync --verbose --files-from=train_512jpg.txt rsync://78.46.86.149:873/danbooru2020/512px/ 512px/ >> download_dafresplit_512px.out 

#nohup rsync --verbose --files-from=val_originalext.txt rsync://78.46.86.149:873/danbooru2020/ . >> download_dafresplit_original.out 
#nohup rsync --verbose --files-from=test_originalext.txt rsync://78.46.86.149:873/danbooru2020/ . >> download_dafresplit_original.out 
nohup rsync --verbose --files-from=train_originalext.txt rsync://78.46.86.149:873/danbooru2020/ . >> download_dafresplit_original.out 
