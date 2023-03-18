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

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---

---

<!-- GETTING STARTED -->
## Usage

To use this API, follow these steps:

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


<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/McdaveUmoh/Student-Management-API/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>
