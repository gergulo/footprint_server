from datetime import datetime
from PIL import Image
import os
import uuid
from django import forms
from django.conf import settings

_default_file_type = "jpg"
_image_type = ["jpg", "jpeg", "png"]


class UploadFileForm(forms.Form):
    file = forms.FileField()


def save_file(type_path, file, compress=False, thumbnail=False, thumbnail_width=800):
    """
    保存文件
    :param type_path: 文件类型文件夹
    :param file: 原始文件
    :param compress: 图片是否压缩，默认是
    :param thumbnail: 图片是否生成缩略图，默认否
    :param thumbnail_width: 缩略图宽度，默认400
    :return:
    """
    # 按日期分文件夹
    file_path = datetime.now().strftime("%Y%m%d")
    # 文件所在文件夹
    file_root = settings.FILE_ROOT + "/" + type_path + "/" + file_path + "/"
    # 生成文件夹
    os.makedirs(file_root,  exist_ok=True)
    # 文件名
    file_name = str(uuid.uuid1()).replace("-", "").upper()
    temp = file.name.split(".")
    if len(temp) > 1:
        file_type = temp[-1]
    else:
        file_type = _default_file_type
    file_name = file_name + "." + file_type
    local_file_path = file_root + file_name
    # 生成文件
    with open(local_file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    file_path1 = settings.FILE_URL + type_path + "/" + file_path + "/" + file_name
    file_path2 = ""
    if file_type in _image_type:    # 指定类型图片才进行压缩或生成缩略图
        if compress:
            # 如果同时有修改尺寸和大小的需要，可以先修改尺寸，再压缩大小
            # compress_image(local_file_path)
            resize_image(local_file_path)
        if thumbnail:
            thumbnail_file_path = thumbnail_image(local_file_path, file_name, thumbnail_width)
            file_path2 = settings.FILE_URL + type_path + "/" + file_path + "/" + thumbnail_file_path
    # 返回：文件在服务器上的路径、原始文件名，缩略图在服务器上的路径（如有）
    return file_path1, file.name, file_path2


def compress_image(file_path, mb=512, step=10, quality=80):
    """
    不改变图片尺寸压缩到指定大小
    :param file_path: 压缩源文件
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(file_path)
    if o_size <= mb:
        return file_path, o_size
    while o_size > mb:
        im = Image.open(file_path)
        im.save(file_path, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(file_path)
    return file_path, get_size(file_path)


def resize_image(file_path, x_s=800):
    """
    修改图片尺寸
    :param file_path: 图片源文件
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(file_path)
    x, y = im.size
    if x > x_s:
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(file_path)


def thumbnail_image(file_path, file_name, x_s=800):
    """
    生成小尺寸图
    :param file_path: 图片源文件
    :param file_name: 图片源文件明
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(file_path)
    x, y = im.size
    if x > x_s:
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
    else:
        out = im
    new_file_path = get_new_file_path(file_path, "t")
    new_file_name = get_new_file_path(file_name, "t")
    out.save(new_file_path)
    return new_file_name


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024


def get_new_file_path(in_file, txt):
    (the_dir, suffix) = os.path.splitext(in_file)
    return "{0}_{1}{2}".format(the_dir, txt, suffix)
