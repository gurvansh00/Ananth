import streamlit as st
from ultralytics import YOLO
from PIL import Image
import time
from openai import OpenAI
client = OpenAI()

#eco

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
	st.markdown("<h1 style='text-align: center; color: grey;'>Big headline</h1>", unsafe_allow_html=True)
	homecol1,homecol2 = st.columns([0.7,0.3])
	homecol2.image("d3df85a0-600f-41f1-9ad3-31da745a9e1d.JPG")
	st.write("Welcome to AI for Earth Waste Management!")
	homecol1.subheader("How It Works")
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
   
    with st.container(height=320):
        learncol1,learncol2 = st.columns([0.3,0.7])
        learncol1.image("https://www.josafety.dk/images/Produktbilleder/Reuse-Affaldsskilt-WA3601P240X240.png")
        learncol2.write("Reuse: Give Things a Second ChanceReuse is all about giving things a second life instead of throwing them away. By finding new uses for old items, we can reduce waste and save valuable resources. Whether it's repurposing old jars as storage containers, sharing clothes or tools with friends, repairing broken items instead of replacing them, borrowing instead of buying, or donating items to those in need, every act of reuse contributes to a more sustainable future. The object could be reused in different ways rather than just being thrown away after one use.")
   
    with st.container(height=320):
        learncol3,learncol4 = st.columns([0.7,0.3])
        learncol3.write("Reduce: Use Wisely, Waste Less Reducing consumption is about being mindful of our purchases and using resources wisely. It involves buying only what we need, choosing products with minimal packaging, and avoiding single-use items whenever possible. By prioritizing quality over quantity, investing in durable goods, and embracing a less-is-more mindset, we can live more sustainably.For reducing, they put it in a bin or contribute it to an area that will reduce and potentially decompose the object. ")
        learncol4.image("https://media.licdn.com/dms/image/C5622AQFztQ772Yi6hQ/feedshare-shrink_2048_1536/0/1662368422476?e=2147483647&v=beta&t=P-p1zfZ46lOgpiN0qceiiQ51vJHTl4si2eyN23ZblEs")
    with st.container(height=320):
        learncol5,learncol6 = st.columns([0.3,0.7])
        learncol6.write("Recycle: Close the Loop Recycling is the process of turning old materials into new products, preventing them from ending up in landfills. It's a crucial part of the circular economy, where materials are reused and recycled indefinitely. By separating recyclables like paper, plastic, glass, and metal from our trash, supporting recycling programs, and purchasing products made from recycled materials, and protect the planet for future generations. It could be put into a center that potentially as recycling opportunities so that the object may be built into something else.")
        learncol5.image("https://hlpklearfold.co.uk/wp-content/uploads/2018/01/Recycle.jpg")
     
    with st.container(height=200):
        learncol7,learncol8 = st.columns([0.7,0.3])
        learncol7.write("Eco Intellects is a product designed to raise public awareness about eco-friendly practices by utilizing everyday trash. Through three options presented on the app—reduce, reuse, and recycle—users can submit their items and choose how to manage them. Detailed descriptions of each option, along with multiple suggestions, will be provided. By using this product, waste production can be minimized, encouraging people to find more sustainable ways to repurpose their trash rather than simply discarding it. Our aim is to reduce the impact of climate change and ocean waste, creating a safer environment for both humans and animals on our beautiful planet, Earth")
        learncol8.image("d3df85a0-600f-41f1-9ad3-31da745a9e1d.JPG")
