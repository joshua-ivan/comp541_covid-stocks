#!/bin/bash
declare -a exchanges=("AMEX" "NASDAQ" "NYSE" "NYSE Arca")
for exchange in "${exchanges[@]}" ; do
    for letter_one in {a..z} ; do
        for letter_two in {a..z} ; do
            python3 percent_performance.py "$exchange" $letter_one$letter_two
        done
    done
done
python3 aggregate_csvs.py
