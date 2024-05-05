import os, pandas as pd, requests

def df_csv(file_path, url):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        print("File loaded successfully.")
    else:
        df = None
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            df = pd.read_csv(file_path)
            print("File downloaded successfully.")
        else:
            print(f"Failed to download file: {response.status_code}")
    return df.to_dict(orient='records')