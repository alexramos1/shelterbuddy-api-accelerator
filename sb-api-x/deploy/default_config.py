import boto3
from os import getenv

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('sb-config')

table.put_item(
    Item = {
      "section": "rescue",
      "settings": [
        "Awaiting Behavior Completion",
        "Awaiting Behavior Retest",
        "Awaiting Behavioral Assessment",
        "Awaiting Foster",
        "Awaiting Sort",
        "Awaiting Spay Check",
        "Awaiting Spay/Neuter",
        "Awaiting Surgery - Not Spay/Neuter",
        "Awaiting Triage Completion",
        "Awaiting Triage",
        "Awaiting Vet Exam / Health Check",
        "Hold Intervention"
      ]
    })
    
table.put_item(
    Item = {
      "section": "ShelterBuddyConnection",
      "settings": {
            "SHELTERBUDDY_API_URL": getenv("SHELTERBUDDY_API_URL"),
            "SHELTERBUDDY_API_USER": getenv("SHELTERBUDDY_API_USER"),
            "SHELTERBUDDY_API_PASSWORD": getenv("SHELTERBUDDY_API_PASSWORD")
      }
    })
    
