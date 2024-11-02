import pandas as pd

class FunctionalDependency:
    def __init__(self, determinants, dependents):
        self.determinants = determinants
        self.dependents = dependents
        self.is_multivalued = False

class MultivaluedDependency:
    def __init__(self, determinants, dependents):
        self.determinants = determinants
        self.dependents = dependents
        self.is_multivalued = True

def parse_fd_file(filepath):
    """Parse the functional dependencies and multivalued dependencies from a given file."""
    fds = []
    mvds = []
    
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                
                if '-->>' in line:
                    determinant, dependents = line.split('-->>')
                    determinants = set(map(str.strip, determinant.split(',')))
                    dependents = set(map(str.strip, dependents.split(',')))
                    mvds.append(MultivaluedDependency(determinants, dependents))
                elif '->' in line:
                    determinant, dependents = line.split('->')
                    determinants = set(map(str.strip, determinant.split(',')))
                    dependents = set(map(str.strip, dependents.split(',')))
                    fds.append(FunctionalDependency(determinants, dependents))
                    
    except Exception as e:
        print(f"Error reading functional dependencies: {e}")

    return fds, mvds

def is_in_first_normal_form(df):
    """Check if the DataFrame is in First Normal Form (1NF)."""
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list) or isinstance(x, dict)).any():
            return False
    return True

def remove_duplicate_rows(df):
    """Remove duplicate rows from DataFrame."""
    return df.drop_duplicates()

def generate_1nf(df):
    """Generate SQL query for 1NF."""
    return "CREATE TABLE MainData AS SELECT * FROM MainData;"

def generate_2nf(fds, primary_keys):
    """Generate SQL queries for 2NF."""
    tables = []
    for fd in fds:
        if set(fd.determinants).issubset(primary_keys):
            table_name = f"Table_{'_'.join(fd.determinants)}"
            query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
            tables.append((table_name, query))
    return tables

def generate_3nf(fds):
    """Generate SQL queries for 3NF."""
    tables = []
    for fd in fds:
        table_name = f"Table_{'_'.join(fd.determinants)}"
        query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
        tables.append((table_name, query))
    return tables

def generate_bcnf(fds):
    """Generate SQL queries for BCNF."""
    tables = []
    for fd in fds:
        if not is_superkey(fd.determinants):
            table_name = f"Table_{'_'.join(fd.determinants)}"
            query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
            tables.append((table_name, query))
    return tables

def is_superkey(determinants):
    """Determine if the given determinants form a superkey."""
    return True

def generate_4nf(mvds):
    """Generate SQL queries for 4NF."""
    tables = []
    for mvd in mvds:
        table_name = f"MVD_Table_{'_'.join(mvd.determinants)}"
        query = f"CREATE TABLE {table_name} AS SELECT {', '.join(mvd.determinants.union(mvd.dependents))} FROM MainData;"
        tables.append((table_name, query))
    return tables

def generate_5nf(fds):
    """Generate SQL queries for 5NF."""
    tables = []
    for fd in fds:
        table_name = f"5NF_Table_{'_'.join(fd.determinants)}"
        query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
        tables.append((table_name, query))
    return tables

def save_queries_to_file(queries, filename):
    """Saves the provided queries to a specified SQL file."""
    try:
        with open(filename, 'w') as file:
            for table_name, query in queries:
                file.write(f"-- Query for {table_name}\n")
                file.write(f"{query};\n\n")
        print(f"Queries saved to {filename}.")
    except Exception as e:
        print(f"Error saving queries to file: {e}")

def main():
    primary_keys = input("Enter the primary keys (comma-separated): ").strip().split(',')

    print("\nReading functional dependencies...")
    fds, mvds = parse_fd_file('fd.txt')

    print("\nReading CSV file...")
    try:
        df = pd.read_excel('data1.xlsx')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print("\nChoose the highest Normal Form to reach:")
    print("1. 1NF")
    print("2. 2NF")
    print("3. 3NF")
    print("4. BCNF")
    print("5. 4NF")
    print("6. 5NF")

    try:
        target_nf = int(input("Enter your choice (1-6): "))
        if target_nf < 1 or target_nf > 6:
            raise ValueError("Invalid choice. Please select a number between 1 and 6.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    all_queries = []

    if target_nf == 1:
        print("\n-- Tables in 1NF --")
        queries_1nf = [("MainData", generate_1nf(df))]
        all_queries.extend(queries_1nf)
        for table_name, query in queries_1nf:
            print(f"\n{query}")

    if target_nf >= 2:
        print("\n-- Tables in 2NF --")
        queries_2nf = generate_2nf(fds, primary_keys)
        all_queries.extend(queries_2nf)
        for table_name, query in queries_2nf:
            print(f"\n{query}")

    if target_nf >= 3:
        print("\n-- Tables in 3NF --")
        queries_3nf = generate_3nf(fds)
        all_queries.extend(queries_3nf)
        for table_name, query in queries_3nf:
            print(f"\n{query}")

    if target_nf >= 4:
        print("\n-- Tables in BCNF --")
        queries_bcnf = generate_bcnf(fds)
        all_queries.extend(queries_bcnf)
        for table_name, query in queries_bcnf:
            print(f"\n{query}")

    if target_nf >= 5:
        print("\n-- Tables in 4NF --")
        queries_4nf = generate_4nf(mvds)
        all_queries.extend(queries_4nf)
        for table_name, query in queries_4nf:
            print(f"\n{query}")

    if target_nf == 6:
        print("\n-- Tables in 5NF --")
        queries_5nf = generate_5nf(fds)
        all_queries.extend(queries_5nf)
        for table_name, query in queries_5nf:
            print(f"\n{query}")

    # Save all queries to a single output file
    save_queries_to_file(all_queries, "Output.sql")

if __name__ == "__main__":
    main()
