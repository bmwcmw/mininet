"Module dependency utility functions for Mininet."

from mininet.util import quietRun
from mininet.log import info, error, debug
from os import environ
import subprocess

def lsmod():
    "Return output of lsmod."
    return quietRun( 'lsmod' )

def rmmod( mod ):
    """Return output of lsmod.
       mod: module string"""
    return quietRun( [ 'rmmod', mod ] )

def modprobe( mod ):
    """Return output of modprobe
       mod: module string"""
    return quietRun( [ 'modprobe', mod ] )

OF_KMOD = 'ofdatapath'
OVS_KMOD = 'openvswitch_mod'
TUN = 'tun'

def moduleDeps( subtract=None, add=None, moduleName='it' ):
    """Handle module dependencies.
       subtract: string or list of module names to remove, if already loaded
       add: string or list of module names to add, if not already loaded"""
    subtract = subtract if subtract is not None else []
    add = add if add is not None else []
    if type( subtract ) is str:
        subtract = [ subtract ]
    if type( add ) is str:
        add = [ add ]
    for mod in subtract:
        if mod in lsmod():
            info( '*** Removing ' + mod + '\n' )
            rmmodOutput = rmmod( mod )
            if rmmodOutput:
                error( 'Error removing ' + mod + ': "%s">\n' % rmmodOutput )
                exit( 1 )
            if mod in lsmod():
                error( 'Failed to remove ' + mod + '; still there!\n' )
                exit( 1 )
    for mod in add:
        if mod not in lsmod():
            info( '*** Loading ' + mod + '\n' )
            modprobeOutput = modprobe( mod )
            if modprobeOutput:
                error( 'Error inserting ' + mod + '\n'
                'Is %s installed and available via modprobe?\n' %
                moduleName +
                'Error was: "%s"\n' % modprobeOutput.strip() )
            if mod not in lsmod():
                error( 'Failed to insert ' + mod + ' - quitting.\n' )
                exit( 1 )
        else:
            debug( '*** ' + mod + ' already loaded\n' )


def pathCheck( *args, **kwargs ):
    "Make sure each program in *args can be found in $PATH."
    moduleName = kwargs.get( 'moduleName', 'it' )
    for arg in args:
        if not quietRun( 'which ' + arg ):
            error( 'Cannot find required executable %s.\n' % arg +
                'Please make sure that %s is installed ' % moduleName +
                'and available in your $PATH:\n(%s)\n' % environ[ 'PATH' ] )
            exit( 1 )


def checkRunning ( *args ):
    "Check if each program in *arg is running"
    try:
        for arg in args:
            subprocess.check_output(["pgrep", arg], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return False
    return True


