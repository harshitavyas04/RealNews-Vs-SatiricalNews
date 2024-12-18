import streamlit as st
import cv2
import pytesseract as pt
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
css = """
<style>
@keyframes move {
    100% {
        transform: translate3d(0, 0, 1px) rotate(360deg);
    }
}
.background {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    background: #fffce6;
    overflow: hidden;
}
.background span {
    width: 15vmin;
    height: 15vmin;
    border-radius: 15vmin;
    backface-visibility: hidden;
    position: absolute;
    animation: move;
    animation-duration: 25s;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}
.background span:nth-child(0) {
    color: #e7f0f4;
    top: 56%;
    left: 10%;
    animation-duration: 76s;
    animation-delay: -102s;
    transform-origin: -12vw 6vh;
    box-shadow: -30vmin 0 4.2850209678796904vmin currentColor;
}
.background span:nth-child(1) {
    color: #e7f0f4;
    top: 24%;
    left: 96%;
    animation-duration: 152s;
    animation-delay: -156s;
    transform-origin: 3vw 8vh;
    box-shadow: 30vmin 0 4.001761009505196vmin currentColor;
}
.background span:nth-child(2) {
    color: #aec6cf;
    top: 23%;
    left: 96%;
    animation-duration: 22s;
    animation-delay: -244s;
    transform-origin: -13vw 1vh;
    box-shadow: 30vmin 0 3.874379473160472vmin currentColor;
}
.background span:nth-child(3) {
    color: #e7f0f4;
    top: 99%;
    left: 83%;
    animation-duration: 246s;
    animation-delay: -38s;
    transform-origin: 2vw 13vh;
    box-shadow: 30vmin 0 4.3384802129291105vmin currentColor;
}
.background span:nth-child(4) {
    color: #e7f0f4;
    top: 54%;
    left: 13%;
    animation-duration: 134s;
    animation-delay: -115s;
    transform-origin: -11vw -21vh;
    box-shadow: -30vmin 0 3.9260329587822396vmin currentColor;
}
.background span:nth-child(5) {
    color: #e7f0f4;
    top: 8%;
    left: 73%;
    animation-duration: 216s;
    animation-delay: -200s;
    transform-origin: -19vw -11vh;
    box-shadow: 30vmin 0 3.889693724619526vmin currentColor;
}
.background span:nth-child(6) {
    color: #e7f0f4;
    top: 87%;
    left: 79%;
    animation-duration: 181s;
    animation-delay: -63s;
    transform-origin: -8vw -16vh;
    box-shadow: 30vmin 0 4.198411946293855vmin currentColor;
}
.background span:nth-child(7) {
    color: #e7f0f4;
    top: 99%;
    left: 35%;
    animation-duration: 189s;
    animation-delay: -182s;
    transform-origin: -12vw 11vh;
    box-shadow: 30vmin 0 3.957988827082369vmin currentColor;
}
.background span:nth-child(8) {
    color: #aec6cf;
    top: 9%;
    left: 4%;
    animation-duration: 41s;
    animation-delay: -206s;
    transform-origin: 1vw 7vh;
    box-shadow: -30vmin 0 4.6830992652098695vmin currentColor;
}
.background span:nth-child(9) {
    color: #e7f0f4;
    top: 56%;
    left: 81%;
    animation-duration: 204s;
    animation-delay: -59s;
    transform-origin: -2vw 21vh;
    box-shadow: 30vmin 0 4.362591393251875vmin currentColor;
}
.background span:nth-child(10) {
    color: #e7f0f4;
    top: 51%;
    left: 95%;
    animation-duration: 106s;
    animation-delay: -142s;
    transform-origin: 20vw -10vh;
    box-shadow: -30vmin 0 4.30464603282698vmin currentColor;
}
.background span:nth-child(11) {
    color: #e7f0f4;
    top: 5%;
    left: 56%;
    animation-duration: 158s;
    animation-delay: -39s;
    transform-origin: 13vw -18vh;
    box-shadow: -30vmin 0 4.49764479881048vmin currentColor;
}
.background span:nth-child(12) {
    color: #aec6cf;
    top: 27%;
    left: 82%;
    animation-duration: 121s;
    animation-delay: -144s;
    transform-origin: 1vw -12vh;
    box-shadow: 30vmin 0 4.588205242391293vmin currentColor;
}
.background span:nth-child(13) {
    color: #aec6cf;
    top: 9%;
    left: 85%;
    animation-duration: 107s;
    animation-delay: -121s;
    transform-origin: -17vw -4vh;
    box-shadow: -30vmin 0 3.993678747491651vmin currentColor;
}
.background span:nth-child(14) {
    color: #e7f0f4;
    top: 69%;
    left: 74%;
    animation-duration: 240s;
    animation-delay: -162s;
    transform-origin: 23vw -8vh;
    box-shadow: 30vmin 0 3.7523169104251917vmin currentColor;
}
.background span:nth-child(15) {
    color: #aec6cf;
    top: 97%;
    left: 31%;
    animation-duration: 83s;
    animation-delay: -207s;
    transform-origin: -1vw -21vh;
    box-shadow: -30vmin 0 4.1247653016130785vmin currentColor;
}
.background span:nth-child(16) {
    color: #e7f0f4;
    top: 87%;
    left: 45%;
    animation-duration: 116s;
    animation-delay: -87s;
    transform-origin: -19vw -2vh;
    box-shadow: 30vmin 0 4.635123079514468vmin currentColor;
}
.background span:nth-child(17) {
    color: #aec6cf;
    top: 43%;
    left: 77%;
    animation-duration: 239s;
    animation-delay: -90s;
    transform-origin: -1vw -20vh;
    box-shadow: -30vmin 0 4.715496254559995vmin currentColor;
}
.background span:nth-child(18) {
    color: #aec6cf;
    top: 7%;
    left: 60%;
    animation-duration: 61s;
    animation-delay: -139s;
    transform-origin: 14vw 7vh;
    box-shadow: -30vmin 0 4.02343739770485vmin currentColor;
}
.background span:nth-child(19) {
    color: #aec6cf;
    top: 35%;
    left: 72%;
    animation-duration: 51s;
    animation-delay: -129s;
    transform-origin: -2vw -14vh;
    box-shadow: 30vmin 0 4.2584078024709235vmin currentColor;
}
</style>
"""
html = """
<div class="background">
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
   <span></span>
</div>
"""
non_animated_css = """
<style>
[data-testid="stSidebar"] {
    background-color: #6E8091;
    opacity: 1;
    position: fixed;
    width: 20%;
    height: 100vh;
    top: 0;
    left: 0;
    overflow: auto;
}
</style>
"""
header_css = """
<style>
[class="st-emotion-cache-1avcm0n ezrtsby2"] {
    background-color: #95B5CA;
    opacity: 1;
    position: absolute;
    width: 100%;
    height: 7vh;
    top: 0;
    left: 0;
    overflow: auto;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)
st.markdown(non_animated_css, unsafe_allow_html=True)
st.markdown(header_css, unsafe_allow_html=True)
def page1():
    st.markdown('<h2 style="color: black; text-align: center; font-family: Georgia, serif;"><b>Real vs Satirical News Detector</b></h2>', unsafe_allow_html=True)
    st.write("\n\n\n")
    st.markdown('''<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>In this day and age where fake news spreads faster than genuine information, satirical news can be a double-edged sword.
    Providing both humour and critical perspectives, satirical news serves as both a source of entertainment and social commentary.
    However, its capability to be confused with genuine information, because of misinformation, similarity of medium and style,
    and presence of confirmation bias leading to reduced trust in media and increased discourse, highlights the importance of
    critical thinking and media literacy while drawing in with such content. The goal of this project is to distinguish
    Satirical News from Real News to combat this critical and relevant issue.</b></p>''', unsafe_allow_html=True)
    st.write("\n\n")
    st.markdown('''<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>To solve this issue, we have created an AI model using various Machine Learning algorithms like KNN and Naive Bayes
    and created a user-friendly interface to distinguish between Real and Satirical News.</b></p>''', unsafe_allow_html=True)
    st.write("\n\n")
    st.markdown('''<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>You can input either text of the article, or a screenshot of the article. It also has a choice over whether the user
    wants to upload the heading of the article, the body of the article, or the entire combined article. The model runs and gives
    output as either Satirical News or Real News.</b></p>''', unsafe_allow_html=True)
def page2():
    st.markdown('<h2 style="color: black; text-align: center; font-family: Georgia, serif;"><b>Use Text</b></h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>1. Heading of article</b></p>', unsafe_allow_html=True)
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>2. Content of article</b></p>', unsafe_allow_html=True)
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>3. Whole article</b></p>', unsafe_allow_html=True)
    st.write("\n\n")
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Please enter option of your choice here</b></p>', unsafe_allow_html=True)
    choice = st.number_input(" ",min_value=1,max_value=3,step=1)
    st.write("\n")
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Enter text here</b></p>', unsafe_allow_html=True)
    text = st.text_input(" ")
    st.write("\n")
    if choice==1:
        #inputData = preprocess(text)
        with open("tfidfHeading", 'rb') as file:
            tfidf_model = pickle.load(file)
        inputData = tfidf_model.transform([text])
        with open("nbHeading", 'rb') as file:
            loaded_model = pickle.load(file)
        output=loaded_model.predict(inputData)
        if output[0]==0:
            st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Satirical News</h5>', unsafe_allow_html=True)
        elif output[0]==1:
            st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Real News</h5>', unsafe_allow_html=True)
    elif choice==2:
        #inputData = preprocess(text)
        with open("tfidfText", 'rb') as file:
            tfidf_model = pickle.load(file)
        inputData = tfidf_model.transform([text])
        with open("nbText", 'rb') as file:
            loaded_model = pickle.load(file)
        output=loaded_model.predict(inputData)
        if output[0]==0:
            st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Satirical News</h5>', unsafe_allow_html=True)
        elif output[0]==1:
            st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Real News</h5>', unsafe_allow_html=True)
    else:
        #inputData = preprocess(text)
        with open("tfidfCombined", 'rb') as file:
            tfidf_model = pickle.load(file)
        inputData = tfidf_model.transform([text])
        with open("knnCombined", 'rb') as file:
            loaded_model = pickle.load(file)
        output=loaded_model.predict(inputData)
        if output[0]==0:
            st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Satirical News</h5>', unsafe_allow_html=True)
        elif output[0]==1:
            st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Real News</h5>', unsafe_allow_html=True)
def page3():
    st.markdown('<h2 style="color: black; text-align: center; font-family: Georgia, serif;"><b>Use Image</b></h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>1. Heading of article</b></p>', unsafe_allow_html=True)
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>2. Content of article</b></p>', unsafe_allow_html=True)
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>3. Whole article</b></p>', unsafe_allow_html=True)
    st.write("\n")
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Please enter option of your choice here</b></p>', unsafe_allow_html=True)
    choice = st.number_input(" ",min_value=1,max_value=3,step=1)
    st.write("\n")
    st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Please upload an image in .jpg, .jpeg or .png format</b></p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(" ", type=["jpg", "jpeg", "png"])
    st.write("\n")
    if uploaded_file is not None:
        st.markdown('<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Uploaded Image:</b></p>', unsafe_allow_html=True)
        st.image(uploaded_file, width=200)
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        image_path = os.path.join("uploads", uploaded_file.name)
        image = cv2.imread(file_path)
        textFromImage = pt.image_to_string(image)
        textFromImage = str(textFromImage)
        if choice==1:
            st.markdown(f'<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Text extracted from image: <h6 style="color: black; text-align: justify; font-family: Georgia, serif;">{textFromImage}</h6></b></p>', unsafe_allow_html=True)
            with open("tfidfHeading", 'rb') as file:
                tfidf_model = pickle.load(file)
            inputData = tfidf_model.transform([textFromImage])
            with open("nbHeading", 'rb') as file:
                loaded_model = pickle.load(file)
            output=loaded_model.predict(inputData)
            if output[0]==0:
                st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Satirical News</h5>', unsafe_allow_html=True)
            elif output[0]==1:
                st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Real News</h5>', unsafe_allow_html=True)
        elif choice==2:
            st.markdown(f'<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Text extracted from image: <h6 style="color: black; text-align: justify; font-family: Georgia, serif;">{textFromImage}</h6></b></p>', unsafe_allow_html=True)
            with open("tfidfText", 'rb') as file:
                tfidf_model = pickle.load(file)
            inputData = tfidf_model.transform([textFromImage])
            with open("nbText", 'rb') as file:
                loaded_model = pickle.load(file)
            output=loaded_model.predict(inputData)
            if output[0]==0:
                st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Satirical News</h5>', unsafe_allow_html=True)
            elif output[0]==1:
                st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Real News</h5>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="color: black; text-align: justify; font-family: Georgia, serif;"><b>Text extracted from image: <h6 style="color: black; text-align: justify; font-family: Georgia, serif;">{textFromImage}</h6></b></p>', unsafe_allow_html=True)
            with open("tfidfCombined", 'rb') as file:
                tfidf_model = pickle.load(file)
            inputData = tfidf_model.transform([textFromImage])
            with open("knnCombined", 'rb') as file:
                loaded_model = pickle.load(file)
            output=loaded_model.predict(inputData)
            if output[0]==0:
                st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Satirical News</h5>', unsafe_allow_html=True)
            elif output[0]==1:
                st.markdown(f'<h5 style="color: black; text-align: justify; font-family: Georgia, serif;">Result: Real News</h5>', unsafe_allow_html=True)
PAGES = {"About Us...": page1, "Use Text": page2, "Use Image": page3}
menu_selection = st.sidebar.selectbox('Go to', list(PAGES.keys()))
page = PAGES[menu_selection]
page()
