import re
import json

# RegEx examples section


text_example = "Order 123 paid by CARD total 1500 KZT"

print("=== RegEx Examples ===")

# search
match = re.search(r"\d+", text_example)
print("search:", match.group(0) if match else None)

# findall
numbers = re.findall(r"\d+", text_example)
print("findall:", numbers)

# split
words = re.split(r"\s+", text_example)
print("split:", words)

# sub
replaced = re.sub(r"\d+", "X", text_example)
print("sub:", replaced)

print()



# Receipt parsing section


with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


# find all prices (example: 1200, 1 200, 1200.50)
price_matches = re.findall(r"\d[\d\s]*\.?\d*", text)

prices = []
for p in price_matches:
    p = p.replace(" ", "")
    try:
        prices.append(float(p))
    except:
        pass


# find product names (lines that contain letters and a price)
products = []
lines = text.split("\n")

for line in lines:
    if re.search(r"[A-Za-zА-Яа-я]", line) and re.search(r"\d", line):
        name = re.sub(r"\d[\d\s]*\.?\d*", "", line).strip()
        if name:
            products.append(name)


# find date (simple pattern)
date_match = re.search(r"\d{2}[-/.]\d{2}[-/.]\d{4}", text)
date = date_match.group(0) if date_match else None


# find payment method
payment_match = re.search(r"CARD|CASH|KASPI|VISA|MASTERCARD", text, re.IGNORECASE)
payment = payment_match.group(0) if payment_match else None


# calculate total
total = round(sum(prices), 2)


# structured output
result = {
    "date": date,
    "payment_method": payment,
    "products": products,
    "prices": prices,
    "calculated_total": total
}

print("=== Parsed Receipt ===")
print(json.dumps(result, indent=2, ensure_ascii=False))