# Import python packages
import streamlit as st
import requests

cnx=st.connection("snowflake")
session=cnx.session()
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(""" 
Choose the fruits you want in your custom Smoothie"""
)


name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

from snowflake.snowpark.functions import col

my_dataframe = session.table("smoothies.public.fruit_options")
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()

# pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
#st.stop()

ingredients_list=st.multiselect('choose upto 5 ingrediants',my_dataframe,max_selections=5)

if ingredients_list:
    
    ingredients_string=''
    for i in ingredients_list:
        ingredients_string+=i+' '

        #search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', i,' is ', search_on, '.')
        st.subheader(i+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    #st.write(ingrediants_string)

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order, order_uid)
                         VALUES ('{ingredients_string}', '{name_on_order}', smoothies.public.order_seq.NEXTVAL)"""

    #st.write(my_insert_stmt)
    #st.stop
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order,icon="✅")

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
#fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
