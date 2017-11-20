from RAMLFlask.Server import Server
from RAMLFlask.Generator import Generator
from RAMLFlask.Comparison import Comparison
import time

current_milli_time = lambda: int(round(time.time() * 1000))

def get_times(x):
    y = []
    y.append(x[1] - x[0])
    y.append(x[2] - x[1])
    y.append(x[3] - x[2])
    y.append(x[4] - x[3])
    y.append(x[5] - x[4])
    y.append(x[6] - x[5])
    y.append(x[7] - x[6])

    return y


def memory_test(file):
    x = []

    x.append(current_milli_time())
    gen = Generator(file)
    x.append(current_milli_time())
    comp = Comparison()
    x.append(current_milli_time())
    server = Server(gen, comp)
    x.append(current_milli_time())

    server.generate(True, False)
    x.append(current_milli_time())
    server.generate(False, True)
    x.append(current_milli_time())
    server.compare(True, True, False)
    x.append(current_milli_time())
    server.compare(False, False, True)
    x.append(current_milli_time())

    print get_times(x)


memory_test("./RAML_files/github/github-api-v3.raml")
#memory_test("./RAML_files/instagram/instagram-api.raml")
#memory_test("./RAML_files/uber/api.raml")
#memory_test("./RAML_files/slack/slack.raml")
#memory_test("./RAML_files/box/boxAPI.raml")
#memory_test("./RAML_files/slideshare/slideshare.raml")
#memory_test("./RAML_files/wordpress/wordpress.raml")
#memory_test("./RAML_files/flickr/flickr.raml")
#memory_test("./RAML_files/gmail/gmail.raml")
#memory_test("./RAML_files/grooveshark/grooveshark.raml")