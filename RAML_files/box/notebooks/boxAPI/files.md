---
site: https://anypoint.mulesoft.com/apiplatform/popular/admin/#/dashboard/apis/7458/versions/7574/portal/pages/6183/preview
apiNotebookVersion: 1.1.66
title: Files
---

```javascript

load('https://github.com/chaijs/chai/releases/download/1.9.0/chai.js')

```



See http://chaijs.com/guide/styles/ for assertion styles



```javascript

assert = chai.assert

```

```javascript

notebookTestFolderName = "API Notebook Test Folder"

fileTestFolderName = "Folder For File Test"

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



Let's select Select a folder called "API Notebook Test Folder" in the root. If it does not exist, you should create it manually before running this notebook. Also you should get ensured that this folder contains a single file which fas at least one version.



```javascript

notebookTestFolder = null

{

  rootFolderResponse = client.folders.folderId('0').get()

  rootEntries = rootFolderResponse.body.item_collection.entries

  for( var ind in rootEntries){  

    var entry = rootEntries[ind]  

    if( entry.type == "folder" && entry.name == notebookTestFolderName ){

      notebookTestFolder = client.folders.folderId(entry.id).get().body

      break

    }

  }  

}

```



In the next two code blocks we prepare the infrastructure for the current notebook run. That's what we do:



1. We create the **/API Notebook Test Folder/Folder For File Test** subfolder (or recreate if it already exists). All the subsequent actions will be limited to this folder.



2. We copy the only file inside the **/API Notebook Test Folder** into the newly created subfolder.



```javascript

fileTestFolder = null

{

  entries = notebookTestFolder.item_collection.entries

  for( var ind in entries){

    

    var entry = entries[ind]

    if(entry.type == "folder" && entry.name == fileTestFolderName ){

	    fileTestFolder = entry

    }

  }  

  if(fileTestFolder){

    client.folders.folderId(fileTestFolder.id).delete({},{query:{recursive:true}})

  }

  fileTestFolderResponse = client.folders.post({

    parent: notebookTestFolder,

    name: fileTestFolderName

  })

  fileTestFolder = fileTestFolderResponse.body

}

fileTestFolderId = fileTestFolder.id

```

```javascript

fileId = null

oldFileId = null

{

  entriesResponse = client.folders.folderId(notebookTestFolder.id).items.get()

  entries = entriesResponse.body.entries

  for(var ind in entries){

    var entry = entries[ind]

    if(entry.type == "file"){



    oldFileId = entry.id

    client.files.fileId(entry.id).copy.post({

      "parent": {

        "id" : fileTestFolderId

       }

    })

    break

    }

  }

  itemsResponse = client.folders.folderId(fileTestFolderId).items.get()

  testFile = itemsResponse.body.entries[0]

  assert(testFile)

  fileId = testFile.id

}

```



Used to retrieve the metadata about a file



```javascript

fileResponse = client.files.fileId(fileId).get()

```

```javascript

assert.equal(fileResponse.status,200)

assert.equal(fileResponse.body.id,fileId)

```



Discards a file to the trash. The 'etag' of the file can be included as an

`If-Match` header to prevent race conditions.

Trash: Depending on the enterprise settings for this user, the item will

either be actually deleted from Box or moved to the trash.



```javascript

fileDeleteResponse = client.files.fileId(fileId).delete()

```

```javascript

assert.equal(fileDeleteResponse.status,204)

```



Retrieves an item that has been moved to the trash. The full item will be

returned, including information about when the it was moved to the trash.



```javascript

fileResponse = client.files.fileId(fileId).trash.get()

```

```javascript

assert.equal(fileResponse.status,200)

```



Restores an item that has been moved to the trash. Default behavior is to

restore the item to the folder it was in before it was moved to the trash.

If that parent folder no longer exists or if there is now an item with the

same name in that parent folder, the new parent folder and/or new name will

need to be included in the request.



```javascript

fileRestoreResponse = client.files.fileId(fileId).post({

  "parent": {

    "id" : fileTestFolder.id

   }

})

```

```javascript

assert.equal(fileRestoreResponse.status,201)

```



Used to update individual or multiple fields in the file object, including

renaming the file, changing its description, and creating a shared link

for the file. To move a file, change the ID of its parent folder. An optional

`If-Match` header can be included to ensure that client only updates the file

if it knows about the latest version.



```javascript

//here we prepare a new file name which has the same extension as the old one

extension = ""

{

  var name = fileResponse.body.name

  var ind = name.lastIndexOf('.')

  if(ind >= 0){

    extension = name.substring(ind)

  }  

}

newFileName = "newName" + extension

```

```javascript

fileUpdateResponse = client.files.fileId(fileId).put({

  "name" : newFileName

})

```

```javascript

assert.equal(fileUpdateResponse.status,200)

fileResponse = client.files.fileId(fileId).get()

```



If there are previous versions of this file, this method can be used to

retrieve metadata about the older versions.

**ALERT: Versions are only tracked for Box users with premium accounts.**



```javascript

versionsResponse = client.files.fileId(oldFileId).versions.get()

```

```javascript

assert(versionsResponse.status==200)

allVersions = versionsResponse.body.entries

versionId = versionsResponse.body.entries[versionsResponse.body.entries.length-1].id

```



Promote an Old Version of a File

If there are previous versions of this file, this method can be used to promote one of the older versions to the top of the stack. This actually mints a copy of the old version and puts it on the top of the versions stack. The file will have the exact same contents, the same SHA1/etag, and the same name as the original. Other properties such as comments do not get updated to their former values.



```javascript

promoteVersionResponse = client.files.fileId(oldFileId).versions.current.post({

  "type" : "file_version" ,

  "id" : versionId

})

```

```javascript

assert(promoteVersionResponse.status==201)

```



Discards a specific file version to the trash.



Trash: Depending on the enterprise settings for this user, the item will either be actually deleted from Box or moved to the trash.



```javascript

allVersions = client.files.fileId(oldFileId).versions.get().body.entries

versionId = allVersions[0].id

versionDeleteResponse = client.files.fileId(oldFileId).versions.version_id(versionId).delete()

```

```javascript

assert.equal(versionDeleteResponse.status, 204)

```



Used to create a copy of a file in another folder. The original version of the file will not be altered.



```javascript

//here we create (or recreate if it already exists) a destination folder for our copy operation

destinationFolderId = null

fileTestFolder = client.folders.folderId(fileTestFolderId).get().body

{

  var entries = fileTestFolder.item_collection.entries

  for( var ind in entries){

    

    var entry = entries[ind]

    if(entry.type == "folder" && entry.name == "Destination Folder" ){

      client.folders.folderId(entry.id).delete({},{query:{recursive:true}})

    }

  }  

  

  destinationFolderResponse = client.folders.post({

    parent: fileTestFolder,

    name: "Destination Folder"

  })

  destinationFolderId = destinationFolderResponse.body.id

}

```

```javascript

fileCopyResponse = client.files.fileId(fileId).copy.post({

  "parent": {

    "id" : destinationFolderId

   }

})

```

```javascript

assert.equal(fileCopyResponse.status,201)

```



Let's get ensured that the file has indeed been copied



```javascript

found = false

{

  var itemsResponse = client.folders.folderId(destinationFolderId).items.get()

  var fileName = client.files.fileId(fileId).get().body.name

  for(var ind in itemsResponse.body.entries){

    var entry = itemsResponse.body.entries[ind]

    if( entry.type== "file" && entry.name == fileName ){

      found = true

      break

    }

  }

}

assert(found)

```









Retrieves all of the tasks for given file. A collection of mini task objects

is returned. If there are no tasks, an empty collection will be returned.



```javascript

fileTasksResponse = client.files.fileId(fileId).tasks.get()

```

```javascript

assert.equal(fileTasksResponse.status,200)

```



Retrieves a thumbnail, or smaller image representation, of this file. Sizes

of 32x32, 64x64, 128x128, and 256x256 can be returned.

Currently thumbnails are only available in .png format and will only be

generated for image file formats.

There are three success cases that your application needs to account for:

  - If the thumbnail isn't available yet, a 202 Accepted HTTP status will

      be returned, including a 'Location' header pointing to a placeholder

      graphic that can be used until the thumbnail is returned. A `Retry-After`

      header will also be returned, indicating the time in seconds after which

      the thumbnail will be available. Your application should only attempt to

      get the thumbnail again after Retry-After time.

  - If Box can't generate a thumbnail for this file type, a 302 Found

      response will be returned, redirecting to a placeholder graphic in the

      requested size for this particular file type.

  - If Box is unable to generate a thumbnail for this particular file, a

      404 'Not Found' response will be returned with a code of

      preview_cannot_be_generated. If there are any bad parameters sent in, a

      standard 400 'Bad Request' will be returned.



```javascript

thumbnailResponse = client.files.fileId(fileId).thumbnail(".png").get()

```

```javascript

assert.equal(thumbnailResponse.status,200)

```



Retrieves the comments on a particular file, if any exist. A collection of

comment objects are returned. If there are no comments on the file, an empty

comments array is returned.



```javascript

fileCommentsResponse = client.files.fileId(fileId).comments.get()

```

```javascript

assert.equal(fileCommentsResponse.status,200)

```



Retrieves the actual data of the file. An optional version parameter can be

set to download a previous version of the file.



```javascript

fileContentResponse = client.files.fileId(fileId).content.get()

```

```javascript

assert.equal(fileContentResponse.status,200)

```



Used to retrieve the metadata about a shared item when only given a shared

link. Because of varying permission levels for shared links, a password may

be required to retrieve the shared item. Once the item has been retrieved,

you can make API requests against the actual resource `/files/{id}` or

`/folders/{id}` as long as the shared link and optional password are in the

header.

A full file or folder object is returned if the shared link is valid and the

user has access to it. An error may be returned if the link is invalid, if a

password is required, or if the user does not have access to the file.



Permanently deletes an item that is in the trash. The item will no longer

exist in Box. This action cannot be undone.



```javascript

//method is not supported at the present time

// fileDeletePermanentlyResponse = client.files.fileId(fileId).trash.delete()

```

```javascript

// assert.equal(fileDeletePermanentlyResponse.status,200)

```