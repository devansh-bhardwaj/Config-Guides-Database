from parsing import parse_page
from links import *
import streamlit as st
import json
from json2html import json2html
import pymongo

client = pymongo.MongoClient(st.secrets.uri)
database = client.big_data_project
collection = database["config_guide"]

def update_database(option):

    os_name_input = st.text_input('Enter OS', key="os_input").strip()
    url_input = st.text_input('Enter Web Page URL', key="url_input")
    
    update_button = st.button("Update Database")

    if update_button:
        if option == 'Config Guide Link':
            links = get_landing_links(url_input)
        else:
            links = [url_input]

        feature_configs = parse_page(links)

        try:
            document = collection.find_one({"operating_system": os_name_input})
            old_dict = document["config"]   
        except:
            old_dict = dict()

        old_dict.update(feature_configs)   

        try:
            collection.delete_one({"operating_system": os_name_input})    
        except:
            pass

        collection.insert_one({"operating_system": os_name_input, "config": old_dict})

        st.success("Updated Database")
        rerun_button = st.button("Re-Run", on_click=clear_inputs)

def view_database():
    os_name_input = st.text_input('Enter OS', key="os_input").strip()
    view_full_button = st.button("View Full Database")
    

    if view_full_button:
        document = collection.find_one({"operating_system": os_name_input})
        if document is not None:
            feature_configs = document["config"]
            json_object = json.dumps(feature_configs, indent = 4)
            html_code = json2html.convert(json = json_object)
            st.markdown(html_code, unsafe_allow_html=True)
            rerun_button = st.button("Re-Run", on_click=clear_inputs)

def clear_inputs():
    st.session_state["os_input"] = ""
    st.session_state["url_input"] = ""
    st.session_state["os_name"] = ""
    st.session_state["user_input"] = ""
    st.session_state["feature_name"] = ""

st.title('Cisco Config Guides Databases')
option = st.sidebar.radio("Update Database or View Database?", ("Update", "View"))

if option == "Update":
    next_option = st.radio("How would you like to add features?", ("Direct Web Page", "Config Guide Link"))
    update_database(next_option)

elif option == 'View':
    view_database()
