from flask import Flask, request, jsonify
from pymongo import MongoClient
import time

app = Flask(__name__)
connection = MongoClient()
db = connection.inventory #database name.
collection = db['products'] # collection name.
collection1=db['income']

@app.route('/add',methods=['POST'])
def add():
      jsonadddata=request.get_json()
      print jsonadddata
      d = {}
      for key, values in jsonadddata.items():
          d['pname'] = key
          for k, v in values.items():
              d[k] = v
      print d['pname']

      if d['pname']=='book':
          if collection.find({"title": d['title'],"price": d['price'],
                              "pages": d['pages'],"type":d['type']}).count() >= 1:
              collection.update({"qty": d['qty']}, {"$inc": {"qty": d['qty']}})
              result = {"status": "updated"}
              return jsonify(result)
          else:
              collection.insert(d)
              result = {"status": "inserted"}
              return jsonify(result)
      else:
        if collection.find({"company":d['company'],"pname":d['pname'],"color":d['color'],"price":d['price']}).count()>=1:
           collection.update({"company":d['company']},{"$inc":{"qty":d['qty']}})
           result={"status":"updated"}
           return jsonify(result)
        else:
          collection.insert(d)
          result={"status":"inserted"}
          return jsonify(result)

@app.route('/search',methods=['POST'])
def search():
     data = request.get_json()
     now='company'  not in [x for v in data.values() for x in v]
     now1='title' not in [x for v in data.values() for x in v]

     pname=data.values()[0]
     print now

     if now==True and now1==True:
            result = list(collection.find(data,{"_id":0}))
            return jsonify(result)
     else:
            d = {}
            for key, values in data.items():
                d['pname'] = key
            for k, v in values.items():
                d[k] = v

                print d

                result=list(collection.find(d,{"_id":0}))
                print result
                return jsonify(result)

@app.route('/buy',methods=['POST'])
def buy():
    data = request.get_json()
    d = {}
    for key, values in data.items():
        d['pname'] = key
        for k, v in values.items():
            d[k] = v

    a = time.strftime('%Y-%m-%d')
    buyupdate = collection.update({"pname": d['pname']}, {'$inc': {'qty': -d['qty']}})
    buyinsert = collection1.insert({"pname": d['pname'], "qty": d['qty'], "price": d['price'] * d['qty'], "date": a})

    if d['pname'] == "book":
        s1 = collection.find({"author": d['author'], "pname": d['pname'], "title": d['title'], "price": d['price'],
                              "qty": {"$gte": d['qty']}})
        if s1:
            buyupdate
            buyinsert
            result = {"status": "ok"}
            return jsonify(result)
        else:
            result = "no available items"
            return jsonify(result)

    else:
        s1 = collection.find({"company": d['company'], "pname": d['pname'], "color": d['color'], "price": d['price'],
                              "qty": {"$gte": d['qty']}})
        if s1:
            buyupdate
            buyinsert
            result = {"status": "ok"}
            return jsonify(result)
        else:
            result = "no available items"
            return jsonify(result)


@app.route('/money',methods=['POST'])
def money():
      f=request.get_json()
      a = time.strftime('%Y-%m-%d')

      s=f.values()[0]


      s1=list(collection1.find(s,{"_id":0}))
      if s1:
          prices_sum = 0
          for i in range(0,len(s1)):
                prices_sum += s1[i]['price']
          return jsonify(prices_sum,s1)

      else:
          result="no transactions today"
          return jsonify(result)

if __name__ == '__main__':
   app.run(debug = True)


