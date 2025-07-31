from ast import If
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Set the page configuration
if "step" not in st.session_state:
    st.session_state.step = 1

# css style for streamlit app
st.markdown("""
<style>

/* Style the main container */
[data-testid="stAppViewContainer"] {
    background: 
    linear-gradient(rgba(255,255,255,0.7), rgba(255,255,255,0.7)),  /* 70% white overlay */
    url("https://i.pinimg.com/1200x/eb/51/61/eb516105fc81981c04a4bdd17f5f98c1.jpg") 
      center/cover ;
    font-family: 'Arial', sans-serif;
    
}

/* Style the form */
[data-testid="stForm"] {
    padding: 3rem;
    background-color: white;
    border-radius: 15px;
    box-shadow: 2px 2px 20px rgba(0, 0, 0, 0.1);
    width: 100%;
    margin-left: auto;
    margin-right: auto;
    font-size: 1.5rem;
}

/* Style the form font size */

/* Adjust the form title */
[data-testid="stForm"] h3 {
    font-size: 1.7rem !important;
    font-weight: bold !important;
}

/* Style the form button */
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    width: 100%;
}
/* Hover state */
div.stButton > button:hover {
    background-color: #45a049;
}

/* Active/clicked state */
div.stButton > button:active {
    background-color: #3e8e41;
    color: white;
}

/* Style ONLY the Take Again button */
div.stButton > button[kind="primary"] {
    background-color: #4CAF50;
    color: white;
    border: none;
}

/* Hover state */
div.stButton > button[kind="primary"]:hover {
    background-color: #45a049;
}

/* Active/clicked state */
div.stButton > button[kind="primary"]:active {
    background-color: #3e8e41;
    color: white;
}

/* Remove default bottom padding */
.block-container {
    padding-bottom: 0 !important;
    padding-top: 0 !important;
}   

/* Style Footer */
.footer {
    width: 100%;
    background: #f2f2f2;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    color: grey;
    border-top: 1px solid #ddd;
    margin-top: 10px;
    margin-bottom: 40px;
}

</style>
""", unsafe_allow_html=True)


# load the trained model and preprocessor
model = joblib.load('best_model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# define the app header
st.markdown("""
<div style='text-align: center; padding: 30px 0; margin-top: 40px;'>
    <h1 style='font-size: 2.5rem; color: #2d3748;'>
        Teen Phone Addiction <span style='color: #319795;'>Risk Assessment</span>
    </h1>
    <p style='font-size: 1.1rem; color: #4a5568; max-width: 700px; margin: auto;'>
        Understand your relationship with technology through our comprehensive assessment tool. 
        Get personalized insights and recommendations for healthier digital habits.
    </p>
    <div style='margin-top: 15px; font-size: 0.9rem; color: #718096;'>
        <span style='margin-right: 20px;'>🕒 3-minute assessment</span>
        <span style='margin-right: 20px;'>📊 Personalized results</span>
        <span>💡 Evidence-based recommendations</span>
    </div>
</div>
""", unsafe_allow_html=True)

def show_header():
    # Custom progress bar with segment markers
    total_steps = 5
    current_step = st.session_state.step
    percentage = (current_step / total_steps) * 100

    st.markdown(f"""
    <div style='position: relative; height: 30px; background: #e0e0e0; border-radius: 10px; overflow: hidden;'>
        <!-- Progress fill -->
        <div style='width: {percentage}%; height: 100%; background: lightblue;'></div>
        
        <!-- Vertical dividers -->
        {''.join([f"<div style='position:absolute; left:{(i/total_steps)*100}%; top:0; bottom:0; width:2px; background:#fff;'></div>" 
        for i in range(1, total_steps)])}
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; font-weight:semi-bold; margin-top: 10px;'>Step {st.session_state.step} / 5</p>", 
        unsafe_allow_html=True
    )
    
# Form steps     
if st.session_state.step == 1:
    with st.form("Step_1_form"):
        show_header()
        st.subheader("Step 1: User Details 👤")

        # define input options
        Age = st.slider("Age *", min_value=13, max_value=19, value=st.session_state.get("Age", 16))

        Gender = st.selectbox("Gender *", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.get("Gender", "Male")))
        
        School_Grade = st.selectbox("Which grade are u in? *", options=["7th", "8th", "9th", "10th", "11th", "12th"], index=["7th", "8th", "9th", "10th", "11th", "12th"].index(st.session_state.get("School_Grade", "9th")))
    
        
        col1, col2 = st.columns([1, 1])
        next_button = col2.form_submit_button("Next",use_container_width=True)

        if next_button:
            st.session_state.update({
                "Age": Age,
                "Gender": Gender,
                "School_Grade": School_Grade
            })
            st.session_state.step = 2         
            st.rerun()   

elif st.session_state.step == 2:
    
    with st.form("Step_2_form"):
        show_header()
                    
        st.subheader("Step 2: Phone Usage Habits 📱")

        Daily_Usage_Hours = st.slider("What is your average daily screen time (hours) *", min_value=0, max_value=12, value=st.session_state.get("Daily_Usage_Hours", 3))

        Weekend_Usage_Hours = st.slider("What is your average weekend phone usage (hours) *", min_value=0, max_value=14, value=st.session_state.get("Weekend_Usage_Hours", 5))

        Screen_Time_Before_Bed = st.slider("What is your average screen time before bed (hours) *", min_value=0, max_value=3, value=st.session_state.get("Screen_Time_Before_Bed", 1))

        Phone_Checks_Per_Day = st.slider("What is your average phone checks per day? *", min_value=20, max_value=150, value=st.session_state.get("Phone_Checks_Per_Day", 50))

        Apps_Used_Daily = st.slider("How many different apps do you use daily? *", min_value=6, max_value=20, value=st.session_state.get("Apps_Used_Daily", 10))


        col1, col2 = st.columns([1, 1])
        previous_button = col1.form_submit_button("Previous",use_container_width=True)
        next_button = col2.form_submit_button("Next",use_container_width=True)

        if previous_button:
            st.session_state.step = 1
            st.rerun()
        if next_button:
            st.session_state.update({
                "Daily_Usage_Hours": Daily_Usage_Hours,
                "Weekend_Usage_Hours": Weekend_Usage_Hours,
                "Screen_Time_Before_Bed": Screen_Time_Before_Bed,
                "Phone_Checks_Per_Day": Phone_Checks_Per_Day,
                "Apps_Used_Daily": Apps_Used_Daily
            })
            st.session_state.step = 3
            st.rerun()
            
            
elif st.session_state.step == 3:
    with st.form("Step_3_form"):
        show_header()
        
        st.subheader("Step 3: App usages 📊")

        Time_on_Social_Media = st.slider("How much time do you spend on social media (in hours) *", min_value=0, max_value=5, value=st.session_state.get("Time_on_Social_Media", 2)) 

        Time_on_Gaming = st.slider("How much time do you spend on gaming (in hours) *", min_value=0, max_value=4, value=st.session_state.get("Time_on_Gaming", 1))

        Time_on_Education = st.slider("How much time do you spend on educational apps (in hours) *", min_value=0, max_value=3, value=st.session_state.get("Time_on_Education", 1))

        Phone_Usage_Purpose = st.selectbox("What is the primary purpose of your phone usage? *", options=["Browsing", "Education","Social Media", "Gaming", "Others"], index=["Browsing", "Education", "Social Media", "Gaming", "Others"].index(st.session_state.get("Phone_Usage_Purpose", "Social Media")))
            
        Parental_Control = st.checkbox("Do your parents monitor your phone usage? *", value=st.session_state.get("Parental_Control", False))
        
        col1, col2 = st.columns([1, 1])
        previous_button = col1.form_submit_button("Previous",use_container_width=True)
        next_button = col2.form_submit_button("Next",use_container_width=True)

        if previous_button:
            st.session_state.step = 2
            st.rerun()
        if next_button:
            st.session_state.update({
                "Time_on_Social_Media": Time_on_Social_Media,
                "Time_on_Gaming": Time_on_Gaming,
                "Time_on_Education": Time_on_Education,
                "Phone_Usage_Purpose": Phone_Usage_Purpose,
                "Parental_Control": Parental_Control
            })
            st.session_state.step = 4
            st.rerun()
               
    
elif st.session_state.step == 4:
    
    with st.form("Step_4_form"):
        show_header()
            
        st.subheader("Step 4: Lifestyle 🧘‍♀️")

        Sleep_Hours = st.slider("What is your average daily sleep time (in hours)? *", min_value=3, max_value=10, value=st.session_state.get("Sleep_Hours", 7))

        Academic_Performance = st.slider("How well are you doing in school (average Results you get for your exams)? *", min_value=50, max_value=100, value=st.session_state.get("Academic_Performance", 75))

        Social_Interactions = st.slider("How would you rate your social interactions? (0 = Poor,  10 = Excellent) *", min_value=0, max_value=10, value=st.session_state.get("Social_Interactions", 5))

        Family_Communication = st.slider("How often do you communicate with your family via phone? (0 = No communication at all,  10 = Communicate everyday) *", min_value=0, max_value=10, value=st.session_state.get("Family_Communication", 5))

        col1, col2 = st.columns([1, 1])
        previous_button = col1.form_submit_button("Previous",use_container_width=True)
        next_button = col2.form_submit_button("Next",use_container_width=True)

        if previous_button:
            st.session_state.step = 3
            st.rerun()
        if next_button:
            st.session_state.update({
                "Sleep_Hours": Sleep_Hours,
                "Academic_Performance": Academic_Performance,
                "Social_Interactions": Social_Interactions,
                "Family_Communication": Family_Communication
            })
            st.session_state.step = 5
            st.rerun()


elif st.session_state.step == 5:
    
    with st.form("Step_5_form"):
        show_header()
            
        st.subheader("Step 5: Mental health and Well-being 🧠")

        Exercise_Hours = st.slider("How long do you exercise for (in hours)? *", min_value=0, max_value=4, value=st.session_state.get("Exercise_Hours", 1))

        Anxiety_Level = st.slider("Rank your Anxiety Level from 1 (low) to 10 (high) *", min_value=1, max_value=10, value=st.session_state.get("Anxiety_Level", 5))

        Depression_Level = st.slider("Rank your Depression Level from 1 (low) to 10 (high) *", min_value=1, max_value=10, value=st.session_state.get("Depression_Level", 5))

        Self_Esteem = st.slider("Rank your Self-Esteem from 1 (low) to 10 (high) *", min_value=1, max_value=10, value=st.session_state.get("Self_Esteem", 5))

        col1, col2 = st.columns([1, 1])
        prev = col1.form_submit_button("Previous",use_container_width=True)
        get_result = col2.form_submit_button("Get Results",use_container_width=True)

        if prev:
            st.session_state.step = 4
            st.rerun()
        if get_result:
            st.session_state.update({
                "Exercise_Hours": Exercise_Hours,
                "Anxiety_Level": Anxiety_Level,
                "Depression_Level": Depression_Level,
                "Self_Esteem": Self_Esteem
            })
            st.session_state.step = 6
            st.rerun()

        input_data = pd.DataFrame([{key: st.session_state.get(key, 0) for key in [
            "Age","Gender","School_Grade","Daily_Usage_Hours","Weekend_Usage_Hours",
            "Screen_Time_Before_Bed","Phone_Checks_Per_Day","Apps_Used_Daily",
            "Time_on_Social_Media","Time_on_Gaming","Time_on_Education","Phone_Usage_Purpose",
            "Parental_Control","Sleep_Hours","Academic_Performance","Social_Interactions",
            "Family_Communication","Exercise_Hours","Anxiety_Level","Depression_Level","Self_Esteem"
        ]}])
        
        input_encoded = preprocessor.transform(input_data)
        st.session_state.result = model.predict(input_encoded)[0]

# get results and display
elif st.session_state.step == 6:
    st.subheader("Assessment Result 📈")
    addiction_level = st.session_state.result
    
    if addiction_level == "High":
        st.error(f"Your predicted phone addiction level is: **{addiction_level}** ")
        st.error("You are at high risk of phone addiction. Please consider reducing your screen time and engaging in more offline activities.")
        st.markdown("""
        <p style='font-size:1.2rem; font-weight:bold;'>🛡️ Recommendations:</p>
        <ul style='font-size:1rem;'>
            <li>Maintain balanced screen time</li>
            <li>Engage in more physical activities</li>
            <li>Prioritize sleep and mental health</li>
            <li>Communicate with family and friends</li>
            <li>Seek professional help if needed</li>
        </ul>
        """, unsafe_allow_html=True)
        
    elif addiction_level == "Moderate":
        st.warning(f"Your predicted phone addiction level is: **{addiction_level}** ")
        st.warning("You may want to monitor your phone usage and consider reducing it if necessary.")
        st.markdown("""
        <p style='font-size:1.2rem; font-weight:bold;'>🛡️ Recommendations:</p>
        <ul style='font-size:1rem;'>
            <li>Monitor your screen time</li>
            <li>Balance online and offline activities</li>
            <li>Maintain healthy sleep patterns</li>
            <li>Engage in social interactions</li>
            <li>Consider setting usage limits</li>
        </ul>
        """, unsafe_allow_html=True)

    elif addiction_level == "Low":
        st.success(f"Your predicted phone addiction level is: **{addiction_level}**")
        st.success("You have a healthy relationship with your phone. Keep up the good work!")
        st.markdown("""
        <p style='font-size:1.2rem; font-weight:bold;'>🛡️ Recommendations:</p>
        <ul style='font-size:1rem;'>
            <li>Continue maintaining a balanced lifestyle</li>
            <li>Engage in physical activities</li>
            <li>Prioritize mental health and well-being</li>
            <li>Stay connected with family and friends</li>
            <li>Keep monitoring your phone usage</li>
        </ul>
        """, unsafe_allow_html=True)
    
    if st.button("Take Again", type="primary"):
        st.session_state.clear()
        st.session_state.step = 1
        st.rerun()
        
st.markdown("""
<div class="footer">
    ⚠️ This assessment is for educational purposes only and does not replace professional medical advice. <br>
    If you have concerns about mental health or addiction, please consult with a healthcare professional.
</div>
""", unsafe_allow_html=True)