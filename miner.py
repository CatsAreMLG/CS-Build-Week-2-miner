import hashlib
import requests
import json

import sys


def proof_of_work(last_proof, difficulty):
    proof = 0
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1
    return proof


def valid_proof(last_proof, proof, difficulty):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:difficulty] == '0'*difficulty


if __name__ == '__main__':
    if len(sys.argv) > 1:
        token = sys.argv[1]
    else:
        token = input("Enter your Auth Token: ")
    node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    coins_mined = 0

    while True:
        res = requests.get(node + '/last_proof',
                           headers={'Authorization': f'Token {token}'}).json()
        last_proof = res['proof']
        difficulty = res['difficulty']

        print('last_proof: ', last_proof)

        print('difficulty: ', difficulty)

        new_proof = proof_of_work(last_proof, difficulty)
        print('proof: ', new_proof)

        mined = requests.post(node + '/mine',
                              headers={'Authorization': f'Token {token}'},
                              json={"proof": new_proof})

        print('mined: ', mined.json())

        balance = requests.get(node + '/get_balance',
                               headers={'Authorization': f'Token {token}'}).json()

        print('balance: ', balance)
