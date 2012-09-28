while [ true ]; do

./fb-printer-new.py

if [ -e print.txt ]; then
  # Use this line for printing to a Named Printer
  lpr -PDYMO_LabelWriter_450 -o landscape -o Pagesize=w68h252 print.txt && rm print.txt
  # Use this line for printing to the default printer (if defined)
  #lpr -o landscape -o Pagesize=w68h252 print.txt && rm print.txt
fi

sleep 4
done
