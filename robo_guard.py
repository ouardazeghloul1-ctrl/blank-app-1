# robo_chat/robo_guard.py

class RoboGuard:
    def __init__(self, package):
        self.package = package

    def allow(self, level):
        hierarchy = {
            "مجانية": 1,
            "فضية": 2,
            "ذهبية": 3,
            "ماسية": 4,
            "ماسية متميزة": 5
        }
        return hierarchy.get(self.package, 1) >= hierarchy[level]
