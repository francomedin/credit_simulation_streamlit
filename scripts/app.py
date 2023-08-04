# Utils
import yaml
from yaml.loader import SafeLoader
import sys
import os
sys.path.append('../data/')
sys.path.append("../scripts/")
sys.path.append("../config/")
import PyPDF2
# Data
import pandas as pd
# Own
from utils import update_or_create_dataset, look_for_csv, calculate_payment
from plot import plot_hist
import plotly.express as px
# Streamlit
import streamlit as st
import streamlit_authenticator as stauth




# Look for CSV file and load the dataset
def main():
    # Login
    try:
        with open('config/config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
    except:
        st.title("Error reading .csv file")
    
   
    
    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
    )

    name, authentication_status, username = authenticator.login('Login', 'main')


    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.write(f'Welcome *{st.session_state["name"]}*')
        page = st.sidebar.selectbox("Select a page", ("Add new Client","Loan Simulation","Data Analysis","Data Description"))

        

        # Pages
        if page == "Add new Client":
            add_client()
        elif page == "Data Analysis":
            df = look_for_csv("data")
            data_analysis(df)
        elif page == "Data Description":
            df = look_for_csv("data")
            data_description(df)
        elif page == "Loan Simulation":
            loan_simulation()
        
       

    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        #st.divider()

   
   


def data_description(df):
    st.subheader("DataFrame Summary Statistics")
    st.write(df.describe())

def add_client():

    st.title("Client Information Form")

    # Get client information
    dni = st.text_input("DNI")
    name = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    age = st.number_input("Edad", min_value=0, max_value=100)
    sueldo_bruto = st.number_input("Sueldo Bruto")
    
    if st.button("Guardar datos"):
        df = update_or_create_dataset(dni, name, apellido, age, sueldo_bruto)
        st.success("Datos guardados exitosamente.")


    # Create a DataFrame if the file exists
    csv_file = 'data/client_data.csv'
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        st.subheader("Client Information DataFrame")
        st.dataframe(df)

def data_analysis(df):
    # Plot Age distribution
    fig_age = px.histogram(df, x='Edad', nbins=20, title='Age Distribution')
    st.plotly_chart(fig_age)

    # Plot Sueldo Bruto column
    fig_sueldo = px.histogram(df, x='Sueldo Bruto', nbins=20, title='Sueldo Bruto Distribution')
    st.plotly_chart(fig_sueldo)

def loan_simulation():
    st.title("Credit Simulator")

    # Get client inputs
    amount = st.number_input("Amount of Money", value=10000, step=1000)
    num_payments = st.number_input("Number of Monthly Payments", value=12, step=1)
    amortization_system = st.selectbox("Amortization System", ["French"]) # , "German", "American"

    if st.button("Simulate"):
        payments = calculate_payment(amount, num_payments, amortization_system)
        if payments:
            total_per_month = sum([row[1] + row[2] for row in payments]) / num_payments
            data = {
                "Remaining Amount": [row[3] for row in payments],
                "Payment Number": [row[0] for row in payments],
                "Amortization": [row[2] for row in payments],
                "Interest": [row[1] for row in payments],
                "Total Amount per Month": [total_per_month] * num_payments,

            }
            st.subheader("Monthly Payments")
            st.table(data)




if __name__ == "__main__":
    main()