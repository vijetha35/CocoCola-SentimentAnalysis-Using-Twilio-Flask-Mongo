# CocoCola-SentimentAnalysis-Using-Twilio-Flask-Mongo

Package Requirement (Refer to requirements.txt) :
pymongo==3.6.1
Flask==0.12.1
Flask_PyMongo==0.5.1
twilio==6.0.0
requests==2.18.4

Running the project:

1.	Change to the project folder after downloading. 
cd CocaCola_DashBoard
2.	Ensure that the packages in the requirements.txt are installed.
3.	I am creating a reviewdb database and review as the Collection. All of these reside by default in /data/db folder for MongoDB. Run the MongoDB instance as follows:    	mongod
4.	Run the following command to run the flask application on localhost :        FLASK_APP=analysis_app.py flask run  
5.	Running the above command should display the following on the terminal.  * Serving Flask app "analysis_app"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
6.	I used ngrok to make the application work on localhost. Since I started the localhost on port 5000. I need to run ngrok as follows:   ./ngrok http 5000
7.	The above command gives the following output on the terminal. I copy the forwarding URL into my Twilio Webhook for messaging, so when a message comes in from the user the requests go to  forwarding URL appended with the callback URL handled in the flask application.  

ngrok by @inconshreveable                                         (Ctrl+C to quit)
                                                                                  
Session Status                online                                              
Session Expires               7 hours, 58 minutes                                 
Version                       2.2.8                                               
Region                        United States (us)                                  
Web Interface                 http://127.0.0.1:4040                               
Forwarding                    http://c0e775a0.ngrok.io -> localhost:5000          
Forwarding                    https://c0e775a0.ngrok.io -> localhost:5000         
                                                                                  
Connections                   ttl     opn     rt1     rt5     p50     p90         
                              0       0       0.00    0.00    0.00    0.00  

8.	Each of the steps above need to be followed for successful execution of the application.  
9.	I have registered the (818) 536-1153 in the Twilio Settings for Testing on your end.
10.	 You will need my Twilio account details for changing the ngrok URL (for receiving user messages). Do let me know if my credentials are required.

