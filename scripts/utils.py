import os
import pandas as pd
import sys
import streamlit as st
import pandas as pd
from faker import Faker
import random
sys.path.append('../data')

def look_for_csv(folder_path):
    csv_file = None
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            csv_file = os.path.join(folder_path, file)
            break

    if csv_file:
        df = pd.read_csv(csv_file, index_col=0)
        return df
    else:
        print('No .csv file found in the folder.')
        return None

def read_csv(csv_path):
    try:
        df = pd.read_csv(csv_path, index_col=0)
        return df
    except FileNotFoundError:
        print("CSV file not found.")
        return None
    except pd.errors.EmptyDataError:
        print("CSV file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error parsing CSV file.")
        return None
    


def update_or_create_dataset(dni, name, apellido, age, sueldo_bruto):
    # Definir el nombre del archivo CSV y la ubicación de la carpeta "data"
    csv_file = 'data/client_data.csv'
    data_folder = 'data'

    # Verificar si el archivo CSV ya existe
    if os.path.exists(csv_file):
        # Si el archivo existe, leer los datos existentes y crear un DataFrame
        df = pd.read_csv(csv_file)
    else:
        # Si el archivo no existe, crear un DataFrame vacío
        df = pd.DataFrame(columns=['DNI', 'Nombre', 'Apellido', 'Edad', 'Sueldo Bruto'])

    # Agregar una nueva fila con los datos del cliente actual al DataFrame
    new_row = {
        'DNI': dni,
        'Nombre': name,
        'Apellido': apellido,
        'Edad': age,
        'Sueldo Bruto': sueldo_bruto
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    df.to_csv(csv_file, index=False)

    return df



def generate_fake_data(num_samples):
    fake = Faker()

    data = []
    for _ in range(num_samples):
        dni = str(random.randint(20000000, 40000000))
        name = fake.first_name()
        apellido = fake.last_name()
        age = random.randint(18, 65)
        sueldo_bruto = random.randint(100000, 600000)

        data.append([dni, name, apellido, age, sueldo_bruto])

    columns = ['DNI', 'Nombre', 'Apellido', 'Edad', 'Sueldo Bruto']
    df = pd.DataFrame(data, columns=columns)
    return df



def calculate_payment(amount, num_payments, amortization_system):
    interest_rate = 0.15  # 15% monthly interest rate

    if amortization_system == "French":
        interest_factor = (1 + interest_rate) ** num_payments
        monthly_payment = amount * (interest_rate * interest_factor) / (interest_factor - 1)
    elif amortization_system == "German":
        monthly_payment = amount / num_payments + (amount * interest_rate)
    elif amortization_system == "American":
        monthly_payment = amount * interest_rate
    else:
        st.error("Invalid amortization system. Choose 'French', 'German', or 'American'")
        return None

    payments = []
    remaining_amount = amount
    for num in range(1, num_payments + 1):
        interest = remaining_amount * interest_rate
        if amortization_system == "French":
            amortization = monthly_payment - interest
        else:
            amortization = monthly_payment

        payments.append([num, interest, amortization, remaining_amount])
        remaining_amount -= amortization

    return payments