import csv
from pathlib import Path

def merge_countries_csv():
    root = Path(__file__).resolve().parents[2]
    src_dir = root / "Countries-v1"
    out_dir = root / "data" / "collected"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "countries-v1.csv"

    if not src_dir.exists():
        raise SystemExit(f"Không tìm thấy thư mục nguồn: {src_dir}")

    csv_files = sorted([p for p in src_dir.glob("*.csv")])
    if not csv_files:
        raise SystemExit(f"Không có file CSV nào trong {src_dir}")

    print(f"Tìm thấy {len(csv_files)} file CSV để ghép.")

    header_written = False
    expected_header = None
    total_rows = 0

    with out_file.open("w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout)
        for f in csv_files:
            with f.open("r", encoding="utf-8-sig", newline="") as fin:
                reader = csv.reader(fin)
                header = next(reader)
                if not header_written:
                    writer.writerow(header)
                    expected_header = header
                    header_written = True
                elif header != expected_header:
                    print(f"⚠️ Header khác nhau trong {f.name}")
                row_count = 0
                for row in reader:
                    writer.writerow(row)
                    row_count += 1
                total_rows += row_count
                print(f"- {f.name}: {row_count} dòng")

    print(f"✅ Xong! File kết quả: {out_file}")
    print(f"Tổng số dòng dữ liệu: {total_rows}")

if __name__ == "__main__":
    merge_countries_csv()
