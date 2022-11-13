from proof_of_possession.client import Client

from proof_of_possession.cloud import Cloud


def main():
    client = Client(z=200, ip="HOSTNAME", port=10)
    client.setup()
    client.read_file_store_as_Fr(filepath="block.txt")
    client.poly()
    T = client.tag_block()

    cloud = Cloud(ip="HOSTNAME", port=10)
    cloud.receive_tagged_block(T=T)

    H = client.gen_challenge()

    cloud.receive_challenge(H=H)
    P = cloud.gen_proof()

    client.receive_proof(P=P)
    print(client.check_proof())z


if __name__ == "__main__":
    main()
