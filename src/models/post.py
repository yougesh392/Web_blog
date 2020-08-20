from src.common.database import Database
import uuid  # for unique identifier
import datetime


class Post(object):
    def __init__(self, blog_id, title, content, author,
                 created_date=datetime.datetime.utcnow(), _id=None):  # default parameter will be at end
        """
        constrictor for the class
        """
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id  # uuid module uuid4 to generate random uuid .hex 32 bit string

        # post = Post(blog_id = "123", title = "a tite", content = "some content", author = "jose")

    def save_to_mongo(self):
        Database.insert(collection="posts", data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return cls(**post_data)
        """     same as returns an object 
                cls(blog_id=post_data['blog_id'],
                   title=post_data['title'],
                   content=post_data['content'],
                   author=post_data['author'],
                   created_date=['created_date'],
                   _id=post_data['_id'])"""

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
