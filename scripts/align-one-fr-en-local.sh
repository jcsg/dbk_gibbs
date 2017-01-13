#!/bin/bash

#$ -S /bin/bash
#$ -V
#$ -cwd
#$ -l num_proc=1,mem_free=4g,h_rt=24:00:00
#$ -j y -o align-one.log

set -u

fr=$(echo $1 | cut -d- -f1,4)
en=$(echo $2 | cut -d- -f1,4)

root=/Users/jcsg/Packages/dbk_gibbs

dir=$root/alignments/$fr/$fr.$en

if [[ -s "$dir/training.align" ]]; then
  echo "$dir already done"
  exit
fi

rm -rf $dir
mkdir -p $dir
cd $dir

paste $root/data/parallel/{$1,$2} $root/data/versenames.txt | awk -F'\t' '{if ($1 != "" && $2 != "") print}' | $root/scripts/splittabs.pl $dir/corpus.$fr $dir/corpus.$en versenames.txt

cp $root/scripts/word-align.conf .
# echo "execDir /Users/jcsg/Packages/berkeleyaligner" >> word-align.confs
echo "foreignSuffix $fr" >> word-align.conf
echo "englishSuffix $en" >> word-align.conf
echo "trainSources $dir/corpus" >> word-align.conf
echo "testSources $dir/corpus" >> word-align.conf

java -server -d64 -Xmx4g -jar /Users/jcsg/Packages/berkeleyaligner/berkeleyaligner.jar ++word-align.conf
