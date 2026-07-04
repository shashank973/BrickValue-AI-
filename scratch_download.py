import urllib.request
import traceback

urls = [
    "https://raw.githubusercontent.com/yasserh/housing-prices-dataset/main/Housing.csv",
    "https://raw.githubusercontent.com/yasserh/housing-prices-dataset/master/Housing.csv",
    "https://raw.githubusercontent.com/Jonas-Nothgraf/Housing-Prices-Dataset/main/Housing.csv",
    "https://raw.githubusercontent.com/Jonas-Nothgraf/Housing-Prices-Dataset/master/Housing.csv",
    "https://raw.githubusercontent.com/hds-oklahoma/HDS5233-Standard-Datasets/master/Housing.csv",
    "https://raw.githubusercontent.com/hds-oklahoma/HDS5233-Standard-Datasets/main/Housing.csv",
    "https://raw.githubusercontent.com/singh-naman/House-Price-Prediction/master/Housing.csv",
    "https://raw.githubusercontent.com/singh-naman/House-Price-Prediction/main/Housing.csv",
    "https://raw.githubusercontent.com/sid-6/House-price-prediction/master/Housing.csv",
    "https://raw.githubusercontent.com/sid-6/House-price-prediction/main/Housing.csv",
    "https://raw.githubusercontent.com/tanishq-g/house-price-prediction/main/Housing.csv",
    "https://raw.githubusercontent.com/tanishq-g/house-price-prediction/master/Housing.csv",
    "https://raw.githubusercontent.com/ajay-dara/Delhi-House-Price-Prediction/master/Housing.csv",
    "https://raw.githubusercontent.com/ajay-dara/Delhi-House-Price-Prediction/main/Housing.csv",
    "https://raw.githubusercontent.com/zobi123/Delhi-House-Price-Prediction/master/Housing.csv",
    "https://raw.githubusercontent.com/zobi123/Delhi-House-Price-Prediction/main/Housing.csv",
    "https://raw.githubusercontent.com/teclov/Delhi-House-Price-Prediction/master/Housing.csv",
    "https://raw.githubusercontent.com/teclov/Delhi-House-Price-Prediction/main/Housing.csv",
    "https://raw.githubusercontent.com/Prashant-Sikka/Delhi-House-Price-Prediction-System/master/Housing.csv",
    "https://raw.githubusercontent.com/Prashant-Sikka/Delhi-House-Price-Prediction-System/main/Housing.csv"
]

print(f"Testing {len(urls)} candidate URLs...")
found = False
for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            if len(content) > 1000:  # Verify it's not a small text error page
                print(f"[SUCCESS] {url} - Size: {len(content)} bytes")
                found = True
                break
            else:
                print(f"[PARTIAL SUCCESS but too small] {url} - Size: {len(content)} bytes")
    except Exception as e:
        print(f"[FAILED] {url} - {str(e)}")

if not found:
    print("None of the candidate URLs succeeded.")
