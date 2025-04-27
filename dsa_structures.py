#This class implements a basic queue structure for storing and managing appointment time slots.
class TimeSlotQueue:
    def __init__(self):
        self.queue = []

    def add_slot(self, slot):
        self.queue.append(slot)

    def get_slot(self):
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def reset_slots(self, slots):
        self.queue = slots