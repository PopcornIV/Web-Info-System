import qrcode

base_url = "http://127.0.0.1:8000/menu/?table="

for table in range(1, 11):  # Generate QR for tables 1 to 10
    url = f"{base_url}{table}"
    img = qrcode.make(url)
    img.save(f"table_{table}.png")
