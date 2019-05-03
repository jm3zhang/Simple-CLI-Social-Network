import mysql.connector
import cmd
import notification
from constant import (
    HOST,
    USER,
    DATABASE,
    PASSWORD,
    PROMPT_NAME,
    POST_TYPE_INITIAL,
    POST_TYPE_RESPONSE,
    POST_TYPE_THUMB,
    THUMB_UP,
    THUMB_DOWN,
    READ_TYPE_ALL,
    READ_TYPE_UNREAD
)
from notification import(
    print_record_already_exist,
    print_record_create_success,
    print_record_create_success_with_id,
    print_error_record_not_found,
    print_error_duplicate_record_found,
    print_error_param_num,
    print_error_not_login,
    print_error_already_followed,
    print_follow_success,
    print_error_not_following,
    print_unfollow_success,
    print_login_success,
    print_logout_success,
    print_join_group_success,
    print_error_already_in_group,
    print_error_not_in_group,
    print_leave_group_success,
    print_error_follow_oneself,
    print_error_invalid_post_type,
    print_error_invalid_thumb_content,
    print_error_already_vote_thumb,
    print_update_thumb_success,
    print_error_invalid_read_type,
    print_already_read_all_topic,
    print_already_read_all_user,
    print_error_read_oneself
)
from helper_func import(
    print_cursor,
    print_post,
    escape_quote
)

class Session(cmd.Cmd):
    prompt = PROMPT_NAME
    def __init__(self):
        super().__init__()
        self.user_id = ""
        self.login_status = False
        self.connection = None

        self.welcome_str = "Welcome to the ece356 project.   Type help to list commands.\n"

    def precmd(self, line):
        self.connect_to_db()
        return escape_quote(line)

    def postcmd(self, stop, line):
        self.connection.commit()
        self.disconnect_db()
        if line == "exit":
            return True
        return False

    def connect_to_db(self):
        self.connection = mysql.connector.connect(
            user=USER,
            database=DATABASE,
            host = HOST,
            password = PASSWORD
        )

    def disconnect_db(self):
        self.connection.close()

    def check_record_exist(self, table, condition):
        cursor = self.connection.cursor()
        query = "select * from {} where {}".format(
            table,
            condition
        )
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def insert_record(self, table, columns, values):
        cursor = self.connection.cursor()
        query = "insert into {} {} VALUES({})".format(
            table,
            columns,
            values
        )
        cursor.execute(query)
        record_id = cursor.lastrowid
        cursor.close()
        return record_id

    def update_record(self, table, column, value, condition):
        cursor = self.connection.cursor()
        query = "update {} set {} = \'{}\' where {}".format(
            table,
            column,
            value,
            condition
        )
        cursor.execute(query)
        record_id = cursor.lastrowid
        cursor.close()
        return record_id

    def remove_record(self, table, condition):
        cursor = self.connection.cursor()
        query = "delete from {} where {}".format(
            table,
            condition
        )
        cursor.execute(query)
        cursor.close()

    def check_exist_thumb_record(self, post_id, user_id):
        cursor = self.connection.cursor()
        query = "select PostRespPost.ResponseID,content from posts inner join postresppost on (Posts.PostID = "\
            "PostRespPost.ResponseID and Type = '{}' and PostRespPost.PostID = {} and Posts.CreatedBy = '{}')".format(
            POST_TYPE_THUMB,
            post_id,
            user_id
        )
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
        
    def query_post_by_topic(self, topic_id, last_read_post_id, read_type):
        cursor = self.connection.cursor()
        query = ""
        if read_type == READ_TYPE_UNREAD:
            query = "select Posts.PostID,Posts.Name as Title,Type,Content,PostUnderTopic.TopicID,Users.Name "\
                "from Posts inner join PostUnderTopic using(PostID) inner join Users on (Posts.CreatedBy = Users.UserID) "\
                "where PostUnderTopic.TopicId = \"{}\" and Posts.PostID > {} and Posts.PostID not in "\
                "(select PostID from Posts inner join UserFollowsUser on (UserFollowsUser.UserID = \"{}\" and "\
                "UserFollowsUser.FollowUserID = Posts.CreatedBy) where PostID <= LastReadPost) order by Posts.PostID desc".format(
                topic_id,
                last_read_post_id,
                self.user_id
            )
        elif read_type == READ_TYPE_ALL:
            query = "select Posts.PostID,Posts.Name as Title,Type,Content,PostUnderTopic.TopicID,Users.Name "\
                "from Posts inner join PostUnderTopic using(PostID) inner join Users on (Posts.CreatedBy = Users.UserID)"\
                "where PostUnderTopic.TopicId = \"{}\" order by Posts.PostID desc".format(
                topic_id
            )
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query_post_by_user(self, user_id, last_read_post_id, read_type):
        cursor = self.connection.cursor()
        query = ""
        if read_type == READ_TYPE_UNREAD:
            query = "select Posts.PostID,Posts.Name as Title,Type,Content,PostUnderTopics.TopicID,Users.Name "\
                "from Posts inner join (select PostID,GROUP_CONCAT(TopicID SEPARATOR ',') as TopicID "\
                "from PostUnderTopic group by PostID) as PostUnderTopics using(PostID) inner join Users on "\
                "(Posts.CreatedBy = Users.UserID) where Posts.CreatedBy =  \"{}\" and Posts.PostID > {} and Posts.PostID not in "\
                "(select PostID from Posts inner join PostUnderTopic using(PostID) inner join UserFollowsTopic on "\
                "(UserFollowsTopic.UserID = \"{}\" and UserFollowsTopic.FollowTopicID = PostUnderTopic.TopicID)"\
                " where PostID <= LastReadPost) order by Posts.PostID desc".format(
                user_id,
                last_read_post_id,
                self.user_id
            )
        elif read_type == READ_TYPE_ALL:
            query = "select Posts.PostID,Posts.Name as Title,Type,Content,PostUnderTopics.TopicID,Users.Name "\
                "from Posts inner join (select PostID,GROUP_CONCAT(TopicID SEPARATOR ',') as TopicID "\
                "from PostUnderTopic group by PostID) as PostUnderTopics using(PostID) inner join Users on "\
                "(Posts.CreatedBy = Users.UserID) where Posts.CreatedBy =  \"{}\" order by Posts.PostID desc".format(
                user_id
            )
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def do_exit(self, arg):
        """
        Command:       exit
        Description:   Exit the command line interface
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        return True

    def do_show_user(self, arg):
        """
        Command:       show_user
        Description:   List out all usernames
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        cursor = self.connection.cursor()
        query = "select * from Users"
        cursor.execute(query)
        print("\nHeader:\n('UserID', 'Name', 'Birthday')\nData:")
        print_cursor(cursor)
        cursor.close()

    def do_login(self, arg):
        """
        Command:       login {UserID}
        Description:   Login with a username
        """
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "UserID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Users", condition)
        if len(result) == 0:
            print_error_record_not_found("Username")
        elif len(result) == 1:
            self.login_status = True
            self.user_id = result[0][0]
            print_login_success(result[0][1])
        else:
            print_error_duplicate_record_found()

    def do_logout(self, arg):
        """
        Command:       logout
        Description:   Logout from current user
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        if self.login_status == False:
            print_error_not_login()
            return
        self.user_id = ""
        self.login_status = False
        print_logout_success()

    def do_create_user(self, arg):
        """
        Command:       create_user {UserID} {Name} {Birthday}(optional)
        Description:   Create a new username
        """
        parameters = arg.split()
        if len(parameters) < 2 or len(parameters) > 3:
            print_error_param_num()
            return
        condition = "UserID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Users", condition)
        if len(result) == 0:
            if len(parameters) == 2:
                values = "\"{}\",\"{}\",NULL".format(
                    parameters[0], 
                    parameters[1]
                )
            elif len(parameters) == 3:
                values = "\"{}\",\"{}\",\"{}\"".format(
                    parameters[0], 
                    parameters[1],
                    parameters[2]
                )
            self.insert_record("Users", "", values)
            print_record_create_success("Username")
        elif len(result) == 1:
            print_record_already_exist("Username")
        else:
            print_error_duplicate_record_found()

    def do_init_post(self, arg):
        """
        Command:       init_post {Title} {TopicID},{TopicID} {Content}
        Description:   Initial a post. Note {TopicID} need to be at least one
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split(' ',2)
        if len(parameters) < 3:
            print_error_param_num()
            return
        topics = set(parameters[1].split(','))
        topic_exists = True
        for _topic in topics:
            condition = "TopicID=\"{}\"".format(
                _topic
            )
            result = self.check_record_exist("Topics", condition)
            if len(result) == 0:
                topic_exists = False
                break
        if not topic_exists:
            print_error_record_not_found("One of the topics is")
        else:
            values = "\"{}\",\"{}\",\"{}\",\"{}\"".format(
                parameters[0],
                POST_TYPE_INITIAL,
                parameters[2],
                self.user_id
            )
            post_id = self.insert_record("Posts", "(Name,Type,Content,CreatedBy)", values)

            for _topic in topics:
                values = "\"{}\",\"{}\"".format(
                    post_id,
                    _topic
                )
                self.insert_record("PostUnderTopic", "", values)
            print_record_create_success_with_id("Post", post_id)

    def do_show_topic(self, arg):
        """
        Command:       show_topic
        Description:   Show all topics
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        cursor = self.connection.cursor()
        query = "select * from Topics"
        cursor.execute(query)
        print("\nHeader:\n('TopicID')\nData:")
        print_cursor(cursor)
        cursor.close()

    def do_create_topic(self, arg):
        """
        Command:       create_topic {TopicID}
        Description:   Create a topic. Note that: {TopicID} will eliminate comma.
        """
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "TopicID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Topics", condition)
        if len(result) == 0:
            values = "\"{}\"".format(
                parameters[0].replace(',','')
            )
            self.insert_record("Topics", "", values)
            print_record_create_success("Topic")
        elif len(result) == 1:
            print_record_already_exist("Topic")
        else:
            print_error_duplicate_record_found()

    def do_follow_topic(self, arg):
        """
        Command:       follow_topic {TopicID}
        Description:   Follow a topic
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "TopicID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Topics", condition)
        if len(result) == 0:
            print_error_record_not_found("Topic")
        elif len(result) == 1:
            condition = "UserID=\"{}\" and FollowTopicID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserFollowsTopic", condition)
            if len(result) == 0:
                values = "\"{}\",\"{}\",NULL".format(
                    self.user_id,
                    parameters[0]
                )
                self.insert_record("UserFollowsTopic", "", values)
                print_follow_success("topic", parameters[0])
            elif len(result) == 1:
                print_error_already_followed(parameters[0])
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_unfollow_topic(self, arg):
        """
        Command:       unfollow_topic {TopicID}
        Description:   Unfollow a topic
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "TopicID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Topics", condition)
        if len(result) == 0:
            print_error_record_not_found("Topic")
        elif len(result) == 1:
            condition = "UserID=\"{}\" and FollowTopicID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserFollowsTopic", condition)
            if len(result) == 0:
                print_error_not_following(parameters[0])
            elif len(result) == 1:
                condition = "UserID=\"{}\" and FollowTopicID=\"{}\"".format(
                    self.user_id,
                    parameters[0]
                )
                self.remove_record("UserFollowsTopic", condition)
                print_unfollow_success("topic", parameters[0])
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_show_group(self, arg):
        """
        Command:       show_group
        Description:   Show all groups
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        cursor = self.connection.cursor()
        query = "select * from UserGroups"
        cursor.execute(query)
        print("\nHeader:\n('GroupID', 'Name', 'CreatedBy')\nData:")
        print_cursor(cursor)
        cursor.close()

    def do_create_group(self, arg):
        """
        Command:       create_group {Name}
        Description:   Create a group
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        values = "\"{}\",\"{}\"".format(
            parameters[0],
            self.user_id
        )
        group_id = self.insert_record("UserGroups", "(Name,CreatedBy)", values)
        print_record_create_success_with_id("Group", group_id)

    def do_join_group(self, arg):
        """
        Command:       join_group {GroupID}
        Description:   Join a groups
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "GroupID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("UserGroups", condition)
        if len(result) == 0:
            print_error_record_not_found("Group")
        elif len(result) == 1:
            group_name = result[0][1]
            condition = "UserID=\"{}\" and GroupID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserJoinGroup", condition)
            if len(result) == 0:
                values = "\"{}\",\"{}\"".format(
                    self.user_id,
                    parameters[0]
                )
                self.insert_record("UserJoinGroup", "", values)
                print_join_group_success(group_name)
            elif len(result) == 1:
                print_error_already_in_group(group_name)
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_leave_group(self, arg):
        """
        Command:       leave_group {GroupID}
        Description:   Leave a group
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "GroupID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("UserGroups", condition)
        if len(result) == 0:
            print_error_record_not_found("Group")
        elif len(result) == 1:
            group_name = result[0][1]
            condition = "UserID=\"{}\" and GroupID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserJoinGroup", condition)
            if len(result) == 0:
                print_error_not_in_group()
            elif len(result) == 1:
                condition = "UserID=\"{}\" and GroupID=\"{}\"".format(
                    self.user_id,
                    parameters[0]
                )
                self.remove_record("UserJoinGroup", condition)
                print_leave_group_success(group_name)
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_follow_user(self, arg):
        """
        Command:       follow_user {UserID}
        Description:   Follow a user (cannot follow yourself)
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        if parameters[0] == self.user_id:
            print_error_follow_oneself()
            return
        condition = "UserID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Users", condition)
        if len(result) == 0:
            print_error_record_not_found("User")
        elif len(result) == 1:
            user_name = result[0][1]
            condition = "UserID=\"{}\" and FollowUserID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserFollowsUser", condition)
            if len(result) == 0:
                values = "\"{}\",\"{}\",NULL".format(
                    self.user_id,
                    parameters[0]
                )
                self.insert_record("UserFollowsUser", "", values)
                print_follow_success("user", user_name)
            elif len(result) == 1:
                print_error_already_followed(user_name)
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_unfollow_user(self, arg):
        """
        Command:       unfollow_user {UserID}
        Description:   Unfollow a user
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 1:
            print_error_param_num()
            return
        condition = "UserID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Users", condition)
        if len(result) == 0:
            print_error_record_not_found("User")
        elif len(result) == 1:
            user_name = result[0][1]
            condition = "UserID=\"{}\" and FollowUserID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserFollowsUser", condition)
            if len(result) == 0:
                print_error_not_following(parameters[0])
            elif len(result) == 1:
                condition = "UserID=\"{}\" and FollowUserID=\"{}\"".format(
                    self.user_id,
                    parameters[0]
                )
                self.remove_record("UserFollowsUser", condition)
                print_unfollow_success("user", user_name)
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_reply_post(self, arg):
        """
        Command:       reply_post {PostID} {Type}(response/thumb) {Content}
        Description:   Reply to a post. Note {Content} is any string if 
                       response; 'up'/'down' if thumb
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split(' ',2)
        condition = "PostID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Posts", condition)
        if len(result) == 0:
            print_error_record_not_found("Post")
        elif len(result) == 1:
            original_post_id = result[0][0]
            original_post_name = result[0][1]
            if parameters[1] == POST_TYPE_RESPONSE:
                values = "\"{}\",\"{}\",\"{}\",\"{}\"".format(
                    original_post_name,
                    POST_TYPE_RESPONSE,
                    parameters[2],
                    self.user_id
                )
                post_id = self.insert_record("Posts", "(Name,Type,Content,CreatedBy)", values)
                values = "\"{}\",\"{}\"".format(
                    original_post_id,
                    post_id
                )
                self.insert_record("PostRespPost", "", values)
                condition = "PostID=\"{}\"".format(
                    parameters[0]
                )
                result = self.check_record_exist("PostUnderTopic", condition)
                for item in result:
                    values = "\"{}\",\"{}\"".format(
                        post_id,
                        item[1]
                    )
                    self.insert_record("PostUnderTopic", "", values)
                print_record_create_success_with_id("Response post", post_id)
            elif parameters[1] == POST_TYPE_THUMB:
                if not (parameters[2] == THUMB_UP or parameters[2] == THUMB_DOWN):
                    print_error_invalid_thumb_content()
                    return
                result = self.check_exist_thumb_record(original_post_id, self.user_id)
                if len(result) == 0:
                    values = "\"{}\",\"{}\",\"{}\",\"{}\"".format(
                        original_post_name,
                        POST_TYPE_THUMB,
                        parameters[2],
                        self.user_id
                    )
                    post_id = self.insert_record("Posts", "(Name,Type,Content,CreatedBy)", values)
                    values = "\"{}\",\"{}\"".format(
                        original_post_id,
                        post_id
                    )
                    self.insert_record("PostRespPost", "", values)
                    condition = "PostID=\"{}\"".format(
                        parameters[0]
                    )
                    result = self.check_record_exist("PostUnderTopic", condition)
                    for item in result:
                        values = "\"{}\",\"{}\"".format(
                            post_id,
                            item[1]
                        )
                        self.insert_record("PostUnderTopic", "", values)
                    print_record_create_success_with_id("Response post", post_id)
                elif len(result) == 1:
                    thumb_id = result[0][0]
                    thumb_content = result[0][1]
                    if parameters[2] == thumb_content:
                        if thumb_content == THUMB_UP:
                            print_error_already_vote_thumb(THUMB_UP, original_post_id)
                        elif thumb_content == THUMB_DOWN:
                            print_error_already_vote_thumb(THUMB_DOWN, original_post_id)
                    else:
                        condition = "PostID = {}".format(
                            thumb_id
                        )
                        self.update_record("Posts", "Content", parameters[2], condition)
                        print_update_thumb_success(parameters[2], original_post_id)
                else:
                    print_error_duplicate_record_found()
            else:
                print_error_invalid_post_type()
        else:
            print_error_duplicate_record_found()

    def do_show_follow_user(self, arg):
        """
        Command:       show_follow_user
        Description:   Show all users you are following
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        if self.login_status == False:
            print_error_not_login()
            return
        cursor = self.connection.cursor()
        query = "select * from UserFollowsUser where UserID = \"{}\"".format(
            self.user_id
        )
        cursor.execute(query)
        print("\nlist of user id you are currently following:\n")
        print_cursor(cursor, 1)
        cursor.close()

    def do_show_follow_topic(self, arg):
        """
        Command:       show_follow_topic
        Description:   Show all topics you are following
        """
        if len(arg) != 0:
            print_error_param_num()
            return
        if self.login_status == False:
            print_error_not_login()
            return
        cursor = self.connection.cursor()
        query = "select * from UserFollowsTopic where UserID = \"{}\"".format(
            self.user_id
        )
        cursor.execute(query)
        print("\nlist of topic id you are currently following:\n")
        print_cursor(cursor, 1)
        cursor.close()

    def do_read_topic(self, arg):
        """
        Command:       read_topic {TopicID} {Type}(all/unread)
        Description:   Read all unread posts by followed topic
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 2:
            print_error_param_num()
            return
        if not (parameters[1] == READ_TYPE_ALL or parameters[1] == READ_TYPE_UNREAD):
            print_error_invalid_read_type()
            return
        condition = "TopicID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Topics", condition)
        if len(result) == 0:
            print_error_record_not_found("Topic")
        elif len(result) == 1:
            condition = "UserID=\"{}\" and FollowTopicID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserFollowsTopic", condition)
            if len(result) == 0:
                print_error_not_following(parameters[0])
            elif len(result) == 1:
                last_read_post_id = result[0][2]
                if last_read_post_id is None:
                    last_read_post_id = -1
                result = self.query_post_by_topic(parameters[0], last_read_post_id, parameters[1])
                if len(result) == 0:
                    print_already_read_all_topic(parameters[0])
                else:
                    print_post(result)
                    condition = "UserID=\"{}\" and FollowTopicID=\"{}\"".format(
                        self.user_id,
                        parameters[0]
                    )
                    self.update_record("UserFollowsTopic", "LastReadPost", result[0][0], condition)
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()

    def do_read_user(self, arg):
        """
        Command:       read_user {UserID} {Type}(all/unread)
        Description:   Read all unread posts by a followed user (cannot read yourself)
        """
        if self.login_status == False:
            print_error_not_login()
            return
        parameters = arg.split()
        if len(parameters) != 2:
            print_error_param_num()
            return
        if parameters[0] == self.user_id:
            print_error_read_oneself()
            return
        if not (parameters[1] == READ_TYPE_ALL or parameters[1] == READ_TYPE_UNREAD):
            print_error_invalid_read_type()
            return
        condition = "UserID=\"{}\"".format(
            parameters[0]
        )
        result = self.check_record_exist("Users", condition)
        if len(result) == 0:
            print_error_record_not_found("User")
        elif len(result) == 1:
            condition = "UserID=\"{}\" and FollowUserID=\"{}\"".format(
                self.user_id,
                parameters[0]
            )
            result = self.check_record_exist("UserFollowsUser", condition)
            if len(result) == 0:
                print_error_not_following(parameters[0])
            elif len(result) == 1:
                last_read_post_id = result[0][2]
                if last_read_post_id is None:
                    last_read_post_id = -1
                result = self.query_post_by_user(parameters[0], last_read_post_id, parameters[1])
                if len(result) == 0:
                    print_already_read_all_user(parameters[0])
                else:
                    print_post(result)
                    condition = "UserID=\"{}\" and FollowUserID=\"{}\"".format(
                        self.user_id,
                        parameters[0]
                    )
                    self.update_record("UserFollowsUser", "LastReadPost", result[0][0], condition)
            else:
                print_error_duplicate_record_found()
        else:
            print_error_duplicate_record_found()