---
site: https://anypoint.mulesoft.com/apiplatform/popular/admin/#/dashboard/apis/7458/versions/7574/portal/pages/6181/edit
apiNotebookVersion: 1.1.66
title: Users, groups and memberships
---

```javascript

load('https://github.com/chaijs/chai/releases/download/1.9.0/chai.js')

```



See http://chaijs.com/guide/styles/ for assertion styles



```javascript

assert = chai.assert

```



Usernames that are manipulated by the Notebook.



```javascript

userName1 = "RamlNotebookUser1"

userName2 = "RamlNotebookUser2"

```



Each box user must have a unique (among all Box users) login. In the next code block we generate two logins which are very likely to appear unique.



```javascript

function generateLogin( prefix ){

  var date = new Date()

  var seconds = Math.floor(date.getTime()/1000)

  var login = prefix+seconds+"@somehost.com"

  return login

}



userLogin1 = generateLogin("NotebookUser1_")

userLogin2 = generateLogin("NotebookUser2_")

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



Get the Current User's Information. Retrieves information about the user who

is currently logged in i.e. the user for whom this auth token was generated.

Returns a single complete user object.

An error is returned if a valid auth token is not included in the API request.



```javascript

currentUserResponse = client.users.me.get()

```

```javascript

assert.equal(currentUserResponse.status,200)

```



Let's store the current user's ID.



```javascript

currentUserId = currentUserResponse.body.id

```



Get All Users in an Enterprise. Returns a list of all users for the

Enterprise along with their user_id, public_name, and login.



```javascript

usersResponse = client.users.get()

```

```javascript

assert.equal(usersResponse.status,200)

```



Each Box user of a particular enterprise must have a unique username (among all users of the enterprise). Let's delete all the users who have those usernames, that we are going to use on further steps. 



```javascript

{

  users = usersResponse.body.entries

  for(var ind in users){

    var u = users[ind]

    if(u.name == userName1 || u.name == userName2){

      client.users.userId(u.id).delete({},{query:{force:true,notify:false}})

    }    

  }

}

```



Used to provision a new user in an enterprise. This method only works

for enterprise admins.



```javascript

newUserResponse = client.users.post({login: userLogin1, name: userName1})

```

```javascript

assert.equal(newUserResponse.status,201)

```



Let's grab the newly created user's ID.



```javascript

newUserId1 = newUserResponse.body.id

```



Let's create one more user and grab his ID too.



```javascript

newUserResponse2 = client.users.post({login: userLogin2, name:userName2})

newUserId2 = newUserResponse2.body.id

```



In order to test user update method, we are going to change some field of 'currentUser'. Let it be a boolean field 'is_sync_enabled'. Remember that it may appear undefined for the present moment.



```javascript

currentUser = currentUserResponse.body

isSyncEnabled = currentUser.is_sync_enabled

if(!isSyncEnabled){

  isSyncEnabled = false;

}

newIsSyncEnabled = !isSyncEnabled

```



Update a User's Information. Used to edit the settings and information about

a user. This method only works for enterprise admins. To roll a user out of

the enterprise (and convert them to a standalone free user), update the

special `enterprise` attribute to be `null`.

Returns the a full user object for the updated user. Errors may be thrown when

the fields are invalid or this API call is made from a non-admin account.



```javascript

updateUserResponse = client.users.userId(currentUserId).put({

  "is_sync_enabled": newIsSyncEnabled

})

```

```javascript

assert.equal(updateUserResponse.status,200)

```



Let's change the 'is_sync_enabled' value back.



```javascript

updateUserResponse = client.users.userId(currentUserId).put({

  "is_sync_enabled": isSyncEnabled

})

```



Add an Email Alias for a User.

Adds a new email alias to the given user's account.

Returns the newly created email_alias object. Errors will be thrown if the

user_id is not valid or the particular user's email alias cannot be modified.



```javascript

// method is not supported at the present time

// emailUpdateResponse = client.users.userId(newUserId1).email_aliases.post({

//   email : "mynewalias@somehost.com"

// })

```

```javascript

// assert.equal(emailUpdateResponse.status,201)

```



Get All Email Aliases for a User.

Retrieves all email aliases for this user. The collection of email aliases

does not include the primary login for the user; use GET /users/USER_ID to

retrieve the login email address.

If the user_id is valid a collection of email aliases will be returned.



There must be more then one email addresses in the "Login and Email Addresses". Otherwise, the method would return an empty array.



```javascript

emailResponse = client.users.userId(currentUserId).email_aliases.get()

```

```javascript

assert.equal(emailResponse.status,200)

```



Assuming that the current user has at least one email alias (remember that a mandatory email is not considered an alias), let's take the first one.



Removes an email alias from a user. If the user has permission to remove

this email alias, an empty 204 No Content response will be returned to confirm deletion.



As we can not call POST for email aliases, me do not test DELETE for them.

If you wish, you may test DELETE with a manually created alias.

For this purpose

1. uncomment the following three code blocks

2. execute email_aliases.get() one more time to refresh the aliases array

3. select the disired alias by setting value to the 'aliasIndex' variable



```javascript

//aliasIndex = 

//emailAliasId = emailResponse.body.entries[aliasIndex].id

```

```javascript



//emailAliasDeleteResponse = client.users.userId(currentUserId).email_aliases.email_aliases_id(emailAliasId).delete()

```

```javascript

//assert.equal(emailAliasDeleteResponse.status,204)

```



Move Folder into Another User's Folder.

Moves all of the content from within one user's folder into a new folder in

another user's account. You can move folders across users as long as the you

have administrative permissions. To move everything from the root folder,

use "0" which always represents the root folder of a Box account.



Currently only moving of the root folder (0) is supported.



```javascript

moveFolderResponse = client.users.userId(newUserId1).folders.folderId('0').put({

  "owned_by": {

    "id": newUserId2

  }

})

```

```javascript

assert.equal(moveFolderResponse.status,200)

```



Retrieves all of the group memberships for a given enterprise. Note this is only available to group admins. To get a users groups use the users/me/memberships endpoint



```javascript

userMembershipsResponse = client.users.userId(currentUserId).memberships.get()

```

```javascript

assert.equal(userMembershipsResponse.status,200)

```



Retrieves all of the groups for given user



```javascript

groupsResponse = client.groups.get()

```

```javascript

assert.equal(groupsResponse.status,200)

```



Allows to create new Group



```javascript

groupCreateResponse = client.groups.post({name: "NewGroup"})

```

```javascript

assert.equal(groupCreateResponse.status,201)

groupId = groupCreateResponse.body.id

```



used to update item



```javascript

groupName = "NewGroup2"

groupUpdateResponse = client.groups.id(groupId).put({

    "name": groupName

})

```

```javascript

assert.equal(groupUpdateResponse.status,200)

```



Retrieves all of the members for a given group



```javascript

groupMembershipsResponse = client.groups.id(groupId).memberships.get()



```

```javascript

assert.equal(groupMembershipsResponse.status,200)

```



Retrieves all of the group collaborations for a given group. Note this is only available to group admins.



```javascript

collaborationsResponse = client.groups.id(groupId).collaborations.get()

```

```javascript

assert.equal(collaborationsResponse.status,200)

```



Used to add a member to a Group.



```javascript

membershipCreateResponse = client.group_memberships.post({

  "user" : {

    "id" : newUserId1

  } ,

  "group" : {

    "id" : groupId

  }

})

```

```javascript

assert.equal(membershipCreateResponse.status,201)

membershipId = membershipCreateResponse.body.id

```



Fetches a specific group membership entry



```javascript

membershipResponse = client.group_memberships.id(membershipId).get()

```

```javascript

assert.equal(membershipResponse.status,200)

```



Used to update a group membership.



```javascript

membershipUpdateResponse = client.group_memberships.id(membershipId).put({

  role : "admin"

})

```

```javascript

assert.equal(membershipUpdateResponse.status,200)

```



Deletes a specific group membership



```javascript

membershipDeleteResponse = client.group_memberships.id(membershipId).delete()

```

```javascript

assert.equal(membershipDeleteResponse.status,204)

```



Permanently deletes a specific group



```javascript

groupDeleteResponse = client.groups.id(groupId).delete()

```

```javascript

assert(groupDeleteResponse.status==204||groupDeleteResponse.status==403)

```





Deletes a user in an enterprise account. An empty 200 response is sent to

confirm deletion of the user. If the user still has files in their account

and the `force` parameter is not sent, an error is returned.



```javascript

deleteUser1Response = client.users.userId(newUserId1).delete()

```

```javascript

assert.equal(deleteUser1Response.status,204)

```

```javascript

deleteUser2Response = client.users.userId(newUserId2).delete({},{

  query: {

    force: true,

    notify: false

  }

})

```

```javascript

assert.equal(deleteUser2Response.status,204)

```