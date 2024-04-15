from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

class UserData:
    def __init__(self, username, name, gender, department_id):
        self.username = username
        self.name = name
        self.gender = gender
        self.department_id = department_id
    
    def to_dict(self):
        return {
            'username': self.username,
            'name': self.name,
            'gender': self.gender,
            'department_id': self.department_id
        }

class SubjectData:
    def __init__(self, subject, attendance):
        self.subject = subject
        self.attendance = attendance

    def to_dict(self):
        return {
            'subject': self.subject,
            'attendance': self.attendance
        }

class ResponseData:
    def __init__(self, user_data, subject_data):
        self.user_data = user_data
        self.subject_data = subject_data

@app.route('/', methods=['POST'])
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
                user_data = UserData(
                    username,
                    name_tag.find_next('td').text.strip(),
                    gender_tag.find_next('td').text.strip(),
                    university_id.find_next('td').text.strip()
                )
                subject_data = [SubjectData(subject.text.strip(), attendance.text.strip()) for subject, attendance in zip(subject_by_subs, attendance_by_subs)]
                user_data_dict = user_data.to_dict()
                subject_data_dicts = [subject.to_dict() for subject in subject_data]
                
                response_data = ResponseData(user_data_dict, subject_data_dicts)
                return jsonify(response_data.__dict__)
            except AttributeError:
                return jsonify({'error': 'Error parsing profile information.'}), 400
        else:
            return jsonify({'error': 'Error fetching profile or subject data.'}), 400
    else:
        return jsonify({'error': 'Login failed. Please check your credentials.'}), 400

if __name__ == '__main__':
    app.run()
