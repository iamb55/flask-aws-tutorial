'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo
from airtable import Airtable
from todoist.api import TodoistAPI

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

base_key = 'appUecpt2d3HIznx5'
table_name = 'Tasks'
todoist_airtable = Airtable(base_key, table_name, api_key='keyDX0FzfNUQr3J0c')

todo_api = TodoistAPI('015e5a3fb7d81644745d7adc8daa56d469e08ab5')


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form) 
    form2 = RetrieveDBInfo(request.form) 
    
    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:     
            db.session.add(data_entered)
#            todoist_airtable.insert({'Task Name': 'SUCCESS'})
            db.session.commit()        
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data)
        
    if request.method == 'POST' and form2.validate():
        try:   
            num_return = int(form2.numRetrieve.data)
            query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
            for q in query_db:
                print(q.notes)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('results.html', results=query_db, num_return=num_return)                
    
    return render_template('index.html', form1=form1, form2=form2)

@application.route('/todoist_webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        event = request.get_json()
        todo_event_data = event[event_data]
        if event[event:name] == "item:added"
            new_todo = {}
            project = todo_api.projects.get_by_id(todo_event_data['project_id'])
            new_todo['Task Name'] = todo_event_data['content']
            new_todo['Project'] = todo_event_data[project]
            new_todo['Priority'] = todo_event_data['priority']
            new_todo['Date Created'] = convert_time_to_ISO(todo_event_data['date_added'])
            new_todo['Original Estimate'] = contert_time_to_ISO(todo_event_data['due_date_utc'])
            new_todo['Task ID'] = todo_event_data['id']
            todoist_airtable.insert(new_todo)
        else if event[event:name] == "item:completed"
        else if event[event:name] == "item:updated"
        else if event[event:name] == "item:uncompleted"
        else if event[event:name] == "item:deleted"

        todoist_airtable.insert({'Task Name': 'SUCCESS'})
        print(request.json)
        return '', 200
    else:
        abort(400)

def convert_time_to_ISO(unformatted_time):
    #Converts time from Todoist format to ISO 8601 format for airtable
    #Todoist: Fri 26 Sep 2014 08:25:05 +0000
    #ISO (Airtable): 2017-10-01T23:02:00.000Z
    time_components = unformatted_time.split(' ')
    ISO_time = split[3] + '-' + month_number(split[2]) + '-' + split[1] + 'T' + split[4] + ":.000Z"
    return ISO_time

def month_number(month_string)
    if month_string == 'Jan'
        return 1
    if month_string == 'Feb'
        return 2
    if month_string == 'Mar'
        return 3
    if month_string == 'Apr'
        return 4
    if month_string == 'May'
        return 5
    if month_string == 'Jun'
        return 6
    if month_string == 'Jul'
        return 7
    if month_string == 'Aug'
        return 8
    if month_string == 'Sep'
        return 9
    if month_string == 'Oct'
        return 10
    if month_string == 'Nov'
        return 11
    if month_string == 'Dec'
        return 12
    


@application.route('/todoist_sync', methods=['GET'])
def todo_sync():
    todo_api.sync()
    tasks = todo_api.state['items']
    #for task in tasks



if __name__ == '__main__':
    application.run(host='0.0.0.0')
