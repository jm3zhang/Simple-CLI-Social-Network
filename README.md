# uw-ECE356-project

Make sure you have python3 installed.

Install dependencies using pip3 install -r requirements.txt

To build database with sample data, open connection to your local database and source database_setup.sql

All constants for database connection is in the constant.py file. If there is additional variable needed, modify connect_to_db() in session.py

Make sure your mysql version supports aggregation function GROUP_CONCAT()

To execute the command line interface, run python3 main.py




You can type "help" to view all available commands. All commands are also listed below.

Note that all commands are case-sensitive


Here is a list of all the commands available:

    show_user: List all users

    login {UserID}: Login with a user ID

    create_user {UserID} {Name} {Birthday}(optional): Create a new user

    show_topic: Show all topics
    
    create_topic {TopicID}: Create a topic. Note that: {TopicID} will not accept comma, comma is used as a separator for topics.

    show_group: Show all groups

    exit: Exit the command line interface
    

Following commands requires user to login using login {UserID}

    init_post {Title} {TopicID},{TopicID} {Content}: Initial a post. Note {TopicID} need to be at least one

    reply_post {PostID} {Type}(response/thumb) {Content}: Reply to a post. Note {Content} is any string if response; 'up'/'down' if thumb

    read_user {UserID} {Type}(all/unread): Read all or unread posts by a followed user (cannot read yourself)

    read_topic {TopicID} {Type}(all/unread): Read all or unread posts by followed topic

    show_follow_user: Show all users you are following
    
    follow_user {UserID}: Follow a user (cannot follow yourself)

    unfollow_user {UserID}: Unfollow a user

    show_follow_topic: Show all topics you are following

    follow_topic {TopicID}: Follow a topic

    unfollow_topic {TopicID}: Unfollow a topic

    create_group {Name}: Create a group

    join_group {GroupID}: Join a groups

    leave_group {GroupID}: Leave a group

    logout: Logout from current user

Following are the sample commands to create sample data (equivalent to the query provided for sample data in database_setup.sql):
    
    create_user tuser1 testuser1 1990-01-23

    create_user tuser2 testuser2 1990-04-05

    create_topic testtopic1

    create_topic testtopic2

    login tuser1

    create_group testgroup

    init_post testtitle testtopic1,testtopic2 testcontent

    follow_user tuser2

    follow_topic testtopic1

    reply_post 1 response testresponse

    reply_post 1 thumb up

    join_group 1

    login tuser2

    join_group 1

    reply_post 1 response testresponse

    logout

    exit
