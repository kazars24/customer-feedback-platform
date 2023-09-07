import streamlit as st


possible_cities = ["", "Москва", "Санкт-Петербург", "Нижний Новгород"]

st.set_page_config(
    page_title="Customer Feedback Platform",
    page_icon="👥",
    layout="wide"
)



st.title("Customer Feedback Platform by Vibe++")

with st.expander("ℹ️ - About this app", expanded=True):
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
            city_name = st.selectbox('Выберите город: ',possible_cities)
        else:
            manual_address = st.text_input(
                "Введите регион:", 
                help="Введите регион вручную.")
        scale_submit_button2 = st.form_submit_button(label="Подтвердить выбор")
            
            

    with c2:
        st.title('Тут будут реультаты')

