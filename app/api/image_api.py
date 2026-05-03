from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import base64
import io
from app import db
from app.utils.image_generator import APIFactory, WanxAPI
from app.models.image_record import ImageRecord

image_bp = Blueprint("image_api", __name__)

@image_bp.route("/api/generate", methods=["POST"])
@login_required
def generate_image():
    data = request.get_json()
    print(f"[API] Received request data: {data}")
    if not data or "prompt" not in data or "api_choice" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    prompt = data["prompt"]
    api_choice = data["api_choice"]
    print(f"[API] api_choice received: {api_choice}")
    
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
    count = min(max(1, data.get("count", 1)), 4)
    size = data.get("size", "1024*1536")

    images = []
    all_logs = []

    api = APIFactory.get_api(api_choice)
    for i in range(count):
        result = api.edit_image(image_data, prompt, api_choice, size=size)
        if isinstance(result, tuple) and len(result) == 2:
            edited_image, logs = result
        else:
            edited_image, logs = result, []

        if edited_image:
            images.append(edited_image)
            all_logs.extend(logs)

            original_bytes = base64.b64decode(image_data)
            result_bytes = base64.b64decode(edited_image.split(",")[1])
            record = ImageRecord(
                user_id=current_user.id,
                image_type="edit",
                prompt=prompt,
                api_choice=api_choice,
                original_image=original_bytes,
                result_image=result_bytes,
                size=size,
                generation_count=count
            )
            db.session.add(record)

    db.session.commit()

    return jsonify({"images": images, "image": images[0] if images else None, "logs": all_logs}), 200

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


@image_bp.route("/api/background", methods=["POST"])
@login_required
def background_generation():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "Missing image"}), 400

    image_data = data["image"].split(",")[1]
    prompt = data.get("prompt", "")

    wanx = APIFactory.get_wanx()
    result, logs = wanx.background_generation(image_data, prompt)

    if result:
        original_bytes = base64.b64decode(image_data)
        result_bytes = base64.b64decode(result.split(",")[1])
        record = ImageRecord(
            user_id=current_user.id,
            image_type="background",
            prompt=prompt,
            api_choice="wanx-background",
            original_image=original_bytes,
            result_image=result_bytes
        )
        db.session.add(record)
        db.session.commit()

    return jsonify({"image": result, "logs": logs}), 200


@image_bp.route("/api/style-repaint", methods=["POST"])
@login_required
def style_repaint():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "Missing image"}), 400

    image_data = data["image"].split(",")[1]
    style_index = data.get("style_index", 0)

    wanx = APIFactory.get_wanx()
    result, logs = wanx.style_repaint(image_data, style_index)

    if result:
        original_bytes = base64.b64decode(image_data)
        result_bytes = base64.b64decode(result.split(",")[1])
        record = ImageRecord(
            user_id=current_user.id,
            image_type="style_repaint",
            prompt=f"style_index:{style_index}",
            api_choice="wanx-style-repaint",
            original_image=original_bytes,
            result_image=result_bytes
        )
        db.session.add(record)
        db.session.commit()

    return jsonify({"image": result, "logs": logs}), 200


@image_bp.route("/api/sketch", methods=["POST"])
@login_required
def sketch_to_image():
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "Missing image"}), 400

    image_data = data["image"].split(",")[1]
    prompt = data.get("prompt", "")

    wanx = APIFactory.get_wanx()
    result, logs = wanx.sketch_to_image(image_data, prompt)

    if result:
        original_bytes = base64.b64decode(image_data)
        result_bytes = base64.b64decode(result.split(",")[1])
        record = ImageRecord(
            user_id=current_user.id,
            image_type="sketch",
            prompt=prompt,
            api_choice="wanx-sketch",
            original_image=original_bytes,
            result_image=result_bytes
        )
        db.session.add(record)
        db.session.commit()

    return jsonify({"image": result, "logs": logs}), 200


@image_bp.route("/api/inpaint", methods=["POST"])
@login_required
def inpaint():
    data = request.get_json()
    if not data or "image" not in data or "mask" not in data:
        return jsonify({"error": "Missing image or mask"}), 400

    image_data = data["image"].split(",")[1]
    mask_data = data["mask"].split(",")[1]
    prompt = data.get("prompt", "")
    count = min(max(1, data.get("count", 1)), 4)
    size = data.get("size", "1024*1536")

    images = []
    all_logs = []

    wanx = APIFactory.get_wanx()
    for i in range(count):
        result, logs = wanx.inpaint(image_data, mask_data, prompt, size=size)

        if result:
            images.append(result)
            all_logs.extend(logs)

            record = ImageRecord(
                user_id=current_user.id,
                image_type="inpaint",
                prompt=prompt,
                api_choice="wanx-x-painting",
                original_image=base64.b64decode(image_data),
                result_image=base64.b64decode(result.split(",")[1]),
                size=size,
                generation_count=count
            )
            db.session.add(record)

    db.session.commit()

    return jsonify({"images": images, "image": images[0] if images else None, "logs": all_logs}), 200
