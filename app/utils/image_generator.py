import base64
import time
import uuid
import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont
import io


def upload_to_oss(image_bytes):
    import oss2
    auth = oss2.Auth(os.getenv("OSS_ACCESS_KEY_ID"), os.getenv("OSS_ACCESS_KEY_SECRET"))
    bucket = oss2.Bucket(auth, f"https://{os.getenv('OSS_ENDPOINT')}", os.getenv("OSS_BUCKET"))
    key = f"tmp/{uuid.uuid4()}.png"
    bucket.put_object(key, image_bytes)
    return f"https://{os.getenv('OSS_BUCKET')}.{os.getenv('OSS_ENDPOINT')}/{key}", key


def delete_from_oss(key):
    try:
        import oss2
        auth = oss2.Auth(os.getenv("OSS_ACCESS_KEY_ID"), os.getenv("OSS_ACCESS_KEY_SECRET"))
        bucket = oss2.Bucket(auth, f"https://{os.getenv('OSS_ENDPOINT')}", os.getenv("OSS_BUCKET"))
        bucket.delete_object(key)
    except Exception:
        pass


class MockAPI:
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        pass
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        pass


class API1(MockAPI):
    def __init__(self):
        try:
            import dashscope
            from dashscope import MultiModalConversation
            import requests
            import os
            import json
            
            self.dashscope = dashscope
            self.MultiModalConversation = MultiModalConversation
            self.requests = requests
            self.json = json
            
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            if not self.api_key:
                print("⚠️  DASHSCOPE_API_KEY 未配置，将使用 Mock API")
                self.available = False
                return
            
            self.dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            
            self.available = True
        except ImportError:
            print("DashScope SDK not installed, using mock API instead")
            self.available = False
    
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        if not self.available:
            logs.append("DashScope SDK not available, using mock API")
            mock_result, mock_logs = self._mock_generate(prompt)
            logs.extend(mock_logs)
            return mock_result, logs
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ]
            
            api_params = {
                "api_key": self.api_key,
                "model": "qwen-image-2.0-pro",
                "messages": messages,
                "stream": False,
                "n": 1,
                "watermark": False,
                "negative_prompt": negative_prompt if negative_prompt else " ",
                "prompt_extend": True,
                "size": size,
            }
            
            if seed is not None:
                api_params["seed"] = int(seed)
            
            response = self.MultiModalConversation.call(**api_params)
            
            if response.status_code == 200:
                logs.append("Response JSON:")
                logs.append(self.json.dumps(response, ensure_ascii=False, indent=2))
                
                image_url = None
                try:
                    for i, content in enumerate(response.output.choices[0].message.content):
                        if 'image' in content:
                            image_url = content['image']
                            log_msg = f"输出图像{i+1}的URL:{image_url}"
                            logs.append(log_msg)
                            break
                except Exception as json_error:
                    log_msg = f"Error extracting image URL from JSON: {str(json_error)}"
                    logs.append(log_msg)
                
                if image_url:
                    try:
                        if not os.path.exists('images'):
                            os.makedirs('images')
                        
                        import uuid
                        file_name = f"images/{str(uuid.uuid4())}.png"
                        
                        log_msg = f"Downloading image to: {file_name}"
                        logs.append(log_msg)
                        img_response = self.requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        with open(file_name, 'wb') as f:
                            f.write(img_response.content)
                        log_msg = f"Image saved to: {file_name}"
                        logs.append(log_msg)
                        
                        with open(file_name, 'rb') as f:
                            img_content = f.read()
                        img_str = base64.b64encode(img_content).decode('utf-8')
                        return f"data:image/png;base64,{img_str}", logs
                    except Exception as download_error:
                        log_msg = f"Error downloading and saving image: {str(download_error)}"
                        logs.append(log_msg)
                        mock_result, mock_logs = self._mock_generate(prompt)
                        logs.extend(mock_logs)
                        return mock_result, logs
                else:
                    logs.append("No image URL found in response")
                    mock_result, mock_logs = self._mock_generate(prompt)
                    logs.extend(mock_logs)
                    return mock_result, logs
            else:
                log_msg = f"HTTP返回码：{response.status_code}"
                logs.append(log_msg)
                log_msg = f"错误码：{response.code}"
                logs.append(log_msg)
                log_msg = f"错误信息：{response.message}"
                logs.append(log_msg)
                mock_result, mock_logs = self._mock_generate(prompt)
                logs.extend(mock_logs)
                return mock_result, logs
        except Exception as e:
            log_msg = f"Error in API1.generate_image: {str(e)}"
            logs.append(log_msg)
            mock_result, mock_logs = self._mock_generate(prompt)
            logs.extend(mock_logs)
            return mock_result, logs
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        if not self.available:
            logs.append("DashScope SDK not available, using mock API")
            mock_result, mock_logs = self._mock_edit(image_data, prompt)
            logs.extend(mock_logs)
            return mock_result, logs
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": f"data:image/png;base64,{image_data}"},
                        {"text": prompt if prompt else "编辑图像"}
                    ]
                }
            ]
            
            api_params = {
                "api_key": self.api_key,
                "model": "qwen-image-2.0-pro",
                "messages": messages,
                "stream": False,
                "n": 1,
                "watermark": False,
                "negative_prompt": negative_prompt if negative_prompt else " ",
                "prompt_extend": True,
                "size": size,
            }
            
            if seed is not None:
                api_params["seed"] = int(seed)
            
            response = self.MultiModalConversation.call(**api_params)
            
            if response.status_code == 200:
                logs.append("Response JSON:")
                logs.append(self.json.dumps(response, ensure_ascii=False, indent=2))
                
                image_url = None
                try:
                    for i, content in enumerate(response.output.choices[0].message.content):
                        if 'image' in content:
                            image_url = content['image']
                            log_msg = f"输出图像{i+1}的URL:{image_url}"
                            logs.append(log_msg)
                            break
                except Exception as json_error:
                    log_msg = f"Error extracting image URL from JSON: {str(json_error)}"
                    logs.append(log_msg)
                
                if image_url:
                    try:
                        if not os.path.exists('images'):
                            os.makedirs('images')
                        
                        import uuid
                        file_name = f"images/{str(uuid.uuid4())}.png"
                        
                        log_msg = f"Downloading image to: {file_name}"
                        logs.append(log_msg)
                        img_response = self.requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        with open(file_name, 'wb') as f:
                            f.write(img_response.content)
                        log_msg = f"Image saved to: {file_name}"
                        logs.append(log_msg)
                        
                        with open(file_name, 'rb') as f:
                            img_content = f.read()
                        img_str = base64.b64encode(img_content).decode('utf-8')
                        return f"data:image/png;base64,{img_str}", logs
                    except Exception as download_error:
                        log_msg = f"Error downloading and saving image: {str(download_error)}"
                        logs.append(log_msg)
                        mock_result, mock_logs = self._mock_edit(image_data, prompt)
                        logs.extend(mock_logs)
                        return mock_result, logs
                else:
                    logs.append("No image URL found in response")
                    mock_result, mock_logs = self._mock_edit(image_data, prompt)
                    logs.extend(mock_logs)
                    return mock_result, logs
            else:
                log_msg = f"HTTP返回码：{response.status_code}"
                logs.append(log_msg)
                log_msg = f"错误码：{response.code}"
                logs.append(log_msg)
                log_msg = f"错误信息：{response.message}"
                logs.append(log_msg)
                mock_result, mock_logs = self._mock_edit(image_data, prompt)
                logs.extend(mock_logs)
                return mock_result, logs
        except Exception as e:
            log_msg = f"Error in API1.edit_image: {str(e)}"
            logs.append(log_msg)
            mock_result, mock_logs = self._mock_edit(image_data, prompt)
            logs.extend(mock_logs)
            return mock_result, logs
    
    def _mock_generate(self, prompt):
        logs = []
        logs.append("Using Qianwen API for image generation")
        logs.append(f"Prompt: {prompt[:100]}")
        img = Image.new('RGB', (512, 512), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 20)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), f"Qianwen Generated Image\nPrompt: {prompt[:100]}", fill=(255, 255, 255), font=font)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs
    
    def _mock_edit(self, image_data, prompt):
        logs = []
        logs.append("Using Qianwen API for image editing")
        if prompt:
            logs.append(f"Prompt: {prompt[:100]}")
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 30)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), "Qianwen Edited", fill=(255, 0, 0), font=font)
        if prompt:
            d.text((10, 50), f"Prompt: {prompt[:50]}", fill=(255, 0, 0), font=font)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs


class API2(MockAPI):
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Tongyi API for image generation")
        logs.append(f"Prompt: {prompt[:100]}")
        img = Image.new('RGB', (512, 512), color=(255, 223, 186))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 20)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), f"Tongyi Generated Image\nPrompt: {prompt[:100]}", fill=(0, 0, 0), font=font)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Tongyi API for image editing")
        if prompt:
            logs.append(f"Prompt: {prompt[:100]}")
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        img = img.convert('L')
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs


class API3(MockAPI):
    def generate_image(self, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Mock API for image generation")
        logs.append(f"Prompt: {prompt[:100]}")
        img = Image.new('RGB', (512, 512), color=(144, 238, 144))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/google-noto-cjk/NotoSansCJK-Light.ttc', 20)
        except:
            font = ImageFont.load_default()
        d.text((10, 10), f"Mock API Generated Image\nPrompt: {prompt[:100]}", fill=(0, 0, 0), font=font)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs
    
    def edit_image(self, image_data, prompt, api_choice, size="1024*1536", negative_prompt="", seed=None):
        logs = []
        logs.append("Using Mock API for image editing")
        if prompt:
            logs.append(f"Prompt: {prompt[:50]}")
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        bordered_img = Image.new('RGB', (img.width + 20, img.height + 20), color=(255, 0, 0))
        bordered_img.paste(img, (10, 10))
        
        buffer = io.BytesIO()
        bordered_img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_str}", logs


class API4(MockAPI):
    def __init__(self):
        try:
            import dashscope
            self.dashscope = dashscope
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            if not self.api_key:
                self.available = False
                return
            dashscope.api_key = self.api_key
            self.available = True
        except ImportError:
            self.available = False

    def generate_image(self, prompt, api_choice, size="1024*1024", negative_prompt="", seed=None):
        logs = []
        if not self.available:
            return self._mock_generate(prompt)
        try:
            from dashscope import MultiModalConversation
            params = dict(
                api_key=self.api_key,
                model="wan2.7-image-pro",
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                stream=False,
                n=1,
                watermark=False,
                size=size,
            )
            if negative_prompt:
                params["negative_prompt"] = negative_prompt
            if seed is not None:
                params["seed"] = int(seed)
            rsp = MultiModalConversation.call(**params)
            logs.append(f"status: {rsp.status_code}")
            if rsp.status_code == 200:
                image_url = None
                for content in rsp.output.choices[0].message.content:
                    if 'image' in content:
                        image_url = content['image']
                        break
                if image_url:
                    img_resp = requests.get(image_url, timeout=60)
                    img_resp.raise_for_status()
                    os.makedirs('images', exist_ok=True)
                    path = f"images/{uuid.uuid4()}.png"
                    with open(path, 'wb') as f:
                        f.write(img_resp.content)
                    img_str = base64.b64encode(img_resp.content).decode()
                    logs.append(f"图像URL: {image_url}")
                    return f"data:image/png;base64,{img_str}", logs
            logs.append(rsp.message)
            return self._mock_generate(prompt)[0], logs
        except Exception as e:
            logs.append(str(e))
            return self._mock_generate(prompt)[0], logs

    def edit_image(self, image_data, prompt, api_choice, **kwargs):
        return self._mock_edit(image_data, prompt)

    def _mock_generate(self, prompt):
        img = Image.new('RGB', (512, 512), color=(30, 30, 60))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"wan2.7-image-pro\n{prompt[:80]}", fill=(255, 255, 255), font=ImageFont.load_default())
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}", []

    def _mock_edit(self, image_data, prompt):
        return self._mock_generate(prompt)


class WanxAPI:
    def __init__(self):
        try:
            import dashscope
            self.dashscope = dashscope
            self.api_key = os.getenv("DASHSCOPE_API_KEY")
            self.available = bool(self.api_key)
            if self.available:
                dashscope.api_key = self.api_key
        except ImportError:
            self.available = False

    def _download_to_base64(self, url):
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        os.makedirs('images', exist_ok=True)
        path = f"images/{uuid.uuid4()}.png"
        with open(path, 'wb') as f:
            f.write(resp.content)
        return "data:image/png;base64," + base64.b64encode(resp.content).decode()

    def inpaint(self, image_data, mask_data, prompt):
        logs = []
        if not self.available:
            return None, ["DASHSCOPE_API_KEY 未配置"]
        try:
            from dashscope import ImageSynthesis
            rsp = ImageSynthesis.call(
                api_key=self.api_key,
                model="wanx2.1-imageedit",
                function="description_edit_with_mask",
                prompt=prompt or "修复该区域",
                base_image_url=f"data:image/png;base64,{image_data}",
                mask_image_url=f"data:image/png;base64,{mask_data}",
                n=1,
            )
            logs.append(f"status: {rsp.status_code}")
            if rsp.status_code == 200:
                result_url = rsp.output.results[0].url
                return self._download_to_base64(result_url), logs
            logs.append(f"code: {rsp.code}, message: {rsp.message}")
            return None, logs
        except Exception as e:
            return None, logs + [str(e)]

    def sketch_to_image(self, image_data, prompt):
        logs = []
        if not self.available:
            return None, ["DASHSCOPE_API_KEY 未配置"]
        image_bytes = base64.b64decode(image_data)
        url, oss_key = upload_to_oss(image_bytes)
        logs.append(f"OSS URL: {url}")
        try:
            from dashscope import ImageSynthesis
            rsp = ImageSynthesis.call(
                api_key=self.api_key,
                model="wanx-sketch-to-image-lite",
                prompt=prompt,
                sketch_image_url=url,
                task="image2image",
                n=1,
                size="768*768",
            )
            logs.append(f"status: {rsp.status_code}")
            if rsp.status_code == 200:
                result_url = rsp.output.results[0].url
                return self._download_to_base64(result_url), logs
            logs.append(f"code: {rsp.code}, message: {rsp.message}")
            return None, logs
        except Exception as e:
            return None, logs + [str(e)]
        finally:
            delete_from_oss(oss_key)

    def _save_temp(self, image_data):
        os.makedirs('images', exist_ok=True)
        path = os.path.abspath(f"images/{uuid.uuid4()}.png")
        with open(path, 'wb') as f:
            f.write(base64.b64decode(image_data))
        return path

    def background_generation(self, image_data, prompt):
        logs = []
        if not self.available:
            return None, ["DASHSCOPE_API_KEY 未配置"]
        # 转换为 RGBA
        img = Image.open(io.BytesIO(base64.b64decode(image_data))).convert("RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        url, oss_key = upload_to_oss(buf.getvalue())
        logs.append(f"OSS URL: {url}")
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-DashScope-Async": "enable",
            }
            payload = {
                "model": "wanx-background-generation-v2",
                "input": {"base_image_url": url, "ref_prompt": prompt or "自然背景"},
                "parameters": {"n": 1, "model_version": "v3"},
            }
            rsp = requests.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/",
                headers=headers, json=payload, timeout=30
            )
            data = rsp.json()
            logs.append(f"create task: {rsp.status_code}")
            if rsp.status_code != 200:
                logs.append(str(data))
                return None, logs
            task_id = data["output"]["task_id"]
            for _ in range(30):
                time.sleep(3)
                r = requests.get(
                    f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"}, timeout=30
                )
                result = r.json()
                status = result["output"]["task_status"]
                logs.append(f"task status: {status}")
                if status == "SUCCEEDED":
                    result_url = result["output"]["results"][0]["url"]
                    return self._download_to_base64(result_url), logs
                if status in ("FAILED", "CANCELED"):
                    logs.append(str(result))
                    return None, logs
            return None, logs + ["timeout"]
        except Exception as e:
            return None, logs + [str(e)]
        finally:
            delete_from_oss(oss_key)

    def style_repaint(self, image_data, style_index):
        logs = []
        if not self.available:
            return None, ["DASHSCOPE_API_KEY 未配置"]
        image_bytes = base64.b64decode(image_data)
        url, oss_key = upload_to_oss(image_bytes)
        logs.append(f"OSS URL: {url}")
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-DashScope-Async": "enable",
            }
            payload = {
                "model": "wanx-style-repaint-v1",
                "input": {"image_url": url, "style_index": int(style_index)},
            }
            rsp = requests.post(
                "https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation",
                headers=headers, json=payload, timeout=30
            )
            data = rsp.json()
            logs.append(f"create task: {rsp.status_code}")
            if rsp.status_code != 200:
                logs.append(str(data))
                return None, logs
            task_id = data["output"]["task_id"]
            # 轮询结果
            for _ in range(30):
                time.sleep(3)
                r = requests.get(
                    f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"}, timeout=30
                )
                result = r.json()
                status = result["output"]["task_status"]
                logs.append(f"task status: {status}")
                if status == "SUCCEEDED":
                    result_url = result["output"]["results"][0]["url"]
                    return self._download_to_base64(result_url), logs
                if status in ("FAILED", "CANCELED"):
                    logs.append(str(result))
                    return None, logs
            return None, logs + ["timeout"]
        except Exception as e:
            return None, logs + [str(e)]
        finally:
            delete_from_oss(oss_key)


# API工厂类
class APIFactory:
    @staticmethod
    def get_api(api_choice):
        print(f"[Factory] Requesting API: {api_choice}")
        if api_choice == 'API-1':
            api = API1()
            print(f"[Factory] Using: API1 (Qianwen)")
            return api
        elif api_choice == 'API-2':
            api = API2()
            print(f"[Factory] Using: API2 (Tongyi)")
            return api
        elif api_choice == 'API-3':
            api = API3()
            print(f"[Factory] Using: API3 (Mock)")
            return api
        elif api_choice == 'API-4':
            api = API4()
            print(f"[Factory] Using: API4 (wan2.7-image-pro)")
            return api
        else:
            print(f"[Factory] Unknown API: {api_choice}, defaulting to API1")
            return API1()

    @staticmethod
    def get_wanx():
        return WanxAPI()