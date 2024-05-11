from argparse import ArgumentParser
import logging

import annotation
import copy_images
import random_dataset


if __name__ == "__main__":
    logging.basicConfig(filename='lab2.log', level=logging.INFO)
    parser = ArgumentParser()
    parser.add_argument('func', type=str, help='1 - create annotation for original dataset;\n'
                                               '2 - create copy of dataset and annotation;\n'
                                               '3 - create random dataset and annotation.',
                        choices=['1', '2', '3'])
    parser.add_argument('-d', '--data_dir', type=str, help='Directory of dataset', required=True)
    parser.add_argument('-c', '--classes', nargs='+', help='List of classes', required=True)
    parser.add_argument('-a', '--annotation', type=str, help='Path to annotation', required=True)
    args = parser.parse_args()

    if args.func == '1':
        annotation.create_annotation(args.data_dir, args.classes, args.annotation)
    elif args.func == '2':
        copy_images.create_dataset_copy(args.data_dir, f"{args.data_dir}_copy", args.classes)
        copy_images.create_copy_annotation(f"{args.data_dir}_copy", args.classes, args.annotation)
    elif args.func == '3':
        cls_dict = random_dataset.create_dataset_random(args.data_dir, f"{args.data_dir}_random", args.classes)
        random_dataset.create_random_annotation(f"{args.data_dir}_random", cls_dict, args.annotation)
