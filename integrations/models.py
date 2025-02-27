from django.db import models
from polymorphic.models import PolymorphicModel  
from organisation.models import Organisation
import requests
from django.utils.timezone import now

class Integration(PolymorphicModel):
    id = models.BigAutoField(primary_key=True)  
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="integrations")
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} (v{self.version}) - {'Enabled' if self.enabled else 'Disabled'}"
    
class MoodleIntegration(Integration):
    moodle_url = models.URLField()  
    api_key = models.CharField(max_length=255)  
    last_sync = models.DateTimeField(auto_now=True)  # Track last sync time

    def __str__(self):
        return f"Moodle Integration for {self.organisation.name}"

    def fetch_courses(self):
        """Fetch and store courses from Moodle"""
        url = f"{self.moodle_url}/webservice/rest/server.php"
        params = {
            "wsfunction": "core_course_get_courses",
            "moodlewsrestformat": "json",
            "wstoken": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            courses_data = response.json()
            for course_data in courses_data:
                MoodleCourse.objects.update_or_create(
                    moodle_integration=self,
                    course_id=course_data["id"],
                    defaults={
                        "name": course_data["fullname"],
                        "shortname": course_data["shortname"],
                        "category_id": course_data["categoryid"]
                    }
                )
        return MoodleCourse.objects.filter(moodle_integration=self)

    def fetch_grades(self, user_id):
        """Fetch and store grades for a specific student"""
        url = f"{self.moodle_url}/webservice/rest/server.php"
        params = {
            "wsfunction": "gradereport_user_get_grade_items",
            "moodlewsrestformat": "json",
            "wstoken": self.api_key,
            "userid": user_id
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            grades_data = response.json()
            for grade_item in grades_data.get("usergrades", []):
                for item in grade_item["gradeitems"]:
                    MoodleGrade.objects.update_or_create(
                        moodle_integration=self,
                        user_id=user_id,
                        course_id=item["courseid"],
                        defaults={
                            "item_name": item["itemname"],
                            "grade": item["graderaw"],
                            "max_grade": item["grademax"]
                        }
                    )
        return MoodleGrade.objects.filter(moodle_integration=self, user_id=user_id)

class MoodleCourse(models.Model):
    """Store courses fetched from Moodle"""
    moodle_integration = models.ForeignKey(MoodleIntegration, on_delete=models.CASCADE, related_name="courses")
    course_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=100)
    category_id = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.shortname})"

class MoodleGrade(models.Model):
    """Store grades fetched from Moodle"""
    moodle_integration = models.ForeignKey(MoodleIntegration, on_delete=models.CASCADE, related_name="grades")
    user_id = models.IntegerField()  # ID of the student
    course = models.ForeignKey(MoodleCourse, on_delete=models.CASCADE, related_name="grades")
    item_name = models.CharField(max_length=255)
    grade = models.FloatField(null=True, blank=True)
    max_grade = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Grade for {self.item_name}: {self.grade}/{self.max_grade} (User {self.user_id})"
