import csv
import time

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

with open("FILE_CREATE", "w", encoding="utf-8") as file:
    with open("CSV_FILE", "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                page = urllib2.urlopen("https://play.google.com/store/apps/details?id=" + row[0])
                soup = BeautifulSoup(page, "html.parser")
                name_elem = soup.find(itemprop="name")
                name = name_elem.get_text() if name_elem else "Not found"
                company_elem = soup.find("span", itemprop="name")
                company = company_elem.get_text() if company_elem else "Not found"
                category_elem = soup.find("span", itemprop="genre")
                category = category_elem.get_text() if category_elem else "Not found"
                line = f"{row[0]};{name};{company};{category}\n"
                file.write(line)
                print(line.strip())
            except Exception:
                file.write(f"{row[0]};Not found\n")
                print(f"{row[0]};Not found")

print("Ended")
