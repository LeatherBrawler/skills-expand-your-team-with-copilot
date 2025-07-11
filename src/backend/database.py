"""
MongoDB database configuration and setup for Mergington High School API
"""

from pymongo import MongoClient
from argon2 import PasswordHasher

# Try to connect to MongoDB, use mock if not available
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    # Test the connection
    client.admin.command('ismaster')
    db = client['mergington_high']
    activities_collection = db['activities']
    teachers_collection = db['teachers']
    USE_MONGODB = True
    print("Using MongoDB")
except Exception as e:
    print(f"MongoDB not available ({e}), using mock database for testing")
    USE_MONGODB = False
    
    # Simple mock collection class
    class MockCollection:
        def __init__(self, initial_data):
            self.data = {}
            for name, details in initial_data.items():
                self.data[name] = details
        
        def find(self, query=None):
            if query is None:
                # Return all documents with _id
                result = []
                for name, doc in self.data.items():
                    result.append({"_id": name, **doc})
                return result
            
            # Simple filtering for testing
            result = []
            for name, doc in self.data.items():
                match = True
                
                # Check difficulty filter
                if "difficulty" in query:
                    if "$exists" in query["difficulty"]:
                        if query["difficulty"]["$exists"] == False:
                            if "difficulty" in doc:
                                match = False
                        else:
                            if "difficulty" not in doc:
                                match = False
                    else:
                        if doc.get("difficulty") != query["difficulty"]:
                            match = False
                
                # Check day filter
                if "schedule_details.days" in query and "$in" in query["schedule_details.days"]:
                    target_day = query["schedule_details.days"]["$in"][0]
                    if target_day not in doc.get("schedule_details", {}).get("days", []):
                        match = False
                
                if match:
                    result.append({"_id": name, **doc})
            
            return result
        
        def count_documents(self, query):
            return len(self.find(query))
        
        def find_one(self, query):
            results = self.find(query)
            return results[0] if results else None
        
        def insert_one(self, doc):
            # Simplified insert
            pass
        
        def update_one(self, query, update):
            # Simplified update
            class MockResult:
                modified_count = 1
            return MockResult()
    
    activities_collection = MockCollection({})
    teachers_collection = MockCollection({})

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""
    
    if USE_MONGODB:
        # Initialize activities if empty
        if activities_collection.count_documents({}) == 0:
            for name, details in initial_activities.items():
                activities_collection.insert_one({"_id": name, **details})
                
        # Initialize teacher accounts if empty
        if teachers_collection.count_documents({}) == 0:
            for teacher in initial_teachers:
                teachers_collection.insert_one({"_id": teacher["username"], **teacher})
    else:
        # Initialize mock database
        activities_collection.data = initial_activities.copy()
        
        # Initialize mock teachers
        teacher_data = {}
        for teacher in initial_teachers:
            teacher_data[teacher["username"]] = teacher.copy()
        teachers_collection.data = teacher_data

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "difficulty": "Beginner"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures, heartwarming friendships, and incredible worlds through Japanese manga! From action-packed shounen to slice-of-life stories, discover amazing characters and stunning artwork that will transport you to new realms of imagination.",
        "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:00"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]

