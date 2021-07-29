for i in $(seq -f "%04g" 0 999)
do
  mkdir -p "dafre/$i"
done

for file in `cat $1`
do 
  echo "$file"
  #rsync -a "$file" /dafre/
  cp "data/$file" "dafre/$file"
done
