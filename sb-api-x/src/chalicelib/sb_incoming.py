# receive a new animal
from .shelterbuddy import ShelterBuddyConnection
from .database import Database
import boto3
import os

conn = ShelterBuddyConnection()
s3client = boto3.client('s3')
photoBucket = os.environ['S3_PHOTO_BUCKET']
db = Database()

def preparePhotos(animal):
    photos = conn.fetchPhotoLinks(animal['Id'])
    print('fetched photos: ' + str(photos))
    for photo in photos:
        sizes = [ 1024, 320 ]
        if('PhotoThumbnailFormat' in photo):
            photoFormat = photo['PhotoThumbnailFormat'].replace("<size>", "%d")
        else:
            photoFormat = photo['Photo'].replace('-jpg/1024---n', '-jpg/%d---n')

        del photo['Photo']
        del photo['PhotoThumbnailFormat']
        photo['Versions'] = []  

        for thSize in sizes:
            photoPath = photoFormat % thSize
            s3path = photoPath[1:]
            photoPayload = conn.fetchPhotoPayload(photoPath)
            s3client.put_object(ContentType='image/jpeg', Bucket=photoBucket, Key=s3path, Body=photoPayload)
            photo['Versions'].append({ str(thSize): photoPath })
            
    animal['Photos'] = photos

def process(animal):
    print('process: ' + str(animal))
    [1 for loop in conn.resolve(animal, 'Uri', lambda uri: conn.fetchUri(uri))]
    
    # inline and prefetch the photo urls
    preparePhotos(animal)
    
    # save to DynamoDB
    db.save(animal)
    
