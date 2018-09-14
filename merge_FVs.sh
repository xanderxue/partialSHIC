for i in `ls data/FVs`
  do
  for j in 2L 2R 3L 3R
    do
    for k in `ls data/FVs/${i}/${j}*|cut -d '.' -f 2|sort -n`
      do
      if [ ${k} == 1 ]
        then
        cp data/FVs/${i}/${j}.1.fvec data/FVs/${i}.${j}.fvec
      else
        cat data/FVs/${i}/${j}.${k}.fvec|awk 'NR>1' >>data/FVs/${i}.${j}.fvec
      fi
    done
  done
done
