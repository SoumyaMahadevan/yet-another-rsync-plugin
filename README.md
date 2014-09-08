yet-another-rsync-plugin
========================

Sublime Tet 2 plugin that syncs between your local and remote directories.

This plugin lets you sync down from remote directories, by automatically setting up local directories in the path you configure.
You can do all your development locally, and each file save syncs back to the corresponding remote location. Great for VPN usage!

========================
To Start:
========================
1. Configure your remote server, and remote prefix. This is common prefix for all remote directories.
2. Configure each of the remote directories to be synced from and to. You can add new directories to this list as needed.
3. Next, configure your local prefix. The local directory name is the same as the remote one.
4. Move and edit (if necessary) exclude-list.txt. These are files that don't need to be synced. The format of the exclude file follows the rsync 'exclude-from' format.


========================
Sync down:
========================
1. Default key binding to sync down is ctrl d + ctrl d.
2. If executed from an existing synced directory, this sync down only the specific remote directory.
3. If not, this syncs down all the remote directories in the list.

========================
Sync up:
========================
1. On every file save, the changes are synced back to the remote repository.