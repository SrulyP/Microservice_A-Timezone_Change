# Communication Contract


**A.** To programmatically request data from the microservice by using the ZeroMQ API request socket, you import the ZeroMQ module by using "import zmq". Then, you create the connection with the microservice. This is done by creating the context and socket. The following code shows how to do set up the connection:
```python
      import zmq
      context = zmq.Context()
      socket = context.socket(zmq.REQ)
      socket.connect("tcp://localhost:5555")
``` 
Once the connection is made, you create a request object using all the parameters needed for the microservice, including the list containing the tasks objects, target timezone, original timezone, and a boolean value of whether to apply the timezone change to all tasks, and lastly, a task ID if apply_to_all has a False value. When the ID is not inputted, the ID is automatically read as None and will raise an error if apply_to_all is False. The following code is an example of how the request parameters look within the example timezonechange function (this is not the full function):

```python
      def timezonechange(tasks, target_timezone, original_timezone, apply_to_all, task_id=None):
          request = {
              "tasks": tasks,
              "target_timezone": target_timezone,
              "original_timezone": original_timezone,
              "apply_to_all": apply_to_all,
              "task_id": task_id
          }
```
An example of a request call is shown below:
```python
      # example tasks list containing 2 task objects.
      tasks = [
          {"task_id": "1234", "timestamp": "2024-11-17 12:00:00"},
          {"task_id": "5678", "timestamp": "2024-11-17 15:00:00"}
      ]

      # request for timezone change one task. In this example, it is for the first task, which has the ID "1234".
      request = timezonechange(tasks, "Asia/Tokyo", "America/Los_Angeles", False, "1234")

      # request for timezone change for both tasks in the list. As you see, no ID is attached, but apply_to_all is True.
      request = timezonechange(tasks, "Africa/Accra", "America/Los_Angeles", True)
```         
After you created the request object, you send it over to the microservice using the ZeroMQ send command:

```python
          socket.send_json(request).
```

**B.** Once the microservice receives the request, it sends back a response if the change was successful and the task(s) changed, or an error message if it was not successful. To read the response, within your program you will use the ZeroMQ receive command and then you can just return the response, as shown below.
```python
    response = socket.recv_json().
    return response
```

**C.** UML sequence diagram:
![Screenshot 2024-11-18 161351](https://github.com/user-attachments/assets/034d32db-2779-4078-a432-cefacea83d47)


