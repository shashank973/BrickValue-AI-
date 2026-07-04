import urllib.request
import os

url = "https://raw.githubusercontent.com/LetisAlba/Data_621/master/Final_Project/csv/Housing.csv"
output_dir = "data"
output_file = os.path.join(output_dir, "Housing.csv")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Downloading from {url}...")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        content = response.read()
        if len(content) > 1000:
            with open(output_file, 'wb') as f:
                f.write(content)
            print(f"[SUCCESS] Downloaded to {output_file} - Size: {len(content)} bytes")
            
            # Print the head of the file
            lines = content.decode('utf-8').splitlines()
            print("First 5 lines:")
            for line in lines[:5]:
                print(line)
        else:
            print("[FAILED] Downloaded content too small, probably an error page.")
except Exception as e:
    print(f"[ERROR] Failed to download: {e}")
