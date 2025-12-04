import streamlit as st 
from pages import Executive_Dashboard
import Project2.pages.Executive_Dashboard as Executive_Dashboard  
import Project2.pages.Inventory_Analytics as Inventory_Analytics
import Project2.pages.Revenue_Analytics as Revenue_Analytics
import plotly.express as px


st.sidebar.title("Navigation")
option=st.sidebar.selectbox("Select the page.. ",["Executive_Dashboard",  "Inventory_Analytics", "Revenue_Analytics"])


st.title("🛒 Amazon India: A Decade of Sales Analytics 📈🇮🇳")
    
if option == "Executive_Dashboard":
     Executive_Dashboard.app()

elif option=="Inventory_Analytic":
     Inventory_Analytics.app()
  
elif option=='Revenue_Analytics':
     
     Revenue_Analytics.app()
  


    
