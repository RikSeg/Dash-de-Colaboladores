import streamlit as st
import pandas as pd
import calendar
from datetime import datetime



# Função para calcular a diferença de tempo em meses e dias
def time_diff_in_months_days(start_date, end_date):
    delta = end_date - start_date
    years = ((end_date - start_date).total_seconds()) / (365.25 * 24 * 3600)
    months = int(years * 12)
    days = delta.days - (months * 30)
    return months, days

# Função para processar os dados
def process_data(df):
    today = datetime.today()
    df['ADMISSÃO'] = pd.to_datetime(df['ADMISSÃO'])
    df['TEMPO DE CASA'] = df['ADMISSÃO'].apply(lambda x: time_diff_in_months_days(x, today))
    df['Tempo Restante para 1 Ano'] = df['TEMPO DE CASA'].apply(lambda x: 12 - x[0])
    return df




# Upload do arquivo
st.title("Lista de Aniversariantes e Colaboradores Próximos de 1 Ano")
uploaded_file = st.file_uploader("Escolha um arquivo CSV ou xlsx", type=["csv", "xlsx"])

today = datetime.today()
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
            data = pd.read_excel(uploaded_file)

    st.write("Visualização dos Dados:")
    st.dataframe(data)

    df = process_data(data)
    st.write("Colaboradores Próximos de 1 Ano de Empresa:")
    st.write(df[df['Tempo Restante para 1 Ano'] <= 1])

    st.write("Lista de Aniversariantes:")
    df['NASCIMENTO'] = pd.to_datetime(df['NASCIMENTO']).dt.strftime('%d/%m')
    aniversariantes = df[df['NASCIMENTO'] >= today.strftime('%d/%m')]
    st.write(aniversariantes)

