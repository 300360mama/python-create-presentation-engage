import os, shutil
from PIL import  Image

path_to_project = "D:\\server\\xamp\\htdocs\\test\\test_pres"
from_slide = "template-3"
to_slide = "testSlide"
folder_with_images = "C:\\Users\\олександр\\Desktop\\DVA Benepali Veeva Engage VF\\"


def main():
    images = get_images(folder_with_images)
    print(images)

    for i in range(0, len(images)):
        filename = to_slide + str(i + 1)
        old_html = path_to_project + "\\app\\" + from_slide + ".html"
        old_css = path_to_project + "\\app\\styles\\" + from_slide + ".css"
        old_model = path_to_project + "\\app\\data\\models\\" + from_slide + ".json"
        old_localization = path_to_project + "\\app\\i18n\\en\\" + from_slide + ".json"
        new_html = path_to_project + "\\app\\" + filename + ".html"
        new_css = path_to_project + "\\app\\styles\\" + filename + ".css"
        new_model = path_to_project + "\\app\\data\\models\\" + filename + ".json"
        new_localization = path_to_project + "\\app\\i18n\\en\\" + filename + ".json"

        copy_file(old_html, new_html)
        copy_file(old_css, new_css)
        copy_file(old_model, new_model)
        copy_file(old_localization, new_localization)

        old_image = folder_with_images+images[i]
        new_image = path_to_project+"\\app\\media\\images\\"+filename
        print(new_image)

        if os.path.isdir(new_image):
            copy_file(old_image, new_image+"\\bg.jpg")
        else:
            os.mkdir(new_image)
            copy_file(old_image, new_image+"\\bg.jpg")
        resize(new_image+"\\bg.jpg", (500, 500))


def resize(image, size):
    o_image = Image.open(image)
    i_width = o_image.width
    i_height = o_image.height

    full_width = 2048
    full_height = 1536
    koeficient = full_width/i_width
    new_width = 2048
    new_height = int(i_height*koeficient)

    if new_height>full_height:
        koeficient = full_height/i_height
        new_height = 1536
        new_width = int(i_width*koeficient)

    size = (new_width, new_height)
    print(size)
    r = o_image.resize(size)
    r.save(image)


def copy_file(old_file, new_file):

    if os.path.isdir(path_to_project):
        shutil.copy(old_file, new_file)


def get_images(path):
    list_imgs = os.listdir(path)
    res = []
    ext = [".jpg", ".png", ".JPG", ".PNG"]
    for image in list_imgs:
        if os.path.splitext(image)[1] in ext:
            res.append(image)

    return res


def set_css(file_css, image):
    images = get_images(folder_with_images)
    width = 100
    height = 100

    css = '''
        #bg {
           position: absolute;
           top: 0;
           left: 0;
           width: 100px;
           height: 100px;
           transform: matrix(0, 1, 1, 0, 0, 0); 
        }
    '''

    os.path.s

    fd = os.open(file_css, os.O_RDWR)

    if os.path.isfile(file_css):
        print(file_css)
        res = os.write(fd, str.encode(css))
        print(res)
    os.close(fd)


if __name__ == '__main__':
    main()
