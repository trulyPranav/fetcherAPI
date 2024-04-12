import streamlit as st
from bs4 import BeautifulSoup
import requests
import json

# Initialize session state for login status
if 'isLogged' not in st.session_state:
    st.session_state.isLogged = False

# Function to handle data request
def handle_data_request():
    # Get query parameters (username and password) from the URL
    query_params = st.query_params()
    username = query_params.get('username', [None])[0]
    password = query_params.get('password', [None])[0]
    
    if username and password:
        # Perform login and fetch data as in your example
        payload = {
            'LoginForm[username]': username,
            'LoginForm[password]': password
        }
        userSession = requests.session()
        login_response = userSession.post(url='https://sctce.etlab.in/user/login', data=payload)
        
        if login_response.status_code == 200:
            # Fetch user profile and subject-attendance data
            profile_response = userSession.get('https://sctce.etlab.in/student/profile')
            subject_response = userSession.get('https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88')
            
            if profile_response.status_code == 200 and subject_response.status_code == 200:
                html_profile = BeautifulSoup(profile_response.content, 'html.parser')
                html_subject = BeautifulSoup(subject_response.content, 'html.parser')
                html_attendance = BeautifulSoup(subject_response.content, 'html.parser')
                
                try:
                    # Extract user data
                    name_tag = html_profile.find('th', string='Name')
                    gender_tag = html_profile.find('th', string='Gender')
                    university_id = html_profile.find('th', string='University Reg No')
                    subject_by_subs = html_subject.find_all('th', class_='span2')
                    attendance_by_subs = html_attendance.find_all('td', class_='span2')
                    
                    # Store user data
                    userData = {
                        'isLoggedIn': True,
                        'Username': username,
                        'Name': name_tag.find_next('td').text.strip(),
                        'Gender': gender_tag.find_next('td').text.strip(),
                        'Department_ID': university_id.find_next('td').text.strip()
                    }
                    
                    # Extract subject and attendance data
                    subject_data = [subject.text.strip() for subject in subject_by_subs]
                    attendance_data = [attendance.text.strip() for attendance in attendance_by_subs]
                    
                    # Combine subject and attendance data
                    data = list(zip(subject_data, attendance_data))
                    
                    # Return data as JSON response
                    st.json({
                        'user_data': userData,
                        'data': data
                    })
                except AttributeError:
                    st.error("Error parsing profile information.")
            else:
                st.error("Error fetching profile or subject data.")
        else:
            st.error("Login failed. Please check your credentials.")
    else:
        st.error("No username or password provided in the query parameters.")

