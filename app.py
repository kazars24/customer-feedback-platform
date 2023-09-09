import json
import random
import time
import streamlit as st
import pydeck as pdk
from geopy.geocoders import Nominatim
from src.llm.agent import Agent

# Load the updated JSON data
with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_pyaterochka.json', 'r', encoding='utf-8') as f:
    shop_data = json.load(f)

# Create lists for red and green points on the map
red_address_data = []
green_address_data = []

for url, data in shop_data.items():
    address = data["address"]
    color = 'red' if data.get("is_worse", False) else 'green'
    try:
        location = Nominatim(user_agent="myGeocoder").geocode(address)
    except Exception:
        time.sleep(2)
        location = Nominatim(user_agent="myGeocoder").geocode(address)
    if location:
        lat, lon = location.latitude, location.longitude
        if color == 'red':
            red_address_data.append({"address": address, "color": color, "lat": lat, "lon": lon})
        else:
            green_address_data.append({"address": address, "color": color, "lat": lat, "lon": lon})

# Create a map using PyDeck with separate layers for red and green points
st.title('Карта магазинов')
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=56.1364,  # Adjust the latitude and longitude to focus on your area
        longitude=40.4086,
        zoom=12,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=red_address_data,
            get_position='[lon, lat]',
            get_fill_color='[255, 0, 0]',  # Red color for is_worse=True
            get_radius=200,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=green_address_data,
            get_position='[lon, lat]',
            get_fill_color='[0, 255, 0]',  # Green color for is_worse=False
            get_radius=200,
        ),
    ],
))

# Function to analyze reviews using the LLM agent
def analyze_reviews(agent, reviews):
    request = 'Отзывы о магазине:\n' + ''.join(reviews)
    return agent.interact(request)

def get_random_sample_reviews(source, len_r=30):
    reviews_list = []
    for shop_url, shop_data in source.items():
        reviews = shop_data.get("reviews_list", [])
        for review in reviews:
            reviews_list.append(f"{review['text']};\n")
    return random.sample(reviews_list, len_r)

# Step 1: Analyze random 30 reviews for two JSONs
st.title('Анализ отзывов')

# Load the JSON data
with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_pyaterochka.json', 'r', encoding='utf-8') as f:
    shop_data_vladimir_pyaterochka = json.load(f)
with open('E:\\customer-feedback-platform\\src\\data\\reviews_data_vladimir_magnit.json', 'r', encoding='utf-8') as f:
    shop_data_vladimir_magnit = json.load(f)

# Example reviews from two JSONs, you can modify this to select random reviews
reviews_vladimir_pyaterochka = get_random_sample_reviews(shop_data_vladimir_pyaterochka)
reviews_vladimir_magnit = get_random_sample_reviews(shop_data_vladimir_magnit)

# Define LLM models and prompts
model_path = "D:\\llama.cpp\\models\\7b\\ggml-model-q4_1.bin"
overall_all_filials_sys_prompt = 'Ты — русскоязычный автоматический анализатор отзывов. Ты получаешь на вход несколько отзывов. Проанализируй текст отзывов и выделите ключевые проблемы в этих отзывах. Ответ дай коротким списком. Обобщи.'

# Create LLM agents
review_overall_all_filials_agent = Agent(model_path, overall_all_filials_sys_prompt)

# Analyze reviews using LLM agents
pyaterochka_summary = analyze_reviews(review_overall_all_filials_agent, reviews_vladimir_pyaterochka)
magnit_summary = analyze_reviews(review_overall_all_filials_agent, reviews_vladimir_magnit)

# Display analysis results
st.write("Анализ отзывов для магазина 'Пятерочка':")
st.write(pyaterochka_summary)

st.write("Анализ отзывов для магазина 'Магнит':")
st.write(magnit_summary)

# Step 2: Define which shops from reviews_data_vladimir_pyaterochka.json are worse than overall shops from reviews_data_vladimir_magnit.json
st.title('Сравнение магазинов')

# Define LLM model and prompt for comparing shops
comparer_sys_prompt = 'Ты — русскоязычный автоматический анализатор магазинов. Ты получаешь на вход два описания магазинов в формате "Магазин 1: <описание 1>; Магазин 1: <описание 1>". Ты должен сравнить их и сообщить, какой магазин лучше.'
comparer_agent = Agent(model_path, comparer_sys_prompt)

# Compare shops based on analysis results
compare_request = f'Какой магазин лучше и почему? Сравни:\n 1. Магазин "Пятерочка": {pyaterochka_summary};\n 2. Магазин "Магнит": {magnit_summary}'
shop_comparison_result = comparer_agent.interact(compare_request)

# Display shop comparison result
st.write("Сравнение магазинов:")
st.write(shop_comparison_result)

# Step 3: Define advises for the shop that is worse
st.title('Советы по развитию')

# Define LLM model and prompt for providing advice
adviser_sys_prompt = 'Ты — русскоязычный бизнес-советник. Ты получаешь на вход данные о магазине. Напиши, что можно улучшить и как на основе данных.'
adviser_agent = Agent(model_path, adviser_sys_prompt)

# Provide advice based on which shop is worse
if 'Пятерочка' in shop_comparison_result:
    advise_request = f'Магазин "Пятерочка": {pyaterochka_summary}'
else:
    advise_request = f'Магазин "Магнит": {magnit_summary}'

shop_advice = adviser_agent.interact(advise_request)

# Display shop advice
st.write("Советы по развитию магазина:")
st.write(shop_advice)
