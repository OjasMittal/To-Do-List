import streamlit as st
import pandas as pd
from pyrebase import initialize_app
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PIL import Image
from streamlit_lottie import st_lottie
import requests

cred = credentials.Certificate("firestore_key.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://todolist-70940-default-rtdb.asia-southeast1.firebasedatabase.app/'
# })
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

firebaseConfig = {
    'apiKey': "AIzaSyD0eI_3tHsmxasKd2KsQnC9Pz1uuIAN8eM",
    'authDomain': "todolist-70940.firebaseapp.com",
    'projectId': "todolist-70940",
    'databaseURL': "https://todolist-70940-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "todolist-70940.appspot.com",
    'messagingSenderId': "695064566243",
    'appId': "1:695064566243:web:70267b2a5436495daba8d6",
    'measurementId': "G-0QP1KRX2V2"
};

firebase = initialize_app(firebaseConfig)
auth = firebase.auth()
#db = firebase.database()
storage = firebase.storage()
ref = db.reference()
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

img = Image.open('icon.png')
st.set_page_config(page_title="To-Do-List", page_icon=img)

hide_menu_style="""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
"""
st.markdown(hide_menu_style,unsafe_allow_html=True)
st.title("***To- Do List Manager***")
col1,col2=st.columns([6,2])
cola,colb=col2.columns([3,1])
with col1:
    st.subheader("Set and Complete your tasks by making a To-Do list !")
with cola:
    lottie_animation_2 = "https://assets10.lottiefiles.com/packages/lf20_z4cshyhf.json"
    lottie_anime_json2 = load_lottie_url(lottie_animation_2)
    st_lottie(lottie_anime_json2, key="hello")
st.sidebar.markdown(
        "<h1 style='text-align: center; '>WELCOME !</h1>",
        unsafe_allow_html=True)
# st.sidebar.image("drop.png")
st.sidebar.image("to_do_icon.jpg")

choice = st.sidebar.selectbox('Login/SignUp', ['Login', 'Sign up'])
email = st.sidebar.text_input("Enter your email address")
password = st.sidebar.text_input("Enter your password", type="password")
# with st.sidebar:
#     lottie_animation_2 = "https://assets4.lottiefiles.com/packages/lf20_1pxqjqps.json"
#     lottie_anime_json2 = load_lottie_url(lottie_animation_2)
#     st_lottie(lottie_anime_json2, key = "hello")
if choice == "Sign up":
    handle = st.sidebar.text_input("Please enter your nickname", value="Cool Panda")
    submit = st.sidebar.button('Create my Account')
    if submit:
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Your account is created successfully!")
            st.balloons()
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            db.child(uid).child("Handle").set(handle)
            db.child(uid).child("Id").set(uid)
            st.title("Welcome " + handle + " !")
        except:
            st.info("This account already exists !")



st.info("Login through login option in the left drop down menu")

if choice == "Login":
    login = st.sidebar.checkbox('Login')
    if login:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            user_ref = db.reference(user['localId'])
        except:
            st.warning("Enter a valid email/password !")
            st.stop()
        if user_ref.get() is None:
            df = pd.DataFrame(
                [
                    {"Task": "None", "Due date": "", "Completed": False},
                    {"Task": "None", "Due date": "", "Completed": False},
                    {"Task": "None", "Due date": "", "Completed": False}
                ]
            )
            user_ref.set(df.to_dict())
        else:
            data_dict = user_ref.get()
            data = pd.DataFrame.from_dict(data_dict)

        edited_df = st.experimental_data_editor(data, use_container_width=True, num_rows="dynamic")
        csv = convert_df(edited_df)
        # if 'key' not in st.session_state:
        #     st.session_state['key'] = edited_df
        # st.session_state.key = edited_df

        #put 2 columns here
        col1,col2,col3,col4=st.columns(4)
        with col3:
            st.download_button(
                label="Download List",
                data=csv,
                file_name='large_df.csv',
                mime='text/csv'
            )
        with col4:
            if st.button("Save Changes"):
                data_dict = edited_df.to_dict()
                user_ref.set(data_dict)
                st.write("Changes Saved!")



st.write("")
st.caption("Made with ❤️ by Ojas Mittal")
