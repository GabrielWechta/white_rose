import random


class Channel:
    def __init__(self):
        self.slots = ["null"]
        self.leader_elected = False
        self.leader_id = None

    def beep(self, slot_ind: int, node_id: int):
        if self.slots[slot_ind] == "null":
            self.slots[slot_ind] = node_id
            self.leader_elected = True
            self.leader_id = node_id
        else:
            self.slots[slot_ind] = "collision"
            self.leader_elected = False
            self.leader_id = None

    def extend_slots(self):
        self.slots.append("null")

    def exists_single(self):
        return self.leader_elected

    def get_leader_id(self):
        return self.leader_id

    def describe(self):
        print(f"{self.slots=}")
        print(f"{len(self.slots)=}")
        print(f"{self.leader_id=}")


class Node:
    def __init__(self, node_id: int, channel: Channel, p_generator_ref):
        self.node_id = node_id
        self.channel = channel
        self.p_generator = p_generator_ref
        self.node_type = "normal"
        self.i = 0

    def election(self):
        p = next(self.p_generator)
        if random.random() <= p:
            # print(f"{self.i}:{self.node_id}")
            self.channel.beep(slot_ind=self.i, node_id=self.node_id)
        self.i += 1
