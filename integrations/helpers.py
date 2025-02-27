import requests

# Function to fetch courses from Moodle
def get_moodle_courses(moodle_url, api_key):
    url = f"{moodle_url}/webservice/rest/server.php"
    params = {
        'wstoken': api_key,
        'wsfunction': 'core_course_get_courses',
        'moodlewsrestformat': 'json',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Return the list of courses
    else:
        return None  # If there's an error, return None

# Function to fetch grades for a specific course
def get_moodle_grades(moodle_url, api_key, course_id):
    url = f"{moodle_url}/webservice/rest/server.php"
    params = {
        'wstoken': api_key,
        'wsfunction': 'gradereport_user_get_grades',
        'courseid': course_id,
        'moodlewsrestformat': 'json',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Return the grades for the course
    else:
        return None  # If there's an error, return None
