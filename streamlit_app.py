# Import python packages
import pandas as pd
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🍹Customize Your Smoothie🍹!")
st.write(
    """ Choose the fruits you want in your custom Smoothie !
    """
)

# Création d'un checkbox
#option = st.selectbox(
#    "What's your favorite fruit ?",
#    ('Banana', 'Strawberries', 'Peaches'),
#)
#st.write("Your favorite fruit is Strawberries", option)

name_on_order = st.text_input("Name on Smoothie :")
st.write("The name on your Smoothie will be : ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
# Affichage de la table fruit_options
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

# Convert the Snowpark Dataframe 
# to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

# Add multiselect 
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients :'
    ,my_dataframe    
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
       

        
    
    #st.write(ingredients_string)
    # permet d'écrire ce qu'il est dans la mémoire de python.
    # dans la table de la base de donnée Smoothie.
    
    # Construire la requête SQL en spécifiant uniquement les colonnes à remplir.
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS)
    VALUES ('{name_on_order}', '{ingredients_string}')
    """
    # Vérification de la requête
    st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered', icon = "✅")

# Parti API requests
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
         
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
