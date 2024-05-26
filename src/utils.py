import json

def load_initial_data(simulator, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    for table_name, families in data['tables'].items():
        simulator.create_table(table_name, families.keys())
        for family_name, rows in families.items():
            for row_key, columns in rows.items():
                for column_name, (value, timestamp) in columns.items():
                    simulator.put(table_name, row_key, family_name, column_name, value, timestamp)
