#!/bin/bash

query="hockey"
method="tfidf"
num_runs=10
output_file="ranking_test_results.csv"

echo "Run,Query,Ranking_Time_Seconds" > $output_file

total_time=0

for i in $(seq 1 $num_runs); do
    echo "Run $i/$num_runs"
    
    output=$(python query.py "$query" "$method" 2>&1)
    
    ranking_time=$(echo "$output" | grep "Ranking time" | awk '{print $4}')
    
    echo "$i,$query,$ranking_time" >> $output_file
    
    total_time=$(awk "BEGIN {print $total_time + $ranking_time}")
done

avg_time=$(awk "BEGIN {printf \"%.4f\", $total_time / $num_runs}")

echo "Average,$query,$avg_time" >> $output_file

echo ""
echo "Average ranking time: $avg_time seconds"
echo "Results saved to $output_file"
