from unicodedata import name
from import_lib import *
from covid_viz import *
from twitter_data_viz import *
from sentimentAnalysis import *

app = Flask(__name__)
VIZ_FOLDER = os.path.join('', 'all_visualizations')
app.config['UPLOAD_FOLDER'] = VIZ_FOLDER 
file = open('model.pkl', 'rb')
clf = pickle.load(file)
file.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/covid_viz")
def covid_viz():
    try:
        rtn_value  = covid_viz_graphs()
        if rtn_value==1:
            hists = os.listdir('static/all_visualizations')
            hists = ['all_visualizations/' + file for file in hists]
            final_list = []
            for inx in range(len(hists)):
                templ = []
                templ.append(inx+1)
                templ.append(hists[inx])
                final_list.append(templ)
            # print(final_list)
            return render_template('all_visualizations.html', hists = final_list)
        else:
            return "No Graphs Found Error in Code"
    except Exception as e:
        print(e)
        return "No Graphs Found Error in Code"

@app.route("/twitter_viz")
def twitter_viz():
    try:
        rtn_value  = twiter_data_visualizatino()
        if rtn_value==1:
            hists = os.listdir('static/twitter_viz')
            hists = ['twitter_viz/' + file for file in hists]
            final_list = []
            for inx in range(len(hists)):
                templ = []
                templ.append(inx+1)
                templ.append(hists[inx])
                final_list.append(templ)
            return render_template('all_visualizations.html', hists = final_list)
        else:
            return "No Graphs Found Error in Code"
    except Exception as e:
        print(e)
        return "No Graphs Found Error in Code"

@app.route("/self_test")
def self_test():
        return render_template('covid_sekf_check.html')
    
@app.route('/self_chk_data', methods=["GET", "POST"])
def self_chk_data():
    try:
        if request.method == "POST":
            myDict = request.form
            fever = float(myDict['fever'])
            age = float(myDict['age'])
            pain = int(myDict['pain'])
            runnyNose = int(myDict['runnyNose'])
            diffBreath = int(myDict['diffBreath'])
            # Code for Inference
            inputFeatures = [fever, pain, age, runnyNose, diffBreath]
            infProb = clf.predict_proba([inputFeatures])[0][1]
            # print(infProb)
            return render_template('show_result.html', inf=round(infProb * 100))
        return render_template('index.html')
    except Exception as e:
        print(e)
        return "No Graphs Found Error in Code"
        
@app.route("/twitter_sentiments_page")
def twitter_sentiments_page():
        return render_template('sentiments.html')

@app.route('/twitter_sentiments', methods=["POST"])
def twitter_sentiments():
    try:
        limit   = request.form["count"]
        hashtags   = request.form["hash"]
        retrn_value = get_analysis(hashtags, int(limit)) 
        if retrn_value==1:
            hists = os.listdir('static/sentiment_analysis')
            hists = ['sentiment_analysis/' + file for file in hists]
            final_list = []
            for inx in range(len(hists)):
                templ = []
                templ.append(inx+1)
                templ.append(hists[inx])
                final_list.append(templ)
            return render_template('all_visualizations.html', hists = final_list)
        else:
            return {"status":0,"error":"No charts Found Error in Code!"}
    except Exception as e:
        print(e)
        return "No Graphs Found Error in Code"

@app.route('/feedback')
def feedback():
    return render_template('feedback_page.html')

@app.route('/feedbackform',methods=["POST"])
def feedbackform():
    try:
        username   = request.form["name"]
        useremail= request.form["email"]
        usermsg= request.form["message"]
        MONGO_URI = "mongodb+srv://dmishra:mizzou12345@cluster0.8jxtq.mongodb.net"
        myClient = pymongo.MongoClient(MONGO_URI)
        my_db = myClient["bigDataProject"]
        my_coll = my_db['feedback']
        my_coll.insert_one({"name": username, "mail": useremail, "message": usermsg, "insert_time": datetime.now()})
        return render_template('thankyou_page.html')
    except Exception as e:
        print(e)
        return render_template('thankyou_page.html')
    

if __name__ == "__main__":
    app.run(debug = True)
