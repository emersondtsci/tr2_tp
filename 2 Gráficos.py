# Manipulação de dados.
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

#Análise de Séries Temporais
from statsmodels.tsa.seasonal import seasonal_decompose

#######################################################################################################################
data_ru = pd.read_csv('data_ru.csv', sep=';', index_col='date')

#st.dataframe(data_ru, column_config={ 'date':'Data', 'lunch':'Almoço', 'dinner':'Jantar'}, use_container_width=True)

#Decomposição dos Almoços.
lunch = seasonal_decompose(data_ru.lunch, model = 'additive', period = 365)
st.header('Decomposição da Série Temporal')
st.markdown('')

st.subheader('Almoço')
fig = plt.figure()
fig = lunch.plot()
fig.set_size_inches(18, 12)
plt.xticks([])
plt.yticks([])
plt.show()

st.pyplot(fig)
st.markdown('<div style="text-align: justify;">A partir das figuras acima, podemos ver que '
            'a série temporal de almoços não é estacionária. Pois apresenta sazonalidade e '
            'uma tendência ascendente.</div>', unsafe_allow_html=True)


#Decomposição dos Jantares.
dinner = seasonal_decompose(data_ru.dinner, model = 'additive', period = 365)

st.markdown('')

st.subheader('Jantar')
# Plot.
fig = plt.figure()
fig = dinner.plot()
fig.set_size_inches(18, 12)
plt.xticks([])
plt.yticks([])
st.pyplot(fig)

st.markdown('<div style="text-align: justify;">A partir das figuras acima, podemos ver que a série temporal '
            'dos jantares não é estacionária. Pois apresenta sazonalidade e uma tendência ascendente.</div>', unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------------------------------------------

st.header('Estacionariedade')
rolling_mean_size = 7
def visualize_stationarity(data_serie, rolling_mean_size):
    """
    Visualiza a estacionaridade dos dados.
    -----
    -----
    - parameters:
        - data_serie_df{Series}: Serie a ser avaliada.
    """
    # Calcula média e desvio padrão móveis.

    rolling_mean = data_serie.rolling(rolling_mean_size).mean()
    rolling_std = data_serie.rolling(rolling_mean_size).std()

    # Plot
    plt.figure(figsize = (15,5))
    plt.plot(data_serie, label = 'Refeições Fornecidas')
    plt.plot(rolling_mean, color = 'yellow', label = "Média Móvel")
    plt.plot(rolling_std, color = 'green', label = "Desvio Padrão Móvel")

    plt.legend(loc = 'best')
    plt.title("Visualizando a Estacionaridade")
    plt.xticks([])
    plt.yticks([])
    plt.show()

    st.pyplot(plt)

st.subheader('Almoço')

# Visualizando a estacionaridade dos Almoços
visualize_stationarity(data_ru.lunch, rolling_mean_size)

st.subheader('Jantar')

visualize_stationarity(data_ru.dinner, rolling_mean_size)

#--------------------------------------------------------------------------------------------

def augmented_dickey_fuller_test(data_serie):
    """
    Teste de Dickey Fuller Aumentado.
    -----
    -----
    - parameters:
        - data_serie_df{Series}: Serie a ser avaliada.
    """
    result = adfuller(data_serie)

    print(f'valor-p: {result[1]}')

    if result[1] < 0.05:
        print('O valor-p é menor que 0.05. Podemos rejeitar a H0. A série é estacionária.')
    else:
        print('O valor-p é maior que 0.05. Não podemos rejeitar a H0. A série não é estacionária.')

st.header('Estacionarização de Dados de Séries Temporais')

st.text('De acordo com os gráficos anteriores, observamos que nossas séries temporais não são estacionárias.')

st.subheader('Diferenciação')

# Aplica a primeira diferenciação para remover as estacionariedades.
first_diff_data_ru = data_ru.copy()

first_diff_data_ru.lunch = first_diff_data_ru.lunch - first_diff_data_ru.lunch.shift(1)
first_diff_data_ru.dinner = first_diff_data_ru.dinner - first_diff_data_ru.dinner.shift(1)

# Remove valores NA gerados no processo
first_diff_data_ru = first_diff_data_ru.dropna()

st.subheader('Almoço')

#Decomposição dos Almoços.
lunch = seasonal_decompose(first_diff_data_ru.lunch, model = 'additive', period = 365)

# Plot
fig = plt.figure()
fig = lunch.plot()
fig.set_size_inches(18, 12)
plt.xticks([])
plt.yticks([])

st.pyplot(plt)

st.text('Visualizando a estacionaridade dos Almoços')
visualize_stationarity(first_diff_data_ru.lunch, rolling_mean_size)

#Teste de Dickey-Fuller Aumentado na série temporal de almoços.
augmented_dickey_fuller_test(first_diff_data_ru.lunch)

st.subheader('Jantar')

#Decomposição dos jantares.
dinner = seasonal_decompose(first_diff_data_ru.dinner, model = 'additive', period = 365)

# Plot
fig = plt.figure()
fig = dinner.plot()
fig.set_size_inches(18, 12)
plt.xticks([])
plt.yticks([])

st.pyplot(plt)

# Visualizando a estacionaridade dos Jantares
visualize_stationarity(first_diff_data_ru.dinner, rolling_mean_size)

#Teste de Dickey-Fuller Aumentado na série temporal de jantares.
augmented_dickey_fuller_test(first_diff_data_ru.dinner)

#######################################################################################################################