import zmq
import pytz
import datetime as dt

# ZeroMQ setup
print("Connecting server.")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print("Server connected successfully.")

def set_timezone(task, target_timezone, original_timezone):
    # original time (naive: no timezone attached)
    naive_time = dt.datetime.strptime(task["timestamp"], "%Y-%m-%d %H:%M:%S")
    original_tz = pytz.timezone(original_timezone)
    target_tz = pytz.timezone(target_timezone)

    # attach the original timezone to the naive time
    original_time = original_tz.localize(naive_time)

    # convert to the target timezone
    target_time = original_time.astimezone(target_tz)

    # place target timezone as string in the task object for easy readability.
    task["timestamp"] = target_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return task


def setup_new_timezone(request):
    # load all the information from the request into variables
    tasks = request["tasks"]
    target_timezone = request["target_timezone"]
    original_timezone = request["original_timezone"]
    apply_to_all = request["apply_to_all"]
    task_id = request["task_id"]

    # if tasks was empty
    if tasks is None:
        return {"error": "No tasks provided"}

    # if requested to change all tasks' timezones
    if apply_to_all is True:
        updated_tasks = [set_timezone(task, target_timezone, original_timezone) for task in tasks]
        return {"tasks": updated_tasks}

    # if requested to change just 1 task's timezone
    else:
        task_to_change = None
        for task in tasks:
            if task["task_id"] == task_id:
                task_to_change = task
                break

        # if task was not found
        if task_to_change is None:
            return {"error": "Task ID was wrong or does not exist"}

        # if task was found, change the timezone of it
        updated_task = set_timezone(task_to_change, target_timezone, original_timezone)
        return {"task": updated_task}


# loop to see if a request was sent
while True:
    print("Waiting for request from client...")
    request = socket.recv_json()
    print("Request received. Changing timezone(s) now.")
    response = setup_new_timezone(request)
    print("Sending response back to client.")
    socket.send_json(response)