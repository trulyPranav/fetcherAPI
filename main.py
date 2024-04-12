from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
#import os
#port = int(os.environ.get("PORT", 5000))
app = Flask(__name__)
CORS(app)
#if __name__ == "__main__":
#    app.run(host="0.0.0.0")
#app.run(host="0.0.0.0", port=port)
@app.route('/api/login', methods=['POST'])

def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    payload = {
        'LoginForm[username]': username,
        'LoginForm[password]': password
    }
    
    userSession = requests.session()
    login_response = userSession.post(url='https://sctce.etlab.in/user/login', data=payload)
    
    if login_response.status_code == 200:
        profile_response = userSession.get('https://sctce.etlab.in/student/profile')
        subject_response = userSession.get('https://sctce.etlab.in/ktuacademics/student/viewattendancesubject/88')
        
        if profile_response.status_code == 200 and subject_response.status_code == 200:
            html_profile = BeautifulSoup(profile_response.content, 'html.parser')
            html_subject = BeautifulSoup(subject_response.content, 'html.parser')
            html_attendance = BeautifulSoup(subject_response.content, 'html.parser')

            try:
                name_tag = html_profile.find('th', string='Name')
                gender_tag = html_profile.find('th', string='Gender')
                university_id = html_profile.find('th', string='University Reg No')
                subject_by_subs = html_subject.find_all('th', class_='span2')
                attendance_by_subs = html_attendance.find_all('td', class_='span2')

                userData = {
                    'Username': username,
                    'Name': name_tag.find_next('td').text.strip(),
                    'Gender': gender_tag.find_next('td').text.strip(),
                    'Department_ID': university_id.find_next('td').text.strip()
                }
                
                subject_data = [subject.text.strip() for subject in subject_by_subs]
                attendance_data = [attendance.text.strip() for attendance in attendance_by_subs]
                data_list = [{'Subject': subject, 'Attendance': attendance} for subject, attendance in zip(subject_data, attendance_data)]
                return jsonify({'userData': userData, 'data': data_list})
            except AttributeError:
                return jsonify({'error': 'Error parsing profile information.'}), 400
        else:
            return jsonify({'error': 'Error fetching profile or subject data.'}), 400
    else:
        return jsonify({'error': 'Login failed. Please check your credentials.'}), 400
