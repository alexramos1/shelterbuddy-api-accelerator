AWS Solution Setup Steps
========================

1. Create Free account

2. Enable MFA and create individual IAM user

3. Setup an SNS topic "admin" in Oregon region (must be Oregon for SMS support).
   Switch back to North California region for all remaining steps.

4. Setup a Budget alert (e.g. $100/month projected spend), use SNS for notification

5. Create another IAM user, "deploy", with access restricted to Lambda, API Gateway, DynamoDB

6. Setup IAM roles: 
- sb-sync with AmazonDynamoDBFullAccess, CloudWatchLogsFullAccess
- sb-search with AmazonDynamoDBReadOnlyAccess

7. Create DynamoDB table "sb-sync":
- Table name: sb-sync, Primary Key: hashKey (String), everything else defaults.

8. Create DynamoDB table "sb-animals":
- Table name: sb-animals, Primary Key: Id (Number), uncheck "Use default settings", select "On-demand"
- Go to Indexes tab. "Create Index." Partition Key = StatusCategory. Add sort key "LocationKey". Save.
- Go to Indexes tab. "Create Index." Partition Key = StatusCategory. Add sort key "AnimalType". Save.
 
 9. Deploy AWS Lambda Functions:
 - Start a command shell
 - Set environment variables AWS_ACCOUNT, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
 - Execute: python deploy_sync_lambda.py
 - Execute: python deploy_search_lambda.py
 
 10. Go into the Environment section of the sb-sync Lambda, and set
   SHELTERBUDDY_API_URL, SHELTERBUDDY_API_USER, SHELTERBUDDY_API_PASSWORD
   
 11. Manually configure the 5-minute scheduler:
 - Go into the sb-sync Lambda definition, click Add Trigger, Cloudwatch Events
 - Under Configure Triggers, pick New Rule, sb-sync, "Every 5 Minutes", rate(5 minutes), Save, Save
 
 12. Create API Gateway mapping for sb-search:
 - Create -> REST -> New API. Set API Name "sb-x", description "Shelterbuddy Accelerator"
 - Actions -> Create Resource -> proxy resource: Yes (checked), name: search, path: {search+}, Enable CORS: Yes
 - Next, take all defaults, and set Lambda Function = sb-search
 - Next, Actions -> Deploy API -> [New Stage] -> "production"
 - Accept all defaults and hit Save Changes 
 