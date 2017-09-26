from flask import Flask, request, jsonify
from pymongo import MongoClient
import time
import redis

app = Flask(__name__)
connection = MongoClient()
db = connection.inventory #database name.
collection = db['products'] # collection name.
collection1 = db['income']    # collection name

@app.route('/add',methods=['POST'])
def add():
      jsonadddata=request.get_json()
      d = {}
      for key, values in jsonadddata.items():
          d['pname'] = key
          for k, v in values.items():
              d[k] = v
      quantity=d['qty']
      del d['qty']
      if collection.find(d,{"_id":0}).count()>=1:
        d[u'qty']=quantity
        collection.update(d,{"$inc":{"qty":d['qty']}})
        result ="successfully added"
        return jsonify(result)
      else:
        d[u'qty'] = quantity
        collection.insert(d)
        result = "successfully added"
        return jsonify(result)

@app.route('/search',methods=['POST'])
def search():
     data = request.get_json()
    # list1=['color','company','price','qty']
    # list2=['company','pages','type','qty','price']

     print data
     now =  'company'  not in [x for v in data.values() for x in v]
    # now1 = list2   not in [x for v in data.values() for x in v]

     print now
   #  print now1
     if now==True:
            print "if block"
            result = list(collection.find(data,{"_id":0}))
     else:
            print "else block"
            d = {}
            for key,values in data.items():
                d['pname'] = key
            for k, v in values.items():
                d[k] = v
                result=list(collection.find(d,{"_id":0}))
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

    if d['pname'] == "book":
        s1 = list(collection.find({"type": d['type'],"pname":d['pname'],"company": d['company'],"price":d['price'],"pages":d['pages'],
                              "qty": {"$gte": d['qty']}}))
        if s1:
             collection.update({"pname": d['pname']}, {'$inc': {'qty': -d['qty']}})
             collection1.insert({"pname": d['pname'], "qty": d['qty'], "price": d['price'] * d['qty'], "date": a})

        else:
            result =list(collection.find({"pname":d['pname']},{"_id":0}))
            #return jsonify(result)
    else:
        s1=list(collection.find({"company": d['company'],"pname":d['pname'],"color":d['color'],"price":d['price'],
                              "qty": {"$gte": d['qty']}}))
        if s1:
            collection.update({"company": d['company']}, {'$inc': {'qty': -d['qty']}})
            collection1.insert({"pname": d['pname'], "qty": d['qty'], "price": d['price'] * d['qty'], "date": a})
            result = {"status": "ok"}
            #return jsonify(result)
        else:
            result =list(collection.find({"pname":d['pname']},{"_id":0}))

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
