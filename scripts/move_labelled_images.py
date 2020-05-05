import os, pathlib, secrets, shutil

imgs_path_str = 'C:\\Users\\Tracking\\centernet-test\\data\\eggPresort'
imgs_path = pathlib.Path(imgs_path_str)
xml_files = list(imgs_path.glob('*.xml'))
passes = 1
while len(xml_files) > 0:
    secure_random = secrets.SystemRandom()
    xml_file = secure_random.choice(xml_files)
    dest_determinant = secure_random.random()
    dest = os.path.join(imgs_path_str, f"{'train' if dest_determinant >= 0.2 else 'test'}")
    print('dest:', dest)
    split_file = str(xml_file).split('\\')
    xml_basename = split_file[-1]
    png_basename = '.'.join(xml_basename.split('.')[:-1]) + '.png'
    png_file = '\\'.join(split_file[:-1]) + "\\" + png_basename
    shutil.move(xml_file, f"{dest}/{xml_basename}")
    shutil.move(png_file, f"{dest}/{png_basename}")
    print(f"Pass {passes}: would have moved file {xml_file} to {dest}/{xml_basename} and {png_file} to {dest}/{png_basename}")
    xml_files.remove(xml_file)
    passes += 1

# one-time approach: randomly choose 107 images to place into the test-2 directory, leaving the rest in place.
# for i in range(107):
#     secure_random = secrets.SystemRandom()
#     xml_file = secure_random.choice(xml_files)
#     split_file = str(xml_file).split('\\')
#     xml_basename = split_file[-1]
#     dest = os.path.join(imgs_path_str, '../train300sq')
#     png_basename = '.'.join(xml_basename.split('.')[:-1]) + '.png'
#     png_file = '\\'.join(split_file[:-1]) + "\\" + png_basename
#     shutil.move(xml_file, f"{dest}/{xml_basename}")
#     shutil.move(png_file, f"{dest}/{png_basename}")
#     xml_files.remove(xml_file)
