# TODO list API
### Created with FLASK framework 

# Description

Vertion 1 of a RESTFul API to create tasks. The user has the posibiltiy to edit the description of the tasks and delete them. 

### Tasks
* `GET /todo/api/v1.0/tasks`
* `POST /todo/api/v1.0/tasks`
* `PUT /todo/api/v1.0/tasks/<task_id>/status`
* `GET /todo/api/v1.0/tasks/<task_id>`
* `DELETE /todo/api/v1.0/tasks/<task_id>`


# Installation process 

## Install the system dependencies
* **git** 
* **pip**

## Get the code
* Clone the repository
`git clone https://github.com/botdeniska/todolist.git`

## Install the project dependencies

`pip install -r requirements.txt`

## Run the command to generate the database
`python app.py`
