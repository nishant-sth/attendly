import dlib
import numpy as np
from sklearn.svm import SVC
import face_recognition_models
import streamlit as st
from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    # Shape predictor
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    # Face recognition
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_image_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 2)

    embeddings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 2) # 128D features embeddings
        embeddings.append(np.array(face_descriptor))

        return embeddings

@st.cache_resource    
def get_train_model():
    X = [] # embedding of all students
    y = [] # student_ids

    student_db = get_all_students()
    
    if student_db:
        for student in student_db:
            embedding = student.get("face_embedding")
            X.append(np.array(embedding))
            y.append(student.get("student_id"))
    
    if len(X) == 0:
        return None
    
    # classification model
    model = SVC(kernel="linear", probability=True, class_weight='balanced')

    try:
        model.fit(X, y)
    except ValueError:
        pass
    
    data = {
        'model': model, 
        'X': X, 
        'y':y
        }
    
    return data

def train_model():
    st.cache_resource.clear()
    model_data = get_train_model()

    return bool(model_data)

def predict_attendence(class_image_np):
    embeddings = get_image_embeddings(class_image_np)

    detected_students = {}
    model_data = get_train_model()

    if not model_data:
        return detected_students, [], len(embeddings)
    
    model = model_data['model']
    X_train = model_data['X']
    y_train = model_data['y'] # ids of the student

    all_students = sorted(set(y_train))

    for embedding in embeddings:
        if len(all_students) >= 2:
            predicted_id = int(model.predict([embedding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[y_train.index(predicted_id)]

        resemblance_thresold = 0.6
        best_match_score = np.linalg.norm(student_embedding - embedding)
        
        if best_match_score <= resemblance_thresold:
            detected_students[predicted_id] = True
    return detected_students, all_students, len(embeddings)

