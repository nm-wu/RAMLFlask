from FlaskRAML import RAMLFlask
from StringIO import StringIO
import datetime
import os
import sys
import shutil

RAMLFlask.Server("./example.raml").exec_all()

#RAMLFlask.Server("./RAML_files/github/github-api-v3.raml").exec_all() #http://api-portal.anypoint.mulesoft.com/github/api/github-api-v3/github-api-v3.raml
#RAMLFlask.Server("./RAML_files/instagram/instagram-api.raml").exec_all() #http://api-portal.anypoint.mulesoft.com/instagram/api/instagram-api/instagram-api.raml
#RAMLFlask.Server("./RAML_files/gmail/gmail.raml").exec_all() #http://api-portal.anypoint.mulesoft.com/onpositive/api/gmail-raml-api/gmail.raml
#RAMLFlask.Server("./RAML_files/uber/api.raml").exec_all() #https://github.com/raml-apis/Uber
#RAMLFlask.Server("./RAML_files/slack/slack.raml").exec_all() #https://github.com/raml-apis/Slack
#RAMLFlask.Server("./RAML_files/box/boxAPI.raml").exec_all() #https://github.com/raml-apis/Box
#RAMLFlask.Server("./RAML_files/slideshare/slideshare.raml").exec_all() #https://github.com/raml-apis/SlideShare
#RAMLFlask.Server("./RAML_files/grooveshark/grooveshark.raml").exec_all() #https://github.com/raml-apis/GrooveShark
#RAMLFlask.Server("./RAML_files/wordpress/wordpress.raml").exec_all() #https://github.com/raml-apis/Wordpress
#RAMLFlask.Server("./RAML_files/flickr/flickr.raml").exec_all() #https://github.com/raml-apis/Flickr

def timed_test(file):
    oldstdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    if os.path.exists('./delegates'):
        shutil.rmtree('./delegates')

    if os.path.exists('./routes'):
        shutil.rmtree('./routes')

    if os.path.exists('./generated'):
        shutil.rmtree('./generated')

    for i in range(100):
        server = RAMLFlask.Server(file)
        server.generate_code()
        server.bind_routes()
        server.static_analysis()
        server.test_analysis()

    results = []
    for i in range(100):
        t0 = datetime.datetime.now()
        server = RAMLFlask.Server(file)
        t1 = datetime.datetime.now()
        server.generate_code()
        t2 = datetime.datetime.now()
        server.bind_routes()
        t3= datetime.datetime.now()
        server.static_analysis()
        t4 = datetime.datetime.now()
        server.test_analysis()
        t5 = datetime.datetime.now()

        t1_0 = t1-t0
        t2_0 = t2-t0
        t3_0 = t3-t0
        t4_0 = t4-t0
        t5_0 = t5-t0

        vals = {
            't1_0': t1_0.total_seconds(),
            't2_0': t2_0.total_seconds(),
            't3_0': t3_0.total_seconds(),
            't4_0': t4_0.total_seconds(),
            't5_0': t5_0.total_seconds()
            }
        results.append(vals)

    averages = {
           't1_0': 0,
           't2_0': 0,
           't3_0': 0,
           't4_0': 0,
           't5_0': 0
        }
    for i in results:
        averages['t1_0'] += i['t1_0']
        averages['t2_0'] += i['t2_0']
        averages['t3_0'] += i['t3_0']
        averages['t4_0'] += i['t4_0']
        averages['t5_0'] += i['t5_0']

    averages['t1_0'] = averages['t1_0'] / len(results)
    averages['t2_0'] = averages['t2_0'] / len(results)
    averages['t3_0'] = averages['t3_0'] / len(results)
    averages['t4_0'] = averages['t4_0'] / len(results)
    averages['t5_0'] = averages['t5_0'] / len(results)

    output = out.getvalue().strip()
    sys.stdout = oldstdout

    print 'RESULTS: ' + file
    print 'T1: ' + str(round(averages['t1_0'],2))
    print 'T2: ' + str(round(averages['t2_0'],2))
    print 'T3: ' + str(round(averages['t3_0'],2))
    print 'T4: ' + str(round(averages['t4_0'],2))
    print 'T5: ' + str(round(averages['t5_0'],2))
    print '\n\n'

    if os.path.exists('./delegates'):
        shutil.rmtree('./delegates')

    if os.path.exists('./routes'):
        shutil.rmtree('./routes')

    if os.path.exists('./generated'):
        shutil.rmtree('./generated')


#timed_test("./RAML_files/github/github-api-v3.raml")
#timed_test("./RAML_files/instagram/instagram-api.raml")
#timed_test("./RAML_files/gmail/gmail.raml")
#timed_test("./RAML_files/uber/api.raml")
#timed_test("./RAML_files/slack/slack.raml")
#timed_test("./RAML_files/box/boxAPI.raml")
#timed_test("./RAML_files/slideshare/slideshare.raml")
#timed_test("./RAML_files/grooveshark/grooveshark.raml")
#timed_test("./RAML_files/wordpress/wordpress.raml")
#timed_test("./RAML_files/flickr/flickr.raml")







