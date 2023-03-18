<a name="readme-top"></a>

<!-- Project Name -->
<div align="center">
  <h1>School Management API</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/McdaveUmoh/Student-Management-API#readme"><strong>Explore the Docs »</strong></a>
    <br />
    <a href="https://github.com/McdaveUmoh/Student-Management-API/issues">Report Bug</a>
    ·
    <a href="https://github.com/McdaveUmoh/Student-Management-API/issues">Observations Feature</a>
  </p>
</div>


<!-- About the Project -->
## About School Management API

 School Management API is a REST API which allows a School Admin to create accounts for both teachers and students account with functionalities for the teacher to create a course, register students for a course, grade the students and the student can login in to change their profile details and view their profile, see their CGPA as well. The app is hosted on heroku to enable you test out all functionalities using Swagger UI. you can visit the API here <a href="https://flask-school-api.herokuapp.com">School Management API</a>.

 Note: This Website was developed with the concept of the Nigerian Army College of Environmental and Science College School Flow, Where the Admin is capable of CRUD Operations for only the Teachers and Students, Then the Teacher is responsible for the CRUD Operations for Courses and Grades. Courses can be created with the list of students appended and can be edited later. To Grade a Student he must be registered in the course.  

### Built With:

[Python]__
[Flask]__
[SQLite]

<p align="right"><a href="#readme-top">back to top</a></p>

---

---

<!-- GETTING STARTED -->
## Usage

To use this API you can use the sample data or follow these steps:

Admin:
{
  "id": 1,
  "username": "dirict",
  "name": "Tony Stark",
  "email": "tony@gmail.com",
  "password": "12345",
  "user_type": "admin"
}

hod:
{
    "id": 2,
    "name": "Ojo Fred",
    "username": "hod1",
    "email": "ojo@gmail.com",
    "password": "12345",
    "user_type": "teacher"
}

student:

{
    "id": 3,
    "name": "Chris Evans",
    "mat_no": "com/101",
    "email": "chris@gmail.com",
    "password": "12345"
}

Course:
{
    "id": 1,
    "name": "com 101",
    "course_unit": 4,
    "teacher_name": "Dr. McDave Umoh",
    "students": [
      3
    ],
    "teacher_id": 2
}


CGPA:
{
  "student_name": "Chris Evans",
  "student_mat_no": "com/101",
  "gpa": 4
}

1. Open the heroku web app on your browser: https://flask-school-api.herokuapp.com/

2. Create an admin or student account:
    - Click 'admin' to reveal a dropdown menu of administration routes, then register an admin account via the '/admin/register' route
    - Click 'students' to reveal a dropdown menu of student routes, then register a student account via the '/students/register' route

3. Sign in via the '/teachers/login' route to generate a JWT token. Copy this access token without the quotation marks

4. Scroll up to click 'Authorize' at top right. Enter the JWT token in the given format, for example:
   ```
   Bearer arandomgeneratedtokenwillbegivenpasteithere
   ```

5. Click 'Authorize' and then 'Close'

6. Now authorized, you can create, view, update and delete students/teachers via the many routes in 'students', 'courses' and 'teachers'. You can also get:
    - All students taking a course
    - A student's CGPA, calculated based on all grades from all courses they are taking

7. To create, view, update and delete Courses/Grades you will be required as the admin to create teachers who will be capable of creating and allocating grades to students

8. When you're done, click 'Authorize' at top right again to then 'Logout'

**Note:** When using this API in production, please [fork this repo](https://github.com/McdaveUmoh/Student-Management-API) and uncomment the `@admin_required()` decorator in line 51 of [the admin views file](https://github.com/McdaveUmoh/Student-Management-API/blob/main/api/admin/views.py). This will ensure that students and other users will not be authorized to access the admin creation route after the first admin is registered.

<p align="right"><a href="#readme-top">back to top</a></p>


## How to Run the Project Locally

Clone the project Repository
```
git clone https://github.com/McdaveUmoh/Student-Management-API.git
```

Enter the project folder and create a virtual environment
``` 
$ cd https://github.com/McdaveUmoh/Student-Management-API
$ python -m venv env 
```

Activate the virtual environment
``` 
$ source env/bin/actvate #On linux Or Unix
$ source env/Scripts/activate #On Windows 
 
```

Install all requirements

```
$ pip install -r requirements.txt
```

Run the project in development
```
$ export FLASK_APP=api/
$ export FLASK_DEBUG=1
$ flask run
```
Or 
``` 
python runserver.py
``` 

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/McdaveUmoh/Student-Management-API/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>
