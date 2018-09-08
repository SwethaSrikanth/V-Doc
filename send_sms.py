from flask import Flask, request, session
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
import urllib2
from BeautifulSoup import BeautifulSoup
from getDrugForDisease import getDrugForDisease, getDrugStoresAndPrice, getDrugPrices
from sklearn.externals import joblib
from model import getDisease

def getCityLocation(number):
    npa = number[2:5]
    nxx = number[5:8]
    thoublock = number[8:]
    link = 'http://www.fonefinder.net/findome.php?npa='+npa+'&nxx='+nxx+'&thoublock='+thoublock+'&usaquerytype=Search+by+Number&cityname='
    page = urllib2.urlopen(link)
    soup = BeautifulSoup(page)
    table = soup.findAll("table",{"border":"3"})
    cols = table[0].findAll("td")
    a_city = cols[2].findAll("a")
    a_state = cols[3].findAll("a")
    a_city = str(a_city[0]).split(">")
    a_state = str(a_state[0]).split(">")
    a_city = a_city[1]
    a_state = a_state[1]
    city = a_city[:-3]
    state = a_state[:-3]
    return city, state

'''
def getDisease(test_list):
    filename = 'final_model.sav'
    loaded_model = joblib.load(filename)
    result = loaded_model.predict([test_list])
    print(result)
    return result[0]
'''


SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)
work_flow = []
print(work_flow)

@app.route('/sms', methods=['GET','POST'])

def sms():
    counter = session.get('counter', 0)
    work_flow = session.get('work_flow', [])
    counter += 1
    session['counter'] = counter
    resp = MessagingResponse()

    print counter
    if counter == 1:
        #resp = MessagingResponse()
        number = request.form['From']
        city, state = getCityLocation(number)
        print "counter is 1"
        resp.message('Hello There! Welcome to Virtual Doc. Hope the weather is great at ' + city + ' ' + state + '. If you know your disease press 1 or else press 2')
        return str(resp)
    elif counter == 2:
        #work_flow = []
        message_body = request.form['Body']
        print "counter is 2"
        if message_body == '1':
            resp.message("Tell me your disease and I will give you the medication")
            work_flow.append(1)
        else:
            work_flow.append(2)
            resp.message("Let me diagnose you! Let's get a bit more specific. \n Press 1 if you have you any discomfort in your chest. \n Press 2 if you have any body pain. \n Press 3 if you are experiencing pain in your head.")
        session['work_flow'] = work_flow
        print work_flow
        return str(resp)
    elif counter == 3:
        #work_flow.append(2)
        if work_flow[-1] == 2:
            message_body = request.form['Body']
            if message_body == '1':
                work_flow.append(1)
                print 'Inside 1'
                resp.message("Don't worry I'll solve your problem, just answer the below questions with a number between 0 to 5. With 5 being severe. \n 1) Severity of Acid Flux? \n 2) Difficulty to swallow \n 3) Severity of wheezing \n 4) Severity of rapid breathing \n 5) Severity of restlessness \n 6) Severity of panic \n Keep a space between each value. Ex - 5 1 0 0")
            elif message_body == '2':
                work_flow.append(2)
                resp.message("Don't worry I'll solve your problem, just answer the below questions with a number between 0 to 5. With 5 being severe. \n 1) Severity of Running Nose? \n 2) Severity of tiredness \n 3) Severity of Vomiting \n 4) Severity of muscle soreness \n 5) Severity of getting chills \n 6) Severity of body temperature \n 7) Severity of nauseous \n Keep a space between each value. Ex - 5 1 0 0")
                print 'Inside 2'
            else:
                work_flow.append(3)
                resp.message("Don't worry I'll solve your problem, just answer the below questions with a number between 0 to 5. With 5 being severe. \n 1) Severity of pain on one side of your head \n 2) Is the pain intense? - 0 for No or 1 for Yes \n 3) Is the pain mild? - 0 for No or 1 for Yes \n 4) Severity of pain on all parts of your head \n Keep a space between each value. Ex - 5 1 0 0")
                print 'Inside 3'
        else:
            message_body = request.form['Body']
            drug_name_store_price_map = getDrugStoresAndPrice(message_body)
            #print drug_name_store_price_map
            final_str = ''
            for each_drug in drug_name_store_price_map.keys():
                store_name, price = drug_name_store_price_map[each_drug]
                make_str = each_drug + ': '
                new_str = ''
                for i in range(0, 4): #len(store_name)
                    new_str += store_name[i] + ' : ' + price[i] + ", "
                make_str +=  new_str
                final_str += make_str + ", "
            print(final_str)
        #resp = MessagingResponse()
            resp.message('Drugs that you can use ' + final_str + " " + str(counter))
            #session.close()
        session['work_flow'] = work_flow
        print work_flow
        return str(resp)
    elif counter == 4 and len(work_flow) == 2:
        message_body = request.form['Body']
        print(message_body)
        message_body = message_body.split(" ")
        if work_flow[-1] == 1:
            test_list = [message_body[0], message_body[1], message_body[2], message_body[3], message_body[4], message_body[5], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif work_flow[-1] == 2:
            test_list = [0, 0, 0, 0, 0, 0, message_body[0], message_body[1], message_body[2], message_body[3], message_body[4], message_body[5], message_body[6], 0, 0, 0, 0]
        else:
            test_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, message_body[0], message_body[1], message_body[2], message_body[3]]
        disease = getDisease(test_list)
        print disease
        drug_name_store_price_map = getDrugStoresAndPrice(disease)
        #print drug_name_store_price_map
        final_str = ''
        for each_drug in drug_name_store_price_map.keys():
            store_name, price = drug_name_store_price_map[each_drug]
            make_str = each_drug + ': '
            new_str = ''
            for i in range(0, 4): #len(store_name)
                new_str += store_name[i] + ' : ' + price[i] + ", "
            make_str +=  new_str
            final_str += make_str + ", "
        print(final_str)
    #resp = MessagingResponse()
        resp.message('Oh Shit! You have '+ disease +'. Drugs that you can use ' + final_str + " " + str(counter))
        #resp.message('')
        return str(resp)
    else:
        session['counter'] = 0
        counter = 0
        session['work_flow'] = []
        resp.message('Bye')
        #session.close()
        return str(resp)

    #return str(resp)

if __name__ == '__main__':
    app.run()
