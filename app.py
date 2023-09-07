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
        if ModelType == "Магазин":

            #@st.cache(allow_output_mutation=True)
            pass

        else:
            #@st.cache(allow_output_mutation=True)
            pass
    
    submit_button = st.form_submit_button(label="✨ Get me the data!")

    with c2:
        st.title('Тут будут реультаты')
        
