import streamlit as st

st.set_page_config(
    page_title="Customer Feedback Platform",
    page_icon="👥",
)

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    # st.image("logo.png", width=400)
    st.title("Customer Feedback Platform by Vibe++")
    st.header("")

with st.expander("ℹ️ - About this app", expanded=True):
    st.write(
        """     
Тут будет описание сервиса
	    """
    )

    st.markdown("")

st.markdown("")
st.markdown("## 📌 Ниже рабочая область")

with st.form(key="my_form"):
    c1, c2 = st.columns([2, 5])
    with c1:
        ModelType = st.radio(
            "Выберете масштаб",
            ["Магазин", "Район", "Город", "Регион"],
            help="Тут нужно выбрать один из предложенных вариантов, в рамках которого требуется провести анализ отзывов.",
        )
        submit_button1 = st.form_submit_button(label="Подтвердить выбор")
        if submit_button1:
            if ModelType == "Магазин":
                shop_address = st.text_input("Введите адрес магазина:", help="Введите адрес магазина вручную.")

            elif ModelType == "Район":
                district = st.text_input("Введите город и название нужного района:",
                                         help="Введите город и район вручную.")

            elif ModelType == "Город":
                city = st.text_input("Введите город:", help="Введите город вручную.")

            else:
                region = st.text_input("Введите регион:", help="Введите регион вручную.")

    submit_button2 = st.form_submit_button(label="Подтвердить выбор")

    with c2:
        st.title('Тут будут реультаты')

