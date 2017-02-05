The API notebooks are all executable! Hit "enter" in any code cell to execute it (and all cells before it that have not executed yet), or scroll to the bottom of the notebook and click "Play notebook". For more information, see [http://apinotebook.com](http://apinotebook.com).

#Considerations

- In order to run these notebooks you will need a Box account. At some point of the execution, you will be prompted to authorize the client application to access to your account.
- You must also register a box application as described [here](https://developers.box.com/oauth/). Your application must poses all possible scopes (by December 2014 these are "Read and write all files and folders" and "Manage an enterprise"). Redirect URI of the application must be set to https://api-notebook.anypoint.mulesoft.com/authenticate/oauth.html. At some point of notebook execution, you will be prompted to enter Client ID and Client Secret of your application.
- The notebook "Files" requires you to have API Notebook Test Folder folder in the root of your box account. This folder must have a single file which has exactly two versions.
