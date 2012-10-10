from ASAP.models import *

def get_university_list(request):
    database_manager = DatabaseManager()
    session = database_manager.get_session()
    universities = session.query(University).order_by(University.name)
    return dict(university_list=[university.to_dict() for university in universities])
