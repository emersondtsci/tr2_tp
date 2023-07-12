import streamlit as st
from PIL import Image

imag = Image.open('pages/train_test_split.png')

st.title('Divisão em Treino e Teste')
st.image(imag,  width=1000)

st.text('Train "dinner" e "lunch": 2016-01-19 00:00:00 --- 2019-05-04 00:00:00 (n=1202)')
st.text('Test "dinner" e "lunch": 2019-05-05 00:00:00 --- 2020-02-29 00:00:00 (n=301)')

imag = Image.open('pages/lr_regression_lunch.jpg')

st.title('Linear Regression: lunch')
st.image(imag,  width=1000)



imag = Image.open('pages/lr_regression_dinner.jpg')

st.title('Linear Regression: dinner')
st.image(imag,  width=1000)








imag = Image.open('pages/lunch.png')

st.title('Resultado dos modelos para os almoços')
st.image(imag,  width=800)

imag = Image.open('pages/dinner.png')

st.title('Resultado dos modelos para os jantares')
st.image(imag,  width=800)
