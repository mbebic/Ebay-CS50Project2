# Creating a Landing Page in a Django Project

Creating a landing page is relatively simple and the directions are easy to follow! 

The first thing is start by creating a project in anaconda prompt. Keep in mind that you would ideally want to make an environment for the project with all necessary packages downloaded. To create a new environment, follow the How to Set Up a Virtual Environment documentation.

To start a project, run the following line:

```shell
django-admin startproject NAME
```

After the project is created, go to the directory via the <code>cd</code> command. 

```shell
cd NAME
```

Start up a server with the following line:

```shell
python manange.py runserver
```

After going to your local hosted webpage <code>127.0.0.1:8000</code> , a screen will show up with a rocket and a message saying "The install worked successfully! Congratulations!

This is not a landing page though. So, an "app" needs to be made to create dynamic web pages.

We start this by running the following line:

```shell
python manage.py startapp pages
```

When the app is made, we need to add it to Django's <code>INSTALLED_APPS</code>. We write the app name 'pages' at the end of the INSTALLED_APPS block in the project's settings.py file.

