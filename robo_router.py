# robo_chat/robo_router.py

from robo_chat.robo_brain import RoboAdvisor

def handle_robo_question(user_profile, alerts_today, question):
    robo = RoboAdvisor(user_profile, alerts_today)
    return robo.answer(question)
