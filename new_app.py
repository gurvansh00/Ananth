import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time
from openai import OpenAI
client = OpenAI()

def identify_material_with_cnn(image):
    return "Plastic"

def identify_object_with_cnn(image):
    return "Bottle"

def generate_prompt(material, obj, action):
    prompt = f"You selected {action} for waste item made of {material} ({obj}). Here are some tips..."
    return prompt

st.set_page_config(page_title="AI for Earth Waste Management")
object = []
type = []
#loading the models
@st.cache_resource
def models():
	mod1 = YOLO('yolov8x-cls.pt')
	mod2 = YOLO('best.pt')
	return mod1,mod2

# Set up the OpenAI API client
#openai.api_key = "sk-proj-ZkBB7k7Yse02mvT17lhbT3BlbkFJ7xSCnwtS80jaaFJp2XR4"

def search(pr):
	completion =client.chat.completions.create(model="gpt-3.5-turbo",messages=[{"role":"assistant","content":pr}])
	response = completion.choices[0].message.content
	return response
tab1,tab2 = st.tabs(["HOME","LEARN"])

with tab1:
    homecol1,homecol2 = st.columns([0.7,0.3])
    homecol2.image("https://static.vecteezy.com/system/resources/previews/002/396/557/non_2x/reduce-reduce-recycle-free-vector.jpg")
    st.header("AI for Earth Waste Management")
    st.write("Welcome to AI for Earth Waste Management!")
    homecol1.subheader("How It Works")
    homecol1.markdown("""
                      - Upload the clicked image
                      - wait for the AI to do its magic
                      - Match the material type with the Object
                      - Choose the option from Reuse, Recycle or Reduce
                      """)
     homecol1.markdown("""
                      - Upload the clicked image
                      - wait for the AI to do its magic
                      - Match the material type with the Object
                      - Choose the option from Reuse, Recycle or Reduce
                      """)
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img)
        col1,col2 = st.columns(2)
        model1,model2 = models()
        res1 = model1.predict(img)
        res2 = model2.predict(img)
        two = res2[0].probs.top5
        col1.header('Object Classification')
        for name in res1[0].probs.top5:
            col1.write(res1[0].names[name])
            object.append(res1[0].names[name])
        col2.header('Material Classification')
        for i in two:
            col2.write(res2[0].names[i])
            type.append(res2[0].names[i])
        st.header('Choose a combination of one value from both categories by defining the numbers below')
        col = st.columns(2)
        x = col[0].number_input('select the number for object',min_value = 0,max_value=5,step=1)
        y = col[1].number_input('select the number for type',min_value = 0,max_value=5,step=1)
        time.sleep(1)
        if x >0 and y>0:
            string = type[y-1]+" "+object[x-1]
            st.write(string)
        col1, col2, col3 = st.columns(3)
        with col1:
            button1 = st.button('Recycle')
        with col2:
            button2 = st.button('Reduce')
        with col3:
            button3 = st.button('Reuse')
        if button1:
            st2 = f'please give 5 detailed ways to recycle{string} waste'
            st.write(search(st2))
        if button2:
            st2 = f'can you please describe detailed steps to reduce {string} waste'
            st.write(search(st2))
        if button3:
            st2 = f'can you please generate 3 ways to reuse/repurpose {string} in a very detailed/step by step manner'
            st.write(search(st2))


with tab2:
    col1,col2 = st.columns([0.7,0.3])
    st.title("Learn")
    st.write("Welcome to the Learning Section!")
    st.write("Here, you can find information about waste management and sustainability.")
   
    with st.container(height=500):
        learncol1,learncol2 = st.columns([0.7,0.3])
        learncol1.image("https://img.freepik.com/premium-vector/reuse-recycle-sign-isolated-white-background-vector-illustration_76844-3535.jpg?w=360")
        learncol2.write("PLACEHOLDER")
   
    with st.container(height=500):
        learncol3,learncol4 = st.columns([0.7,0.3])
        learncol3.write("PLACEHOLDER")
        learncol4.image("https://en.pimg.jp/049/862/808/1/49862808.jpg")
   
    with st.container(height=500):
        learncol5,learncol6 = st.columns([0.7,0.3])
        learncol5.write("PLACEHOLDER")
        learncol6.image("https://images.prismic.io/palmettoblog/ca5236ef-970b-4165-8242-53919833a4bc_why-you-should-recycle-environmental-economic-benefits.jpg?auto=compress,format&rect=0,19,1143,762&w=1200&h=800")

