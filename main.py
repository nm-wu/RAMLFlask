from StringIO import StringIO
import datetime
import os
import sys
import shutil

from RAMLFlask.Server import Server
from RAMLFlask.Generator import Generator
from RAMLFlask.Comparison import Comparison

gen = Generator('./example.raml')
comp = Comparison()
Server(gen, comp).exec_all()

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
        gen = Generator(file)
        comp = Comparison()

        server = Server(gen, comp)
        server.generate()
        server.compare()

    results = []
    for i in range(100):
        t0 = datetime.datetime.now()
        gen = Generator(file)
        comp = Comparison()
        server = Server(gen, comp)
        t1 = datetime.datetime.now()

        server.generate(True, False)
        t2 = datetime.datetime.now()
        server.generate(False, True)
        t3 = datetime.datetime.now()
        server.compare(True, True, False)
        t4 = datetime.datetime.now()
        server.compare(False, False, True)
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
#timed_test("./RAML_files/uber/api.raml")
#timed_test("./RAML_files/slack/slack.raml")
#timed_test("./RAML_files/box/boxAPI.raml")
#timed_test("./RAML_files/slideshare/slideshare.raml")
#timed_test("./RAML_files/wordpress/wordpress.raml")
#timed_test("./RAML_files/flickr/flickr.raml")
#timed_test("./RAML_files/gmail/gmail.raml")
#timed_test("./RAML_files/grooveshark/grooveshark.raml")







