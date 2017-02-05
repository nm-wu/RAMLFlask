---
site: https://anypoint.mulesoft.com/apiplatform/popular/admin/#/dashboard/apis/7458/versions/7574/portal/pages/6184/preview
apiNotebookVersion: 1.1.66
title: Tasks, task assignments, events and searches
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



We shall need a file for our test. You may choose any file inside your account by setting it's ID as value of the **fileId** in the next code block. The file will be used for two purposes:



1. you will be assigned a task on the file (this task will be deleted later on)

2. the file will be given a comment (which will be deleted later on)

3. we will create a shared link for the file



Alternatively you may create an **/API Notebook Test Folder** subfolder in the root and place the file into it. In this case you don't need to modify the **fileId** variable.



```javascript

fileId = null

```

```javascript

if( fileId == null ){

  

  var notebookTestFolderId = null

  var rootFolderResponse = client.folders.folderId('0').get()

  var rootEntries = client.folders.folderId('0').items.get().body.entries

  for( var ind in rootEntries){  

    var entry = rootEntries[ind]  

    if( entry.type == "folder" && entry.name == notebookTestFolderName ){

      notebookTestFolderId = entry.id

      break

    }

  }  

  entriesResponse = client.folders.folderId(notebookTestFolderId).items.get()

  entries = entriesResponse.body.entries

  for(var ind in entries){

    var entry = entries[ind]

    if(entry.type == "file"){



      fileId = entry.id

      break

    }

  }

}

```



Create a Task. Used to create a single task for single user on a single file.

A new task object will be returned upon success.



```javascript

taskCreateResponse = client.tasks.post({

  "item": {

    "type": "file",

    "id": fileId

  },

  "action": "review"

})

```

```javascript

assert.equal(taskCreateResponse.status,201)

taskId = taskCreateResponse.body.id

```



Fetches a specific task



```javascript

taskResponse = client.tasks.taskId(taskId).get()

```

```javascript

assert.equal(taskResponse.status,200)

```



Updates a specific task



```javascript

taskUpdateResponse = client.tasks.taskId(taskId).put({

  "message": "REVIEW PLZ K THX"

})

```

```javascript

assert.equal(taskUpdateResponse.status,200)

```



Lrt's extract ID of the current user so that we could ascribe a task to him.



```javascript

currentUserId = client.users.me.get().body.id

```



Used to assign a task to a single user. There can be multiple assignments

on a given task.

A new task assignment object will be returned upon success.



```javascript

assignmentCreateResponse = client.task_assignments.post({

  "task": {

    "id": taskId,

    "type": "task"

  },

  "assign_to": {

    "id": currentUserId

  }

})

```

```javascript

assert.equal(assignmentCreateResponse.status,201)

assignmentId = assignmentCreateResponse.body.id

```



Fetches a specific task assignment.

The specified task assignment object will be returned upon success.



```javascript

assignmentResponse = client.task_assignments.task_assignments_id(assignmentId).get()

```

```javascript

assert.equal(assignmentResponse.status,200)

```



Used to update a task assignment.

A new task assignment object will be returned upon success.



```javascript

assignmentUpdateResponse = client.task_assignments.task_assignments_id(assignmentId).put({

  "message": "hello!!!",

  "resolution_state" : "completed"

})

```

```javascript

assert.equal(assignmentUpdateResponse.status,200)

```



Retrieves all of the assignments for a given task.

A collection of task assignment mini objects will be returned upon success.



```javascript

assignmentsResponse = client.tasks.taskId(taskId).assignments.get()

```

```javascript

assert.equal(assignmentsResponse.status,200)

assert(assignmentsResponse.body.entries.length>0)

```







Deletes a specific task assignment.

An empty `204 No Content` response will be returned upon success.



```javascript

assignmentDeleteResponse = client.task_assignments.task_assignments_id(assignmentId).delete()

```

```javascript

assert.equal(assignmentDeleteResponse.status,204)

```



Used to add a comment by the user to a specific file or comment (i.e. as a

reply comment).



```javascript

newComment = "This comment is creted by API Notebook"

commentCreateResponse = client.comments.post({

  "item": {

    "type": "file",

    "id": fileId

  },

  "message": newComment

})

```

```javascript

assert.equal(commentCreateResponse.status,201)

commentId = commentCreateResponse.body.id

```



Used to retrieve the message and metadata about a specific comment.

Information about the user who created the comment is also included.



```javascript

commentResponse = client.comments.commentId(commentId).get()

```

```javascript

assert.equal(commentResponse.status,200)

```



Used to update the message of the comment. The full updated comment object

is returned if the ID is valid and if the user has access to the comment.



```javascript

commentUpdateResponse = client.comments.commentId(commentId).put({

  message:"This comment is creted by API Notebook. UPDATED."

})

```

```javascript

assert.equal(commentUpdateResponse.status,200)

```



Permanently deletes a comment. An empty 204 response is returned to confirm

deletion of the comment. Errors can be thrown if the ID is invalid or if the

user is not authorized to delete this particular comment.



```javascript

commentDeleteResponse = client.comments.commentId(commentId).delete()

```

```javascript

assert.equal(commentDeleteResponse.status,204)

```



We need a query string in order to test a search operation. By default we will use name of the file involved. Alternatively, you may set any query string in the following code block. 



```javascript

queryString = null

```

```javascript

if(queryString==null){

  queryString = client.files.fileId(fileId).get().body.name

}

```



Searching a User's Account. The search endpoint provides a simple way of

finding items that are accessible in a given user's Box account.

A collection of search results is returned. If there are no matching search

results, the entries array will be empty.

ALERT: We'll be adding more types of items returned as search results and more

filters on search queries, so as you're parsing the results, be prepared to skip

over any types of items your app does not recognize.



```javascript

searchResponse = client.search.get({

  query: queryString

})

```

```javascript

assert.equal(searchResponse.status,200)

```



Let's share the file so that we could test retrieving metadata about a shared item.



```javascript

sharedLinkResponse = client.files.fileId(fileId).put({"shared_link": {"access": "open"}})

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



```javascript

shared_itemsResponse = client.shared_items.get({}, {

  headers:{

    "BoxApi": "shared_link=" + sharedLinkResponse.body.shared_link.url

  }

})

```

```javascript

assert.equal( shared_itemsResponse.status, 200)

```



Permanently deletes a specific task. An empty 204 response will be

returned upon success.



```javascript

taskDeleteResponse = client.tasks.taskId(taskId).delete()

```

```javascript

assert.equal( taskDeleteResponse.status, 204)

```











Use this to get events for a given user. A chunk of event objects is

returned for the user based on the parameters passed in. Parameters

indicating how many chunks are left as well as the next stream_position

are also returned.



```javascript

eventsResponse = client.events.get()

```

```javascript

assert.equal( eventsResponse.status, 200)

```



Long polling. To get real-time notification of activity in a Box account,

use the long poll feature of the /events API.

To do so, first call the `/events` API with an OPTIONS call to retrieve the

long poll URL to use.

Next, make a GET request to the provided URL to begin listening for events.

If an event occurs within an account you are monitoring, you will receive a

response with the value new_change.

It's important to note that this response will not come with any other

details, but should serve as a prompt to take further action such as calling

the `/events` endpoint with your last known `stream_position`. After sending

this response, the server will close the connection and you will need to

repeat the long poll process to begin listening for events again.

If no events occur for a period of time after you make the GET request to

the long poll URL, you will receive a response with the value reconnect. When

you receive this response, you'll make another OPTIONS call to the /events

endpoint and repeat the long poll process.



```javascript

eventsResponse = client.events.options()

```

```javascript

assert.equal( eventsResponse.status, 200)

```