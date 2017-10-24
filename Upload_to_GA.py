import logging
import os
import sys
from apiclient.discovery import build
#import gflags
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OOB_CALLBACK_URN
from oauth2client.file import Storage
from oauth2client import tools
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from apiclient.http import MediaFileUpload

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You get these values by
# creating a new project in the Google APIs console and registering for
# OAuth2.0 for installed applications: <https://code.google.com/apis/console>
CLIENT_SECRETS = 'XXXX.apps.googleusercontent.com.json'


# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" 
#% os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics',
    redirect_uri=OOB_CALLBACK_URN,
    message=MISSING_CLIENT_SECRETS_MESSAGE)



# Name of file that will store the access and refresh tokens to access
# the API without having to login each time. Make sure this file is in
# a secure place.
TOKEN_FILE_NAME = 'analytics.dat'


#  """Returns an instance of service from discovery data and does auth.

#  This method tries to read any existing OAuth 2.0 credentials from the
#  Storage object. If the credentials do not exist, new credentials are
#  obtained. The crdentials are used to authorize an http object. The
#  http object is used to build the analytics service object.

#  Returns:
#    An analytics v3 service object.
#  """

  # Create an httplib2.Http object to handle our HTTP requests.
http = httplib2.Http()

  # Prepare credentials, and authorize HTTP object with them.
storage = Storage(TOKEN_FILE_NAME)
#
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = tools.run_flow(FLOW, storage)
storage.put(credentials)
http = credentials.authorize(http)

  # Retrieve service.
service = build('analytics', 'v3', http=http)



media = MediaFileUpload(
      'XXXXXXX.csv', # The CSV file to upload
      mimetype='application/octet-stream',
      resumable=False)

daily_upload = service.management().uploads().uploadData(
      accountId='XXXXXX',
      webPropertyId='XXXXXX',
      customDataSourceId='XXXXXXX',
#      date=upload_date,  # Upload Date
#      appendNumber=append_number,  # The append number of the current upload
#      reset=reset_date,  # Reset will delete any existing data for the date if set to true
#      type='cost',  # Type of data being uploaded
      media_body=media).execute()
								   
