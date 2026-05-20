import requests
import json
import re

def main():
    # 1. Gửi yêu cầu lấy dữ liệu từ trang chủ Hội Quán
    url = "https://sv2.hoiquan4.live/trang-chu"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        html_content = response.text
        
        # 2. Dùng thuật toán (Regex) để tự tìm tất cả các tên BLV hoặc ID trận đang có trên trang
        # (Đoạn này tìm các chuỗi có dạng hqtv_blv_... trong mã nguồn)
        blv_list = re.findall(r'hqtv_blv_[a-zA-Z0-9_]+', html_content)
        blv_list = list(set(blv_list)) # Lọc bỏ trùng lặp
        
        # 3. Tạo cấu trúc JSON cho MonPlayer
        mon_data = {
            "name": "Nguồn Hội Quán Tự Động",
            "author": "Auto Bot",
            "groups": [{
                "group_name": "Trận Đấu Đang Đá 🔥",
                "channels": []
            }]
        }
        
        # Nếu không quét được BLV nào (vắng trận), thêm kênh dự phòng
        if not blv_list:
            blv_list = ['hqtv_channel_1', 'hqtv_channel_2']
            
        for blv in blv_list:
            # Tạo tên hiển thị đẹp đẽ cho app
            display_name = blv.replace('hqtv_blv_', '🎙️ BLV ').upper()
            if 'channel' in blv:
                display_name = f"📺 Kênh Dự Phòng {blv[-1]}"
                
            channel_info = {
                "name": display_name,
                "url": f"https://hqlive.yarncdn.live/live/{blv}/playlist.m3u8",
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "https://sv2.hoiquan4.live/",
                    "Origin": "https://sv2.hoiquan4.live"
                }
            }
            mon_data["groups"][0]["channels"].append(channel_info)
            
        # 4. Lưu thành file json công khai
        with open("nguon.json", "w", encoding="utf-8") as f:
            json.dump(mon_data, f, ensure_ascii=False, indent=2)
            print("Đã cập nhật file nguon.json thành công!")
            
    except Exception as e:
        print(f"Lỗi rồi: {e}")

if __name__ == "__main__":
    main()
