# 尝试导入必要的库，如果失败则提供错误信息
try:
    import cv2
    import time
    import mediapipe as mp
    import os
    import logging
    print("所有依赖库导入成功")
except ImportError as e:
    print(f"导入库失败: {e}")
    print("\n解决方案:")
    print("1. 您正在使用Python 3.14，这是一个非常新的版本，可能与某些库不兼容")
    print("2. 建议降级到Python 3.9或3.10版本，这些版本与OpenCV和MediaPipe的兼容性更好")
    print("3. 如果必须使用Python 3.14，请尝试以下命令安装兼容版本:")
    print("   pip install -r requirements.txt")
    print("4. 如果上述方法仍然失败，可以尝试使用conda创建新的环境:")
    print("   conda create -n gesture python=3.10")
    print("   conda activate gesture")
    print("   pip install -r requirements.txt")
    print("\n按任意键退出...")
    input()
    exit(1)
# Hand Landmarker
# 对于大拇指，比较指尖和第一个关节的x坐标位置
# 对于其他四指，比较指尖和第二个关节的y坐标位置
# landmarks
file_path = 'address.DATA.txt'  # 将文件路径替换为你的txt文件路径
with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
        content1 = lines[0]
        content2 = lines[1]
        content3 = lines[2]
        content4 = lines[3]
        content5 = lines[4]

# 配置初始化
class Detector:
    def __init__(self, static_image_mode=False,
                        face=True,
                        hand=True):
        # 检测手势
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=1,  # 限制检测手数，提高性能
            min_detection_confidence=0.5,  # 降低检测置信度阈值，提高性能
            min_tracking_confidence=0.5  # 降低跟踪置信度阈值，提高性能
        )

        # 检测面部
        self.mp_face_detection = mp.solutions.face_detection
        self.face = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.5  # 降低检测置信度阈值，提高性能
        )

        #用于绘制姿势估计、目标检测等结果的工具模块
        self.mp_drawing = mp.solutions.drawing_utils
        #定义的一些绘图样式，可以用于设置绘图的颜色、线条粗细等样式属性，使得绘制的结果更加美观和易于理解。
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.tipIds = [4, 8, 12, 16, 20]# 指尖列表
        self.lm_x_point = []
        self.lm_y_point = []
        self.frame_index = 0
        self.results = None
        self.face_results = None
        self.is_face = face
        self.is_hand = hand

    def get_content_type(self, content):
        """
        获取内容类型
        返回: 'python', 'url', 'file', 'unknown'
        """
        import os

        # 检查是否是Python文件
        if content.endswith('.py'):
            return 'python'
        # 检查是否是URL
        elif content.startswith('http://') or content.startswith('https://'):
            return 'url'
        # 检查是否是其他类型的文件
        elif os.path.isfile(content):
            return 'file'
        # 检查是否可能是URL（包含点但没有路径分隔符）
        elif '.' in content and not os.path.sep in content:
            return 'url'
        # 其他情况作为文件路径处理
        else:
            return 'file'  # 默认作为文件处理

    def open_content(self, content, gesture_name):
        """
        根据内容类型打开内容
        """
        import subprocess
        import sys
        import os
        import webbrowser

        content_type = self.get_content_type(content)

        try:
            if content_type == 'python':
                print(f"检测到Python文件: {content}")
                # 使用当前Python解释器来执行脚本，确保使用相同的环境
                python_executable = sys.executable
                subprocess.Popen([python_executable, content], shell=True)
                print(f"{gesture_name}. 执行Python脚本:", content)

            elif content_type == 'url':
                print(f"检测到URL链接: {content}")
                if not content.startswith('http://') and not content.startswith('https://'):
                    content = 'https://' + content
                webbrowser.open(content)
                print(f"{gesture_name}. 打开URL:", content)

            elif content_type == 'file':
                print(f"检测到文件: {content}")
                os.startfile(content)
                print(f"{gesture_name}. 打开文件:", content)

            else:
                print(f"未知内容类型，尝试打开: {content}")
                # 先尝试作为URL打开
                if '.' in content and not os.path.sep in content:
                    webbrowser.open('https://' + content)
                    print(f"{gesture_name}. 打开URL:", content)
                else:
                    # 尝试作为文件路径打开
                    os.startfile(content)
                    print(f"{gesture_name}. 打开文件:", content)

        except Exception as e:
            print(f"无法打开内容: {e}")

        print("--------------------------------------------")
        return True

    def open_url_if_all_fingers_up1(self, fingers_status):
        print(f"检测手势1，手指状态: {fingers_status}")
        if fingers_status[0][1] == 1 and fingers_status[0][2] == 0 and fingers_status[0][0] == 0 and fingers_status[0][3] == 0 and fingers_status[0][4] == 0:
            # 检查是否是Python文件，如果是，处理依赖问题
            if self.get_content_type(content1) == 'python':
                print(f"检测到Python文件: {content1}")
                try:
                    return self.open_content(content1, "一根手指举起")
                except Exception as e:
                    print(f"执行Python脚本失败: {e}")
                    # 检查是否是缺少依赖的错误
                    if "ModuleNotFoundError" in str(e):
                        print("检测到缺少依赖库，请运行install_dependencies.bat安装所需依赖")
                        # 提供选项自动安装依赖
                        try:
                            choice = input("是否自动安装依赖？(y/n): ")
                            if choice.lower() == 'y':
                                print("正在安装依赖...")
                                # 使用当前Python解释器对应的pip
                                import subprocess
                                import sys
                                python_executable = sys.executable
                                pip_executable = python_executable.replace('python.exe', 'pip.exe')
                                subprocess.run([pip_executable, 'install', 'pandas', 'matplotlib'], check=True)
                                print("依赖安装完成，请再次做出手势1来执行脚本")
                        except Exception as install_error:
                            print(f"安装依赖失败: {install_error}")
                            print("请手动运行install_dependencies.bat文件安装依赖")
            else:
                # 对于非Python文件，直接使用通用处理方法
                return self.open_content(content1, "一根手指举起")
            
            # 检查是否是Python文件
            if content1.endswith('.py'):
                print(f"检测到Python文件: {content1}")
                try:
                    # 使用当前Python解释器来执行脚本，确保使用相同的环境
                    python_executable = sys.executable
                    subprocess.Popen([python_executable, content1], shell=True)
                    print("一根手指举起. 执行Python脚本:", content1)
                except Exception as e:
                    print(f"执行Python脚本失败: {e}")
                    # 检查是否是缺少依赖的错误
                    if "ModuleNotFoundError" in str(e):
                        print("检测到缺少依赖库，请运行install_dependencies.bat安装所需依赖")
                        # 提供选项自动安装依赖
                        try:
                            choice = input("是否自动安装依赖？(y/n): ")
                            if choice.lower() == 'y':
                                print("正在安装依赖...")
                                # 使用当前Python解释器对应的pip
                                python_executable = sys.executable
                                pip_executable = python_executable.replace('python.exe', 'pip.exe')
                                subprocess.run([pip_executable, 'install', 'pandas', 'matplotlib'], check=True)
                                print("依赖安装完成，请再次做出手势1来执行脚本")
                        except Exception as install_error:
                            print(f"安装依赖失败: {install_error}")
                            print("请手动运行install_dependencies.bat文件安装依赖")
                  
            # 检查是否是URL
            elif content1.startswith('http://') or content1.startswith('https://'):
                print(f"检测到URL链接: {content1}")
                import webbrowser
                webbrowser.open(content1)
                print("一根手指举起. 打开URL:", content1)
            # 检查是否是其他类型的文件
            elif os.path.isfile(content1):
                print(f"检测到文件: {content1}")
                os.startfile(content1)
                print("一根手指举起. 打开文件:", content1)
            # 如果都不是，则尝试作为文件路径或URL处理
            else:
                print(f"未知内容类型，尝试打开: {content1}")
                try:
                    # 先尝试作为URL打开
                    if '.' in content1 and not os.path.sep in content1:
                        import webbrowser
                        webbrowser.open('https://' + content1)
                        print("一根手指举起. 打开URL:", content1)
                    else:
                        # 尝试作为文件路径打开
                        os.startfile(content1)
                        print("一根手指举起. 打开文件:", content1)
                except Exception as e:
                    print(f"无法打开内容: {e}")
            print("--------------------------------------------")
            return True  # 返回True而不是使用time.sleep
        else:
            return False

    def open_url_if_all_fingers_up2(self, fingers_status):
        print(f"检测手势2，手指状态: {fingers_status}")
        if fingers_status[0][1] == 1 and fingers_status[0][2] == 1 and fingers_status[0][0] == 0 and fingers_status[0][3] == 0 and fingers_status[0][4] == 0:
            # 自动识别文件类型并执行相应操作
            import subprocess
            import sys
            import os

            # 检查是否是Python文件
            if content2.endswith('.py'):
                print(f"检测到Python文件: {content2}")
                try:
                    # 使用当前Python解释器来执行脚本，确保使用相同的环境
                    python_executable = sys.executable
                    subprocess.Popen([python_executable, content2], shell=True)
                    print("两根手指举起. 执行Python脚本:", content2)
                except Exception as e:
                    print(f"执行Python脚本失败: {e}")

            # 检查是否是URL
            elif content2.startswith('http://') or content2.startswith('https://'):
                print(f"检测到URL链接: {content2}")
                import webbrowser
                webbrowser.open(content2)
                print("两根手指举起. 打开URL:", content2)
            # 检查是否是其他类型的文件
            elif os.path.isfile(content2):
                print(f"检测到文件: {content2}")
                os.startfile(content2)
                print("两根手指举起. 打开文件:", content2)
            # 如果都不是，则尝试作为文件路径或URL处理
            else:
                print(f"未知内容类型，尝试打开: {content2}")
                try:
                    # 先尝试作为URL打开
                    if '.' in content2 and not os.path.sep in content2:
                        import webbrowser
                        webbrowser.open('https://' + content2)
                        print("两根手指举起. 打开URL:", content2)
                    else:
                        # 尝试作为文件路径打开
                        os.startfile(content2)
                        print("两根手指举起. 打开文件:", content2)
                except Exception as e:
                    print(f"无法打开内容: {e}")
            print("--------------------------------------------")
            return True  # 返回True而不是使用time.sleep
        else:
            return False


    def open_url_if_all_fingers_up3(self, fingers_status):
        print(f"检测手势3，手指状态: {fingers_status}")
        if fingers_status[0][1] == 1 and fingers_status[0][2] == 1 and fingers_status[0][0] == 0 and fingers_status[0][3] == 1 and fingers_status[0][4] == 0:
            # 自动识别文件类型并执行相应操作
            import subprocess
            import sys
            import os

            # 检查是否是Python文件
            if content3.endswith('.py'):
                print(f"检测到Python文件: {content3}")
                try:
                    # 使用当前Python解释器来执行脚本，确保使用相同的环境
                    python_executable = sys.executable
                    subprocess.Popen([python_executable, content3], shell=True)
                    print("三根手指举起. 执行Python脚本:", content3)
                except Exception as e:
                    print(f"执行Python脚本失败: {e}")

            # 检查是否是URL
            elif content3.startswith('http://') or content3.startswith('https://'):
                print(f"检测到URL链接: {content3}")
                import webbrowser
                webbrowser.open(content3)
                print("三根手指举起. 打开URL:", content3)
            # 检查是否是其他类型的文件
            elif os.path.isfile(content3):
                print(f"检测到文件: {content3}")
                os.startfile(content3)
                print("三根手指举起. 打开文件:", content3)
            # 如果都不是，则尝试作为文件路径或URL处理
            else:
                print(f"未知内容类型，尝试打开: {content3}")
                try:
                    # 先尝试作为URL打开
                    if '.' in content3 and not os.path.sep in content3:
                        import webbrowser
                        webbrowser.open('https://' + content3)
                        print("三根手指举起. 打开URL:", content3)
                    else:
                        # 尝试作为文件路径打开
                        os.startfile(content3)
                        print("三根手指举起. 打开文件:", content3)
                except Exception as e:
                    print(f"无法打开内容: {e}")
            print("--------------------------------------------")
            return True  # 返回True而不是使用time.sleep
        else:
            return False
    def open_url_if_all_fingers_up4(self, fingers_status):
        print(f"检测手势4，手指状态: {fingers_status}")
        if fingers_status[0][1] == 1 and fingers_status[0][2] == 1 and fingers_status[0][0] == 0 and fingers_status[0][3] == 1 and fingers_status[0][4] == 1:

             # 检查文件是否是Python文件
            if content4.endswith('.py'):
                import subprocess
                import sys
                try:
                    # 使用当前Python解释器来执行脚本，确保使用相同的环境
                    python_executable = sys.executable
                    subprocess.Popen([python_executable, content4], shell=True)
                    print("四根手指举起. 执行Python脚本:", content4)
                except Exception as e:
                    print(f"执行Python脚本失败: {e}")
                  
            else:
                os.startfile(content4)
                print("四根手指举起. 打开文件:", content4)
            print("--------------------------------------------")
            return True  # 返回True而不是使用time.sleep
        else:
            return False


    def open_url_if_all_fingers_up5(self, fingers_status):
        print(f"检测手势5，手指状态: {fingers_status}")
        if all(finger == 1 for finger in fingers_status[0]):
            # 自动识别文件类型并执行相应操作
            import subprocess
            import sys
            import os

            # 检查是否是Python文件
            if content5.endswith('.py'):
                print(f"检测到Python文件: {content5}")
                try:
                    # 使用当前Python解释器来执行脚本，确保使用相同的环境
                    python_executable = sys.executable
                    subprocess.Popen([python_executable, content5], shell=True)
                    print("五根手指举起. 执行Python脚本:", content5)
                except Exception as e:
                    print(f"执行Python脚本失败: {e}")

            # 检查是否是URL
            elif content5.startswith('http://') or content5.startswith('https://'):
                print(f"检测到URL链接: {content5}")
                import webbrowser
                webbrowser.open(content5)
                print("五根手指举起. 打开URL:", content5)
            # 检查是否是其他类型的文件
            elif os.path.isfile(content5):
                print(f"检测到文件: {content5}")
                os.startfile(content5)
                print("五根手指举起. 打开文件:", content5)
            # 如果都不是，则尝试作为文件路径或URL处理
            else:
                print(f"未知内容类型，尝试打开: {content5}")
                try:
                    # 先尝试作为URL打开
                    if '.' in content5 and not os.path.sep in content5:
                        import webbrowser
                        webbrowser.open('https://' + content5)
                        print("五根手指举起. 打开URL:", content5)
                    else:
                        # 尝试作为文件路径打开
                        os.startfile(content5)
                        print("五根手指举起. 打开文件:", content5)
                except Exception as e:
                    print(f"无法打开内容: {e}")
            print("--------------------------------------------")
            return True  # 返回True而不是使用time.sleep

        else:
            return False

    # def open_url_if_all_fingers_up6(self):
    # # 检查左右手的手指是否都全部张开
    #     if all(finger == 1 for finger in self.fingersIsUp()[0]) and all(finger == 1 for finger in self.fingersIsUp()[1]):
    #         os.startfile(content6)  # 替换为你的文件路径
    #         print("All fingers are up. Opening URL4:", content6)
    #         time.sleep(1.2)



#主要实现检测部分
    def runDetec(self, image):
        """ 运行检测程序 """
        if self.is_face or self.is_hand:
            #防止图像像素数据的修改
            image.flags.writeable = False
            #BGR转RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if self.is_face:    self.face_results = self.face.process(image)
            if self.is_hand:    self.results = self.hands.process(image)
            #允许图像像素数据的修改
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # draw hand
        if self.is_hand:
            # 检测到手部地标列表不为空
            if self.results.multi_hand_landmarks:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    #传入参数
                    self.mp_drawing.draw_landmarks(
                        #1.图片
                        image,
                        #手部地标信息
                        hand_landmarks,
                        #手部地标信息之间的连接关系
                        self.mp_hands.HAND_CONNECTIONS,
                        #手部地标信息绘制的样式
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        #手部地标信息之间的连接线绘制的样式
                        self.mp_drawing_styles.get_default_hand_connections_style())
        # draw face
        if self.is_face:
            if self.face_results.detections:
                for detection in self.face_results.detections:
                    #传参图片和检测到的人脸信息
                    self.mp_drawing.draw_detection(image, detection)
        return image



#返回；类型为列表list
#实现对检测到的手部周围绘制边界框，并在图像上显示手部的ID、类型信息以及帧索引信息。
    def getBox(self, img) -> list:
        """ 计算手部周围的边界框 """
        bboxs = []
        #-为通道数，彩色为3灰度为1
        image_height, image_width, _ = img.shape
        #如果检测到手部地标信息列表不为空
        if self.results.multi_hand_landmarks:
            # 遍历检测到的所有的手
            self.lm_x_point.clear()
            self.lm_y_point.clear()

            index = 0
            self.frame_index = (self.frame_index + 1) % 1
            for hand_landmarks in self.results.multi_hand_landmarks:
                xList, yList = [], []
                for _, lm in enumerate(hand_landmarks.landmark):
                    xList.append(int(lm.x * image_width))
                    yList.append(int(lm.y * image_height))

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                              (0, 255, 0), 2)
                hand_type = self.results.multi_handedness[index].classification[0].label
                cv2.putText(img, "id: {}, hand: {}".format(index, hand_type),
                            (xmin - 25, ymin - 20),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
                cv2.putText(img, "frame_index: {}".format(self.frame_index), (20, 20),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                index += 1
                self.lm_x_point.append(xList)
                self.lm_y_point.append(yList)
                bboxs.append(bbox)
        return bboxs

#检测手指是否伸直
#返回手指竖起和弯曲的列表
    def fingersIsUp(self) -> list:
        """
        返回竖起和弯曲的手指列表,1表示竖起,0表示弯曲
        """
        #迭代处理每个检测到的手部
        index = 0
        multi_fingers = []
        #landhand为整个手部
        for landhands in self.results.multi_hand_landmarks:
            hand_type = self.results.multi_handedness[index].classification[0].label
        #为每个手部储存手指状态
            fingers = []
            # 判断大拇指
            if hand_type == "Right":
                # 如果大拇指尖x坐标小于
                if self.lm_x_point[index][self.tipIds[0]] > self.lm_x_point[index][self.tipIds[0] - 1]:
                    fingers.append(0)
                else:   fingers.append(1)
            else:
                if self.lm_x_point[index][self.tipIds[0]] < self.lm_x_point[index][self.tipIds[0] - 1]:
                    fingers.append(0)
                else:   fingers.append(1)

            # 4 Fingers，4个手指在握拳状态，使用 y 轴坐标来判断
            for i in range(1, 5):
                # 如果指尖坐标小于下面两个关节的 y 坐标，说明手是伸直的
                if self.lm_y_point[index][self.tipIds[i]] < self.lm_y_point[index][self.tipIds[i] - 2]:
                    fingers.append(1)
                else: fingers.append(0)
        #muliti_fingers包含了每个手部的每个手指的位置信息
            multi_fingers.append(fingers)
            index += 1
            #返回给调用fingerisup方法的代码
        return multi_fingers




if __name__ == '__main__':
    detector = Detector(face=True, hand=True)
    cap = cv2.VideoCapture(0)

    # 设置摄像头参数以提高性能
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # 添加一个变量来防止重复触发
    last_gesture_time = 0
    gesture_cooldown = 3  # 手势冷却时间（秒）
    
    # 添加手势连续检测计数器
    gesture_counters = {
        "gesture1": 0,
        "gesture2": 0,
        "gesture3": 0,
        "gesture4": 0,
        "gesture5": 0,
        "none": 0
    }
    last_detected_gesture = "none"
    required_consecutive_detections = 5  # 需要连续检测到5次相同手势才触发

    while cap.isOpened():
        flag, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not flag:
            print("Ignoring empty camera frame.")
            continue

        # 处理每一帧
        current_time = time.time()
        frame = detector.runDetec(frame)
        bboxs = detector.getBox(frame)

        if bboxs:
            fingers_status = detector.fingersIsUp()
            # 输出手指状态数组
            print(f"手指状态: {fingers_status}")
            
            # 检测当前手势
            current_gesture = "none"
            if fingers_status[0][1] == 1 and fingers_status[0][2] == 0 and fingers_status[0][0] == 0 and fingers_status[0][3] == 0 and fingers_status[0][4] == 0:
                current_gesture = "gesture1"
            elif fingers_status[0][1] == 1 and fingers_status[0][2] == 1 and fingers_status[0][0] == 0 and fingers_status[0][3] == 0 and fingers_status[0][4] == 0:
                current_gesture = "gesture2"
            elif fingers_status[0][1] == 1 and fingers_status[0][2] == 1 and fingers_status[0][0] == 0 and fingers_status[0][3] == 1 and fingers_status[0][4] == 0:
                current_gesture = "gesture3"
            elif fingers_status[0][1] == 1 and fingers_status[0][2] == 1 and fingers_status[0][0] == 0 and fingers_status[0][3] == 1 and fingers_status[0][4] == 1:
                current_gesture = "gesture4"
            elif all(finger == 1 for finger in fingers_status[0]):
                current_gesture = "gesture5"
            
            # 更新手势计数器
            if current_gesture == last_detected_gesture:
                gesture_counters[current_gesture] += 1
            else:
                # 手势改变，重置所有计数器
                for key in gesture_counters:
                    gesture_counters[key] = 0
                gesture_counters[current_gesture] = 1
                last_detected_gesture = current_gesture
            
            print(f"当前手势: {current_gesture}, 连续检测次数: {gesture_counters[current_gesture]}")
            
            # 检查冷却时间和连续检测次数
            if current_time - last_gesture_time > gesture_cooldown:
                if gesture_counters["gesture1"] >= required_consecutive_detections:
                    if detector.open_url_if_all_fingers_up1(fingers_status):
                        print("程序一已启动")
                        last_gesture_time = current_time
                        # 重置计数器
                        for key in gesture_counters:
                            gesture_counters[key] = 0
                elif gesture_counters["gesture2"] >= required_consecutive_detections:
                    if detector.open_url_if_all_fingers_up2(fingers_status):
                        print("程序二已启动")
                        last_gesture_time = current_time
                        # 重置计数器
                        for key in gesture_counters:
                            gesture_counters[key] = 0
                elif gesture_counters["gesture3"] >= required_consecutive_detections:
                    if detector.open_url_if_all_fingers_up3(fingers_status):
                        print("程序三已启动")
                        last_gesture_time = current_time
                        # 重置计数器
                        for key in gesture_counters:
                            gesture_counters[key] = 0
                elif gesture_counters["gesture4"] >= required_consecutive_detections:
                    if detector.open_url_if_all_fingers_up4(fingers_status):
                        print("程序四已启动")
                        last_gesture_time = current_time
                        # 重置计数器
                        for key in gesture_counters:
                            gesture_counters[key] = 0
                elif gesture_counters["gesture5"] >= required_consecutive_detections:
                    if detector.open_url_if_all_fingers_up5(fingers_status):
                        print("程序五已启动")
                        last_gesture_time = current_time
                        # 重置计数器
                        for key in gesture_counters:
                            gesture_counters[key] = 0

        cv2.imshow('Hand & Face Detection', frame)

        if cv2.waitKey(5) & 0xFF == 32:  # ASCII
            break
