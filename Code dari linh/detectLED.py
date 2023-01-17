# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage - sources:
    $ python path/to/detect.py --weights yolov5s.pt --source 0              # webcam
                                                             img.jpg        # image
                                                             vid.mp4        # video
                                                             path/          # directory
                                                             path/*.jpg     # glob 
                                                             a  
                                                             'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                             'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python path/to/detect.py --weights yolov5s.pt                 # PyTorch
                                         yolov5s.torchscript        # TorchScript
                                         yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                         yolov5s.mlmodel            # CoreML (under development)
                                         yolov5s.xml                # OpenVINO
                                         yolov5s_saved_model        # TensorFlow SavedModel
                                         yolov5s.pb                 # TensorFlow protobuf
                                         yolov5s.tflite             # TensorFlow Lite
                                         yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                         yolov5s.engine             # TensorRT
"""
from datetime import datetime
import timeit
import argparse
import os
import sys
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync
from Rx import OCC
import numpy as np
import time
import os
import imutils



@torch.no_grad()
def run(weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
        source=ROOT / 'data/images',  # file/dir/URL/glob, 0 for webcam
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        ):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data)
    stride, names, pt, jit, onnx, engine = model.stride, model.names, model.pt, model.jit, model.onnx, model.engine
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Half
    half &= (pt or jit or engine) and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
    if pt or jit:
        model.model.half() if half else model.model.float()

    # Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
        bs = len(dataset)  # batch_size
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1, 3, *imgsz), half=half)  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0
    sohinh= 0
    tong=0
    dung=0
    ma_tam = [[], [], [], []]
    ma = [[], [], [], []]
    for path, im, im0s, vid_cap, s in dataset:
        sohinh +=1
        start = timeit.default_timer()
        t1 = time_sync()
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(im, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        dt[2] += time_sync() - t3

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        print('toa do=========',xywh)
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        #======Gán nhã cho LED hay ko
                        annotator.box_label(xyxy, label, color=colors(c, True))
                        # print('toa do0=========', int(xyxy[0]))
                        # print('toa do=========', xyxy)
                        # cv2.rectangle(im0,(int(xyxy[0]),int(xyxy[1])),(int(xyxy[2]),int(xyxy[3])),(255, 0, 0), 2)
                        if int(xyxy[0]):
                            imge = im0[int(xyxy[1]): int(xyxy[3]),int(xyxy[0]): int(xyxy[2])]
                            gray = cv2.cvtColor(imge, cv2.COLOR_BGR2GRAY)
                            thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                                          9, -30)
                            thres1 = cv2.resize(thres, (imge.shape[1] * 4, imge.shape[0] * 4))
                            # cv2.imshow('Thres',thres1)
                            contours = cv2.findContours(thres, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                            contours = imutils.grab_contours(contours)
                            contours = sorted(contours, key=cv2.contourArea, reverse=False)
                            # print('Contours',contours)
                            number = 0
                            ma = [[], [], [], []]
                            td = []
                            for c in contours:
                                (x, y, w, h) = cv2.boundingRect(c)
                                # print(x, y, w, h)
                                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                # approximate the contour
                                if (2< w < 20) and (2 < h < 20):
                                    
                                    ma[0].append(x)
                                    ma[1].append(y)
                                    a = [x + w / 2, y + h / 2]  # Tin toa do tam cua các box LED
                                    td.append(a)
                                    ma[2].append(w)
                                    ma[3].append(h)
                                    # if x==min(maX)and y==min(maY):
                                    # cv2.rectangle(im0, (x, y), (x + w, y + h), (0, 255, 0), 1)
                                    # print(x, y, w, h)
                                    number += 1
                                    
                                    if len(ma[0])==0:
                                        ma = ma_tam
                                    else:
                                        ma_tam = ma

                            # print('Xmin: ',ma)
                            # Roi LED cạnh
                            # print('Td==',td)
                            xmin = min(ma[0])
                            # print('xmin==',xmin)
                            # print('X',ma[0])
                            xmax = max(ma[0])
                            # print('xmax==',xmax)
                            ymin = min(ma[1])
                            ymax = max(ma[1])
                            # print('ymin==',ymin)
                            # print('ymax==',ymax)
                            # print('Xlen',len(ma[0]))

                            # ===================
                            # cv2.rectangle(img, (xmin, ymin), (xmin + 7, ymin + 7), (255, 0, 0), 1)
                            # cv2.rectangle(img, (xmin, ymax), (xmin + 7, ymax + 7), (255, 0, 0), 1)
                            # cv2.rectangle(img, (xmax, ymax), (xmax + 7, ymax + 7), (255, 0, 0), 1)
                            # cv2.rectangle(img, (xmax, ymin), (xmax + 7, ymin + 7), (255, 0, 0), 1)

                            # Xu ly bit==========================================
                            bit = []
                            dx = (xmax - xmin) / (8 - 1)
                            # print('dx=',dx)
                            dy = (ymax - ymin) / (8 - 1)
                            # print('dy=',dy)
                            c = ymin
                            while c <= ymax + 1:
                                # print('x=====',c)
                                b = xmin
                                while b <= xmax + 1:
                                    for j in td:
                                        if b <= j[0] <= b + dx and c <= j[1] <= c + dy:
                                            d = 1
                                            break
                                        else:
                                            d = 0
                                    bit.append(d)

                                    # print('y=======',b)
                                    b = b + dx
                                c += dy

                            # print(len(bit),'==>',bit)
                            print("Number of Contours found = " + str(number))
                            img1 = cv2.resize(imge, (imge.shape[0] * 4, imge.shape[1] * 4))
                            # cv2.imshow('Pix',img1)
                            # my_track_method.init(frame, select_box)

                            # cv2.putText(frame, "LED Tracking", (80, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            # print('bit1==',type(bit[0]))

                            # Tính và hiển thị nhiệt độ và độ ẩm
                            tem = bit[8:16]
                            tem1 = sum(val * (2 ** idx) for idx, val in enumerate(reversed(tem)))
                            # print('tem==',tem1)
                            hum = bit[16:24]
                            hum1 = sum(val * (2 ** idx) for idx, val in enumerate(reversed(hum)))
                            dis = bit[24:32]
                            dis1 = sum(val * (2 ** idx) for idx, val in enumerate(reversed(dis)))
                            if bit[0:8] == [1, 0, 1, 1, 1, 0, 0, 1]:
                                dung +=1
                                cv2.putText(im0, "Temperature: " + str(tem1) + "*C", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                            1, (0, 255, 0), 2)
                                cv2.putText(im0, "Humidity: " + str(hum1) + "%", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (0, 255, 0), 2)
                                cv2.putText(im0, "Distance: " + str(dis1) + "cm", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (0, 255, 0), 2)
                            #cv2.imshow('frame', frame)
                            #print("type of frame", type(frame))
                        # else:
                        #     cv2.putText(frame, "Object can not be tracked!", (80, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        #                 (0, 0, 255), 2)
                        #     cv2.imshow('frame', frame)
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Print time (inference-only)
            LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

            # Stream results
            #im0 = annotator.result()
            # print("type of im0",type(im0))
            if view_img:
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond
            stop = timeit.default_timer()
            tong += int((stop - start)*1000)
            print("Time=====",int((stop - start)*1000))
            print ("======hinh va thoi gian ",sohinh,"===",tong,"dung==",dung)
            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path += '.mp4'
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)
        if sohinh==100:
            print("BER= ",(sohinh-dung)/sohinh)
            # break

    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights)  # update model (to fix SourceChangeWarning)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(FILE.stem, opt)
    return opt


def main(opt,OCC):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))

# from Rx import OCC
# if __name__ == "__main__":
#     occ=OCC
#     occ()
#     #opt = parse_opt()
#     #main(opt,OCC)
#
if __name__=='__main__':
    opt = parse_opt()
    check_requirements(exclude=('tensorboard', 'thop'))
    # run(**vars(opt))
    # occ=OCC()
    # occ()
    run(**vars(opt))

