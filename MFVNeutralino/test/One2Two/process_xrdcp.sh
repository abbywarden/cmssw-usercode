#!/bin/bash

for x in "$@"; do
  store="poop"
  echo $x
  ndr=$(ls $x | wc -l)
  mydir="${x#/eos/uscms}"
  echo $mydir
  for i in $(seq 0 $ndr); do
      j="000$i"
      #nd=$(printf '%04i' $j )
      for file in "$x/$j/"*; do
          trimmed="${file#/eos/uscms}"
          xrdcp root://cmseos.fnal.gov$trimmed .
      done
  done
done
