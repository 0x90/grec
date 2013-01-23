#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Small script for file recovery after git rm
# based on http://stackoverflow.com/questions/14475003/recover-files-after-git-rm-rf
#
# author: @090h
# Tested on MacOSX 10.8.2
# usage: ./grec.py -p /Users/090h/projects/git-test/ -r recov
#
# Doesn't work at Windows, because of `file` command usage

from subprocess import Popen, PIPE, STDOUT
import os,argparse

def exec_cmd(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()

def recover(project_dir,recovery_dir):
    obj_dir  = os.path.join(project_dir,'.git/objects')
    tmp = '/tmp/somefile'

    if not os.path.exists(obj_dir):
        print("Invalid git directory")

    if not os.path.exists(recovery_dir):
        os.mkdir(recovery_dir)

    os.chdir(project_dir)
    for root, subFolders, files in os.walk(obj_dir):
        for file in files:
            obj_file = os.path.join(root,file)
            obj_name = obj_file.replace(obj_dir,'').replace('/','')
            obj = exec_cmd('git cat-file -p '+ obj_name)
            open(tmp,'wb').write(obj)
            ext = exec_cmd('file ' + tmp).split(': ')[1].split(' ')[0].lower()
            ext_path = os.path.join(recovery_dir,ext)
            if not os.path.exists(ext_path):
                os.mkdir(ext_path)

            rec_path = os.path.join(ext_path,obj_name+'.'+ext)
            os.rename(tmp,rec_path)
            print 'Recovering %s file to %s' % (ext,rec_path,)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Small script for file recovery after git rm -rf")
    parser.add_argument('-p', help = 'project path with .git directory inside')
    parser.add_argument('-r', help = 'path to recover to ')
    args = vars(parser.parse_args())
    recover(args['p'],args['r'])
