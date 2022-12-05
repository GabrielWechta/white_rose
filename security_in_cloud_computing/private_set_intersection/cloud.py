from mcl_utils import get_Fr, get_G
from private_set_intersection.private_set_intersection_utils import GROUP


class Cloud:
    def __init__(self, g: GROUP, private_set: list):
        self.g = g
        self.exp = get_Fr()
        self.private_set = private_set

        self.mine_public_set = None
        self.party_public_set = None
        self.party_public_set_mine = None
        self.mine_public_set_party = None

    def produce_mine_public_set(self):
        mine_public_set = []
        for priv in self.private_set:
            g_hat = get_G(value=priv.encode(), group=GROUP)
            mine_public_set.append(g_hat * self.exp)

        self.mine_public_set = mine_public_set
        return mine_public_set

    def produce_party_public_set_mine(self):
        party_public_set_mine = []
        for party_pub in self.party_public_set:
            party_public_set_mine.append(party_pub * self.exp)
        self.party_public_set_mine = party_public_set_mine
        return party_public_set_mine

    def set_party_public_set(self, public_set_party: list):
        self.party_public_set = public_set_party

    def set_mine_public_set_party(self, mine_public_set_party: list):
        self.mine_public_set_party = mine_public_set_party

    def calculate_intersection(self):
        print(f"I have: {self.private_set}")
        print("We share:")
        for i, mps in enumerate(self.mine_public_set_party):
            for ps in self.party_public_set:
                if ps * self.exp == mps:
                    print(self.private_set[i])
