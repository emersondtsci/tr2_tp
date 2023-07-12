import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = "Sobre o conjunto de dados",
    #page_icon=""
    )
st.title('Home')
st.sidebar.success("Selecione uma página")

######################### - LEITURA DOS DADOS - ##############################

df = pd.read_csv('data_ru.csv', sep=';', index_col='date')

######################### - DATAFRAME - ##############################

st.header('Séries Temporais - Refeições do RU')
st.subheader('Conjunto de Dados')
st.dataframe(df, column_config={ 'date':'Data', 'lunch':'Almoço', 'dinner':'Jantar'}, use_container_width=True)

st.write(f'Número de Linhas do conjunto de dados: {df.shape[0]}')
st.write(f'Número de Colunas do conjunto de dados: {df.shape[1]} ')
st.write(f'Intervalo dos dados: {df.index.min()} : {df.index.max()}')

st.markdown('')

st.markdown('<div style="text-align: justify;">O conjunto de dados contém informações de aproximadamente 4 anos e 3 meses sobre o'
            'número total de refeições (almoços e jantares) fornecidas pelo RU entre 04 de'
            'janeiro de 2016 e 31 de Março de 2020, cada registro é feito diariamente. O'
            'conjunto de dados tem um total de 1095 observações, sem valores ausentes.</div>', unsafe_allow_html=True)


######################### - ESTATÍTICAS DESCRITÍVAS - ##############################

st.markdown('')

st.subheader('Estatísticas Descritivas dos Dados')
st.dataframe(df.describe(), use_container_width=True, column_config={ 'date':'Data', 'lunch':'Almoço', 'dinner':'Jantar'})

st.markdown('')

st.markdown('<div style="text-align: justify;">Analisado o Desvio Padrão das variáveis "lunch" e "dinner",'
                        'podemos concluir que temos um conjunto de dados é muito disperso em relação a média dos dados.'
                        '</div>', unsafe_allow_html=True)
#st.write(print('  '))
st.markdown('')

st.markdown('<div style="text-align: justify;">Uma curiosidade ocorre na coluna "dinner", vemos que o primeiro quartil, '
            'igual a 25% dos dados, são iguais ao valor mínimo e indica que em pelo menos 25% dos dias do nosso '
            'conjunto de dados não foi servido o jantar.</div>', unsafe_allow_html=True)

