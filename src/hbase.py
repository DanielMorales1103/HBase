class HBaseSimulator:
    def __init__(self):
        self.tables = {}
        self.table_status = {}

    def check_table_enabled(self, table_name):
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")
        if not self.table_status.get(table_name, True): 
            raise ValueError(f"Table '{table_name}' is disabled.")
        
    def create_table(self, table_name, column_families):
        if table_name in self.tables:
            raise ValueError("Table already exists.")
        self.tables[table_name] = {cf: {} for cf in column_families}
        self.table_status[table_name] = True
        print(f"Table '{table_name}' created with column families {column_families}.")

    def list_tables(self):
        return list(self.tables.keys())

    def put(self, table_name, row_key, column_family, column, value, timestamp=None):
        self.check_table_enabled(table_name)
        if column_family not in self.tables[table_name]:
            raise ValueError("Column family does not exist.")
        cell = (value, timestamp)
        self.tables[table_name][column_family].setdefault(row_key, {})[column] = cell

    def get(self, table_name, row_key, column_family, column):
        self.check_table_enabled(table_name)
        try:
            return self.tables[table_name][column_family][row_key][column]
        except KeyError:
            return None
    def scan(self, table_name):
        self.check_table_enabled(table_name)
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")
        # Recuperamos y retornamos todos los datos de la tabla
        return self.tables[table_name]
    
    def disable_table(self, table_name):
        self.check_table_exists(table_name)
        self.table_status[table_name] = False
        print(f"Table '{table_name}' has been disabled.")

    def drop_table(self, table_name):
        self.check_table_exists(table_name)
        del self.tables[table_name]
        del self.table_status[table_name]
        print(f"Table '{table_name}' has been dropped.")
    
    def enable_table(self, table_name):
        if table_name in self.tables:
            self.table_status[table_name] = True
            print(f"Table '{table_name}' has been enabled.")
        else:
            raise ValueError("Table does not exist.")
    
    def is_enabled(self, table_name):
        if table_name in self.tables:
            return self.tables[table_name].get('enabled', True)
        else:
            raise ValueError("Table does not exist.")
    
    def check_table_exists(self, table_name):
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")
        
    def truncate_table(self, table_name):
        self.check_table_exists(table_name)
        print(f"Starting truncate operation on table '{table_name}'.")
        self.disable_table(table_name)
        self.drop_table(table_name)
        self.create_table(table_name, [])  # Assuming no column families are specified
        print(f"Table '{table_name}' has been truncated and recreated.")
        
    def alter_table(self, table_name, operation, column_family):
        self.check_table_enabled(table_name)
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")

        if operation == "add":
            if column_family in self.tables[table_name]:
                raise ValueError(f"Column family '{column_family}' already exists in table '{table_name}'.")
            self.tables[table_name][column_family] = {}
            print(f"Added column family '{column_family}' to table '{table_name}'.")
        elif operation == "remove":
            if column_family not in self.tables[table_name]:
                raise ValueError(f"Column family '{column_family}' does not exist in table '{table_name}'.")
            del self.tables[table_name][column_family]
            print(f"Removed column family '{column_family}' from table '{table_name}'.")
        else:
            raise ValueError("Invalid operation. Use 'add' or 'remove'.")
    
    def drop_all_tables(self):
        self.tables.clear()  # Elimina todas las tablas
        self.table_status.clear()  # Limpia el estado de todas las tablas
        print("All tables have been dropped.")
        
    def describe_table(self, table_name):
        if table_name not in self.tables:
            raise ValueError("Table does not exist.")
        
        description = f"Table '{table_name}' description:\n"
        description += "Column Families:\n"
        for column_family in self.tables[table_name]:
            description += f"  - {column_family}\n"
        
        # Si decides incluir el estado de habilitación en la descripción
        status = "enabled" if self.table_status.get(table_name, True) else "disabled"
        description += f"Status: {status}"

        print(description)
