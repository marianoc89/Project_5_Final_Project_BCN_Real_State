import streamlit as st
from st_pages import Page, show_pages, add_page_title
import codecs
import streamlit.components.v1 as components

########## Tab-Title ##########

st.set_page_config(
    page_title="BCN - Barcelona Real Estate",
    page_icon="🏘️",
    layout="wide"
)
########## Pages and sidebar ##########

st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/6rMFTd3/Logo-only.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Barcelona Real Estate";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("main.py", "ML App", "🏠"),
        Page("pages/dashboard.py", "Analytics", "📊"),
        Page("pages/about.py", "About", "💼"),
    ]
)

########## Boddy Logo ##########

st.markdown(
    '<center><img src="https://i.ibb.co/tMjd8Zq/Logo-2-removebg-preview-ps.png" style="width:549px;height:174px;"></center>',
    unsafe_allow_html=True
)
st.divider()

st.write("\n")

########## Boddy 1 ##########

# Title and Description
st.header("Data Analytics Dashboard")
st.divider()

########## Boddy 2 ##########

# Title and Description
st.markdown("In this section you can find the great Real State Dashboard that our Analytics Team has made with all the information about the current market situation in Barcelona as well as some predictions about it.")
st.subheader("About Our Advanced Machine Learning Models:")
st.markdown("**Time Series Forecasting:** We utilize an **_ARIMA regression model_** with an impressive **accuracy of 0.828**. This model is specifically designed to predict the Euribor Rate for the next 12 months, providing valuable insights into interest rate trends.")
st.markdown("**Precise Price Predictions**: Our **_Linear Regression model_** is employed to predict m2 prices on a neighborhood basis. With an exceptional **R2 score of 0.9339** and an **RMSE error of only €361.363 per m2**, this model ensures accurate predictions for the next three years (current year plus two).")
st.markdown("**Predictive Market Analysis**: Our **_Gradient Boosting Regressor model_** is used to forecast price/m2 based on the current market price and relevant features in a given neighborhood. With an **R2 score of 0.6780** and an **RMSE error of €961.460 per m2**, this model provides valuable insights into potential price fluctuations.")
st.markdown("These models allow us to provide you with precise and reliable predictions, helping you make informed decisions in the real estate market.")
########## Boddy 2 ##########
st.subheader('Enjoy the Dasboard embeded below 👇🏻')
st.markdown("_For full experience we recommend opening it in full screen mode._")
st.divider()

########## Dashboard ##########

f = codecs.open("data/tableau.html")
tableau = f.read()
components.html(tableau, width=1450 ,height=850, scrolling=True)

st.divider()
st.markdown("_Please note that this data was scraped on 23/6/2023_")