import os

# Đường dẫn tới thư mục "Countries" (tính từ vị trí file script)
countries_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'Countries')

# Duyệt qua tất cả file trong thư mục
for root, dirs, files in os.walk(countries_dir):
    for file in files:
        if file.endswith('.bak'):
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Đã xóa: {file_path}")
            except Exception as e:
                print(f"Lỗi khi xóa {file_path}: {e}")

print("Hoàn tất xóa file .bak.")
