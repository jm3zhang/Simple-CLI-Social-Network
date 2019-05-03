from constant import (
    POST_TYPE_RESPONSE,
    POST_TYPE_THUMB,
    THUMB_UP,
    THUMB_DOWN,
    READ_TYPE_UNREAD,
    READ_TYPE_ALL
)

def print_record_already_exist(record_type):
    print("\n{} already exists.\n".format(record_type))

def print_record_create_success(record_type):
    print("\n{} creates successfully.\n".format(record_type))

def print_record_create_success_with_id(record_type, record_id):
    print("\n{} created successfully with ID: {}.\n".format(record_type, record_id))

def print_error_record_not_found(record_type):
    print("\n{} not found.\n".format(record_type))

def print_error_duplicate_record_found():
    print("\nFound duplicated record on primary key. Something is wrong.\n")

def print_error_param_num():
    print("\nWrong number of parameters.\n")

def print_error_not_login():
    print("\nYou are not logged in\n")

def print_error_already_followed(name):
    print("\nYou have already followed {}.\n".format(name))

def print_follow_success(record_type, record_name):
    print("\nFollow {} {} successfully.\n".format(record_type, record_name))

def print_error_not_following(name):
    print("\nYou are not currently following {}.\n".format(name))

def print_unfollow_success(record_type, record_name):
    print("\nUnfollow {} {} successfully.\n".format(record_type, record_name))

def print_login_success(username):
    print("\nYou have logged in as: {}\n".format(username))

def print_logout_success():
    print("\nLogout successfully.\n")

def print_join_group_success(group_name):
    print("\nJoin group {} successfully.\n".format(group_name))

def print_error_already_in_group(group_name):
    print("\nYou are already in the group {}.\n".format(group_name))

def print_error_not_in_group():
    print("\nYou are not currently in this group.\n")

def print_leave_group_success(group_name):
    print("\nLeave group {} successfully.\n".format(group_name))

def print_error_follow_oneself():
    print("\nYou cannot follow yourself\n")

def print_error_invalid_post_type():
    print(
        "\nType of this post is not valid. It only supports '{}' or '{}'\n".format(
            POST_TYPE_RESPONSE,
            POST_TYPE_THUMB
        )
    )

def print_error_invalid_thumb_content():
    print(
        "\nContent of thumb is not valid. It only supports '{}' or '{}'\n".format(
            THUMB_UP,
            THUMB_DOWN
        )
    )

def print_error_already_vote_thumb(thumb_type, post_id):
    print(
        "\nYou already vote thumb {} on post {}\n".format(
            thumb_type,
            post_id
        )
    )

def print_update_thumb_success(thumb_type, post_id):
    print(
        "\nSuccessfully update your vote to thumb {} on post {}\n".format(
            thumb_type,
            post_id
        )
    )

def print_error_invalid_read_type():
    print(
        "\nType of this read is not valid. It only supports '{}' or '{}'\n".format(
            READ_TYPE_UNREAD,
            READ_TYPE_ALL
        )
    )

def print_already_read_all_topic(topic_name):
    print(
        "\nYou have already read all posts under topic id {}\n".format(
            topic_name
        )
    )

def print_already_read_all_user(user_id):
    print(
        "\nYou have already read all posts from user id {}\n".format(
            user_id
        )
    )

def print_error_read_oneself():
    print("\nYou cannot read yourself\n")