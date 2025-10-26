import pandas as pd
import requests

# ==== 1️⃣ Đường dẫn file CSV ====
csv_path = "anime_data.csv"   # thay bằng file của bạn

# ==== 2️⃣ Đọc file ====
df = pd.read_csv(csv_path)

# ==== 3️⃣ URL API ====
api_url = "http://127.0.0.1:8000/api/anime/add/"

# ==== 4️⃣ Lặp qua từng dòng và gửi request ====
for idx, row in df.iterrows():
    anime_data = {
        "anime_code": row.get("ID", ""),
        "title": row.get("Title", ""),
        "subtitle": row.get("SubTitle", ""),
        "description": row.get("Description", ""),
        "image_link": row.get("Image_link", ""),
        "new_episode": row.get("Tập mới", ""),
        "latest_episode": row.get("Tập mới nhất", ""),
        "release_schedule": row.get("Lịch chiếu", ""),
        "genres": row.get("Thể loại", ""),
        "director": row.get("Đạo diễn", ""),
        "country": row.get("Quốc gia", ""),
        "duration": row.get("Thời lượng", ""),
        "anime_link": row.get("link_anime", ""),
    }

    try:
        response = requests.post(api_url, json=anime_data, timeout=10)
        if response.status_code in [200, 201]:
            print(f"✅ {idx+1}/{len(df)} | Thành công: {anime_data['title']}")
        else:
            print(f"⚠️ {idx+1}/{len(df)} | Lỗi {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ {idx+1}/{len(df)} | Lỗi khi gửi request: {e}")
