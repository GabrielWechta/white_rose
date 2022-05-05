class Attacker:
    def __init__(self):
        pass

    @staticmethod
    def produce_stage_one_messages():
        stage_one_messages = []
        for i in range(3):
            stage_one_messages.append(i.to_bytes(16, 'big'))

        return stage_one_messages
