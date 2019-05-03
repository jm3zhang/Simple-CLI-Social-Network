from constant import (
    POST_TYPE_INITIAL,
    POST_TYPE_RESPONSE,
    POST_TYPE_THUMB
)

def print_cursor(cursor, index=None):
    row = cursor.fetchone()
    while row is not None:
        if index is None:
            print(row)
        else:
            print(row[index])
        row = cursor.fetchone()
    print("\n")

# +--------+---------+----------+------------------+-----------+--------+
# | PostID | Title   | Type     | Content          | topicid   | Name   |
# +--------+---------+----------+------------------+-----------+--------+
# |     27 | ti      | thumb    | down             | test_topic | edward |
# |     26 | ti      | response | this             | test_topic | edward |
# |     25 | titleee | response | this is a reply? | test_topic | edward |
# |     23 | titleee | initial  | haha             | test_topic | edward |
# |     18 | title   | initial  | content          | test_topic | edward |
# +--------+---------+----------+------------------+-----------+--------+
# (23, 'titleee', 'initial', 'haha', 'test_topic', 'edward')
def print_post(result):
    for post in result:
        if post[2] == POST_TYPE_INITIAL:
            print(
                "\n{} created a new post (PostID: {}) under topic: {}\nTitle: {}\nContent: {}\n".format(
                    post[5],
                    post[0],
                    post[4],
                    post[1],
                    post[3]
                )
            )
        elif post[2] == POST_TYPE_RESPONSE:
            print(
                "\n{} responsed to post \"{}\" (PostID: {}) under topic: {}\nResponse: {}\n".format(
                    post[5],
                    post[1],
                    post[0],
                    post[4],
                    post[3]
                )
            )
        elif post[2] == POST_TYPE_THUMB:
            print(
                "\n{} voted a thumb {} to post \"{}\" (PostID: {}) under topic: {}\n".format(
                    post[5],
                    post[3],
                    post[1],
                    post[0],
                    post[4]
                )
            )

def escape_quote(string):
    return string.replace('"','\\"')