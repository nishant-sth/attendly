from src.database.config import supabase
import bcrypt

# Password Hashing
def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Password Validation
def validate_password(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

def check_teacher_exits(username):
    # check the unique username, return false when username already taken 
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
        }
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def login_teacher(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if validate_password(password, teacher['password']):
            return teacher
        return None
    
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(name, face_embedding=None, voice_embedding=None):
    data = {
        "name": name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code, 
        "name": name, "section": section, 
        "teacher_id": teacher_id
        }
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response = supabase.table("subjects").select("*, subject_students(count), attendence_logs(timestamp)").eq("teacher_id", teacher_id).execute()   
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions


        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects

def enroll_in_subject(subject_id, student_id):
    data = {
        'subject_id': subject_id,
        'student_id': student_id
    }
    response = supabase.table("subject_students").insert(data).execute()
    return response.data 

def unenroll_in_subject(subject_id, student_id):
    data = {
        'subject_id': subject_id,
        'student_id': student_id
    }
    response = supabase.table("subject_students").delete().eq("subject_id", subject_id).eq("student_id", student_id).execute()
    return response.data 

def get_student_subjects(student_id):
    response = supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

def get_student_attendence(student_id):
    response = supabase.table("attendence_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

def create_attendence(logs):
    response = supabase.table("attendence_logs").insert(logs).execute()
    return response.data