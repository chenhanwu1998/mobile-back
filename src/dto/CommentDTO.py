from datetime import datetime

from src.entity.Comment import Comment


class CommentDTO(Comment):
    def __init__(self, comment_id=None, comment_content=None, user=None, article_id=None, update_time: datetime = None,
                 to_user: str = None, comment_status: str = None, user_photo: str = None):
        super().__init__(comment_id, comment_content, user, article_id, update_time, to_user, comment_status)
        self.user_photo = user_photo
