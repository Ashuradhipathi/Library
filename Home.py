import streamlit as st 

def main():
    st.markdown("""
    <div style='text-align: center;'>
        <h1>Hello</h1>
    </div>
    """, unsafe_allow_html=True)
    url="https://i.ibb.co/FYgXtTZ/3d-rendering-emotions.jpg"
    st.image(url)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center;'>
        <h4>Heyy Folks, Join us?</h4>
    </div>
    """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()