import streamlit as st
import google.generativeai as genai
import urllib.parse

# Configure the Gemini API (Replace with your actual key or use Streamlit Secrets)
# For local testing, paste your key here. For cloud deployment, use st.secrets.
#API_KEY = st.secrets.get("GEMINI_API_KEY", "${{ secrets.GEMINI_API }}")
API_KEY = st.secrets["GEMINI_API_KEY"]

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()
genai.configure(api_key=API_KEY)

# App Title & Styling
st.set_page_config(page_title="Word of the Day Helper", page_icon="✏️")
st.title("✏️ Kid's Word of the Day Helper")
st.write("Type your homework word below to get the meaning, a sentence, and a drawing idea!")

# User Input
word = st.text_input("Enter the Word of the Day:", value="").strip()

if word:
    try:
        # Initialize Gemini Model
        model = genai.GenerativeModel('gemini-3.5-flash')
        
        # Crafting a prompt tailored for a child's homework
        prompt = f"""
        The word is '{word}'. Provide the following for an elementary school child's homework:
        1. Meaning: A very simple, easy-to-understand definition.
        2. Sentence it!: A fun, clear sentence using the word that a child can easily copy.
        Keep the tone encouraging and simple.
        """
        
        with st.spinner('Thinking...'):
            response = model.generate_content(prompt)
            
        st.success("Success!")
        
        # Display the Text results
        st.subheader(f"✨ Results for: **{word.capitalize()}**")
        st.write(response.text)
        
        st.markdown("---")
        
        # Generate a drawing idea using a free image generation API (Pollinations.ai)
        st.subheader("🎨 Draw a Picture About It!")
        st.write("Here is an idea of what you can draw. Try to copy this image in your notebook:")
        
        # Clean the word for the URL
        encoded_word = urllib.parse.quote(f"simple child friendly drawing of {word}, cartoon style, white background")
        image_url = f"https://image.pollinations.ai/p/{encoded_word}?width=500&height=500&seed=42&nofeed=true"
        
        st.image(image_url, caption=f"Drawing inspiration for '{word}'")
        
    except Exception as e:
        st.error(f"Oops! Something went wrong. Make sure your API key is correct. Error: {e}")
