![logo](https://user-images.githubusercontent.com/36375214/40588957-3674c082-61ee-11e8-9f24-197d6e2a33a7.png)

[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/Naereen/ama) [![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://bitbucket.org/lbesson/ansi-colors) [![Build Status](https://travis-ci.org/dalaineme/m-tracker.svg?branch=develop-api)](https://travis-ci.org/dalaineme/m-tracker) [![Coverage Status](https://coveralls.io/repos/github/dalaineme/m-tracker/badge.svg?branch=develop-api)](https://coveralls.io/github/dalaineme/m-tracker?branch=develop-api) ![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)

Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

**TL;DR** [View a live demo of the UI](https://dalaineme.github.io/m-tracker/) **or** [Check out the Pivotal Tracker Board](https://www.pivotaltracker.com/n/projects/2173228) **or** [Check out the heroku link.](https://dc-the-m-tracker.herokuapp.com)

#### Log in as Admin

> Email: **admin@admin.com** > **Any random password will work**

#### :computer: Desktop, Tablet and :iphone: Mobile Responsive

![the_tracker](https://user-images.githubusercontent.com/36375214/40584974-6ae25d60-61b3-11e8-93a3-ec4c17f45076.gif)

## UI Pages

* **Admin Pages**
  * [Admin can login.](https://dalaineme.github.io/m-tracker/UI/login.html)
  * [Admin can view all maintenance/repair requests.](https://dalaineme.github.io/m-tracker/UI/admin/index.html)
  * [Admin can filter maintenance/repair requests.](https://dalaineme.github.io/m-tracker/UI/admin/index.html)
  * [Admin can approve/reject maintenance/repair requests.](https://dalaineme.github.io/m-tracker/UI/admin/index.html)
  * [Admin can resolve active maintenance/repair requests.](https://dalaineme.github.io/m-tracker/UI/admin/index.html)
* **User Pages**
  * [A user can Signup.](https://dalaineme.github.io/m-tracker/UI/signup.html)
  * [A user can Login.](https://dalaineme.github.io/m-tracker/UI/login.html)
  * [A user can make maintenance/repair requests.](https://dalaineme.github.io/m-tracker/UI/user/index.html)
  * [A user can view their maintenance/repair requests.](https://dalaineme.github.io/m-tracker/UI/user/index.html)
  * [A user can view feedback.](https://dalaineme.github.io/m-tracker/UI/user/index.html)

## API Endpoints

| Endpoint                      | Functionality             | HTTP method |
| ----------------------------- | ------------------------- | ----------- |
| /api/v1/users/register        | Register a user           | POST        |
| /api/v1/users/login           | Log in a user             | POST        |
| /api/v1/logout                | Log out a user            | POST        |
| /api/v1/requests              | Create a request          | POST        |
| /api/v1/requests              | Get all users reqeusts    | GET         |
| /api/v1/requests/_request_id_ | Get request by request_id | GET         |
| /api/v1/requests/_request_id_ | Edit a request            | PUT         |
| /api/v1/requests/_request_id_ | Delete a request          | DELETE      |

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

Clone the repo.

```
$ git clone https://github.com/dalaineme/m-tracker.git
```

Change directory into the Project folder.

```
$ cd m-tracker
```

Launch the UI by opening **_index.html_**.

## Built With

* [HTML](https://www.w3.org/html/) - The Scripting language used.
* [CSS](https://www.w3.org/Style/CSS/Overview.en.html)
* [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript/)

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/dalaineme) [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

* **Dalin Oluoch** :feelsgood:

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/dalaineme/m-tracker/blob/master/LICENSE) file for details
