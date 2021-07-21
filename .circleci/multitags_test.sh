
echo "Starting test"
echo "Multitags test"
echo date

if python main.py -tags process -tags add_info; then
  echo "Process ended succefully"
else
  echo "----- >>>  Test fail!! <<< -----"
  exit 1
fi

FILE1=processed_dev/sample_process.csv
FILE2=processed_dev/data_extra.csv
if [[ -f "$FILE1" && -f "$FILE2" ]]; then
    echo "$FILE1 and $FILE2 exists."
else
  echo "$FILE1 or $FILE2 do not exists"
  echo "----- >>>  Test fail!! <<< -----"
  exit 1
fi

rm $FILE1
rm $FILE2
echo "Test ended OK!"
