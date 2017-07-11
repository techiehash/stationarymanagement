import re
import json
import requests

while True:

    string = raw_input('>')
    input = string.split()
    actions = ['add', 'search', 'buy', 'trans']
    input1=raw_input("Enter url")

    if input[0] == actions[0]:
        string1 = actions[0]
        matches = re.search(r'(.*)of(.*)', string)
        group1 = matches.group(1)
        lwords = re.findall('^\w+(.*)', group1)
        ss = lwords[0]
        rspace = ss.strip()
        group2 = matches.group(2)
        list1 = []
        result = group2.split()

        for i in result:
            num = re.search('[0-9]*', i)
            matching = num.group()

            if i == matching:
                i = int(i)
                list1.append(i)
            else:
                list1.append(i)

        d = {}
        d[rspace] = dict(zip(list1[::2], list1[1::2]))
        jsondata = json.dumps(d)
        #url = 'http://127.0.0.1:5000/add'
        url=input1+'/add'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=jsondata, headers=headers)
        print r.content

    elif input[0] == actions[1]:
        ss = input[1]
        string1 = actions[1]
        rspace = ss.strip()
        res=string.split()
        length= len(res)
        if (length <= 2):
            d = {}
            d['pname'] = rspace
            jsondata = json.dumps(d)
           # url = 'http://127.0.0.1:5000/search'
            url = input1 + '/search'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=jsondata, headers=headers)
            data = r.content
            print data
        else:
            string1 = actions[1]
            matches = re.search(r'(.*)of(.*)', string)
            group1 = matches.group(1)
            lwords = re.findall('^\w+(.*)', group1)
            ss = lwords[0]
            rspace = ss.strip()
            group2 = matches.group(2)
            list1 = []
            result = group2.split()

            for i in result:
                num = re.search('[0-9]*', i)
                matching = num.group()

                if i == matching:
                    i = int(i)
                    list1.append(i)
                else:
                    list1.append(i)

            d = {}
            d[rspace] = dict(zip(list1[::2], list1[1::2]))
            jsondata = json.dumps(d)
            #url = 'http://127.0.0.1:5000/search'
            url=input1+'/search'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=jsondata, headers=headers)
            print r.content
    elif input[0] == actions[2]:
        string1 = actions[2]
        matches = re.search(r'(.*)of(.*)', string)
        group1 = matches.group(1)
        lwords = re.findall('^\w+(.*)', group1)
        ss = lwords[0]
        rspace = ss.strip()
        group2 = matches.group(2)
        list1 = []
        result = group2.split()

        for i in result:
            num = re.search('[0-9]*', i)
            matching = num.group()

            if i == matching:
                i = int(i)
                list1.append(i)
            else:
                list1.append(i)

        d = {}
        d[rspace] = dict(zip(list1[::2], list1[1::2]))

        jsondata = json.dumps(d)
      #  url = 'http://127.0.0.1:5000/buy'
        url = input1 + '/buy'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=jsondata, headers=headers)
        print r.content


    elif input[0] == actions[3]:
        string1 = actions[3]

        lwords = re.findall('^\w+(.*)', string)
        rspace = input[0].strip()
        d = {}
        #
        onlydata = lwords[0]

        list2 = onlydata.split()

        d[rspace] = dict(zip(list2[::2], list2[1::2]))

        jsondata = json.dumps(d)
        # print 'json data is {}'.format(jsondata)
        #url = 'http://127.0.0.1:5000/money'
        url = input1 + '/money'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=jsondata, headers=headers)
        print r.content

        data1 = data[1]
        list2 = []

        if type(data) == type(list2):
            for i in data1:
                for k, v in i.items():
                    print k, v
                print "\n"
            print "total net", data[0]
        else:
            print data