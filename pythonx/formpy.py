#!/usr/bin/env python

from __future__ import print_function
""" Multi language formatting with text-objects.
Source repository: https://github.com/jchlanda/formpy.vim
Inspired by:
  Fraser Cormack's formative.vim (https://github.com/frasercrmck/formative.vim)
Currently supports:
- ClangFormat (https://clang.llvm.org/docs/ClangFormat.html),
- yapf (https://github.com/google/yapf),
- cmake-format (https://github.com/cheshirekow/cmake_format).
"""
__all__ = []
__version__ = '0.2'
__author__ = 'Jakub Chlanda'
__license__ = 'This file is placed in the public domain.'
__email__ = "j.chlanda@gmail.com"

import difflib
import json
import subprocess
import sys
import vim
import logging

# TODO:
# - errors vs print outs vs raising exceptions,
# - add code comments,
# - decide if to remove loggins.


class FileTypeException(Exception):

  def __init__(self, file_type):
    self.file_type = file_type


class BinaryNotFoundException(Exception):

  def __init__(self, binary):
    self.binary = binary


class FileType:
  c = 1
  python = 2
  cmake = 3


class Binary:

  def __init__(self, file_type):
    self.file_type = file_type
    if FileType.python == file_type:
      self.binary = 'yapf'
    elif FileType.c == file_type:
      self.binary = 'clang-format'
    elif FileType.cmake == file_type:
      self.binary = 'cmake-format'

    # Check if appropriate formatter is available.
    try:
      dev_null = open(os.devnull, 'w')
      subprocess.call([self.binary, '--help'], stdout=dev_null, stderr=dev_null)
    except OSError as e:
      raise BinaryNotFoundException(self.binary)

  def constructCommand(self, file_type, line_start, line_end, vim_buffer):
    command = [self.binary]
    if FileType.python == file_type:
      lines = '%s-%s' % (line_start, line_end)
      style = Formatter.vimEval('g:formpy_style_python')
      command.extend(['--style', style, '--lines', lines])
      # TODO: Remove
      # command.extend([
      #     '--style', '{based_on_style: chromium, indent_width: 2}', '--lines',
      #     lines
      # ])
    elif FileType.c == file_type:
      style = Formatter.vimEval('g:formpy_style_c')
      lines = '%s:%s' % (line_start, line_end)
      command.extend(['-style', style, '-lines', lines])
    elif FileType.cmake == file_type:
      lines = '%s-%s' % (line_start, line_end)
      command.extend([vim_buffer.name])

    return command


class Formatter:
  """ Formatter - handle all formatting tasks.

    Responsible for:
    - communication with vim - obtaining text object, updating the diff,
    - communication with yapf.
    """

  @staticmethod
  def vimEval(name):
    """ A wrapper around vim eval.
        Return evaluated expression or None.
        """
    if (vim.eval('exists("' + name + '")') == "1"):
      return vim.eval(name)
    else:
      return None

  def __init__(self):
    self.lines = None
    self.line_start = None
    self.line_end = None
    self.encoding = None
    self.buffer = None
    self.text = None
    self.formatted_lines = None
    self.line_start = vim.current.range.start + 1
    self.line_end = vim.current.range.end + 1
    try:
      file_type = Formatter.vimEval('s:formpy_filetype')
      if 'python' == file_type:
        self.file_type = FileType.python
      elif file_type in [
          'c', 'cpp', 'objc', 'objcpp', 'java', 'javascript', 'proto'
      ]:
        self.file_type = FileType.c
      elif 'cmake' == file_type:
        self.file_type = FileType.cmake
      else:
        raise FileTypeException(file_type)
      self.binary = Binary(self.file_type)
    except FileTypeException as fte:
      raise fte
    except BinaryNotFoundException as bnfe:
      raise bnfe
    except Exception as e:
      # TODO: Handle this.
      raise ValueError('Something went wrong in Formatter.__init__\n' + str(e))
    # TODO: How applicable this is?
    # Only log if on systems that support /tmp dir (and when user asked for
    # it).

  def __loadBuffer(self):
    """ Load current vim buffer.
        """
    self.encoding = Formatter.vimEval('&encoding')
    self.buffer = vim.current.buffer
    self.text = '\n'.join(self.buffer)

  def __postProcessDiff(self):
    """ Apply the formatting.
        Go over all the lines and replace the original object with the formatted one.
        """
    lines = self.formatted_lines[0:]
    update = difflib.SequenceMatcher(None, vim.current.buffer, lines)
    for op in reversed(update.get_opcodes()):
      if op[0] is not 'equal':
        if op[1] in range(self.line_start - 1, self.line_end):
          vim.current.buffer[op[1]:op[2]] = lines[op[3]:op[4]]

  def executeFormat(self):
    """ Main hook
        Retrieve lines, format the object, apply the changes.
        """
    self.__loadBuffer()

    startupinfo = None
    if sys.platform.startswith('win32'):
      startupinfo = subprocess.STARTUPINFO()
      startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
      startupinfo.wShowWindow = subprocess.SW_HIDE

    # Call the binary.
    command = self.binary.constructCommand(self.file_type, self.line_start,
                                           self.line_end, self.buffer)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        startupinfo=startupinfo)
    stdout, stderr = p.communicate(input=self.text.encode(self.encoding))

    # Report error, or replace the object with formatted version.
    if stderr:
      # TODO: This is not applicable any more, handle multiple binaries.
      print(
          "Error while parsing the input file.\n"
          "'yapf' can only format syntactically correct files.\n",
          file=sys.stderr)
      return
    if not stdout:
      print(
          "No output from the formatter (crashed?).\nPlease report the bug.\n")
      return
    else:
      self.formatted_lines = stdout.decode(self.encoding).split('\n')
      self.__postProcessDiff()


def main(argv):
  try:
    F = Formatter()
    F.executeFormat()
  except FileTypeException as fte:
    sys.stderr.write(" -------> FTE: {0}\n".format(fte.file_type))
    sys.exit()
  except BinaryNotFoundException as bnfe:
    sys.stderr.write(" -------> BNFE: {0}\n".format(bnfe.binary))
    sys.exit()
  except Exception as e:
    raise ValueError('Something went wrong in main\n' + str(e))
  pass


if __name__ == "__main__":
  main(sys.argv)

