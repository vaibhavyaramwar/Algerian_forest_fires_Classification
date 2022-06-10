from flask import Flask,request,jsonify,render_template
import pickle
import sklearn
import pandas as pd
import json

from Forest import Forest
import Db_ops as db

app = Flask(__name__)
model = pickle.load(open("model.pkl","rb"))

@app.route("/predict",methods=["POST"])
def predict_api():
    print(request.json['data'])
    data=request.json['data']
    print(data)
    newdata = [list(data.values())]
    output = model.predict(newdata)[0]
    return jsonify(str(output))


@app.route("/predictbulk",methods=["POST"])
def predict_bulk_api():
    try:
        results=[]
        filedata = request.files["file"]
        filedata.save(filedata.filename)
        if filedata.content_type == "text/csv":
            db.insert_algerian_forest_Data(filedata.filename)
            resultData = db.get_algerian_forest_Data(filedata.filename)
            print(resultData)
           # df=pd.read_csv(filedata.filename)
            try:
                y_pred=model.predict(resultData)

                y_pred = y_pred.astype(str)
                for i in range(len(y_pred)):
                    if y_pred[i] == 0:
                        y_pred[i] = "Not Fire"
                    else:
                        y_pred[i] = "Fire"
                    forest = Forest(str(resultData[i][0]), str(resultData[i][1]),
                                    str(resultData[i][2]), str(resultData[i][3]),
                                    str(resultData[i][4]), str(resultData[i][5]),
                                    str(y_pred[i]))
                    results.append(json.dumps(forest.__dict__))
                return jsonify(results)
            except Exception as e:
                return "Invalid File Format , check the fields in the file ones , also check the logs for file name : "+filedata.filename
        else:
            return "Invalid File Format Extension"
    except Exception as e:
        print(e)
        return "Exception occured while processing the file , kindly check error log for file name : "+filedata.filename

if __name__ == "__main__":
    app.run(debug=True)