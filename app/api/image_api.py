from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import base64
import io
from app import db
from app.utils.image_generator import APIFactory
from app.models.image_record import ImageRecord

image_bp = Blueprint("image_api", __name__)

@image_bp.route("/api/generate", methods=["POST"])
@login_required
def generate_image():
    data = request.get_json()
    if not data or "prompt" not in data or "api_choice" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = data["prompt"]
    api_choice = data["api_choice"]
    
    # 新增：接收高级参数
    count = data.get("count", 1)
    size = data.get("size", "1024*1536")
    negative_prompt = data.get("negativePrompt", "")
    seed = data.get("seed", None)
    
    # 限制生成数量
    count = min(max(1, count), 4)
    
    images = []
    all_logs = []
    
    # 循环生成多张图像
    for i in range(count):
        api = APIFactory.get_api(api_choice)
        result = api.generate_image(
            prompt, 
            api_choice,
            size=size,
            negative_prompt=negative_prompt,
            seed=seed
        )
        
        if isinstance(result, tuple) and len(result) == 2:
            image_data, logs = result
        else:
            image_data, logs = result, []
        
        if image_data:
            images.append(image_data)
            all_logs.extend(logs)
            
            # 保存到数据库
            image_bytes = base64.b64decode(image_data.split(",")[1])
            record = ImageRecord(
                user_id=current_user.id,
                image_type="generate",
                prompt=prompt,
                api_choice=api_choice,
                result_image=image_bytes,
                size=size,
                negative_prompt=negative_prompt,
                seed=seed,
                generation_count=count
            )
            db.session.add(record)
    
    db.session.commit()
    
    # 返回图像数组（兼容前端）
    return jsonify({"images": images, "image": images[0] if images else None, "logs": all_logs}), 200

@image_bp.route("/api/edit", methods=["POST"])
@login_required
def edit_image():
    data = request.get_json()
    if not data or "image" not in data or "api_choice" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    image_data = data["image"].split(",")[1]
    prompt = data.get("prompt", "")
    api_choice = data["api_choice"]
    
    api = APIFactory.get_api(api_choice)
    result = api.edit_image(image_data, prompt, api_choice)
    if isinstance(result, tuple) and len(result) == 2:
        edited_image, logs = result
    else:
        edited_image, logs = result, []
    
    if edited_image:
        original_bytes = base64.b64decode(image_data)
        result_bytes = base64.b64decode(edited_image.split(",")[1])
        record = ImageRecord(
            user_id=current_user.id,
            image_type="edit",
            prompt=prompt,
            api_choice=api_choice,
            original_image=original_bytes,
            result_image=result_bytes
        )
        db.session.add(record)
        db.session.commit()
    
    return jsonify({"image": edited_image, "logs": logs}), 200

@image_bp.route("/api/history", methods=["GET"])
@login_required
def get_history():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    
    pagination = ImageRecord.query.filter_by(user_id=current_user.id).order_by(
        ImageRecord.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    records = [record.to_dict() for record in pagination.items]
    
    return jsonify({
        "records": records,
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }), 200

@image_bp.route("/api/history/<int:record_id>", methods=["DELETE"])
@login_required
def delete_history(record_id):
    record = ImageRecord.query.filter_by(id=record_id, user_id=current_user.id).first()
    if not record:
        return jsonify({"error": "Record not found"}), 404
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({"message": "Record deleted successfully"}), 200
