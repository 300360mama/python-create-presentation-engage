import os
import shutil
from PIL import Image
import json
from natsort import natsorted
from config import config
# import tinify


path_to_project = config["path_to_project"]
from_slide = config["from_slide"]
name_slide = config["name_slide"]
folder_with_images = config["folder_with_images"]
old_html = path_to_project + "\\app\\" + from_slide + ".html"
old_css = path_to_project + "\\app\\styles\\" + from_slide + ".css"
old_model = path_to_project + "\\app\\data\\models\\" + from_slide + ".json"
old_localization = path_to_project + "\\app\\i18n\\en\\" + from_slide + ".json"


def main():
    images = get_images(folder_with_images)

    for i in range(0, len(images)):
        filename = name_slide + str(i + 1)
        new_html = path_to_project + "\\app\\" + filename + ".html"
        new_css = path_to_project + "\\app\\styles\\" + filename + ".css"
        new_model = path_to_project + "\\app\\data\\models\\" + filename + ".json"
        new_localization = path_to_project + "\\app\\i18n\\en\\" + filename + ".json"

        copy_file(old_html, new_html)
        copy_file(old_css, new_css)
        copy_file(old_model, new_model)
        copy_file(old_localization, new_localization)

        old_image = folder_with_images+images[i]
        slide_folder_with_images = path_to_project+"\\app\\media\\images\\"+filename
        new_image = slide_folder_with_images+"\\bg."+get_extension(images[i])

        if os.path.isdir(slide_folder_with_images):
            copy_file(old_image, new_image)
        else:
            os.mkdir(slide_folder_with_images)
            copy_file(old_image, new_image)

        resize(new_image)
        set_css(new_css, new_image)
        set_structure(path_to_project+"\\structure.json", filename, 'core')
        set_model(new_model, filename, "bg."+get_extension(images[i]))
        clean_localization(new_localization)
        set_html(new_html)


def resize(image):
    o_image = Image.open(image)
    i_width = o_image.width
    i_height = o_image.height

    full_width = 2048
    full_height = 1536
    coefficient = full_width/i_width
    new_width = 2048
    new_height = int(i_height*coefficient+0.5)

    if new_height > full_height:
        coefficient = full_height/i_height
        new_height = 1536
        new_width = int(i_width*coefficient+0.5)

    size = (new_width, new_height)
    extension = get_extension(image)

    if extension == "jpg":
        extension = "jpeg"
    print(extension)
    r = o_image.resize(size)
    r.save(image, extension)


def copy_file(old_file, new_file):
    if os.path.isdir(path_to_project):
        shutil.copy(old_file, new_file)


def get_images(path):
    list_imgs = os.listdir(path)
    res = []
    ext = ["jpg", "png"]
    for image in list_imgs:
        if get_extension(image).lower() in ext:
            res.append(image)

    natsorted(res, key=lambda y: y.lower())
    return res


def set_css(file_css, image):
    o_image = Image.open(image)
    width = int(o_image.width/2)
    height = int(o_image.height/2)
    left = int(1024 - width)/2 - 84
    top = int(768 - height)/2 - 179

    css = '''
#bg {0}
    position: absolute;
    top: 0;
    left: 0;
    width: {1}px;
    height: {2}px;
    transform: matrix(1, 0, 0, 1, {3}, {4}); 
{5}
'''

    css = css.format('{', width, height, left, top, '}')
    fd = os.open(file_css, os.O_RDWR)

    if os.path.isfile(file_css):
        os.write(fd, str.encode(css))
    os.close(fd)


def set_structure(structure_file, slide, chapter):

    if os.path.isfile(structure_file):
        with open(structure_file, 'r') as structure:
            data = json.load(structure)
            new_slide = {
                "name": slide,
                "title": slide,
                "template": slide+".html"
            }
            data["slides"][slide] = new_slide
            data["chapters"][chapter]["content"].append(slide)

        with open(structure_file, 'w') as structure:
            json.dump(data, structure)


def set_model(file, slide, name_image):
    with open(file, 'r') as model:
        data = json.load(model)
        if data["sidebar"]:
            del data["sidebar"]

        if data["headline"]:
            del data["headline"]

        new_model = {
                "src": "media/images/"+slide+"/"+name_image,
                "size": "100% 100%",
                "position": "center center"
        }
        data["bg"] = new_model

    with open(file, 'w') as model:
        json.dump(data, model)


def set_html(file):
    with open(file) as html:
        data = html.read()
        slide = os.path.basename(file)
        slide = os.path.splitext(slide)
        str1 = data.replace("<link rel=\"stylesheet\" href=\"styles/template-3.css\">", "<link rel=\"stylesheet\" href=\"styles/"+slide[0]+".css\">")
        str2 = str1.replace("<co-grid-container fixed id=\"contentArea\" class=\"content-area back-cont-bio\" user-label=\"Content area\">", "<co-grid-container fixed id=\"contentArea\" class=\"content-area back-cont-bio\" user-label=\"Content area\">\n<co-image id=\"bg\" model=\"m.bg\" user-label=\"Background\"></co-image>\n")

    with open(file, "w") as html:
        html.write(str2)


def clean_localization(file):
    with open(file, 'w') as model:
        data = {}
        json.dump(data, model)


def get_extension(image):
    extension = os.path.splitext(image)[1][1:].lower()
    return extension


# def optimize_image(image):
#     tinify.key = config["api_key"]
#     source = tinify.from_file(image)
#     source.to_file(image)


if __name__ == '__main__':
    main()

