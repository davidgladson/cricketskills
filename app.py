# app.py
import streamlit as st

def main():
    # Set page config
    st.set_page_config(
        page_title="Cricket Skills",
        page_icon="🏏",
        layout="wide"
    )

    # Header
    st.title("Welcome to Cricket Skills")
    st.subheader("Master the art of cricket with expert guidance")

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.header("What We Offer")
        st.write("""
        - Professional cricket coaching
        - Video analysis of your technique
        - Personalized training programs
        - Mental conditioning sessions
        """)

    with col2:
        st.header("Why Choose Us")
        st.write("""
        - Experienced coaches
        - State-of-the-art facilities
        - Comprehensive skill development
        - Progress tracking
        """)

    # Call to Action
    st.markdown("---")
    st.header("Ready to elevate your game?")
    
    contact_form = st.form("contact_form")
    with contact_form:
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit = st.form_submit_button("Send Message")

if __name__ == "__main__":
    main()
