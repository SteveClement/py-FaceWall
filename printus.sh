while [ true ]; do

./fb-printer.py

if [ -e print.txt ]; then
  lpr -o landscape -o Pagesize=w68h252 print.txt && rm print.txt
fi

sleep 1
done
