from Patient import Patient
from Hospital import Hospital
import time


alice = Patient(5001, 'aliceCert.pem', 'aliceKey.pem', 'Alice')
bob = Patient(5002, 'bobCert.pem', 'bobKey.pem', 'Bob')
charlie = Patient(5003, 'charlieCert.pem', 'charlieKey.pem', 'Charlie')
hospital = Hospital(5004, 'hospitalCert.pem', 'hospitalKey.pem')

alice.run()
bob.run()
charlie.run()
hospital.run()

host_info = ('localhost', 5001, 'localhost', 5002, 'localhost', 5003)

alice.distribute_shares(*host_info)
bob.distribute_shares(*host_info)
charlie.distribute_shares(*host_info)

time.sleep(1)
print(f"Expected total amount of share Alice: {alice.secret}")
print(f"Expected total amount of share Bob: {bob.secret}")
print(f"Expected total amount of share Charlie: {charlie.secret}")

while True:
    pass