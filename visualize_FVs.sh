for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  x=0
  for i in Neut Hard Soft PartialHard PartialSoft
    do
    let "x=${x}+1"
    for j in {-2..10}
      do
      if [ ${i} == "Neut" ] && [ ${j} == 0 ]
        then
        filename=spNeut.fvec
      fi
      if [ ${j} == -2 ] && [ ${i} != "Neut" ]
        then
        filename=`echo "neut.fvec linkedHard.fvec linkedSoft.fvec linkedPartialHard.fvec linkedPartialSoft.fvec"|cut -d " " -f ${x}`
      fi
      if [ ${j} == -1 ] && [ ${i} != "Neut" ]
        then
        filename=`echo "neut.fvec hard.fvec soft.fvec partialHard.fvec partialSoft.fvec"|cut -d " " -f ${x}`
      fi
      if [ ${j} -gt -1 ] && [ ${i} != "Neut" ]
        then
        filename=sp${i}_${j}.fvec
      fi
      if [ ${j} == 0 ] || [ ${i} != "Neut" ]
        then
        if [ -f FVs_SAFE_stats/$pop/${filename} ]
          then
          echo "library(RColorBrewer)
          FVs=as.matrix(read.table('FVs_SAFE_stats/$pop/${filename}'))
          FVs=FVs[-1,]
          if(${j}<0){
            FVs=FVs[,-1]
          }
          FVs[FVs=='nan']=0
          FV=NULL
          for(k in 1:ncol(FVs)){
            FV=c(FV,median(as.numeric(FVs[,k])))
          }
          FV_image=NULL
          for(k in 1:(length(FV)/11)){
            FV_image=rbind(FV_image,FV[(((k-1)*11)+1):(k*11)])
          }
          {
            pdf('FVs_SAFE_stats/$pop/heatmap_`echo ${filename}|sed -e 's/sp//g' -e 's/fvec/pdf/g'`')
            heatmap(FV_image,Rowv=NA,Colv=NA,col=colorRampPalette(brewer.pal(9,'Greens'))(1000))
            dev.off()
          }
          "|R -s
        fi
      fi
    done
  done
done
