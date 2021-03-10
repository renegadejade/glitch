"""
Stores Data on Google Cloud
"""

from google.cloud import firestore

DB = firestore.Client()

SKILLS = []
skills_ref = DB.collection(("skills",)).stream()

for skill in skills_ref:
    SKILLS.append(skill.to_dict())
