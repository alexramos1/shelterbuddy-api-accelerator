from chalicelib.shelterbuddy import ShelterBuddyConnection

conn = ShelterBuddyConnection()

path = '/storage/image/7411ba69e4984436ab9b9cbc52c66b1a-1554419868-1554419887-jpg/128---n'

img = conn.fetchPhotoPayload(path)

with open("test_utils-img-result.jpg", 'rb') as f:
        ref = f.read()
        
if not(ref == img):
    raise "not equal"
else:
    print("ok: the bytes are equal")