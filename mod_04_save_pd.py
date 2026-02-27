import pandas as pd

news_df = pd.DataFrame(columns=["Title","Text","Date","Summary","Keywords","Category"])

# Δημιουργία ενός πίνακα, βάζω στήλες κτλ
def create_df():
    name = input("give me name  ").strip()
    columns1 = []
    
    while True:
        add_columns = input("press 1 to add column, 2 to exit")
        if add_columns == "1":
            column_name = input("give me new column")
            columns1.append(column_name)
        elif add_columns == "2":
            break
        else: print("this is not an option")

    df = pd.DataFrame(columns=columns1)

    globals()[f"{name}_df"] = df
    print(df)
    return(df)

#Εκδοχή χωρίς globals
def create_df_better():
    dataframes = {}
    name = input("Give me DataFrame name: ").strip()
    
    columns = []
    while True:
        add_columns = input("Press 1 to add column, 2 to exit: ").strip()
        if add_columns == '1':
            columns.append(input("Give me new column name: ").strip())
        elif add_columns == '2':
            break
        else:
            print("Invalid input. Please enter 1 or 2.")
    
    dataframes[name] = pd.DataFrame(columns=columns)
    print(f"DataFrame '{name}' created with columns: {columns}")
    return dataframes[name]

#Συμπληρώνω μια γραμμή 
def fill_a_new_line():
    raw_data = input("import with this order Title, Text, Date, Summary, seperated by comma ")
    x, y, z, w = raw_data.split(",",3)
    return[x.strip(),y.strip(),z.strip(),w.strip()]
    
#Συμπληρώνω μια γραμμή με δύο ορίσματα - τη γραμμή και το df  
def import_new_line_to_df(new_line, news_df):
    news_df.loc[len(news_df)] = new_line
    return news_df

#Εισαγωγή μιας νέας στήλης
def import_a_column(df):
    new_column = input("Import your new column name: ")
    default_value = input(f"Default value for '{new_column}' (leave empty for None): ")
    df[new_column] = default_value if default_value else None
    return df


print(news_df)