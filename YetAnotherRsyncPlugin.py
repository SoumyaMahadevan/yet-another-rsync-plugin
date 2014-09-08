import sublime
import sublime_plugin
import subprocess
import os

settings = sublime.load_settings('YetAnotherRsyncPlugin.sublime-settings')
def setting(setting_name):
    return settings.get(setting_name)

def get_local_path(dir_name):
    return setting('yarp_local_prefix') + '/' + dir_name + '/'

def get_remote_path(dir_name):
    if setting('yarp_remote_server'):
        return setting('yarp_remote_server') + ':' + setting('yarp_remote_prefix') + '/' + dir_name + '/'
    else:
        return setting('yarp_remote_prefix') + '/' + dir_name + '/'

def construct_rsync_command(current_file=None, sync_up=True):
    dir_names = []
    if current_file and current_file.startswith(setting('yarp_local_prefix')):
        dir_names.append(current_file.split(setting('yarp_local_prefix') + '/', 1)[1].split('/')[0])
    else:
        if not sync_up:
            # sync down everything
            dir_names = setting('yarp_remote_dirs')

    commands = []
    for dir_name in dir_names:
        local_path = get_local_path(dir_name)
        if not os.path.isdir(local_path):
            # Create local path if it does not exist
            os.makedirs(local_path)
        remote_path = get_remote_path(dir_name)
        if sync_up:
            cmd = ['/usr/bin/rsync', '-auvzC', '--exclude-from=%s' % setting('yarp_exclude_file_path'),
                    local_path, remote_path]
        else:
            cmd = ['/usr/bin/rsync', '-auvzC', '--delete', '--exclude-from=%s' % setting('yarp_exclude_file_path'),
                    remote_path, local_path]
        commands.append(cmd)
    return commands

def exec_rsync_commands(commands=[]):
    for cmd in commands:
        print "Executing %s" % cmd
        subprocess.check_call(cmd, stderr=subprocess.STDOUT)

class YetAnotherRsyncPlugin(sublime_plugin.EventListener):
    def on_post_save(self, view):
        """ Sync saved file """
        current_file = view.file_name()
        commands = construct_rsync_command(current_file=current_file, sync_up=True)
        exec_rsync_commands(commands)

class RsyncDown(sublime_plugin.TextCommand):
    """ Bulk sync on pressing ctrl shift down """

    def run_(self, args):
        current_file = self.view.file_name()
        commands = construct_rsync_command(current_file=current_file, sync_up=False)
        exec_rsync_commands(commands)
        self.view.run_command('revert')
