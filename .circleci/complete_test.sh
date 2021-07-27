
echo "Starting test"
echo "Complete test"
echo date

echo "Avoid tags test"
if python main.py -tags complete -tags all; then
  echo "Process ended succefully"
else
  echo "----- >>>  Test fail!! <<< -----"
  exit 1
fi

FILE1=processed_dev/sample_process.csv
FILE2=processed_dev/data_extra.csv
if [ -f "$FILE1" ]; then
  echo "$FILE1 exists"
  echo "----- >>>  Test fail!! <<< -----"
  exit 1
else
  echo "$FILE1 do not exists."
  if [ -f "$FILE2" ]; then
    echo "$FILE2 exists."
  else
    echo "$FILE2 do not exists"
    echo "----- >>>  Test fail!! <<< -----"
    exit 1
fi

rm $FILE2

echo "Multiprocess test"
if python main.py -tags complete; then
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
