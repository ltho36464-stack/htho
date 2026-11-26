import urllib.request
import json
import datetime
import os

url = "https://wtxmd52.tele68.com/v1/txmd5/sessions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)
json_data = json.loads(res.read().decode())
new_data = json_data.get('list', [])

if not new_data:
    print("Khong co du lieu tu API.")
else:
    filename = "3.txt"
    old_ids = set()
    
    # 1. Đọc file cũ để lấy danh sách các ID đã có (chống trùng lặp)
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                # Tìm các dòng có chứa ID (dòng bắt đầu bằng số thứ tự)
                parts = line.split()
                if len(parts) > 2 and parts[0].isdigit() and parts[1].isdigit():
                    old_ids.add(parts[1]) # Lưu ID cũ vào bộ nhớ

    # 2. Lọc ra các phiên MỚI CHƯA CÓ trong file cũ
    added_count = 0
    lines_to_add = []
    
    for item in new_data:
        session_id = str(item.get('id', ''))
        if session_id not in old_ids:
            xx = item.get('dices', [0,0,0])
            xx_str = f"[{xx[0]},{xx[1]},{xx[2]}]"
            kq = item.get('resultTruyenThong', 'N/A')
            point = str(item.get('point', 0))
            # Format dòng mới
            lines_to_add.append(f"{session_id:<12} {kq:<6} {xx_str:<12} {point:<6}")
            added_count += 1

    # 3. Ghi nối tiếp vào file nếu có phiên mới
    if added_count > 0:
        # Đảo ngược danh sách để phiên cũ nhất lên trước, mới nhất ở dưới
        lines_to_add.reverse() 
        
        with open(filename, "a", encoding="utf-8") as f:
            # Nếu file mới tinh, tạo tiêu đề
            if os.path.getsize(filename) == 0:
                f.write("="*50 + "\n")
                f.write("DANH SACH KET QUA XUC XAC (LUY KE)\n")
                f.write("="*50 + "\n")
                f.write(f"{'ID':<12} {'KQ':<6} {'Xuc xac':<12} {'Diem':<6}\n")
                f.write("-"*50 + "\n")
            
            for line in lines_to_add:
                f.write(line + "\n")
        print(f"=> Da them {added_count} phien moi vao file {filename}!")
    else:
        print("=> Khong co phien moi nao. Du lieu da cap nhat.")