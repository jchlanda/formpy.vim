#!/usr/bin/env python

from __future__ import print_function
""" ClangFormat functionality with YetAnotherPythonFormatter with text-objects.
Source repository: https://github.com/jchlanda/formpy.vim
Heavily inspired by: clang-format,
                     yapf,
                     Fraser Cormack's formative.vim
                     (https://github.com/frasercrmck/formative.vim)
"""
__all__ = []
__version__ = '0.1'
__author__ = 'Jakub Chlanda'
__license__ = 'This file is placed in the public domain.'

import difflib
import json
import subprocess
import sys
import vim
import logging


class Formatter:
    """ Formatter - handle all formatting tasks.

    Responsible for:
    - communication with vim - obtaining text object, updating the diff,
    - communication with yapf.
    """

    def __init__(self):
        self.lineSplit = "-"
        self.lines = None
        self.lineStart = None
        self.lineEnd = None
        self.encoding = None
        self.buffer = None
        self.text = None
        self.cursor = None
        self.formattedLines = None
        # Only log if on systems that support /tmp dir (and when user asked for
        # it).
        self.enableLogging = 1 == self.__vimEval(
            'g:formpy_logging') and os.path.exists("/tmp")

    def __vimEval(self, name):
        """ A wrapper around vim eval.
        Return evaluated expression or None.
        """
        if (vim.eval('exists("' + name + '")') == "1"):
            return vim.eval(name)
        else:
            return None

    def __setLines(self):
        """ Set up the lines.
        Establish the line range of the object to be formatted.
        """
        self.lines = self.__vimEval('l:lines')
        if not self.lines:
            self.lineStart = vim.current.range.start + 1
            self.lineEnd = vim.current.range.end + 1
            self.lines = '%s%s%s' % (self.lineStart, self.lineSplit,
                                     self.lineEnd)

    def __loadBuffer(self):
        """ Load current vim buffer.
        """
        self.encoding = self.__vimEval('&encoding')
        self.buffer = vim.current.buffer
        self.text = '\n'.join(self.buffer)
        self.cursor = int(vim.eval('line2byte(line("."))+col(".")')) - 2
        if self.cursor < 0:
            print('Couldn\'t determine cursor position. Is your file empty?')
            return False
        return True

    def __postProcessDiff(self):
        """ Apply the formatting.
        Go over all the lines and replace the original object with the formatted one.
        """
        lines = self.formattedLines[0:]
        update = difflib.SequenceMatcher(None, vim.current.buffer, lines)
        if self.enableLogging:
            for line in lines:
                logging.debug(line)
        for op in reversed(update.get_opcodes()):
            if op[0] is not 'equal':
                if op[1] in range(self.lineStart - 1, self.lineEnd):
                    if self.enableLogging:
                        logging.debug('updating')
                        logging.debug(lines[op[3]:op[4]])
                    vim.current.buffer[op[1]:op[2]] = lines[op[3]:op[4]]
                else:
                    if self.enableLogging:
                        logging.debug('Not in range {0}, not updating'.format(
                            self.lines))
                        logging.debug('Vim.current.range.start: {0}'.format(
                            vim.current.range.start))
                        logging.debug('Vim.current.range.end: {0}'.format(
                            vim.current.range.end))
                        logging.debug(op)
                        logging.debug(lines[op[3]:op[4]])

    def executeFormat(self):
        """ Main hook
        Retrieve lines, format the object, apply the changes.
        """
        self.__setLines()
        self.__loadBuffer()

        if self.enableLogging:
            logging.basicConfig(
                filename="/tmp/formpy-format.log",
                level=logging.DEBUG,
                filemode="w")

        startupinfo = None
        if sys.platform.startswith('win32'):
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        # Construct the command.
        style = self.__vimEval('g:formpy_style')
        if self.enableLogging:
            logging.debug(style)
        binary = 'yapf'
        command = [binary, '--style', style, '--lines', self.lines]

        # Call yapf.
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo)
        stdout, stderr = p.communicate(input=self.text.encode(self.encoding))

        # Report error, or replace the object with formatted version.
        if stderr:
            print(
                "Error while parsing the input file.\n"
                "'yapf' can only format syntactically correct files.\n",
                file=sys.stderr)
            return
        if not stdout:
            if self.enableLogging:
                logging.debug("Stdout.")
            print(
                "No output from the formatter (crashed?).\nPlease report the bug.\n"
            )
            return
        else:
            self.formattedLines = stdout.decode(self.encoding).split('\n')
            self.__postProcessDiff()


def main(argv):
    F = Formatter()
    F.executeFormat()
    pass


if __name__ == "__main__":
    main(sys.argv)
