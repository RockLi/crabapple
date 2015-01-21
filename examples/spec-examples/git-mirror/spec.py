# Syntax version of this spec file
syntax_version = '1.0'

# Name of your project
name = 'demo'

# Repo URL of Github
repo_url = 'http://github.com/demo/demo'

# Watched Branches
watched_branches = ['master']

# Notifiers: email, irc
notifiers = []


# Called when we try to run the testing
def _on_test():
    pass

on_test = _on_test

# Timeout for one deployment, 0 means no limitations
test_timeout = 0


# Triggered when try to do the deployment
def _on_deploy():
    # Non-zero and not None means the deployment is failed
    return crabapple_run_shell_script('./scripts/mirror.sh')

on_deploy = _on_deploy

# Timeout for one deployment, 0 means no limitations
deploy_timeout = 0
