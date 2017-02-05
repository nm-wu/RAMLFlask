Configuring connector

- In order to run this connector you will need a Box account.
- You must also register a box application as described [here](https://developers.box.com/oauth/). Your application must poses all possible scopes (by December 2014 these are "Read and write all files and folders" and "Manage an enterprise").
- Do not forget to set redirect URI for the application. In our case Mule application is launched locally and the redirect URI belongs to the localhost domain: http://localhost:9000/codeBox
- Specify Client Id, Client Secret and redirect URI of your application in the Authentication tab of the HTTP Request Configuration dialog. Alternatively, you may set corresponding attributes right in the XML file.


Running connector

- Make a call on your Local Authorization URL which is http://localhost:9000/authorizeBox. You will be prompted to authorize your application.
- Make a call on the http://localhost:8081/box URL.