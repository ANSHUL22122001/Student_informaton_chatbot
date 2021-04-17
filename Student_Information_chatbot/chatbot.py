from flask import Flask, render_template, request, jsonify
from assistant import check
import os



app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/chat", methods=['GET', 'POST'])
def chat():
	user_query = request.json
	user_query = user_query['name']
	result = check(user_query)

	file = open('voice.txt','w')
	newresult=""
	cond=True
	
	if '</a>' in result:
		for i in result:
			if cond and i!='<':
				newresult=newresult+i
			if i == '<':
				cond=False
			if i == '>':
				cond=True
	else:
		newresult=result
			
 
	newresult=newresult.replace("It’s","It\'s") 
	newresult=newresult.replace(">"," then click on ")
	newresult=newresult.replace("CUBOT","CU BOT")
	newresult=newresult.replace("AI","A.I.")      
	file.write(newresult)
	file.close()
	os.system("python3 voice.py &")

	return jsonify(result)
    
    


if __name__ == "__main__":
    app.run(debug=True)
