import csv
import mysql.connector as connection

def insert_algerian_forest_Data(filename):

    try:
        myDb = connection.connect(host="localhost", port=5506, user="root", password="mysql", database="testDb",
                                  use_pure=True)

        with open(filename, "r") as data:
            print(data)
            readData = csv.reader(data, delimiter="\n")
            cursor = myDb.cursor()

            for result in readData:
                print(result)
                if result[0].count("Temperature") == 0:
                    splittedResult =  result[0].split(",")
                    splittedResult[0] = "'"+filename+"'"

                    fsresult = ""
                    for rs in splittedResult:
                        fsresult = fsresult+","+rs

                    fsresult = fsresult[1:]

                    print(
                        "INSERT INTO algerian_forest_classifier(filename,temperature,rh,ws,rain,ffmc,dc) VALUES ({data})".format(
                            data=(fsresult)))
                    cursor.execute(
                        "INSERT INTO algerian_forest_classifier(filename,temperature,rh,ws,rain,ffmc,dc) VALUES ({data})".format(
                            data=(fsresult)))
                    myDb.commit()

    except Exception as e:
        myDb.close()
        print(e)


def get_algerian_forest_Data(filename):
    try:
        fsResult=[]
        myDb = connection.connect(host="localhost", port=5506, user="root", password="mysql", database="testDb",
                                  use_pure=True)

        cursor = myDb.cursor()
        cursor.execute("select temperature,rh,ws,rain,ffmc,dc  from Algerian_forest_classifier where filename={filenamedata}".format(filenamedata="'"+filename+"'"))

        for result in cursor.fetchall():
            fsResult.append(list(result))

        myDb.close()

        return fsResult
    except Exception as e:
        myDb.close()
        print(e)