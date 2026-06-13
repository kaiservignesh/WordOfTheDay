import streamlit as st
import google.generativeai as genai
import urllib.parse

# Configure the Gemini API using Streamlit Secrets
#API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
API_KEY = st.secrets["GEMINI_API_KEY"]

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()
genai.configure(api_key=API_KEY)

# App Title & Page Settings
st.set_page_config(page_title="Word of the Day", page_icon="✏️", layout="centered")

# Custom CSS to make the text big, clean, and kid-friendly
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #2E4057; }
    .meaning-box { background-color: #E8F1F5; padding: 15px; border-radius: 10px; border-left: 5px solid #2980B9; font-size: 18px; margin-bottom: 20px;}
    .sentence-box { background-color: #E8F8F5; padding: 15px; border-radius: 10px; border-left: 5px solid #27AE60; font-size: 18px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title("✏️ Kid's Word of the Day Helper")
st.write("Type your homework word below to get your meaning, sentence, and drawing!")

# User Input
word = st.text_input("👉 Enter your homework word here:", value="").strip()

if word:
    try:
        # Using the faster, lighter model for rate-limit safety
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
        
        # Strict prompt for a 7-year-old child's level
        prompt = f"""
        The word is '{word}'. Provide homework help for a 7-year-old child.
        Follow these rules strictly and do not include any other conversational introduction or pro-tips:
        
        MEANING: [Provide exactly a one-word or two-word definition that a 7-year-old understands. No more than two words.]
        SENTENCE: [Write one very short, simple sentence using the word that a child can easily copy.]
        DRAWING: [Provide 3 to 4 simple emojis spaced out that match the word perfectly for a child to look at and draw.]
        """
        
        with st.spinner('Thinking...'):
            text_response = model.generate_content(text_prompt)
            output = text_response.text

        meaning_text = "Try again!"
        sentence_text = "Try again!"
        drawing_text = "⭐ ✨ 🎈"
        
        # Splitting the lines carefully
        for line in output.split("\n"):
            if line.startswith("MEANING:"):
                meaning_text = line.replace("MEANING:", "").strip()
            elif line.startswith("SENTENCE:"):
                sentence_text = line.replace("SENTENCE:", "").strip()
            elif line.startswith("DRAWING:"):
                drawing_text = line.replace("DRAWING:", "").strip()

        # Display Text Results
        st.markdown(f"## ✨ Results for: **{word.capitalize()}**")
        
        st.markdown('<p class="big-font">📝 Meaning:</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="meaning-box">{meaning_text}</div>', unsafe_allow_html=True)
        
        st.markdown('<p class="big-font">💬 Sentence it!</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="sentence-box">"{sentence_text}"</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # DISPLAYING THE ACTUAL IMAGE
        #st.markdown('<p class="big-font">🎨 Look at this picture and draw it!</p>', unsafe_allow_html=True)
        
        # Formatting the image prompt for a clean, easy-to-copy kid's drawing
        #image_prompt = f"a very simple child friendly line drawing of {word}, cute cartoon style, coloring book style, clear white background"
        #encoded_word = urllib.parse.quote(image_prompt)
        
        # Free image URL source
        #image_url = f"https://image.pollinations.ai/p/{encoded_word}?width=600&height=500&seed=15&nofeed=true"
        
        # This function forces Streamlit to render the actual image on screen
        #st.image(image_url, use_column_width=True)

        # Display the drawing icons
        st.markdown('<p class="big-font">🎨 Look at these pictures and draw them!</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: #FAFAFA; border: 3px dashed #BDC3C7; padding: 30px; border-radius: 10px; text-align: center; font-size: 50px; letter-spacing: 15px;">
            {drawing_text}
        </div>
        <p style="text-align: center; font-size: 14px; color: #7F8C8D; margin-top: 10px;">✏️ Pick one or two of these shapes to draw in your notebook!</p>
        """, unsafe_allow_html=True)
            
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            st.warning("⏳ The app is thinking a little too fast! Please wait 30 seconds and try typing the word again.")
        else:
            st.error(f"Something went wrong. Error details: {e}")
