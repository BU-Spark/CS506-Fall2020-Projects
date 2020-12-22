import pandas as pd

def filter(keyword, value, filepath, output_name):
    df = pd.read_csv(filepath)

    filtered = pd.DataFrame()

    df = df.dropna()
    for i in range(df.shape[0]):
        if value in df.loc[i][keyword]:
            filtered = filtered.append(df.loc[i])

    filtered.to_csv(output_name)

filter('Neighborhood', 'Boston', 'Reopen-Boston-Fund.csv', 'filtered_Reopen.csv')
#filter('Neighborhood', 'Boston', 'Small-Business-Relief-Fund.csv', 'filtered_Small.csv')