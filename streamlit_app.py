import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Titre de l'application
st.title("🥤Customize Your Smoothie🥤")

# Description de l'application
st.write("Choose the fruits you want in your custom Smoothie!")


cnx = st.connexion("snowflake")
session = cnx.session()

# Récupérer les options de fruits depuis la base de données
fruit_options_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Convertir les noms de fruits en une liste
fruit_names = fruit_options_df['FRUIT_NAME'].tolist()

max_selection = 5

# Formulaire pour entrer les données
with st.form("order_form"):
    # Multiselect pour choisir les ingrédients
    selected_fruits = st.multiselect(
        'Choose up to 5 ingredients', 
        options=fruit_names,
    )
    
    # Input pour le nom sur la commande
    name_on_order = st.text_input("Name on Order:")
    
    # Checkbox pour l'état de la commande
    order_filled = st.checkbox('Order Filled', value=False)
    
    # Bouton de soumission du formulaire
    submit_button = st.form_submit_button(label="Add Order")

    if submit_button:
        if selected_fruits and name_on_order:
            # Convertir les fruits sélectionnés en une chaîne de noms de fruits
            ingredients = ', '.join(map(str, selected_fruits))
            
            # Construire la requête SQL pour insérer les données dans la table orders
            insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
            VALUES ('{ingredients}', '{name_on_order}', {order_filled})
            """
            
            # Exécuter la requête SQL
            session.sql(insert_stmt).collect()
            
            # Afficher un message de succès
            st.success("Order added to the database!")
        else:
            # Afficher un message d'erreur si les conditions ne sont pas remplies
            st.error("Please select at least one ingredient and enter the name on order.")

# Récupérer les commandes existantes de la table orders
orders_df = session.table("smoothies.public.orders").to_pandas()

# Afficher les commandes existantes
st.write("Existing Orders:")

# Afficher le dataframe des commandes existantes
st.dataframe(orders_df)
