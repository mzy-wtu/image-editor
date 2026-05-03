from app import db
from datetime import datetime

class ImageRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    image_type = db.Column(db.String(20), nullable=False)
    prompt = db.Column(db.Text, nullable=True)
    api_choice = db.Column(db.String(20), nullable=False)
    original_image = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)
    result_image = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    file_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 新增高级参数字段
    size = db.Column(db.String(20), default="1024*1536")
    negative_prompt = db.Column(db.Text, nullable=True)
    seed = db.Column(db.Integer, nullable=True)
    generation_count = db.Column(db.Integer, default=1)
    
    user = db.relationship("User", backref=db.backref("images", lazy="dynamic"))
    
    def to_dict(self):
        import base64
        result_image_b64 = base64.b64encode(self.result_image).decode("utf-8") if self.result_image else None
        original_image_b64 = base64.b64encode(self.original_image).decode("utf-8") if self.original_image else None
        
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_type": self.image_type,
            "prompt": self.prompt,
            "api_choice": self.api_choice,
            "result_image": f"data:image/png;base64,{result_image_b64}" if result_image_b64 else None,
            "original_image": f"data:image/png;base64,{original_image_b64}" if original_image_b64 else None,
            "file_path": self.file_path,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "size": self.size,
            "negative_prompt": self.negative_prompt,
            "seed": self.seed,
            "generation_count": self.generation_count
        }
