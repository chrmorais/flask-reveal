# -*- coding: utf-8 -*-

import os
import shutil
import tarfile
import zipfile


def move_and_replace(src, dst):
    """
    Helper function used to move files from one place to another,
    creating os replacing them if needed

    :param src: source directory
    :param dst: destination directory
    """

    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    for src_dir, _, files in os.walk(src):
        # using os walk to navigate through the directory tree
        # keep te dir structure by replacing the source root to
        # the destination on walked path
        dst_dir = src_dir.replace(src, dst)

        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)  # to copy not fail, create the not existing dirs

        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)

            if os.path.exists(dst_file):
                os.remove(dst_file)  # to copy not fail, create existing files

            shutil.move(src_file, dst_dir)  # move the files

    shutil.rmtree(src)  # remove the dir structure from the source


def extract_file(compressed_file, path='.'):
    if os.path.isfile(compressed_file):
        if tarfile.is_tarfile(compressed_file):
            with tarfile.open(compressed_file, 'r:gz') as tfile:
                basename = tfile.members[0].name
                tfile.extractall(path+'/')
        elif zipfile.is_zipfile(compressed_file):
            with zipfile.ZipFile(compressed_file, 'r') as zfile:
                basename = zfile.namelist()[0]
                zfile.extractall(path)
        else:
            raise NotImplementedError('File type not supported')
    else:
        raise FileNotFoundError(
            '{0} is not a valid file'.format(compressed_file))

    return os.path.abspath(os.path.join(path, basename))
