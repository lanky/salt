'''
Manage groups on Linux
'''

import grp


def __virtual__():
    '''
    Set the user module if the kernel is Linux
    '''
    return 'group' if __grains__['kernel'] == 'Linux' else False


def add(name, gid=None):
    '''
    Add the specified group

    CLI Example::

        salt '*' group.add foo 3456
    '''
    cmd = 'groupadd '
    if gid:
        cmd += '-g {0} '.format(gid)
    cmd += name

    ret = __salt__['cmd.run_all'](cmd)

    return not ret['retcode']


def delete(name):
    '''
    Remove the named group

    CLI Example::

        salt '*' group.delete foo
    '''
    ret = __salt__['cmd.run_all']('groupdel {0}'.format(name))

    return not ret['retcode']


def info(name):
    '''
    Return information about a group

    CLI Example::

        salt '*' group.info foo
    '''
    grinfo = grp.getgrnam(name)
    return {'name': grinfo.gr_name,
            'passwd': grinfo.gr_passwd,
            'gid': grinfo.gr_gid,
            'members': grinfo.gr_mem}


def getent():
    '''
    Return info on all groups

    CLI Example::

        salt '*' group.getent
    '''
    ret = []
    for grinfo in grp.getgrall():
        ret.append(info(grinfo.gr_name))
    return ret


def chgid(name, gid):
    '''
    Change the gid for a named group

    CLI Example::

        salt '*' group.chgid foo 4376
    '''
    pre_gid = __salt__['file.group_to_gid'](name)
    if gid == pre_gid:
        return True
    cmd = 'groupmod -g {0} {1}'.format(gid, name)
    __salt__['cmd.run'](cmd)
    post_gid = __salt__['file.group_to_gid'](name)
    if post_gid != pre_gid:
        if post_gid == gid:
            return True
    return False
