import streamlit as st
import pandas as pd 
import plotly.express as px
import numpy as np
import textwrap


df = pd.read_csv('amazon.csv')
df_s_tratamento = df.copy()
df = df.drop(df.columns[9:16],axis=1)
df = df.rename(columns={
    'product_name':'nome_produto',
    'category': 'categoria',
    'discounted_price': 'preco_desconto',
    'actual_price': 'preco_atual',
    'discount_percentage': 'porcentagem_desconto',
    'rating':'avaliacao',
    'rating_count': 'quantidade_avaliacao',
    'about_product': 'sobre_produto'
})

colunas = ['preco_desconto','preco_atual']
df[colunas] = df[colunas].replace('₹|,','',regex=True) # retirando o simbolo da Rupia e |
df['preco_atual'] = df['preco_atual'].astype(float)*0.064 # convertendo rupia para real
df['preco_desconto'] = df['preco_desconto'].astype(float)*0.064 # convertendo rupia para real
df['preco_atual'] = df['preco_atual'].round(2) # arredondando para 2 casas decimas
df['preco_desconto'] = df['preco_desconto'].round(2) # arredondando para 2 casas decimas
df['avaliacao']= df['avaliacao'].replace("|", None)
df['avaliacao']= df['avaliacao'].astype(float)
df['sub_categoria']  = df['categoria'].str.split("|").str[0] # retirando o | e pegando somente a string antes 
df['sub_categoria']  = df['sub_categoria'].str.replace("&"," ").str.replace(r'([a-z])([A-Z])', r'\1 \2')
df['quantidade_avaliacao'] = df['quantidade_avaliacao'].str.replace(",","").astype(float)


df_grafico1 = round(df.groupby('sub_categoria')['preco_atual'].sum().reset_index().sort_values(by='preco_atual',ascending=False))
df_grafico1['sub_categoria'] = df_grafico1['sub_categoria'].apply(lambda x: "<br>".join(textwrap.wrap(x, width=11)))

df_grafico2 = round(df.groupby('sub_categoria')['avaliacao'].mean().reset_index().sort_values(by='avaliacao',ascending=False),2)
df_grafico2['sub_categoria'] = df_grafico2['sub_categoria'].apply(lambda x: "<br>".join(textwrap.wrap(x, width=11)))

#vendas por categoria = countrow groupby(categoria)



fig = px.bar(df_grafico1,
             x='sub_categoria', y='preco_atual', 
             text='preco_atual',
             title='Total gasto por categoria',
             text_auto='.2s',
             color_discrete_sequence=["orange"],
             labels = ({'sub_categoria':'','preco_atual':''})
             )




fig2 = px.bar( df_grafico2, 
               x='sub_categoria', y='avaliacao',
               text='avaliacao',
               title='Media de Avaliação por Categoria do Produto',
               color_discrete_sequence=["green"],
               labels = ({'sub_categoria':'Categoria','avaliacao':'Media'})
               )




quantidade_total_avaliacao = df['quantidade_avaliacao'].sum()
quantidade_total_avaliacao_formatada = '{:,.0f}'.format(quantidade_total_avaliacao)
quantidade_total_vendas = df['avaliacao'].count() 






st.title("Dashboard Amazon - Projeto")
st.subheader("")


esquerda , direita = st.columns(2)

with esquerda:
    st.subheader(f"QTD Total de Avaliações: {quantidade_total_avaliacao_formatada}")


with direita:
    st.subheader(f"Quantidade Total de Vendas: {quantidade_total_vendas}")

st.subheader("")
st.text("Dataframe sem tratamento =)")
st.dataframe(df_s_tratamento,width = 1000 , height = 200)

st.subheader("")
st.text("Dataframe Tratado =)")
st.dataframe(df,width = 1000 , height = 200)

st.write(fig)

st.write(fig2)

#st.sidebar.title("Filtros")

#st.sidebar.selectbox("Selecione o filtro :money_with_wings:", ['']+["Teste1","Teste2","Teste3"])
