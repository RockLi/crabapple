Crabapple
========

A highly configurable automatic deployment tool integrated with Github. It has limited features and supposed to be used by startups and small organizations.

Mission
========

To simplify your deployment at the early stage of your business and make you focused on building your products. 

Status
=======

~~IDEA~~ -> ~~POC~~ -> **Alpha** 

Read more about our definition of status at [starfruit.io](http://blog.starfruit.io/definition-of-status).


Main Features
=======

* Integrated with Github
* Highly Configurable
* Admin UI
* Docker Supported
* Builtin deployment templates to simplify your deployment
* Notification
* Friendly with your existing tool

Workflow Overview
====

![Crabapple](http://code-trick.com/assets/images/crabapple.png)


Installation
====

1. Install crabapple

   ```pip install crabapple```

   If you cloned the repo manually, you can run ```pip install -U .``` to install *crabapple*.


2. Prepare spec for your project

   ```crabapple new --name demo```

   This command will generate a skeleton spec for your project under current folder, tweak that file to match your requirements.

   ```
   $ tree demo

     demo
     └── spec
   ```

3. Start crabapple in your server to monitor events from Github

   ```crabapple server --host 0.0.0.0 --port 50000 --spec demo/spec```

   This command will listen at port 50000 and do the auto deployment in terms of the ```spec```.

   If you want it go to the background, run with ```--daemon```.

4. Add a webhook to your Github Repo

   Go to the settings page of your repo, add a webhook, content-type should be ```application/json```.

   URL similiar to: ```http://xxx.xxx.xxx.xxx:50000/github/event_handler```

5. Test it and have fun

   Push something to your master branch and see what's happening.

Usage
=====

```crabapple subcommand [args]```

Use ```crabapple help subcommand``` to show the detailed explaination for specific command.

1. new

   This subcommand is used to generate a skeleton deploymeny project, as the optional, you can choose which template to use.
   The templates there are designed to follow the best practise of the deployment of that specific application to simplify your life.

   Parameters List:

   ```
   --name name      : Project name
   [--template tpl] : Template to use
                      django
                      flask
                      tornado

   ```

   Examples:

   ```crabapple new --name myproj``` Use generic template to generate the spec file

   ```crabapple new --name myproj --template django``` Use django template to generate the spec file

2. server

   This subcommand will launch a HTTP server to monitor events from Github and take actions in terms of your spec.
   Parameters List:

   ```
   -c, --config : Load options from the configuration file
   -h, --host   : Host to bind
   -p, --port   : Port to listen
   -d, --daemon : Run in the background or not
   -s, --spec   : Which spec to use
   --admin      : Enable the Admin UI
   --logdir     : Directory to put all the logs
   --datadir    : Directory To store all the persistent data
   --store      : Persistent way, default to sqlite 
   ```

   Examples:

   ```crabapple server --host 0.0.0.0 --port 50000 --daemon --spec myproj/spec```
   
   ```crabapple server --config some_config_file```

3. deploy

   This subcommand will do the real deployment by following your deployment spec. It's also used by the ```crabapple server``` to do the automatic deployment.

   Parameters List:

   ```
   -s, --spec  : Spec file to use
   ```

   Examples:

   ```crabapple deploy --spec myproj/spec```


Deployment Spec
=====

**Crabapple** heavily used this spec to various kinds of stuff. The syntax of it is **Python** which means you can write any custom functions to extend what you want. Please checkout examples under folder ```examples```.

Simple Example:
```
# Syntax version of this spec file
syntax_version = '1.0'

# Name of your project
name = 'demo'

# Repo URL of Github
repo_url = 'http://github.com/demo/demo'

# Watched Branches, pushes to these branches will trigger the deployment
watched_branches = ['master']

# Notifiers: email, irc
# notifiers = ['email']

# Email notifier
# notifier_email = {
#     'sender': {
#         'protocol': 'SMTP',
#         'host': 'smtp.gmail.com',
#         'port': 587,
#         'user': 'demo@example.com',
#         'password': '******',
#     },
#     'recipients': ['demo@example.com']
#}

# Called when we try to run the testing
def _on_test():
    # Non-zero and not None means the testing is failed
    print 'run my tests'

on_test = _on_test

# Timeout for one deployment, 0 means no limitations
test_timeout = 0

# Triggered when try to do the deployment
def _on_deploy():
    # Non-zero and not None means the deployment is failed
    print 'run my deployment'

on_deploy = _on_deploy

# Timeout for one deployment, 0 means no limitations
deploy_timeout = 0

```


About
=====

An opensource project released by [Starfruit.io](starfruit.io). We build reuseable open source project for startups. 

Donate
======

Feel free to buy us a cup of coffee to encourge us to deliver better open source projects.  


