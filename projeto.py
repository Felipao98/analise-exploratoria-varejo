import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

df_dsa = pd.read_csv("dataset.csv")

print(df_dsa.columns)
print(df_dsa.dtypes)
print(df_dsa['Valor_Venda'].describe()) 
print(df_dsa[df_dsa.duplicated()]) 
print(df_dsa.isnull().sum())
print(df_dsa.head())

#PERGUNTA DE NEGOCIO 1 
df_dsa_p1 = df_dsa[df_dsa['Categoria'] == 'Office Supplies'] 
df_dsa_p1_total = df_dsa_p1.groupby('Cidade')['Valor_Venda'].sum()  
cidade_maior_venda = df_dsa_p1_total.idxmax() 
print("Cidade com maior valor de venda para 'Office Supplies': ", cidade_maior_venda)
df_dsa_p1_total.sort_values(ascending=False) 

#PERGUNTA DE NEGOCIO 2 
df_dsa_p2 = df_dsa.groupby('Data_Pedido')['Valor_Venda'].sum() 
print(df_dsa_p2.head()) 
plt.figure(figsize=(20,6)) 
df_dsa_p2.plot(x='Data_Pedido', y='Valor_Venda', color='green') 
plt.title('Total de Vendas Por Data do Pedido') 
plt.show() 

#PERGUNTA DE NEGOCIO 3 
df_dsa_p3 = df_dsa.groupby('Estado')['Valor_Venda'].sum().reset_index() 
plt.figure(figsize=(16,6))
sns.barplot(data=df_dsa_p3, x='Estado', y='Valor_Venda').set(title='Vendas por Estado') 
plt.xticks(rotation=80) 
plt.show()

#PERGUNTA DE NEGOCIO 4
df_dsa_p4 = df_dsa.groupby('Cidade')['Valor_Venda'].sum().reset_index().sort_values(by='Valor_Venda', ascending=False).head(10)
print(df_dsa_p4.head(10)) 
plt.figure(figsize=(16,6)) 
sns.set_palette('coolwarm') 
sns.barplot(data=df_dsa_p4, x='Cidade', y='Valor_Venda').set(title='As 10 Cidades com Maior Total de Vendas') #grafico de barras
plt.show()

#PERGUNTA DE NEGOCIO 5
df_dsa_p5 = df_dsa.groupby('Segmento')['Valor_Venda'].sum().reset_index().sort_values(by='Valor_Venda', ascending=False)
print(df_dsa_p5.head()) 

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct * total / 100))
        return ' $ {v:d}'.format(v=val)
    return my_format

plt.figure(figsize=(16,6)) 
plt.pie(df_dsa_p5['Valor_Venda'], labels=df_dsa_p5['Segmento'], autopct=autopct_format(df_dsa_p5['Valor_Venda']), startangle=90) 

centre_circle = plt.Circle((0,0), 0.82, fc='white') 
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.annotate(text='Total de Vendas: ' + '$ ' + str(int(sum(df_dsa_p5['Valor_Venda']))), xy=(-0.25, 0))
plt.title('Total de Vendas por Segmento')
plt.show()

#PERGUNTA DE NEGOCIO 6 
df_dsa['Data_Pedido'] = pd.to_datetime(df_dsa['Data_Pedido'], dayfirst=True) 
print(df_dsa.dtypes) 
print(df_dsa.head())
df_dsa['Ano'] = df_dsa['Data_Pedido'].dt.year 
print(df_dsa.head())
df_dsa_p6 = df_dsa.groupby(['Ano', 'Segmento'])['Valor_Venda'].sum() 
print(df_dsa_p6)

#PERGUNTA DE NEGOCIO 7 
df_dsa['Desconto'] = np.where(df_dsa['Valor_Venda'] > 1000, 0.15, 0.10) 
print(df_dsa.head())
print(df_dsa['Desconto'].value_counts()) 
print("No total 457 Vendas Receberiam Desconto de 15%.")

#PERGUNTA DE NEGOCIO 8
df_dsa['Valor_Venda_Desconto'] = df_dsa['Valor_Venda'] - (df_dsa['Valor_Venda'] * df_dsa['Desconto'])
print(df_dsa.head())

df_dsa_p8_vendas_antes_desconto = df_dsa.loc[df_dsa['Desconto'] == 0.15, 'Valor_Venda']

df_dsa_p8_vendas_depois_desconto = df_dsa.loc[df_dsa['Desconto'] == 0.15, 'Valor_Venda_Desconto']

media_vendas_antes_desconto = df_dsa_p8_vendas_antes_desconto.mean()

media_vendas_depois_desconto = df_dsa_p8_vendas_depois_desconto.mean()

print("Media das vendas antes do desconto de 15%: ", round(media_vendas_antes_desconto, 2))
print("Media das vendas depois do desconto de 15%: ", round(media_vendas_depois_desconto, 2))

#PERGUNTA DE NEGOCIO 9
df_dsa['Mes'] = df_dsa['Data_Pedido'].dt.month
print(df_dsa.head())

df_dsa_p9 = df_dsa.groupby(['Ano', 'Mes', 'Segmento'])['Valor_Venda'].agg([np.sum, np.mean, np.median])
print(df_dsa_p9)

anos = df_dsa_p9.index.get_level_values(0)
meses = df_dsa_p9.index.get_level_values(1)
segmentos = df_dsa_p9.index.get_level_values(2)

plt.figure(figsize=(12,6))
sns.set() 
fig1 = sns.relplot(kind='line', data=df_dsa_p9, y='mean', x=meses, hue=segmentos, col=anos, col_wrap=4) 
plt.show()

#PERGUNTA DE NEGOCIO 10
df_dsa_p10 = df_dsa.groupby(['Categoria', 'SubCategoria']).sum(numeric_only=True).sort_values('Valor_Venda', ascending=False).head(12)

df_dsa_p10 = df_dsa_p10[['Valor_Venda']].astype(int).sort_values(by='Categoria').reset_index()

print(df_dsa_p10)

df_dsa_p10_cat = df_dsa_p10.groupby('Categoria').sum(numeric_only=True).reset_index()

print(df_dsa_p10_cat)

cores_categorias = ['#5d00de', '#0ee84f', '#e80e27']

cores_subcategorias = ['#aa8cd4', '#aa8cd5', '#aa8cd6', '#aa8cd7', '#26c957', '#26c958', '#26c959', '#26c960', '#e65e65', '#e65e66', '#e65e67', '#e65e68']

fig, ax = plt.subplots(figsize=(18,12))

p1 = ax.pie(df_dsa_p10_cat['Valor_Venda'], radius=1, labels=df_dsa_p10_cat['Categoria'], wedgeprops=dict(edgecolor='white'), colors=cores_categorias)

p2 = ax.pie(df_dsa_p10['Valor_Venda'], radius=0.9, labels=df_dsa_p10['SubCategoria'], autopct=autopct_format(df_dsa_p10['Valor_Venda']), colors=cores_subcategorias, labeldistance=0.7, wedgeprops=dict(edgecolor='white'), pctdistance=0.53, rotatelabels=True)

centre_circle = plt.Circle((0,0), 0.6, fc='white')

fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.annotate(text='Total de Vendas: ' + '$ ' + str(int(sum(df_dsa_p10['Valor_Venda']))), xy=(-0.2, 0))
plt.title('Total de Vendas por Categoria e Top 12 SubCategorias')
plt.show()