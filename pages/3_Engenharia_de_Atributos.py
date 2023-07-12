import streamlit as st
import pandas as pd
import holidays
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go

from statsmodels.graphics.tsaplots import plot_pacf

data_ru = pd.DataFrame()
data_ru['date'] = pd.period_range(start='2016-01-04', end='2020-03-31', freq='D').to_timestamp()
prof_data_ru = pd.read_csv('data_ru.csv', sep = ";")
prof_data_ru["date"] = pd.to_datetime(prof_data_ru["date"])
data_ru = data_ru.merge(prof_data_ru, on='date', how='left')

data_ru['lunch'] = data_ru['lunch'].fillna(0)
data_ru['dinner'] = data_ru['dinner'].fillna(0)
st.title('Engennharia de Atributos')

def brazil_holidays(in_df):
    """
    Lista feriados brasileiros.
    -----
    -----
    - parameters:
        - in_df{DataFrame}: DataFrame que contenha o atributo 'date'.
    -----
    - return: Lista com os feriados do Brasil.
    """
    df_holidays = in_df.copy()
    df_holidays['date'] = pd.to_datetime(df_holidays.date)

    min_year = df_holidays.date.min().year
    max_year = df_holidays.date.max().year

    years_list = pd.period_range(min_year, max_year, freq = 'Y')

    list_of_holidays = []

    for year in years_list:
        list_of_holidays.append(holidays.BR(years = int(str(year))).keys())

    holiday_list = [item for sublist in list_of_holidays for item in sublist]

    return holiday_list

def create_datetime_attributes(in_df):
    """
    Cria novos atributos de data e hora.
    -----
    -----
    - parameters:
        - in_df{DataFrame}: DataFrame que contenha o atributo 'date'.
    -----
    - return: DataFrame com os atributos criados.
    """
    df_with_datetime_attributes = in_df.copy()
    df_with_datetime_attributes['date'] = pd.to_datetime(df_with_datetime_attributes.date)
    df_with_datetime_attributes['month'] = df_with_datetime_attributes.date.dt.month
    df_with_datetime_attributes['day_of_month'] = df_with_datetime_attributes.date.dt.day
    df_with_datetime_attributes['day_of_year'] = df_with_datetime_attributes.date.dt.dayofyear
    df_with_datetime_attributes['week_of_year'] = df_with_datetime_attributes.date.dt.isocalendar().week
    df_with_datetime_attributes['day_of_week'] = df_with_datetime_attributes.date.dt.weekday + 1
    df_with_datetime_attributes['year'] = df_with_datetime_attributes.date.dt.year
    df_with_datetime_attributes['is_weekend'] = df_with_datetime_attributes.date.dt.weekday // 5
    df_with_datetime_attributes['start_of_month'] = df_with_datetime_attributes.date.dt.is_month_start.astype(int)
    df_with_datetime_attributes['end_of_month'] = df_with_datetime_attributes.date.dt.is_month_end.astype(int)
    df_with_datetime_attributes['is_holiday'] = np.where(df_with_datetime_attributes.date.isin(brazil_holidays(df_with_datetime_attributes)), 1, 0)
    #is_vacations

    return df_with_datetime_attributes

# Criando novos atributos de data.
data_ru_with_datetime_attributes = create_datetime_attributes(data_ru)

# Define a coluna de 'date' como índice do conjunto de dados.
data_ru_with_datetime_attributes = data_ru_with_datetime_attributes.set_index('date')

st.markdown('<div style="text-align: justify;">Foram criados novos atributos temporais derivados das datas.</div>', unsafe_allow_html=True)


st.dataframe(data_ru_with_datetime_attributes, column_config={ 'date':'Data', 'lunch':'Almoço', 'dinner':'Jantar'}, use_container_width=True)

st.subheader('Matriz de Correlação')

sns.heatmap(data_ru_with_datetime_attributes.corr(), annot=True, fmt=".1f", linewidth=.5)
plt.show()
st.pyplot(plt)

################################################################################################################


st.header('Atributos Lag/Shifted')

st.subheader('Função de Autocorrelação (FAC)')

# Calcular a autocorrelação
autocorrelation_lunch = data_ru_with_datetime_attributes['lunch'].autocorr()
autocorrelation_dinner = data_ru_with_datetime_attributes['dinner'].autocorr()


# Plotar o gráfico da função de autocorrelação

fig, ax = plt.subplots()
pd.plotting.autocorrelation_plot(data_ru_with_datetime_attributes['dinner'], ax=ax)
ax.set_title('Função de Autocorrelação dos jantares')
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
st.pyplot(fig)


fig, ax = plt.subplots()
pd.plotting.autocorrelation_plot(data_ru_with_datetime_attributes['lunch'], ax=ax)
ax.set_title('Função de Autocorrelação dos almoços')
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
st.pyplot(fig)


# Função de Autocorrelação Parcial (FACP)
fig, ax = plt.subplots()
plot_pacf(data_ru_with_datetime_attributes['dinner'], ax=ax)
ax.set_title('Função de Autocorrelação Parcial dos jantares')
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
st.pyplot(fig)

# Função de Autocorrelação Parcial (FACP)
fig, ax = plt.subplots()
plot_pacf(data_ru_with_datetime_attributes['lunch'], ax=ax)
ax.set_title('Função de Autocorrelação Parcial dos almoços')
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
st.pyplot(fig)

# Criando colunas com os lags
data_ru_with_datetime_lag_attributes = data_ru_with_datetime_attributes.copy()

lag = 14

 # valores lags
for lag in range(1, lag + 1):
    data_ru_with_datetime_lag_attributes['lag_{}_lunch'.format(lag)] = data_ru_with_datetime_attributes['lunch'].shift(lag)
    data_ru_with_datetime_lag_attributes['lag_{}_dinner'.format(lag)] = data_ru_with_datetime_attributes['dinner'].shift(lag)

######################################################################################################################

# Atributos Rolling Window

# Média móvel de 6 dias
rolling_mean = 7

data_ru_with_datetime_lag_MM_attributes = data_ru_with_datetime_lag_attributes.copy()

# Criando colunas com a Média movel
data_ru_with_datetime_lag_MM_attributes['rolling_mean_lunch'] = (data_ru_with_datetime_lag_MM_attributes['lunch'].shift().rolling(rolling_mean).mean())
data_ru_with_datetime_lag_MM_attributes['rolling_mean_dinner'] = (data_ru_with_datetime_lag_MM_attributes['dinner'].shift().rolling(rolling_mean).mean())

data_ru_with_datetime_lag_MM_attributes = data_ru_with_datetime_lag_MM_attributes.dropna()

st.dataframe(data_ru_with_datetime_lag_MM_attributes.corr(), use_container_width=True)

figure = go.Figure()
figure.add_trace( go.Scatter(name = 'MM_7p_lunch', x = data_ru_with_datetime_lag_MM_attributes.index, y =  data_ru_with_datetime_lag_MM_attributes['rolling_mean_lunch']) )
figure.add_trace( go.Scatter(name = 'MM_7p_dinner', x = data_ru_with_datetime_lag_MM_attributes.index, y =  data_ru_with_datetime_lag_MM_attributes['rolling_mean_dinner']) )
figure.update_layout( title_text = '<b>Média Movel de 7 períodos<b>', template = 'simple_white' )

