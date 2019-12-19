#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  x=0
  for i in Neut Hard Soft PartialHard PartialSoft
    do
    let "x=$x+1"
    for j in {-2..10}
      do
      if [ $i == "Neut" ]
        then
        filename=spNeut.fvec
      else
        if [ $j == -2 ]
          then
          filename=`echo "neut.fvec linkedHard.fvec linkedSoft.fvec linkedPartialHard.fvec linkedPartialSoft.fvec"|cut -d " " -f $x`
        else
          if [ $j == -1 ]
            then
            filename=`echo "neut.fvec hard.fvec soft.fvec partialHard.fvec partialSoft.fvec"|cut -d " " -f $x`
          else
            filename=sp${i}_$j.fvec
          fi
        fi
      fi
      if [ $i != "Neut" ] || [ $j == 0 ]
        then
        if [ -f trainingData/FVs/$pop/$filename ]
          then
          echo "library(RColorBrewer)
          FVs=as.matrix(read.table('trainingData/FVs/$pop/$filename'))
          FVs=FVs[-1,]
          if($j<0){
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
            pdf('trainingData/FVs/$pop/heatmap_`echo $filename|sed -e 's/sp//g' -e 's/fvec/pdf/g'`')
            heatmap(FV_image,Rowv=NA,Colv=NA,col=colorRampPalette(brewer.pal(9,'Greens'))(1000))
            dev.off()
          }
          "|R -s
        fi
      fi
    done
  done
done

