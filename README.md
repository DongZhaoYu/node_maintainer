# Node Maintainer

To maintain a node in a proper status. Usually it may need some real time maintenance. This is usually achieved by monitoring some conditions. When the condition cannot be kept it will trigger some action to repair or mitigate the situation. Node mainter is a framework to ease such things.

## usage

```pydocstring
python maintainer.py {clean} [options]
```

### supported subcommand

#### clean
this will clean the cached temporary data in the node
```pydocstring
python ./maintainer.py clean [--host host_name] [--user user_name] [--passwrd  password]
```
If the host name, user name or the password is not provided in the command. The configured value in the configure file will be used.
