# Blog

this web app it's just a tutorial to train on Flask framework in web by Python Programming language



what i learn from

- send mails
- divide the whole project to some modules
- how to deal with static files
- how to deal with images in flask
- make base template and make all templates inherit from it
- flash messages



to install and run the project:

1. if you don't have Python first install it and add it to the path then go to the next

2. install all modules in requirements.txt file in the project as: 

   - pip install -r requirements.txt 

3. go to the project files open cmd there and type the following code in the console:

   ```python
   # open flask shell
   flask shell
   ```

   ```python
   # in python shell write that
   # to create the physical database
   import db from appname.db
   db.create_all()
   ```

4. go to Gmail to set up it to send emails

   1. go to Gmail application and search for app passwords then create new one
   2. go to conifg.py file, edit MAIL_USERNAME to your email MAIL_PASSWORD to password that you generate from gmail

5. install all modules needed to run the project

   ```shell
   # open cmd and write
   pip install -r requirements.txt
   ```

6. run the project

   ```shell
   # open cmd and write 
   py app.py
   ```

and then go to your browser and go to localhost on port 8000 then you can access the app

