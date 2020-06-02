import boto3
import sys
import datetime

sqs = boto3.client('sqs')

from_q_name = sys.argv[1]
to_q_name = sys.argv[2]
print("From: " + from_q_name + " To: " + to_q_name)

from_q = sqs.get_queue_url(QueueName=from_q_name)['QueueUrl']
to_q = sqs.get_queue_url(QueueName=to_q_name)['QueueUrl']

while messages := sqs.receive_message(QueueUrl=from_q, AttributeNames=['SentTimestamp']).get('Messages',[]):
    for message in messages:
        ts = datetime.datetime.utcfromtimestamp(int(message['Attributes']['SentTimestamp']) / 1000)
        print('Moving MessageID=%s, MD5=%s, Timestamp=%s' % (message['MessageId'], message['MD5OfBody'], ts))
        sqs.send_message(QueueUrl=to_q, MessageBody=message['Body'])
        sqs.delete_message(QueueUrl=from_q, ReceiptHandle=message['ReceiptHandle'])
