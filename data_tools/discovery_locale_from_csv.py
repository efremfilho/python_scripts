import chardet

def detect_encoding(file):
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

encoding = detect_encoding('/content/[YOUR CSV].csv')
print(f"Encoding: {encoding}")
