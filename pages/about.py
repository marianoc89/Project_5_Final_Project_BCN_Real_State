import streamlit as st
from st_pages import Page, show_pages, add_page_title
from streamlit_card import card


########## Tab-Title ##########

st.set_page_config(
    page_title="BCN - Barcelona Real Estate",
    page_icon="🏘️",
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
st.write("\n")

########## Boddy ##########

st.header("Who We Are:")
st.markdown('At BCN, we are a team of expert **Data Science professionals** dedicated to optimizing investments in the real estate industry. We specialize in providing agile, understandable, and actionable results to help our clients make informed decisions.')
st.write("\n")
st.header("What We Do:")
st.markdown('Our primary objective is to _assist investors in finding the best opportunities in the Barcelona real estate market_. Through comprehensive analysis, market research, and leveraging the power of big data and data science, we provide valuable insights into locations, investment opportunities, and market trends.')
st.write("\n")
st.header("How We Do It:")
st.markdown('Using cutting-edge technologies such as **Big Data and Machine Learning**, we study asset positioning to identify the most promising investment options. _Our predictive models analyze a wide range of factors, including turnover, rent/price ranges, economic indicators, and demographic variables, to help boost sales and maximize investments_. With data science as our foundation, we offer in-depth analyses of present and future investments, predictive market models, and identify potential investment areas for the coming years.')
st.write("\n")
st.header("Why Data is Crucial:")
st.markdown("In the real estate industry, data plays a pivotal role in empowering professionals to make informed, data-driven decisions. Through real estate data analytics, we provide valuable insights that enable our clients to assess property values, evaluate opportunities, mitigate risks, and plan for development. Whether you're a property owner, manager, or investor, having quick and easy access to comprehensive and relevant data is essential in today's market. **Our tools and expertise ensure that you have the information you need to thrive in the ever-changing real estate landscape.**")
st.write("\n")

########## Bottom ##########

st.divider()
st.markdown(
    '<center><img src="https://assets-global.website-files.com/62d64ff33158a9a2aba96531/63e22d9d29cb7279ce51bdae_Real%20Estate%20Data%20Analytics%20Thumbnail%20(1).svg" ></center>',
    unsafe_allow_html=True
)

########## Contact Section ##########
st.divider()
st.header("Contact Us:")
st.markdown("Mariano Ciarrocca, the founder of BCN Real Estate, is a seasoned expert in the field of data science and analytics for the real estate industry in Barcelona. With a deep understanding of data-driven decision-making and extensive knowledge of the local market, Mariano combines his expertise to empower investors with actionable insights to optimize their real estate investments.")
st.markdown("Connect directly with him on LinkedIn to learn more about his experience and stay updated on the latest trends and innovations in data science and real estate analytics. This provides an opportunity to engage with like-minded professionals and explore how BCN Data Analytics can benefit your real estate ventures in Barcelona.")

card(
    title="LinkedIn",
    text="See my profile",
    image="https://i.ibb.co/rxNbkc1/DSCF4986-HDR-Photoshop.jpg",
    url = "https://www.linkedin.com/in/marianociarrocca/"
)

st.header("Thank you! 👋🏻")
