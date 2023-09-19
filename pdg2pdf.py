# pdg2pdf 步骤整合
import imghdr
import os
import sys
import re
import time
from PIL import Image
import jpg2pdf


# path = '/Users/osx/Desktop/test'  # 处理目录【修改】
# suffix = 'jpg'  # "处理目录"中的指定图片后缀【修改】


# def get_file_list(file_list_path, file_list_suffix):
#     """得到指定后缀的文件列表"""
#
#     exclude = (['.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini'])
#     result_list = []
#     if os.path.isfile(file_list_path):
#         result_list.append(os.path.abspath(file_list_path))
#     else:
#         for dir_path, dir_names, file_names in os.walk(file_list_path):
#             if os.path.abspath(dir_path) != os.path.abspath(file_list_path):  # 只允许 1 层目录
#                 continue
#             for name in file_names:
#                 if (not os.path.basename(name) in exclude) \
#                         and (os.path.splitext(name)[1][1:] == file_list_suffix):  # 指定后缀
#                     abs_path = os.path.abspath(os.path.join(dir_path, name))
#                     result_list.append(abs_path)
#     return result_list

# def rename(path, suffix, re1, re2=''):
#     """rename主方法"""
#
#     count = 0
#     file_list = get_file_list(path, suffix)
#     for tar in file_list:
#         base_name = os.path.basename(tar)
#         new_base_name = re.sub(re1, re2, base_name)
#         new_path = os.path.join(os.path.dirname(tar), new_base_name)
#         print('%s --> %s' % (base_name, new_base_name))
#         os.rename(tar, os.path.abspath(new_path))
#         count += 1
#
#     print('----------')
#     print('总共处理了：%s' % (count))


# exif


# path = '/Users/osx/Desktop/test'  # 处理目录【修改】
# suffix = 'jpg'  # "处理目录"中的指定图片后缀【修改】
# out_path = os.path.join(path, 'no-exif')  # 输出目录


# if os.path.exists(out_path):
#     print('输出目录已存在，请移走后再运行程序！')
#     sys.exit()


# def get_file_list(file_list_path, file_list_suffix):
#     """得到指定后缀的文件列表"""
#
#     exclude = (['.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini'])
#     result_list = []
#     if os.path.isfile(file_list_path):
#         result_list.append(os.path.abspath(file_list_path))
#     else:
#         for dir_path, dir_names, file_names in os.walk(file_list_path):
#             if os.path.abspath(dir_path) != os.path.abspath(file_list_path):  # 只允许 1 层目录
#                 continue
#             for name in file_names:
#                 if (not os.path.basename(name) in exclude) \
#                         and (os.path.splitext(name)[1][1:] == file_list_suffix):  # 指定后缀
#                     abs_path = os.path.abspath(os.path.join(dir_path, name))
#                     result_list.append(abs_path)
#     return result_list

# 未用到的未知用处的函数
# def parse_image(in_image_file, out_image_file):
#     """
#     删除图片exif信息
#     """
#
#     # -----删除exif信息-----
#     image_file = open(in_image_file, 'rb')
#     image = Image.open(image_file)
#     data = list(image.getdata())
#     image_without_exif = Image.new(image.mode, image.size)
#     image_without_exif.putdata(data)
#     image_without_exif.save(out_image_file)


# def resume(file_list):
#     """删除最后处理的5个图片（按最修改时间排序）"""
#
#     new_file_list = sorted(file_list, key=os.path.getmtime, reverse=True)
#     i = 0
#     for new_tar in new_file_list:
#         if i >= 5:
#             break
#         print("mtime: %s  delete: %s" % (time.strftime("%Y-%m-%d %H:%M:%S",
#                                                        time.localtime(os.path.getmtime(new_tar))
#                                                        ), new_tar))
#         os.remove(new_tar)
#         i += 1


# def analyse(in_reverse, file_list):
#     """打印最大、最小的5个文件"""
#
#
#     new_file_list = sorted(file_list, key=os.path.getsize, reverse=in_reverse)
#     i = 0
#     for new_tar in new_file_list:
#         if i >= 5:
#             break
#         print("size(Kilobyte): %s" % (round(os.path.getsize(new_tar) / float(1024))))
#         i += 1


# def noexif(path, suffix):
#     """noexif主方法方法"""
#     path = path
#     suffix = suffix
#     out_path = os.path.join(path, 'no-exif')  # 输出目录
#     if not os.path.exists(out_path):
#         os.makedirs(out_path)
#     file_list = get_file_list(out_path, suffix)
#     print('max --> min')
#     analyse(True, file_list)
#     print('----------')
#     print('min --> max')
#     analyse(False, file_list)
#     print('----------')
#     resume(file_list)
#     print('----------')
#     count = 0
#     file_list = get_file_list(path, suffix)
#     for tar in file_list:
#         tar_name = os.path.basename(tar)
#         tar_out = os.path.join(out_path, tar_name)
#         # 跳过已有文件
#         if os.path.exists(tar_out):
#             continue
#
#         count += 1
#         print('%s  %s' % (count, tar_name))
#         # parse_image(tar, tar_out)  # 处理图片
#
#     print('----------')
#     print('总共处理了：%s' % (count))

# 后缀名批量修改
def batch_rename(work_dir, old_ext):
    """
    传递当前目录，原来后缀名，新的后缀名后，批量重命名后缀
    return True if success; False if any error found(like unidentified files)
    """
    errors = []
    file_names = os.listdir(work_dir)
    file_names.sort()

    for file_name in file_names:
        # 获取得到文件后缀
        split_file = os.path.splitext(file_name)
        # 定位后缀名为old_ext 的文件
        new_ext = imghdr.what(work_dir + file_name)
        if split_file[1] == old_ext and new_ext and new_ext.upper() in ["PNG", "JPG", "JPEG"]:
            # 修改后文件的完整名称
            # print(f"split_file: {split_file}, new_ext: {new_ext}")
            newname = split_file[0] + "." + new_ext
            # 实现重命名操作
            os.rename(
                os.path.join(work_dir, file_name),
                os.path.join(work_dir, newname)
            )
        else:
            errors.append(f"{file_name}: unable to handle file, new_ext: {new_ext}")

    if len(errors) > 0:
        print("errors at batch_rename: ", errors)

    return len(errors) == 0


def png_to_jpg(jpg_base):
    files = os.listdir(jpg_base)
    counter = 0

    for file_name in files:
        file_type = imghdr.what(jpg_base + file_name)
        if file_type is None:
            continue
        if file_type.upper() not in ["PNG", "JPEG"]:
            print(f"Non-PNG/JPEG file found; file_name: {file_name}, file_type: {file_type}")
        if file_type.upper() != "PNG":
            continue

        # The image object is used to save the image in jpg format
        img_png = Image.open(jpg_base + file_name)
        jpeg_file_name = jpg_base + file_name.split(".")[0] + ".jpeg"
        img_png.convert('RGB').save(jpeg_file_name)
        counter += 1

    print(f"{counter} PNG files converted to JPEG file")


def sort_files(file_names):
    """
    sort files in book order:
        cov001 cover_front
        cov002 cover_back
        bok001 内页
        leg001 版权页
        fow001 前言
        fow002
    """
    contents = []
    cov, bok = [], []
    leg, fow = [], []
    file_names.sort()

    for file_name in file_names:
        if file_name.lower().startswith("cov"):
            cov.append(file_name)
        elif file_name.lower().startswith("bok"):
            bok.append(file_name)
        elif file_name.lower().startswith("leg"):
            leg.append(file_name)
        elif file_name.lower().startswith("fow"):
            fow.append(file_name)
        else:
            contents.append(file_name)

    return cov + bok + leg + fow + contents


def jpg_to_pdf(jpgBase, pdfBase, pdfName='test.pdf'):
    counter = 0
    with jpg2pdf.create(pdfBase + pdfName) as pdf:
        files = os.listdir(jpgBase)
        files = sort_files(files)

        for filename in files:
            file_type = imghdr.what(jpgBase + filename)
            # print(f"file_type: {file_type}")
            if file_type is None:
                continue
            if file_type.upper() != "JPG" and file_type.upper() != "JPEG":
                print(f"{filename}: not a JPG/JPEG file, file_type: {file_type}, skipping....")
                continue
            pdf.add(jpgBase + filename)
            counter += 1

        print(f"{counter} jpeg files were converted")
        print("-->" + pdfBase + pdfName)


# 主函数
def main():
    # 修改pdg后缀为jpg
    pdg_folder_name = input("Please enter PDG folder name: ")
    work_dir = f'/Users/ztong12/Downloads/pdf_book_generator/zip/{pdg_folder_name}/'  # pdg文件目录【修改】
    is_batch_rename_success = batch_rename(work_dir, '.pdg')  # pdg转jpg
    if not is_batch_rename_success:
        to_continue = input("errors found at batch_rename(), do you want to continue? Yes/No: ")
        if to_continue.upper() == "NO":
            print("ending conversion....")
            return


    """ TODO START
    # 进行文件重命名和删除exif
    # path = work_dir  # 处理目录
    # suffix = 'jpg'  # "处理目录"中的指定图片后缀
    # re1 = '000'
    # rename(path, suffix, re1)
    # noexif(path, suffix)  # 消除exif（耗时较多且大部分图片没必要）

    # 进行jpg2pdf操作
    # jpgBase=path+'no-exif'  # 消除exif时jpg文件目录
    # jpg_base = work_dir  # jpg来源的文件夹  # 不消除exif时jpg文件目录
    TODO END"""

    pdf_base = '/Users/ztong12/Downloads/pdf_book_generator/pdf/'  # pdf文件目录【修改】
    pdf_name = f'{pdg_folder_name}.pdf'  # pdf文件名【修改】

    png_to_jpg(work_dir)
    #
    jpg_to_pdf(work_dir, pdf_base, pdf_name)


if __name__ == '__main__':
    main()
