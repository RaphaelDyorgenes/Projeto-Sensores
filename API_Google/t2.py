import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *

# Consulta no banco de dados
query = "SELECT * FROM tb_registro"

# Carergar os dados dp MySQL
df = conexao(query)

# Botão para atualização dos dados
if st.button('Atualizar Dados'):
    df = conexao(query)

# ********** Menu Lateral **********
st.sidebar.header('Selecione os campos')

# Seleção de coluna X

colunaX = st.sidebar.selectbox(
    'Eixo X',
    options=['umidade','temperatura','pressao','altitude','co2','poeira'],
    index=0
)

colunaY = st.sidebar.selectbox(
    'Eixo Y',
    options=['umidade','temperatura','pressao','altitude','co2','poeira'],
    index=1
)

# Verificar os atributos do filtro
def filtros(atributo):
    return atributo in [colunaX,colunaY]

# Filtro do Range -> SLIDER
st.sidebar.header('Selecione o Filtro')

# TEMPERATURA
if filtros('temperatura'):
    temperatura_range = st.sidebar.slider(
        'Temperatura (°C)',
        min_value=float(df['temperatura'].min()),
        # Valor minimo 
        max_value=float(df['temperatura'].max()),
        #valor maximo
        value=(float(df['temperatura'].min()),float(df['temperatura'].max())),
        step= 0.1
    )

# UMIDADE
if filtros('umidade'):
    umidade_range = st.sidebar.slider(
        'umidade',
        min_value=float(df['umidade'].min()),
        # Valor minimo 
        max_value=float(df['umidade'].max()),
        #valor maximo
        value=(float(df['umidade'].min()),float(df['umidade'].max())),
        step= 0.1
    )

# PRESSAO
if filtros('pressao'):
    pressao_range = st.sidebar.slider(
        'pressao',
        min_value=float(df['pressao'].min()),
        # Valor minimo 
        max_value=float(df['pressao'].max()),
        #valor maximo
        value=(float(df['pressao'].min()),float(df['pressao'].max())),
        step= 0.1
    )

# altitude
if filtros('altitude'):
    altitude_range = st.sidebar.slider(
        'altitude',
        min_value=float(df['altitude'].min()),
        # Valor minimo 
        max_value=float(df['altitude'].max()),
        #valor maximo
        value=(float(df['altitude'].min()),float(df['altitude'].max())),
        step= 0.1
    )

# co2
if filtros('co2'):
    co2_range = st.sidebar.slider(
        'co2',
        min_value=float(df['co2'].min()),
        # Valor minimo 
        max_value=float(df['co2'].max()),
        #valor maximo
        value=(float(df['co2'].min()),float(df['co2'].max())),
        step= 0.1
    )
# POEIRA
if filtros('poeira'):
    poeira_range = st.sidebar.slider(
        'poeira',
        min_value=float(df['poeira'].min()),
        # Valor minimo 
        max_value=float(df['poeira'].max()),
        #valor maximo
        value=(float(df['poeira'].min()),float(df['poeira'].max())),
        step= 0.1
    )
df_selecionado = df.copy()
if filtros("temperatura"):
    df_selecionado = df_selecionado[
        (df_selecionado['temperatura'] >= temperatura_range[0])&
        (df_selecionado['temperatura'] >= temperatura_range[1])
    ]
if filtros("pressao"):
    df_selecionado = df_selecionado[
        (df_selecionado['pressao'] >= temperatura_range[0])&
        (df_selecionado['pressao'] >= temperatura_range[1])
    ]
if filtros("altitude"):
    df_selecionado = df_selecionado[
        (df_selecionado['altitude'] >= temperatura_range[0])&
        (df_selecionado['altitude'] >= temperatura_range[1])
    ]
if filtros("umidade"):
    df_selecionado = df_selecionado[
        (df_selecionado['umidade'] >= temperatura_range[0])&
        (df_selecionado['umidade'] >= temperatura_range[1])
    ]
if filtros("co2"):
    df_selecionado = df_selecionado[
        (df_selecionado['umidade'] >= temperatura_range[0])&
        (df_selecionado['umidade'] >= temperatura_range[1])
    ]

if filtros("poeira"):
    df_selecionado = df_selecionado[
        (df_selecionado['poeira'] >= temperatura_range[0])&
        (df_selecionado['poeira'] >= temperatura_range[1])
    ]

def home():
    with st.expander('tabela'):
        mostrarDados = st.multiselect(
            'Filtro: ',
            df_selecionado.columns,
            default=[],

        )

        if mostrarDados:
            st.write(df_selecionado[mostrarDados])

    if not df_selecionado.empty:
        media_umidade = df_selecionado['umidade'].mean()
        media_temperatura = df_selecionado['temperatura'].mean()
        media_co2 = df_selecionado['co2'].mean()

        media1, media2, media3 = st.columns(3, gap="Large")

        with media1:
            st.info('Média de registros de umidade', icon='🐲')
            st.metric(label= 'Média', value=f"{media_umidade:.2f}")

        with media2:
            st.info('Média de registros de temperatura', icon='🐲')
            st.metric(label= 'Média', value=f"{media_temperatura:.2f}")

        with media3:
            st.info('Média de registros de co2', icon='🐲')
            st.metric(label= 'Média', value=f"{media_co2 :.2f}")
def graficos():
    st.title('Dashboard Monitoramento')

    aba1 = st.tabs("Gráficos de LInha")

    with aba1:
        if df_selecionado.empty:
            st.write('Nenhum dado disponivelpara gerar o gráfico')
            return

        if colunaX == colunaY:
            st.warning('Selecione uma opção diferente para os eixos X e Y')
            return
       
        try:
            grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().redet.index(name='Contagem')
            fig_valores = px.bar(
                grupo_dados1,
                x = colunaX,
                y = 'Contagem',
                orientation='h',
                title = f"Contagem de Registros po {colunaX.captalize()}"
            )
        except Exception as e:
            st.error(f'Erro ao crir gráfico de linha: {e}')
            st.plotly_chart(fig_valores, use_container_width=True)
home()