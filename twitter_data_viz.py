from import_lib import *

ent = ''
global all_hashtags_urls
all_hashtags_urls = []

# to fetch all the data in entities key of twitter json file
def getEntityData(entities_values, all_hashtags_urls,temp_dict):
    hash_tags = entities_values['hashtags']
    for i in hash_tags:
        for key in i:
        # print(key)
            if(key == 'text'):
                hs = i[key]
                # print("#"+hs)
                temp_dict['hashtags'] = hs.lower()
                all_hashtags_urls.append(temp_dict)
            else:
                pass
            
# to create json file of all hastags along with theit ids and created date 
def createJsonFile(all_hashtags_urls):
    with open("covidfiledata.json", "a") as out_file:
        for obj in all_hashtags_urls:    
            json.dump(obj, out_file)
            out_file.write('\n')   

# reading all json files
def main_function():
    for filecount in range(1,6):
        with jsonlines.open('data/covid{}.jsonl'.format(filecount)) as reader_js:    
            print('Name of file reading -----covid{}----'.format(filecount))
            try:
                for obj_json in reader_js:
                    try:
                        temp_dict = {}
                        for inx in obj_json:   
                            if(inx == 'created_at'):
                                temp_dict['created_at'] =  obj_json[inx]
                            elif(inx == 'id_str'):
                                temp_dict['id_str'] =  obj_json[inx]
                                # print(temp_dict)
                            elif(inx == 'entities'):
                                ent = obj_json[inx]
                                getEntityData(ent, all_hashtags_urls, temp_dict)
                            elif(inx == 'retweeted_status'):
                                retweet_data = obj_json[inx]['entities']
                                getEntityData(retweet_data, all_hashtags_urls, temp_dict)
                            else:
                                continue
                        # print("-----temperory crerated json-----", temp_dict, "------", all_hashtags_urls)
                    except Exception as e:
                        print("Oops Exception Found in innner loop ! ",e)
            except Exception as e:
                print("Oops exception  ! ",e)
    createJsonFile(all_hashtags_urls)
          
def twiter_data_visualizatino():
    try:
        ##################  Creating a pyspark session
        spark = SparkSession.builder.getOrCreate()
        #Importing Dataset
        df = spark.read.json('data/covidfiledata.json')
        df.registerTempTable("covidData")
        res = spark.sql("select count(*) from covidData")
        basic_q = "select count(*) from covidData where hashtags = "
        total_records = res.select("count(1)").collect()[0][0]
        res1 = spark.sql(basic_q+"'covid19'")
        res2 = spark.sql(basic_q+"'covid19pandemic'")
        res3 = spark.sql(basic_q+"'covidvaccination' or hashtags ='largestvaccinedrive' or hashtags ='vaccination'")
        res4 = spark.sql(basic_q+"'vaccinedeaths' or hashtags ='death'")
        res5 = spark.sql(basic_q+"'booster' or hashtags ='pfizer' or hashtags = 'covid19boostershot' or hashtags = 'covid19booster'")
        other_hastags = int(total_records) - (int(res1.select("count(1)").collect()[0][0]) + int(res2.select("count(1)").collect()[0][0]) + int(res3.select("count(1)").collect()[0][0]) + 
        int(res4.select("count(1)").collect()[0][0]) + int(res5.select("count(1)").collect()[0][0]))
        final_json = {
            "covid19" : res1.select("count(1)").collect()[0][0],
            "covid19pandemic" : res2.select("count(1)").collect()[0][0],
            "covidvaccination" : res3.select("count(1)").collect()[0][0],
            "vaccinedeaths" : res4.select("count(1)").collect()[0][0],
            "covid19booster" : res1.select("count(1)").collect()[0][0],
            "others" : other_hastags
            }
        xAxis = [key for key, value in final_json.items()]
        yAxis = [value for key, value in final_json.items()]
        plt.grid(True)
        ## LINE GRAPH ##
        plt.figure(figsize=(10,10),facecolor='#89c7da70') 
        plt.plot(xAxis,yAxis, color='maroon', marker='o')
        plt.xticks(rotation = 45,fontsize="15",color='maroon')
        plt.yticks(fontsize="15",color='maroon') 
        plt.rcParams['font.size'] = 18
        plt.xlabel('Name of Hashtags' ,fontsize="20",color='maroon')
        plt.ylabel('Count of Hashtags',fontsize="20",color='maroon')
        plt.title("Count of Hashtags by Name",color='maroon')
        plt.savefig('static/twitter_viz/twitter_viz.jpg', bbox_inches="tight")
        return 1
    except Exception as e:
        print(e)
        return 0
    
# print(twiter_data_visualizatino())