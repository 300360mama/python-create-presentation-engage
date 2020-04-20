import os
import shutil
from PIL import Image
import  json
path_to_project = "D:\\server\\xamp\\htdocs\\test\\test_py"
from_slide = "template-3"
to_slide = "newSlide"
folder_with_images = "C:\\Users\\олександр\\Desktop\\Presentazione PVS - approvato\\"


def main():
    images = get_images(folder_with_images)

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

        if os.path.isdir(new_image):
            copy_file(old_image, new_image+"\\bg.jpg")
        else:
            os.mkdir(new_image)
            copy_file(old_image, new_image+"\\bg.jpg")
        resize(new_image+"\\bg.jpg")
        set_css(new_css, new_image+"\\bg.jpg")
        set_structure(path_to_project+"\\structure.json", filename, 'core')


def resize(image):
    o_image = Image.open(image)
    i_width = o_image.width
    i_height = o_image.height

    full_width = 2048
    full_height = 1536
    koeficient = full_width/i_width
    new_width = 2048
    new_height = int(i_height*koeficient+0.5)

    if new_height > full_height:
        koeficient = full_height/i_height
        new_height = 1536
        new_width = int(i_width*koeficient+0.5)
        print(new_width)

    size = (new_width, new_height)
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
    o_image = Image.open(image)
    width = int(o_image.width/2)
    height = int(o_image.height/2)

    css = '''
        #bg {0}
           position: absolute;
           top: 0;
           left: 0;
           width: {1}px;
           height: {2}px;
           transform: matrix(0, 1, 1, 0, 0, 0); 
        {3}
    '''

    css = css.format('{', width, height, '}')

    fd = os.open(file_css, os.O_RDWR)

    if os.path.isfile(file_css):
        res = os.write(fd, str.encode(css))
    os.close(fd)


def set_structure(file, slide, chapter):

    if os.path.isfile(file):
        with open(file, 'r') as structure:
            data = json.load(structure)
            new_slide = {
                "name": slide,
                "template": slide+".html"
            }
            data["slides"][slide] = new_slide
            data["chapters"][chapter]["content"].append(slide)

        with open(file, 'w') as structure:
            json.dump(data, structure)


def set_model(file, slide):


if __name__ == '__main__':
    main()

