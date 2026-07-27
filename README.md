# Attendly

Attendly is an AI-assisted attendance management platform built with Streamlit. It is designed to simplify classroom attendance by combining facial recognition, optional voice verification, subject management, and attendance reporting in a single web application.

## Project Overview

Attendly supports two user roles:

- Teachers can create subjects, manage student enrollments, share subject access codes, capture attendance using images or voice, and review attendance records.
- Students can register through face-based authentication, enroll in classes, and monitor their attendance progress.

The platform is intended for education environments where attendance needs to be faster, more consistent, and easier to manage.

## Core Functionality

### Teacher Features
- Teacher registration and login
- Create and manage subjects
- Share subject join codes for student enrollment
- Capture attendance from classroom photos
- Perform voice-based attendance checks
- Review summarized attendance records for each subject

### Student Features
- Face-based student login
- Optional voice enrollment during account creation
- Enroll in subjects using a subject code
- View enrolled subjects and attendance statistics
- Unenroll from subjects when needed

### AI and Automation Features
- Face recognition based attendance using embedding-based matching
- Optional voice embedding and speaker verification
- Automatic subject enrollment through join links or join codes
- Attendance results presented in a review dialog before final submission

## Technology Stack

- Python
- Streamlit
- Supabase for backend data storage
- NumPy and Pandas for data handling
- Pillow for image processing
- scikit-learn for model training
- dlib and face_recognition_models for face recognition
- librosa, resemblyzer, and webrtcvad for voice-based features
- bcrypt for password hashing
- segno for QR-related subject sharing

## Project Structure

- app.py: Main application entry point
- src/screens: User-facing screens for home, teacher, and student flows
- src/components: UI dialogs, cards, and reusable interface elements
- src/pipelines: Face recognition and voice processing pipelines
- src/database: Supabase connection and database access logic
- src/ui: Shared styling and layout components

## Database Model

The application uses Supabase tables for:

- teachers
- students
- subjects
- subject_students
- attendence_logs

The schema definition is available in src/database/db_tables.sql.

## Setup Instructions

### Prerequisites
- Python 3.10 or newer
- A working Supabase project
- A Windows-compatible environment for the face recognition dependencies

### Installation
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Configuration
Create a Streamlit secrets file at .streamlit/secrets.toml with the following structure:

```toml
[secrets]
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_key"
```

### Run the Application

```bash
streamlit run app.py
```

## Application Workflow

### Teacher Workflow
1. Register or log in as a teacher.
2. Create one or more subjects.
3. Share the subject code with students.
4. Use the attendance tab to add classroom images.
5. Run face analysis and review the generated attendance list.
6. Confirm the attendance records for storage.

### Student Workflow
1. Open the student portal.
2. Register a face profile, optionally adding a voice profile.
3. Enroll in subjects using a subject code.
4. Access the dashboard to view enrolled courses and attendance history.

## Notes for Contributors

- The application uses Streamlit session state for short-term UI state management.
- AI recognition performance depends on image quality, lighting, and the quality of enrolled face data.
- The project is designed for extension, including improved attendance analytics, more robust voice matching, and role-based reporting.

## License

This project is intended for educational and demonstration purposes. Please review and adjust licensing terms before production deployment.
