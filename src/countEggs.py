import argparse, csv, os
import timeit
import cv2
import pycocotools.coco as coco
from lib.detectors.detector_factory import detector_factory
from datasets.dataset_factory import get_dataset
from utils.debugger import Debugger
from opts import opts

#img_dir = os.path.join(os.getcwd(), 'data\\egg\\val')
img_dir = r'P:\\Robert\\tf-test\\workspace\\egg-counting\\images\\test-2'

if __name__ == '__main__':
  performance_results = [['filename', 'num labelled', 'num predicted',
    'abs. error', 'pct. error']]
  opt = opts().init()
  Dataset = get_dataset(opt.dataset, opt.task)
  opt = opts().update_dataset_info_and_set_heads(opt, Dataset)
  Detector = detector_factory[opt.task]
  start_t = timeit.default_timer()
  detector = Detector(opt)
  print('model load time:', timeit.default_timer() - start_t)
  parsed = coco.COCO(opt.demo)
  for i, imgId in enumerate(parsed.imgs):
    file_name = parsed.imgs[imgId]['file_name']
    img = cv2.imread(os.path.join(img_dir, file_name))
    print('processing image at', os.path.join(img_dir, file_name))
    run_dict = detector.run(img)
    num_predicted = len([result for result in run_dict['results'][1] if result[-1] > 0.3])
    num_labelled = len([parsed.loadAnns(ids=[annID]) for annID in parsed.getAnnIds(imgIds=[imgId])])
    #print('num predicted: %i | num labelled: %i'%(num_predicted, num_labelled))
    abs_diff = abs(num_labelled - num_predicted)
    rel_error = abs_diff / num_labelled if num_labelled > 0 else ''
    performance_results.append([file_name, num_labelled, num_predicted, abs_diff,
        rel_error*(1 if type(rel_error) is str else 100)])
  with open('egg_counts.csv', 'wt', newline='') as resultsFile:
    writer = csv.writer(resultsFile)
    writer.writerows(performance_results)
