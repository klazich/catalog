from oauth2client.client import flow_from_clientsecrets

from config import app_dir

flow = flow_from_clientsecrets( app_dir + '/client_secret.json')
