# -*- coding: utf-8 -*-
import os
from ftplib import *
import sys
import math

ftp = FTP()


# 
# Variables contents paths in
# 

dest_dir = 'D:\hello'
remote_dir = 'test 123'

# 
# Functions
# 

def _open_conn(ftp_data):   # Tries to open connection to ftp-server
    try:
        ftp.connect('192.168.0.100', 2121)
    except Exception as message:
        print('Connection error:\n' + str(message))
        sys.exit()
    else:
        ftp.login('dima', '1111')
        print('Authentication and encode success')


def _is_ftp_dir(ftp_data, remote_path): # Determines if a directory is a directory
    original_cwd = ftp_data.pwd()
    try:
        ftp_data.cwd(remote_path)
        print(remote_path + ' is directory\nEntering...')
        ftp_data.cwd(original_cwd)
        return True
    except Exception as e:
        print(remote_path + " is not a directory")
        return False


def _check_if_contains_local(filename, dest_dir):
    print('Checking for: {0}'.format(filename))
    if filename in os.listdir():
        print('Already downloaded: {0}\nSkipping...'.format(filename))
        return True
    else:
        return False


def _mirror_ftp_dir(remote_path, dest_curdir):  # Mirrors directory from ftp to local machine
    mirrored_dir = os.path.join(dest_curdir, remote_path)
    print('Trying to make mirror: ' + mirrored_dir)
    if not os.path.exists(mirrored_dir):
        os.makedirs(mirrored_dir)
        print('created dir: {0}'.format(mirrored_dir))


# def calculate_usage_of_space(ftp_data, remote_path, dest_path, overall_size):
#     original_ftp_dir = ftp_data.pwd()
#     for name in ftp_data.nlst():
#         if _is_ftp_dir(ftp, name):
#             ftp.cwd(name)
#             original_os_dir = os.getcwd()
#             calculate_usage_of_space(ftp, name, dest_dir + '\\' + name, overall_size)
#             ftp.cwd(original_ftp_dir)
#         else:
#             if _check_if_contains_local(name, dest_path) == False:
#                 overall_size += ftp.size(name)
#             print(overall_size)
#             ftp_data.cwd(original_ftp_dir)
#             pass
#             return overall_size


def human_read_format(size):
    pwr = math.floor(math.log(size, 1024))
    suff = ['B', 'KB', 'MB', 'GB']
    return f"{size / 1024 ** pwr:.0f}{suff[pwr]}"


def _download_ftp_file(ftp_data, filename, dest_path):  # Downloads single file
    try:
        print('Downloading: {0}'.format(filename))
        ftp_data.retrbinary('RETR {0}'.format(filename), open(filename, 'wb').write)
        print('Downloaded: {0}'.format(filename))
    except FileNotFoundError as message:
        print('Failed: {0}'.format(message))


def download_ftp_tree(ftp_data, remote_path, dest_path):    # Checking for directories/files, than downloads contents
    original_ftp_dir = ftp_data.pwd()
    for name in ftp_data.nlst():
        if _is_ftp_dir(ftp, name):
            current_local_dir = os.getcwd()
            _mirror_ftp_dir(name, current_local_dir)
            ftp.cwd(name)
            print(ftp.nlst())
            original_os_dir = os.getcwd()
            os.chdir(name)
            print('Local dir changed to: {0}'.format(name))
            download_ftp_tree(ftp, name, dest_dir + '\\' + name)
            os.chdir(original_os_dir)
            ftp.cwd(original_ftp_dir)
        else:
            if _check_if_contains_local(name, dest_path) == False:
                _download_ftp_file(ftp_data, name, dest_path)
            ftp_data.cwd(original_ftp_dir)
            print('Back to: ' + original_ftp_dir)
            pass


# 
# Main executions
# 

if __name__ == '__main__':
    _open_conn(ftp)
    print('Connection opened')
    os.chdir(dest_dir)
    ftp.cwd(remote_dir)
    # print(calculate_usage_of_space(ftp, remote_dir, dest_dir))
    download_ftp_tree(ftp, remote_dir, dest_dir)
    print("Downloading success")
