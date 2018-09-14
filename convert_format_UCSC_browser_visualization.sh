for i in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  echo "track name=${i}_sweep_classifications visibility=2 itemRgb=On" >results/${i}.bed
  for j in 2L 2R 3L 3R
    do
    if [ ${j} == '2L' ]
      then
      cat results/${i}.${j}.bed|awk 'NR>1'|awk '($3<49364326)' >>results/${i}.bed
    fi
    if [ ${j} == '2R' ]
      then
      cat results/${i}.${j}.bed|awk 'NR>1'|awk '($3<61545106)' >>results/${i}.bed
    fi
    if [ ${j} == '3L' ]
      then
      cat results/${i}.${j}.bed|awk 'NR>1'|awk '($3<41963436)' >>results/${i}.bed
    fi
    if [ ${j} == '3R' ]
      then
      cat results/${i}.${j}.bed|awk 'NR>1'|awk '($3<53200685)' >>results/${i}.bed
    fi
  done
  for l in pi thetaW tajD thetaH fayWuH HapCount H1 H12 H2/H1 ZnS Omega iHSMean iHSMax iHSOutFrac nSLMean nSLMax nSLOutFrac distVar distSkew distKurt HAF-Mean HAF-Median HAF-Mode HAF-Lower95% HAF-Lower50% HAF-Upper50% HAF-Upper95% HAF-Max HAF-Var HAF-SD HAF-Skew HAF-Kurt HAFunique-Mean HAFunique-Median HAFunique-Mode HAFunique-Lower95% HAFunique-Lower50% HAFunique-Upper50% HAFunique-Upper95% HAFunique-Max HAFunique-Var HAFunique-SD HAFunique-Skew HAFunique-Kurt phi-Mean phi-Median phi-Mode phi-Lower95% phi-Lower50% phi-Upper50% phi-Upper95% phi-Max phi-Var phi-SD phi-Skew phi-Kurt kappa-Mean kappa-Median kappa-Mode kappa-Lower95% kappa-Lower50% kappa-Upper50% kappa-Upper95% kappa-Max kappa-Var kappa-SD kappa-Skew kappa-Kurt SFS-Mean SFS-Median SFS-Mode SFS-Lower95% SFS-Lower50% SFS-Upper50% SFS-Upper95% SFS-Max SFS-Var SFS-SD SFS-Skew SFS-Kurt SAFE-Mean SAFE-Median SAFE-Mode SAFE-Lower95% SAFE-Lower50% SAFE-Upper50% SAFE-Upper95% SAFE-Max SAFE-Var SAFE-SD SAFE-Skew SAFE-Kurt
    do
    if [ ${l} == "H2/H1" ]
      then
      m=H2-H1
    else
      if [ `echo ${l}|rev|cut -c 1` == "%" ]
        then
        m=`echo ${l}|rev|cut -c 2-|rev`
      else
        m=${l}
      fi
    fi
    echo "track type=bedGraph name=${i}_${m}" >results/${i}.${m}.bed
    n=`head -1 data/sumstats/${i}/2L.1.stats|tr '\t' '\n'|grep -n "${l}"|cut -d ":" -f 1|head -1`
    for j in 2L 2R 3L 3R
      do
      for k in `ls data/sumstats/${i}|grep "${j}"|cut -d "." -f 2|sort -n`
        do
        if [ ${j} == '2L' ]
          then
          cat data/sumstats/${i}/${j}.${k}.stats|awk 'NR>1'|cut -f 1-3,${n}|awk '($3<49364326)' >temp1
        fi
        if [ ${j} == '2R' ]
          then
          cat data/sumstats/${i}/${j}.${k}.stats|awk 'NR>1'|cut -f 1-3,${n}|awk '($3<61545106)' >temp1
        fi
        if [ ${j} == '3L' ]
          then
          cat data/sumstats/${i}/${j}.${k}.stats|awk 'NR>1'|cut -f 1-3,${n}|awk '($3<41963436)' >temp1
        fi
        if [ ${j} == '3R' ]
          then
          cat data/sumstats/${i}/${j}.${k}.stats|awk 'NR>1'|cut -f 1-3,${n}|awk '($3<53200685)' >temp1
        fi
        cat temp1|awk '{printf "%s\n", "chr"}' >temp0
        paste -d "" temp0 temp1 >>results/${i}.${m}.bed
      done
    done
  done
  rm temp0 temp1
done

cd results

for i in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  mkdir ${i}
  cp ${i}.bed ${i}/
  for l in pi thetaW tajD thetaH fayWuH HapCount H1 H12 H2-H1 ZnS Omega iHSMean iHSMax iHSOutFrac nSLMean nSLMax nSLOutFrac distVar distSkew distKurt HAF-Mean HAF-Median HAF-Mode HAF-Lower95 HAF-Lower50 HAF-Upper50 HAF-Upper95 HAF-Max HAF-Var HAF-SD HAF-Skew HAF-Kurt HAFunique-Mean HAFunique-Median HAFunique-Mode HAFunique-Lower95 HAFunique-Lower50 HAFunique-Upper50 HAFunique-Upper95 HAFunique-Max HAFunique-Var HAFunique-SD HAFunique-Skew HAFunique-Kurt phi-Mean phi-Median phi-Mode phi-Lower95 phi-Lower50 phi-Upper50 phi-Upper95 phi-Max phi-Var phi-SD phi-Skew phi-Kurt kappa-Mean kappa-Median kappa-Mode kappa-Lower95 kappa-Lower50 kappa-Upper50 kappa-Upper95 kappa-Max kappa-Var kappa-SD kappa-Skew kappa-Kurt SFS-Mean SFS-Median SFS-Mode SFS-Lower95 SFS-Lower50 SFS-Upper50 SFS-Upper95 SFS-Max SFS-Var SFS-SD SFS-Skew SFS-Kurt SAFE-Mean SAFE-Median SAFE-Mode SAFE-Lower95 SAFE-Lower50 SAFE-Upper50 SAFE-Upper95 SAFE-Max SAFE-Var SAFE-SD SAFE-Skew SAFE-Kurt
    do
    cp ${i}.${l}.bed ${i}/
  done
  gzip -r ${i}
done

for i in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  cat ${i}.bed|awk 'NR>1'|sort -k1,1 -k2,2n >temp
  ./bedToBigBed temp anoGam3.chrom.sizes ${i}/${i}.bb
  for l in pi thetaW tajD thetaH fayWuH HapCount H1 H12 H2-H1 ZnS Omega iHSMean iHSMax iHSOutFrac nSLMean nSLMax nSLOutFrac distVar distSkew distKurt HAF-Mean HAF-Median HAF-Mode HAF-Lower95 HAF-Lower50 HAF-Upper50 HAF-Upper95 HAF-Max HAF-Var HAF-SD HAF-Skew HAF-Kurt HAFunique-Mean HAFunique-Median HAFunique-Mode HAFunique-Lower95 HAFunique-Lower50 HAFunique-Upper50 HAFunique-Upper95 HAFunique-Max HAFunique-Var HAFunique-SD HAFunique-Skew HAFunique-Kurt phi-Mean phi-Median phi-Mode phi-Lower95 phi-Lower50 phi-Upper50 phi-Upper95 phi-Max phi-Var phi-SD phi-Skew phi-Kurt kappa-Mean kappa-Median kappa-Mode kappa-Lower95 kappa-Lower50 kappa-Upper50 kappa-Upper95 kappa-Max kappa-Var kappa-SD kappa-Skew kappa-Kurt SFS-Mean SFS-Median SFS-Mode SFS-Lower95 SFS-Lower50 SFS-Upper50 SFS-Upper95 SFS-Max SFS-Var SFS-SD SFS-Skew SFS-Kurt SAFE-Mean SAFE-Median SAFE-Mode SAFE-Lower95 SAFE-Lower50 SAFE-Upper50 SAFE-Upper95 SAFE-Max SAFE-Var SAFE-SD SAFE-Skew SAFE-Kurt
    do
    cat ${i}.${l}.bed|awk 'NR>1'|sort -k1,1 -k2,2n|awk '!a[$1 $2]++' >temp
    bedGraphToBigWig temp anoGam3.chrom.sizes ${i}/${i}.${l}.bw
  done
  rm temp
done

for i in pi thetaW tajD thetaH fayWuH HapCount H1 H12 H2-H1 ZnS Omega iHSMean iHSMax iHSOutFrac nSLMean nSLMax nSLOutFrac distVar distSkew distKurt HAF-Mean HAF-Median HAF-Mode HAF-Lower95 HAF-Lower50 HAF-Upper50 HAF-Upper95 HAF-Max HAF-Var HAF-SD HAF-Skew HAF-Kurt HAFunique-Mean HAFunique-Median HAFunique-Mode HAFunique-Lower95 HAFunique-Lower50 HAFunique-Upper50 HAFunique-Upper95 HAFunique-Max HAFunique-Var HAFunique-SD HAFunique-Skew HAFunique-Kurt phi-Mean phi-Median phi-Mode phi-Lower95 phi-Lower50 phi-Upper50 phi-Upper95 phi-Max phi-Var phi-SD phi-Skew phi-Kurt kappa-Mean kappa-Median kappa-Mode kappa-Lower95 kappa-Lower50 kappa-Upper50 kappa-Upper95 kappa-Max kappa-Var kappa-SD kappa-Skew kappa-Kurt SFS-Mean SFS-Median SFS-Mode SFS-Lower95 SFS-Lower50 SFS-Upper50 SFS-Upper95 SFS-Max SFS-Var SFS-SD SFS-Skew SFS-Kurt SAFE-Mean SAFE-Median SAFE-Mode SAFE-Lower95 SAFE-Lower50 SAFE-Upper50 SAFE-Upper95 SAFE-Max SAFE-Var SAFE-SD SAFE-Skew SAFE-Kurt
  do
  for j in AOM BFM BFS CMS GAS GNS GWA KES UGS
    do
    cat ${j}.${i}.bed|awk 'NR>1'|cut -f 4 >temporary
    echo "a=as.matrix(read.table('temporary'))
    write.table(matrix(quantile(a,c(.025,.975)),nrow=1),'temp.${i}.${j}',row.names=F,col.names=F)
    "|R -s >/dev/null
    rm temporary
  done
done

for i in AOM BFM BFS CMS GAS GNS GWA KES UGS
 do
 echo "track ${i}_sweep_classifications
bigDataUrl ${i}/${i}.bb
shortLabel ${i}_sweep_classifications
longLabel ${i}_sweep_classifications
visibility dense
priority 1
itemRgb on
type bigBed 9 .
" >>trackDb.txt
  for j in pi thetaW tajD thetaH fayWuH HapCount H1 H12 H2-H1 ZnS Omega iHSMean iHSMax iHSOutFrac nSLMean nSLMax nSLOutFrac distVar distSkew distKurt HAF-Mean HAF-Median HAF-Mode HAF-Lower95 HAF-Lower50 HAF-Upper50 HAF-Upper95 HAF-Max HAF-Var HAF-SD HAF-Skew HAF-Kurt HAFunique-Mean HAFunique-Median HAFunique-Mode HAFunique-Lower95 HAFunique-Lower50 HAFunique-Upper50 HAFunique-Upper95 HAFunique-Max HAFunique-Var HAFunique-SD HAFunique-Skew HAFunique-Kurt phi-Mean phi-Median phi-Mode phi-Lower95 phi-Lower50 phi-Upper50 phi-Upper95 phi-Max phi-Var phi-SD phi-Skew phi-Kurt kappa-Mean kappa-Median kappa-Mode kappa-Lower95 kappa-Lower50 kappa-Upper50 kappa-Upper95 kappa-Max kappa-Var kappa-SD kappa-Skew kappa-Kurt SFS-Mean SFS-Median SFS-Mode SFS-Lower95 SFS-Lower50 SFS-Upper50 SFS-Upper95 SFS-Max SFS-Var SFS-SD SFS-Skew SFS-Kurt SAFE-Mean SAFE-Median SAFE-Mode SAFE-Lower95 SAFE-Lower50 SAFE-Upper50 SAFE-Upper95 SAFE-Max SAFE-Var SAFE-SD SAFE-Skew SAFE-Kurt
    do
    echo "track ${i}_${j}
bigDataUrl ${i}/${i}.${j}.bw
shortLabel ${i}_${j}
longLabel ${i}_${j}
type bigWig
viewLimits `cat temp.${j}.${i}|tr ' ' ':'`
" >>trackDb.txt
  done
done

for i in pi thetaW tajD thetaH fayWuH HapCount H1 H12 H2-H1 ZnS Omega iHSMean iHSMax iHSOutFrac nSLMean nSLMax nSLOutFrac distVar distSkew distKurt HAF-Mean HAF-Median HAF-Mode HAF-Lower95 HAF-Lower50 HAF-Upper50 HAF-Upper95 HAF-Max HAF-Var HAF-SD HAF-Skew HAF-Kurt HAFunique-Mean HAFunique-Median HAFunique-Mode HAFunique-Lower95 HAFunique-Lower50 HAFunique-Upper50 HAFunique-Upper95 HAFunique-Max HAFunique-Var HAFunique-SD HAFunique-Skew HAFunique-Kurt phi-Mean phi-Median phi-Mode phi-Lower95 phi-Lower50 phi-Upper50 phi-Upper95 phi-Max phi-Var phi-SD phi-Skew phi-Kurt kappa-Mean kappa-Median kappa-Mode kappa-Lower95 kappa-Lower50 kappa-Upper50 kappa-Upper95 kappa-Max kappa-Var kappa-SD kappa-Skew kappa-Kurt SFS-Mean SFS-Median SFS-Mode SFS-Lower95 SFS-Lower50 SFS-Upper50 SFS-Upper95 SFS-Max SFS-Var SFS-SD SFS-Skew SFS-Kurt SAFE-Mean SAFE-Median SAFE-Mode SAFE-Lower95 SAFE-Lower50 SAFE-Upper50 SAFE-Upper95 SAFE-Max SAFE-Var SAFE-SD SAFE-Skew SAFE-Kurt
  do
  for j in AOM BFM BFS CMS GAS GNS GWA KES UGS
    do
    rm temp.${i}.${j}
  done
done
