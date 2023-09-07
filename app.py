import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
import geopandas as gpd
import pandas as pd
import numpy as np

possible_cities = ["", "Москва", "Санкт-Петербург", "Нижний Новгород"]

st.set_page_config(
    page_title="Customer Feedback Platform",
    page_icon="👥",
    layout="wide"
)

st.title("Customer Feedback Platform by Vibe++")

with st.expander("ℹ️ - О проекте", expanded=True):
    st.write(
        """     
Тут будет описание сервиса
	    """
    )

    st.markdown("")

st.markdown("")
st.markdown("## 📌 Ниже рабочая область")

c1, c2 = st.columns([2, 5])
with c1:
    with st.form(key="scale_form"):
        scale = st.radio(
            "Выберите масштаб",
            ["Магазин", "Район", "Город", "Регион"],
            help="Тут нужно выбрать один из предложенных вариантов, в рамках которого требуется провести анализ отзывов.",
        )
        scale_submit_button1 = st.form_submit_button(label="Подтвердить выбор")

    with st.form(key="name_form"):
        if scale == "Магазин":
            name = st.text_input(
                "Введите адрес магазина:",
                help="Введите адрес магазина вручную.")
        elif scale == "Район":
            name = st.text_input(
                "Введите район:",
                help="Введите район вручную.")
        elif scale == "Город":
            city_name = st.selectbox('Выберите город: ', possible_cities)
        else:
            manual_address = st.text_input(
                "Введите регион:",
                help="Введите регион вручную.")
        scale_submit_button2 = st.form_submit_button(label="Подтвердить выбор")

    with c2:
        st.title('Тут будут реультаты')

        # список адресов
        addresses = ['Ваш адрес 1', 'Ваш адрес 2', 'Ваш адрес 3']
        ratings = np.array([1.2, 3.1, 4.8])

        geolocator = Nominatim(user_agent="myGeocoder")

        lats = []
        longs = []
        for address in addresses:
            location = geolocator.geocode(address)
            lats.append(location.latitude)
            longs.append(location.longitude)

        # создаем фрейм данных с адресами и рейтингами
        df = pd.DataFrame({
            'Адрес': addresses,
            'Широта': lats,
            'Долгота': longs,
            'Рейтинг': ratings
        })

        # определяем цвета для рейтингов
        color_scale = np.array(['red', 'orange', 'yellow', 'green', 'blue'])
        df['color'] = pd.cut(df['Рейтинг'], bins=[0., 1., 2., 3., 4., 5.], labels=color_scale)

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=np.mean(df['Широта']),
                longitude=np.mean(df['Долгота']),
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[Долгота, Широта]',
                    get_color='color',
                    get_radius=200,
                ),
            ],
        ))
