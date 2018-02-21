" Multi language formatting with text-objects.
" Author: Jakub Chlanda <j.chlanda@gmail.com>
" Version: 0.2
" License: This file is placed in the public domain.
" Source repository: https://github.com/jchlanda/formpy.vim
" Inspired by:
"   Fraser Cormack's formative (https://github.com/frasercrmck/formative.vim)
" Currently supports:
" - ClangFormat (https://clang.llvm.org/docs/ClangFormat.html),
" - yapf (https://github.com/google/yapf),
" - cmake-format (https://github.com/cheshirekow/cmake_format).

" Initialization {{{
if !exists("g:loaded_formpy") || &cp
  finish
endif

let s:cpo_save = &cpo
set cpo&vim

if !has("python3")
  let s:python_cmd = "pyf "
else
  let s:python_cmd = "py3f "
endif

" Absolute path of the script file:
let g:formpy_source =
  \ get( g:, "formpy_source", expand("<sfile>:p:h")."/../pythonx/formpy.py")
" Style for python:
if !exists("g:formpy_style_python")
  let g:formpy_style_python = get( g:, "formpy_style_python", "pep8")
endif
" Style for c-language family:
if !exists("g:formpy_style_c")
  let g:formpy_style_c = get( g:, "formpy_style_c", "LLVM")
endif

" }}}

" Functions {{{
function! formpy#FormPy(type, ...)
  let s:formpy_filetype = &filetype
  if a:0                     " Invoked from Visual mode.
    let s:beg = "'<"
    let s:end = "'>"
  elseif a:type == "file"    " Invoked on the whole file.
    let s:beg = "1"
    let s:end = "$"
  elseif a:type == "oneline" " Invoked on one line only.
    let s:beg = "."
    let s:end = "."
  else                       " Invoked from Normal mode.
    echo " NORMAL"
    let s:beg = "'["
    let s:end = "']"
  endif

  silent execute "normal! :".s:beg.",".s:end . s:python_cmd . g:formpy_source."\<CR>"

endfunction
" }}}

let &cpo = s:cpo_save
unlet s:cpo_save
