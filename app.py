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
        The word is '{word}'. Provide homework help for a 7-year-old (1st/2nd grade).
        Respond ONLY in this exact format, with no extra text or conversational chatter:
        
        MEANING: [Write a very short, simple definition using words a 7-year-old knows. Max 15 words.]
        SENTENCE: [Write one easy, fun sentence using the word that a child can easily read and copy.]
        """
        
        with st.spinner('Thinking...'):
            response = model.generate_content(prompt)
            output = response.text

        # Parsing the response safely
        meaning_text = "Could not find meaning. Try again!"
        sentence_text = "Could not make a sentence. Try again!"
        
        for line in output.split("\n"):
            if line.startswith("MEANING:"):
                meaning_text = line.replace("MEANING:", "").strip()
            elif line.startswith("SENTENCE:"):
                sentence_text = line.replace("SENTENCE:", "").strip()

        st.markdown(f"## ✨ Results for: **{word.capitalize()}**")
        
        # Displaying tailored boxes for the child
        st.markdown('<p class="big-font">📝 Meaning:</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="meaning-box">{meaning_text}</div>', unsafe_allow_html=True)
        
        st.markdown('<p class="big-font">💬 Sentence it!</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="sentence-box">"{sentence_text}"</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        """# DISPLAYING THE ACTUAL IMAGE
        st.markdown('<p class="big-font">🎨 Look at this picture and draw it!</p>', unsafe_allow_html=True)
        
        # Formatting the image prompt for a clean, easy-to-copy kid's drawing
        image_prompt = f"a very simple child friendly line drawing of {word}, cute cartoon style, coloring book style, clear white background"
        encoded_word = urllib.parse.quote(image_prompt)
        
        # Free image URL source
        image_url = f"https://image.pollinations.ai/p/{encoded_word}?width=600&height=500&seed=15&nofeed=true"
        
        # This function forces Streamlit to render the actual image on screen
        st.image(image_url, use_column_width=True)"""
        
        # DISPLAYING THE ACTUAL IMAGE
        st.markdown('<p class="big-font">🎨 Look at this picture and draw it!</p>', unsafe_allow_html=True)
        
        # Creating a super clean, easy-to-draw cartoon prompt
        image_prompt = f"a very simple child friendly line drawing of a {word}, cute cartoon style, white background"
        encoded_word = urllib.parse.quote(image_prompt)
        
        # Free image URL source
        image_url = f"https://image.pollinations.ai/p/{encoded_word}?width=500&height=500&seed=24"
        
        # FIX: Using the updated, secure container layout to force the image to show
        st.image(image_url, caption=f"Drawing idea for: {word}", output_format="JPEG")
        
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower():
            st.warning("⏳ The app is thinking a little too fast! Please wait 30 seconds and try typing the word again.")
        else:
            st.error(f"Something went wrong. Error details: {e}")
