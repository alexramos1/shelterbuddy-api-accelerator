from shelterbuddy import ShelterBuddyConnection
import sys

conn = ShelterBuddyConnection()

path = '/storage/image/7411ba69e4984436ab9b9cbc52c66b1a-1554419868-1554419887-jpg/1024---n'

img = conn.fetchPhotoPayload(path)

with open(sys.argv[1], 'wb') as f:
        f.write(img)