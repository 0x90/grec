#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Small script for file recovery after git rm
# based on http://stackoverflow.com/questions/14475003/recover-files-after-git-rm-rf
#
# author: @090h
# Tested on MacOSX 10.8.2
# Doesn't work at Windows, because of `file` command usage
from subprocess import Popen, PIPE, STDOUT
import os,argparse

root_dir = '/Users/090h/Dropbox/git-0x90/'
obj_dir = root_dir + '.git/objects'
tmp = '/tmp/somefile'
recover_dir = root_dir + 'recovered'

def exec_cmd(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read()

def recover():
    os.chdir(root_dir)

    if not os.path.exists(recover_dir):
        os.mkdir(recover_dir)

    for root, subFolders, files in os.walk(obj_dir):
        for file in files:
            obj_file = os.path.join(root,file)
            obj_name = obj_file.replace(obj_dir,'').replace('/','')
            obj = exec_cmd('git cat-file -p '+ obj_name)
            open(tmp,'wb').write(obj)
            ext = exec_cmd('file '+tmp).split(': ')[1].split(' ')[0].lower()
            ext_path = os.path.join(recover_dir,ext)
            if not os.path.exists(ext_path):
                os.mkdir(ext_path)

            rec_path = os.path.join(ext_path,obj_name+'.'+ext)
            os.rename(tmp,rec_path)
            print 'Recovering file to %s' % (rec_path,)



class valid_dir(argparse.Action):
    def __call__(self,parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))

        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))

        if not os.path.exists(prospective_dir):
            print("Invalid git directory")
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Small script for file recovery after git rm')
    #parser = argparse.ArgumentParser(description='test', fromfile_prefix_chars="@")
    #parser.add_argument('-p', '--launch_directory', action=readable_dir, default=ldir)
    parser.add_argument('-d', 'project path with .git directory inside',action=valid_dir)
    parser.add_argument('-r', 'path to recover to ')
    parser.add_help('help')
    args = parser.parse_args()
    print (args)
