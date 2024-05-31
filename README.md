# blog_website
Blog Website

**ADDED FEATURES:**
1. Profile View
2. Edit Profile Form
3. Change Password feature
4. Date-Time added in Blogs
5. Blog connected to Users through Author Field
6. **Contact page view **to send mail via django smtp




Backend Framework: `Django`
<br/><br/>
Front-end : `Bootstrap, SCSS, HTML,CSS, Javascript`
<br/><br/>
Database: `Sqlite3`
<br/><br/>

### Installation

1. Install all the requirements

   ```bash
   pip install -r requirements.txt
   ```

    ```bash
   cd socials
   ```


2. Make migrations/ Create db.sqlite3

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a super user.
   This is to access Admin panel and admin specific pages.

   ```djangotemplate
   python manage.py createsuperuser
   ```
   

   Enter your username, email and password.

4. Run server
   ```bash
   python manage.py runserver
