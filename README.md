# ABOUT

**OpenClassrooms - Développeur d'application Python - Projet #10: Make a secured RESTful API using Django REST**

_Tested with Windows 10 and Python 3.10.2_


# Hao2do (Windows)
### Retrieving a copy of the "depository"

- `git clone https://github.com/munchou/OpenClassroms-Project-10.git`

or download the ZIP file and extract it in a chosen folder.

### Creating and activating the virtual environment
(Python must have been installed)
- `cd OpenClassroms-Project-10` (or any folder where the project is located)
- `python -m venv ENV` where ENV is the name of the folder where the environment will be created.
- Activation : `env/Scripts/activate`
    
### Installing the needed modules

- `pip install -r requirements.txt`

### Starting the program
You must be located in the folder where "manage.py" is in order to start the local server.
If need, make the necessary migrations with `python manage.py migrate`
Then connec to the server:
- `python manage.py runserver`

### Getting to the application
In any browser, type either addresses:
http://127.0.0.1:8000/ or http://localhost:8000/
They both allow to access the API.

### Connecting to an account
There are by default 3 available users (and the admin).

|       *ID*        |   *Password*   |
|-------------------|----------------|
| User2             |    user4321    |
| User3             |    user4321    |
| User4             |    user4321    |
| admin             |      admin     |

### What the API can do for you (and all of that for free!)
Direct access to [the documentation here](https://documenter.getpostman.com/view/28047851/2s93sjUUSd) (made with Postman) .
|  | API endpoint | HTTP method | URI           |
|- |-             |-            |-              |
|1 | Sign up      | POST        | /signup/      |
|2 | User authentication | POST | /login/       |
|2b | Refresh the token | POST | /login/refresh/|
|2c | Change the user's password | PUT | /change_password/{user_id}/ |
|2d | Log out (optional) | POST | /logout/      |
|3 | Get the list of the available projects the user is linked to | GET | /projects/|
|4 | Create a project | POST    | /projects/    |
|5 | Get the details of a project | GET | /projects/{project_id}/|
|6 | Update a project | PUT | /projects/{project_id}/|
|7 | Delete a project and its issues | DELETE | /projects/{project_id}/|
|8 | Add a user (collaborator) to a project | POST | /projects/{project_id}/users/|
|9 | Get all the users (collab.) linked to a project | GET | /projects/{project_id}/users/|
|10| Remove a collaborator from a project | DELETE | /projects/{project_id}/users/{user_id}/|
|11 | Get all the issues of the project | GET | /projects/{project_id}/issues/ |
|12 | Create an issue for a project | POST | /projects/{project_id}/issues/ |
|13 | Update the issue of a project | PUT | /projects/{project_id}/issues/{issue_id}/ |
|14 | Delete the issue of a project | DELETE | /projects/{project_id}/issues/{issue_id}/ |
|15 | Create a comment for the issue | POST | /projects/{project_id}/issues/{issue_id}/comments/ |
|16 | Get the list of all comments of an issue | GET| /projects/{project_id}/issues/{issue_id}/comments/ |
|17 | Update the comment | PUT | /projects/{project_id}/issues/{issue_id}/comments/{comment_id} |
|18 | Delete the comment | DELETE | /projects/{project_id}/issues/{issue_id}/comments/{comment_id} |
|19 | Retrieve the comment of the issue | GET | /projects/{project_id}/issues/{issue_id}/comments/{comment_id} |


Have fun! If you're happy and you know it, clap you hands! Or give me money. Plenty.