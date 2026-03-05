import re
import json

# read receipt text
with open("raw.txt","r",encoding="utf-8") as f:
   text=f.read()

lines=text.splitlines()

# extract product names
products=[]
for i in range(len(lines)-1):
   if re.fullmatch(r"\d+\.",lines[i].strip()):
       name=lines[i+1].strip()
       if name:
           products.append(name)

# extract prices after "Стоимость"
prices=[]
for i in range(len(lines)-1):
   if lines[i].strip()=="Стоимость":
       s=lines[i+1].strip()
       s=s.replace(" ","").replace(",",".")
       if re.fullmatch(r"\d+(\.\d{2})",s):
           prices.append(float(s))

# calculate total from items
calculated_total=round(sum(prices),2)

# extract total from receipt
total_from_receipt=None
m=re.search(r"ИТОГО:\s*([\d\s]+,\d{2})",text)
if m:
   total_from_receipt=float(m.group(1).replace(" ","").replace(",","."))

# extract payment method
payment_method=None
payment_amount=None
m=re.search(r"(Банковская карта|Наличные)\s*:\s*([\d\s]+,\d{2})",text)
if m:
   payment_method=m.group(1)
   payment_amount=float(m.group(2).replace(" ","").replace(",","."))

# extract date and time
datetime=None
m=re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})",text)
if m:
   datetime=m.group(1)

# structured result
result={
"datetime":datetime,
"payment_method":payment_method,
"payment_amount":payment_amount,
"products":products,
"prices":prices,
"items_count":len(products),
"calculated_total":calculated_total,
"total_from_receipt":total_from_receipt,
"total_matches":calculated_total==total_from_receipt if total_from_receipt else None
}

print(json.dumps(result,indent=2,ensure_ascii=False))