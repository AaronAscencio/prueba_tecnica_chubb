import pandas as pd 

# Leyendo el archivo excel
df = pd.read_excel('example_file.xlsx')
# Aplicando el cambio de formato en el cual solo se obtendra el mes y dia 
df['campo-3'] = df['campo-3'].dt.strftime('%m-%d')
# Guardando en un archivo plano
df.to_csv('output_file.csv', index=False)