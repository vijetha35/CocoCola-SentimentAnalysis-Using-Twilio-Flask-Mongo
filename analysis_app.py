from twilio.rest import Client
from flask import Flask, request,jsonify,render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
from pymongo import MongoClient 
from flask_pymongo import PyMongo
from twilio.rest import Client
import re

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'reviewdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/reviewdb'
mongo = PyMongo(app)

# we need not store all these templates for each user, and can compare if there were changes made in the UI for these templates, and only then store them in the DB, else 
# we could display the below message templates for the response messages. 
message_template ="Hi <firstName>, I saw that your <productType> was delivered. How are you enjoying it so far?"
negative_template="I'm sorry to hear that, what do you dislike about  <productType> ?"
positive_template="Great, can you describe what you love most about <productType> ?"

def sentiment_analysis(incoming_message):
	
	#my phone number :(872) 395-4226

	# Endpoint: https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0

	# Key 1: 9044f18aeabb4d9ba91e4e8812651cc4

	# Key 2: 7857d2e41d684842be1a76c2cb2217ef
	documents ={ 'documents': [ {'id': '1' , 'text' :incoming_message}]}
	subscription_key = '9044f18aeabb4d9ba91e4e8812651cc4'

	text_analytics_base_url='https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/'
	language_api_url =  text_analytics_base_url+'languages'
	headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
	response  = requests.post(language_api_url, headers=headers, json=documents)
	languages = response.json()
	language = languages['documents'][0]['detectedLanguages'][0]['iso6391Name']
	sentiment_api_url = text_analytics_base_url + "sentiment"
	headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
	response  = requests.post(sentiment_api_url, headers=headers, json=documents)
	sentiments = response.json()
	sentiment = sentiments['documents'][0]['score']
	return language, sentiment
@app.route("/")
def hello():
	# rendering the dashboard
	return render_template('dashboard.html')

@app.route('/send_survey_sms', methods=['POST', 'GET'])
def send_survey_sms():
	
	account_sid='ACdc25a68d904d95f374a05594bebff23d'
	auth_token = "2e0ecc40981108578a5d45ffddc2bb6b"
	client = Client(account_sid, auth_token)
	
	name =request.form['customerName']
	customer_number  =request.form['phoneNumber']
	product = request.form['options']
   	message_content = request.form["format"]
   	positive = request.form["positive"]
   	negative = request.form["negative"]
   	reviewTab= mongo.db.review
   	customer_number = re.sub("[()-]","",customer_number)
   	if customer_number.startswith("+") and customer_number[1]!='1':
   		customer_number= customer_number.replace("+","")
   	if not customer_number.startswith("+1"):
   		customer_number="+1"+customer_number
   	if reviewTab.find_one({'id': customer_number })==None:
   		reviewTab.insert_one({'name': name, "id": customer_number, "positive_template" :positive, "negative_template":negative,"message_template":message_content,"product":product})
   	else:
	   	reviewTab.update_one(
	        {"id": customer_number},
	        {
	        	"$set": {
	            "name":name,
	            "positive_template" :positive, 
	            "negative_template":negative,
	            "message_template":message_content,
	            "product" :product
	        	}
	        }
	    )
	print name, customer_number, product, message_content, positive, negative

	
	company_number = "+18723954226"

	message_content = message_content.replace("<firstName>", name)
	message_content = message_content.replace("<productType>", product)

	message = client.messages.create(to=customer_number, body= message_content, from_=company_number)
	
	template ={

		'sid' :message.sid,
		'name':name
	} 
	return render_template('dashboard.html', **template)

@app.route('/respond_survey', methods=['POST'])
def respond_survey():
	
 	number = request.form['From']
 	message_body = request.form['Body']
 	
 	language, sentiment = sentiment_analysis(message_body)
  	resp = MessagingResponse()
  
  	
  	reviewTab= mongo.db.review
	messageText =""
	result = reviewTab.find_one({'id':number})
	
	if sentiment > 0.5:
		print "result positive" ,result, " template ",result['positive_template']
		messageText = result['positive_template']
  	else:
  		result = reviewTab.find_one({'id':number})
  		print "result negative" ,result, " template ",result['negative_template']
  		messageText = result['negative_template']

  	product = result['product']
  	messageText = messageText.replace("<productType>",product)
  	
  	name = result['name']
  	messageText = messageText.replace("<firstName>", name)
  	resp.message(messageText)
  	
   	return str(resp)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 5000)
