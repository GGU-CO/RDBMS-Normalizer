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
    fds = []
    mvds = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
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
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list) or isinstance(x, dict)).any():
            return False
    return True

def generate_1nf(df):
    query = "CREATE TABLE MainData AS SELECT * FROM MainData;"
    print(query)
    return query

def generate_2nf(fds, primary_keys):
    tables = []
    for fd in fds:
        if set(fd.determinants).issubset(primary_keys):
            table_name = f"Table_{'_'.join(fd.determinants)}"
            query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
            print(query)
            tables.append((table_name, query))
    return tables

def generate_3nf(fds, primary_keys):
    tables = []
    for fd in fds:
        if not (set(fd.determinants).issubset(primary_keys)) and not any(dep in primary_keys for dep in fd.dependents):
            table_name = f"Table_{'_'.join(fd.determinants)}"
            query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
            print(query)
            tables.append((table_name, query))
    return tables

def generate_bcnf(fds):
    tables = []
    for fd in fds:
        if not is_superkey(fd.determinants):
            table_name = f"Table_{'_'.join(fd.determinants)}"
            query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
            print(query)
            tables.append((table_name, query))
    return tables

def is_superkey(determinants):
    return True  # Placeholder: Add logic for determining superkeys

def generate_4nf(mvds):
    tables = []
    for mvd in mvds:
        table_name = f"MVD_Table_{'_'.join(mvd.determinants)}"
        query = f"CREATE TABLE {table_name} AS SELECT {', '.join(mvd.determinants.union(mvd.dependents))} FROM MainData;"
        print(query)
        tables.append((table_name, query))
    return tables

def generate_5nf(fds):
    tables = []
    for fd in fds:
        table_name = f"5NF_Table_{'_'.join(fd.determinants)}"
        query = f"CREATE TABLE {table_name} AS SELECT {', '.join(fd.determinants.union(fd.dependents))} FROM MainData;"
        print(query)
        tables.append((table_name, query))
    return tables

def save_queries_to_file(queries, filename):
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
    primary_keys = set(primary_keys)
    fds, mvds = parse_fd_file('fd.txt')

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

    target_nf = int(input("Enter your choice (1-6): ").strip())
    all_queries = []

    if target_nf >= 1:
        print("\n-- Tables in 1NF --")
        queries_1nf = [("MainData", generate_1nf(df))]
        all_queries.extend(queries_1nf)

    if target_nf >= 2:
        print("\n-- Tables in 2NF --")
        queries_2nf = generate_2nf(fds, primary_keys)
        all_queries.extend(queries_2nf)

    if target_nf >= 3:
        print("\n-- Tables in 3NF --")
        queries_3nf = generate_3nf(fds, primary_keys)
        all_queries.extend(queries_3nf)

    if target_nf >= 4:
        print("\n-- Tables in BCNF --")
        queries_bcnf = generate_bcnf(fds)
        all_queries.extend(queries_bcnf)

    if target_nf >= 5:
        print("\n-- Tables in 4NF --")
        queries_4nf = generate_4nf(mvds)
        all_queries.extend(queries_4nf)

    if target_nf == 6:
        print("\n-- Tables in 5NF --")
        queries_5nf = generate_5nf(fds)
        all_queries.extend(queries_5nf)

    save_queries_to_file(all_queries, "Output.sql")

if __name__ == "__main__":
    main()
