class EventModel:
    def __init__(self, id, name, date, time, location, description):
        self.id = id
        self.name = name
        self.date = date
        self.time = time
        self.location = location
        self.description = description

class CalendarModel:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events

    def delete_event(self, event):
        self.events.remove(event)

    def update_event(self, event, name, date, time, location, description):
        event.name = name
        event.date = date
        event.time = time
        event.location = location
        event.description = description