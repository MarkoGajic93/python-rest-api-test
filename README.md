Usage:
- create config.ini file that contains:
  [email]
  gmail_username=your@email.com
  gmail_app_password=your app password
- place that file into config package
- paste the path to config.ini file into the config.read method (in the init method of service.notifier.EmailNotifier)
