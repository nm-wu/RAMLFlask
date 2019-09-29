from RAMLFlask.Server import Server
from RAMLFlask.Generator import Generator
from RAMLFlask.Comparison import Comparison

from StringIO import StringIO
import datetime
import os
import sys
import shutil

import statistics as s


def clean(val):
    new_val = str(round(val,4))

    while len(new_val.split('.')[1]) < 4:
        new_val += '0'

    return new_val


def iqr(array):
    array = sorted(array)
    mid = len(array)/2

    if (len(array) % 2 == 0):
        # even
        lowerQ = s.median(array[:mid])
        upperQ = s.median(array[mid:])
    else:
        # odd
        lowerQ = s.median(array[:mid])  # same as even
        upperQ = s.median(array[mid + 1:])

    return upperQ - lowerQ

def timed_test(file, warmup=100, repeats=100):
    oldstdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    if os.path.exists('./delegates'):
        shutil.rmtree('./delegates')

    if os.path.exists('./routes'):
        shutil.rmtree('./routes')

    if os.path.exists('./generated'):
        shutil.rmtree('./generated')

    for i in range(warmup):
        gen = Generator(file)
        comp = Comparison()

        server = Server(gen, comp)
        server.generate()
        server.compare()

    results = [[],[],[],[],[],[]]
    for i in range(repeats):
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
        t2_0 = t2-t1
        t3_0 = t3-t2
        t4_0 = t4-t3
        t5_0 = t5-t4
        total = t5-t0

        results[0].append(t1_0.total_seconds())
        results[1].append(t2_0.total_seconds())
        results[2].append(t3_0.total_seconds())
        results[3].append(t4_0.total_seconds())
        results[4].append(t5_0.total_seconds())
        results[5].append(total.total_seconds())

    sys.stdout = oldstdout

    print('"' + file  + '";"M1";' + ";".join(str(v) for v in results[0]))
    print('"' + file  + '";"M2";' + ";".join(str(v) for v in results[1]))
    print('"' + file  + '";"M3";' + ";".join(str(v) for v in results[2]))
    print('"' + file  + '";"M4";' + ";".join(str(v) for v in results[3]))
    print('"' + file  + '";"M5";' + ";".join(str(v) for v in results[4]))
    print('"' + file  + '";"M6";' + ";".join(str(v) for v in results[5]))

    if os.path.exists('./delegates'):
        shutil.rmtree('./delegates')

    if os.path.exists('./routes'):
        shutil.rmtree('./routes')

    if os.path.exists('./generated'):
        shutil.rmtree('./generated')

    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Step              # Mean   # Median # Min    # Max    # Range  # StdDev # IQR    #'
    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Server creation   # ' + clean(s.mean(results[0])) + ' # ' + clean(s.median(results[0])) + ' # ' + clean(min(results[0])) + ' # ' + clean(max(results[0])) + ' # ' + clean(max(results[0])-min(results[0])) + ' # ' + clean(s.stdev(results[0])) + ' # ' + clean(iqr(results[0])) + ' # '
    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Code generation   # ' + clean(s.mean(results[1])) + ' # ' + clean(s.median(results[1])) + ' # ' + clean(min(results[1])) + ' # ' + clean(max(results[1])) + ' # ' + clean(max(results[1])-min(results[1])) + ' # ' + clean(s.stdev(results[1])) + ' # ' + clean(iqr(results[1])) + ' # '
    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Route binding     # ' + clean(s.mean(results[2])) + ' # ' + clean(s.median(results[2])) + ' # ' + clean(min(results[2])) + ' # ' + clean(max(results[2])) + ' # ' + clean(max(results[2])-min(results[2])) + ' # ' + clean(s.stdev(results[2])) + ' # ' + clean(iqr(results[2])) + ' # '
    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Change comparison # ' + clean(s.mean(results[3])) + ' # ' + clean(s.median(results[3])) + ' # ' + clean(min(results[3])) + ' # ' + clean(max(results[3])) + ' # ' + clean(max(results[3])-min(results[3])) + ' # ' + clean(s.stdev(results[3])) + ' # ' + clean(iqr(results[3])) + ' # '
    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Test comparison   # ' + clean(s.mean(results[4])) + ' # ' + clean(s.median(results[4])) + ' # ' + clean(min(results[4])) + ' # ' + clean(max(results[4])) + ' # ' + clean(max(results[4])-min(results[4])) + ' # ' + clean(s.stdev(results[4])) + ' # ' + clean(iqr(results[4])) + ' # '
    print '#-------------------#--------#--------#--------#--------#--------#--------#--------#'
    print '# Total             # ' + clean(s.mean(results[5])) + ' # ' + clean(s.median(results[5])) + ' # ' + clean(min(results[5])) + ' # ' + clean(max(results[5])) + ' # ' + clean(max(results[5])-min(results[5])) + ' # ' + clean(s.stdev(results[5])) + ' # ' + clean(iqr(results[5])) + ' # '
    print '#----------------------------------------------------------------------------------#'


#timed_test("./RAML_files/github/github-api-v3.raml")
#timed_test("./RAML_files/instagram/instagram-api.raml")
#timed_test("./RAML_files/uber/api.raml")
#timed_test("./RAML_files/slack/slack.raml")
#timed_test("./RAML_files/box/boxAPI.raml")
#timed_test("./RAML_files/slideshare/slideshare.raml")
#timed_test("./RAML_files/wordpress/wordpress.raml")
#timed_test("./RAML_files/flickr/flickr.raml")
#timed_test("./RAML_files/gmail/gmail.raml")
timed_test("./RAML_files/grooveshark/grooveshark.raml")