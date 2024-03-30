import csv

def fetch_details_by_id(target_id):
    details_dict = {}
    csv_file = "../database/all_logs.csv"
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['ID']) == target_id:
                minute_key = row['Date'] + ' ' + row['Time'][:5]
                if minute_key not in details_dict:
                    details_dict[minute_key] = []
                details_dict[minute_key].append({
                    'ID': int(row['ID']),
                    'Name': row['Name'],
                    'Time': row['Time'],
                    'Date': row['Date'],
                    'Location': row['Location']
                })
    return details_dict

k = fetch_details_by_id(1)
for minute_key, entries in k.items():
    print(f"For minute {minute_key}:")
    for entry in entries:
        print(entry)
