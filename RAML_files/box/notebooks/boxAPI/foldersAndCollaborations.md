c---
site: https://anypoint.mulesoft.com/apiplatform/popular/admin/#/dashboard/apis/7458/versions/7574/portal/pages/6182/preview
apiNotebookVersion: 1.1.66
title: Folders and collaborations
---

```javascript

load('https://github.com/chaijs/chai/releases/download/1.9.0/chai.js')

```



See http://chaijs.com/guide/styles/ for assertion styles



```javascript

assert = chai.assert

```



Folder names that are manipulated by the Notebook.



```javascript

notebookTestFolderName = "API Notebook Test Folder"

testFolderName = "Test Folder"

testFolderNameNew = "Test Folder New"

parentFolderName1 = "Parent Folder 1"

parentFolderName2 = "Parent Folder 2"

folderNames = [ testFolderName, testFolderNameNew, parentFolderName1, parentFolderName2 ]

```

```javascript

// Read about the Box API at https://anypoint.mulesoft.com/apiplatform/popular/admin/#/dashboard/apis/7458/versions/7574/contracts

API.createClient('client', '/apiplatform/repository/public/organizations/30/apis/7458/versions/7574/definition');

```

```javascript

cId = prompt("Please, enter the clientId of your own application");

cSecret = prompt("Please, enter the clientSecret of your own application");

  

API.authenticate(client, 'oauth_2_0', {

  clientId: cId,

  clientSecret: cSecret

});

```



We are going to select a **/API Notebook Test Folder** subfolder in the root. If it does not already exist we shall create it. All the subsequent operations will be limited to this subfolder.



```javascript

notebookTestFolder = null

{

  rootFolderResponse = client.folders.folderId('0').get()

  entries = rootFolderResponse.body.item_collection.entries

  for( var ind in entries){  

    var entry = entries[ind]

    

    if( entry.type == "folder" && entry.name == notebookTestFolderName ) {  

      notebookTestFolder = client.folders.folderId(entry.id).get().body

      break

    }

  }

  if(notebookTestFolder==null){

    notebookTestFolder = client.folders.post( { parent: rootFolder, name: notebookTestFolderName }).body

  }

}

```



Now we are going to delete all the folders that could have been created during earlier notebook runs.



```javascript

{

  var entries = client.folders.folderId(notebookTestFolder.id).items.get().body.entries

  for( var ind in entries){  

    var entry = entries[ind]

    

    if( entry.type == "folder" && folderNames.indexOf(entry.name) >= 0 ) {  

      client.folders.folderId(entry.id).delete({},{query:{recursive:true}})

    }

  }

}

```



Allows to create new Folder



```javascript

folderCreateResponse = client.folders.post({

  parent: notebookTestFolder,

  name: testFolderName

})

```

```javascript

assert.equal(folderCreateResponse.status,201)

folderId = folderCreateResponse.body.id

```



Retrieves the full metadata about a folder, including information about

when it was last updated as well as the files and folders contained in it.

The root folder of a Box account is always represented by the id **0**.



```javascript

folderResponse = client.folders.folderId(folderId).get()

```

```javascript

assert.equal(folderResponse.status,200)

assert.equal(folderResponse.body.id,folderId)

```



Used to delete a folder. A recursive parameter must be included in order to

delete folders that have items inside of them. An optional `If-Match` header

can be included to ensure that client only deletes the folder if it knows

about the latest version.



```javascript

folderDeleteResponse = client.folders.folderId(folderId).delete()

```

```javascript

assert.equal(folderDeleteResponse.status,204)

```



Retrieves an item that has been moved to the trash. The full item will be

returned, including information about when the it was moved to the trash.



```javascript

trashedFolderResponse = client.folders.folderId(folderId).trash.get()

```

```javascript

assert.equal(trashedFolderResponse.status,200)

assert.equal(trashedFolderResponse.body.id,folderId)

```



Retrieves the files and/or folders that have been moved to the trash. Any

attribute in the full files or folders objects can be passed in with the

fields parameter to get specific attributes, and only those specific

attributes back; otherwise, the mini format is returned for each item by

default.

Multiple attributes can be passed in separated by commas e.g.

`fields=name,created_at`. Paginated results can be retrieved using the limit

and offset parameters.



```javascript

trashItemsResponse = client.folders.trash.items.get()

```

```javascript

assert.equal(trashItemsResponse.status,200)

```



Restores an item that has been moved to the trash. Default behavior is to

restore the item to the folder it was in before it was moved to the trash.

If that parent folder no longer exists or if there is now an item with the

same name in that parent folder, the new parent folder and/or new name

will need to be included in the request.



```javascript

restoreFolderResponse = client.folders.folderId(folderId).post({

  "parent": notebookTestFolder

})

```

```javascript

assert.equal(restoreFolderResponse.status,201)

```



Used to update information about the folder. To move a folder, update the ID

of its parent. To enable an email address that can be used to upload files

to this folder, update the `folder_upload_email` attribute. An optional

If-Match header can be included to ensure that client only updates the folder

if it knows about the latest version.



```javascript

folderUpdateResponse = client.folders.folderId(folderId).put({

  "name": testFolderNameNew,

})

```

```javascript

assert.equal(folderUpdateResponse.status,200)

assert.equal(folderUpdateResponse.body.name,testFolderNameNew)

```



Retrieves the files and/or folders contained within this folder

without any other metadata about the folder.



```javascript

folderItemsResponse = client.folders.folderId(folderId).items.get()

```

```javascript

assert.equal(folderItemsResponse.status,200)

```



We are about to test a copy operation for folders. For this purpose we'll create two parent folders and a child folder inside one of them. 



```javascript

parentFolder1 = client.folders.post({

  parent: notebookTestFolder,

  name: parentFolderName1

}).body



parentFolder2 = client.folders.post({

  parent: notebookTestFolder,

  name: parentFolderName2

}).body

```

```javascript

childFolder = client.folders.post({

  parent: parentFolder1,

  name: "Child Folder"

}).body

childFolderId = childFolder.id

```



Used to create a copy of a folder in another folder. The original version

of the folder will not be altered.



```javascript

client.folders.folderId(childFolderId).copy.post({

  "parent": {

    "id" : parentFolder2.id

   }

})

```

```javascript

itemsResponse2 = client.folders.folderId(parentFolder2.id).items.get()

assert(itemsResponse2.body.entries.length>0)

```



Use this to get a list of all the collaborations on a folder i.e. all of

the users that have access to that folder.



```javascript

collaborationsResponse = client.folders.folderId(folderId).collaborations.get()

```

```javascript

assert.equal(collaborationsResponse.status,200)

```



In order to add a new collaboration we need a new Box user, and we are going to create him.

If you do not have enterprise access and, thus, unable to create users, you may manually create a new Box user and use his ID as 'newUserId' value.



```javascript

newUserId = null

```



Each box user must have a unique (among all Box users) login. In the next code block we generate a login which is very likely to appear unique.



```javascript

function generateLogin( prefix ){

  var date = new Date()

  var seconds = Math.floor(date.getTime()/1000)

  var login = prefix+seconds+"@somehost.com"

  return login

}



userLogin = generateLogin("NotebookUser_")

```



Each Box user of a particular enterprise must have a unique username (among all users of the enterprise). Let's delete a the users who has a username, that we are going to use on further steps. 



```javascript

userName = "RamlNotebookUser"

{

  var usersResponse = client.users.get()

  var users = usersResponse.body.entries

  for( var ind in users ){

    var u = users[ind]

    if(u.name == userName){

      client.users.userId(u.id).delete({},{query:{force:true,notify:false}})

      break

    }

  }

}

```

```javascript

newUserResponse = client.users.post( { login: userLogin, name: userName } )

```

```javascript

if(newUserResponse.body.id){

  newUserId = newUserResponse.body.id

}

```



Used to add a collaboration for a single user to a folder. Either an email

address or a user ID can be used to create the collaboration.



```javascript

collaborationsCreateResponse = client.collaborations.post({

  "item": {

    "id": folderId,

    "type": "folder"

  },

  "accessible_by": {

    "id": newUserId,

    "type": "user"    

  },

  "role": "editor"

})

```

```javascript

assert.equal(collaborationsCreateResponse.status,201)

collaborationId = collaborationsCreateResponse.body.id

```



Let's check that the collaboration has indeed been added.



```javascript

folderCollaborationsResponse = client.folders.folderId(folderId).collaborations.get()

```

```javascript

assert.equal(folderCollaborationsResponse.status,200)

assert(folderCollaborationsResponse.body.entries.length>0)

```



Used to retrieve all pending collaboration invites for this user.



```javascript

pendingCollaborationsResponse = client.collaborations.get({ status: "pending" })

```

```javascript

assert.equal(pendingCollaborationsResponse.status,200)

```



Used to edit an existing collaboration. Descriptions of the various roles can be found here.



```javascript

collaborationsUpdateResponse = client.collaborations.id(collaborationId).put({

  "role": "viewer"

})

```

```javascript

assert(collaborationsUpdateResponse.body.status, 200)

```



Used to delete a single collaboration.



```javascript

collaborationDeleteResponse = client.collaborations.id(collaborationId).delete()

```

```javascript

assert.equal(collaborationDeleteResponse.status,204)

```



Permanently deletes an item that is in the trash. The item will no longer

exist in Box. This action cannot be undone.



```javascript

//method is not supported at the present time

// folderDeletePermanentlyResponse = client.folders.folderId(folderId).trash.delete()

```

```javascript

// assert.eq(folderDeletePermanentlyResponse.status,200)

```