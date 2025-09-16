import os
import pandas as pd


def main():
	data = [
		{"CaseNumber": "2025-001", "Article": "158", "Part": "3", "Point": "в", "Amount": 300000, "RekvizitCode": 1},
		{"CaseNumber": "2025-002", "Article": "158", "Part": "3", "Point": "в", "Amount": 200000, "RekvizitCode": 1},
		{"CaseNumber": "2025-003", "Article": "159", "Part": "4", "Point": "",  "Amount": 1200000, "RekvizitCode": 2},
		{"CaseNumber": "2025-004", "Article": "158", "Part": "2", "Point": "",  "Amount": 10000,   "RekvizitCode": 6},
	]
	df = pd.DataFrame(data)
	os.makedirs("/workspace/samples", exist_ok=True)
	path = "/workspace/samples/input.xlsx"
	df.to_excel(path, index=False)
	print("Wrote", path)


if __name__ == "__main__":
	main()

