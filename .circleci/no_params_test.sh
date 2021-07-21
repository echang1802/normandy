
echo "Starting test"
echo "No params test"
echo date

if python main.py ; then
  echo "Process ended succefully"
else
  echo "----- >>>  Test fail!! <<< -----"
  exit 1
fi

FILE=processed_dev/sample_process.csv
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else
  echo "$FILE do not exists"
  echo "----- >>>  Test fail!! <<< -----"
  exit 1
fi

rm $FILE
echo "Test ended OK!"
