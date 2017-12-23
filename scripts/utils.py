localport = 27018  # local port for MongoDB
remoteport = 27017  # remote server port for MongoDB
identityfile = '../key/ssh/id_rsa'
user = 'yqiu'
server_address = 'phoenix.cs.colostate.edu'
local_bind_ip = "127.0.0.1"

from sshtunnel import SSHTunnelForwarder


def startServer():
    server = SSHTunnelForwarder(
        server_address,
        ssh_username=user,
        ssh_pkey=identityfile,
        remote_bind_address=(local_bind_ip, remoteport),
        local_bind_address=("localhost", localport)
    )
    server.start()
    return server


def convert_csv_to_json(csv_line, csv_header, id_header):
    json_elements = []
    for index, heading in enumerate(csv_header):
        # print heading
        if (heading == id_header):
            json_elements.append("\"" + "_id" + "\": \"" + unicode(csv_line[index], 'utf-8') + "\"")
        else:
            json_elements.append("\"" + heading + "\": \"" + unicode(csv_line[index], 'utf-8') + "\"")
    line = "{ " + ', '.join(json_elements) + " }"
    return line


from csv import Dialect
from _csv import QUOTE_MINIMAL


class tsv(Dialect):
    delimiter = '\t'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL
