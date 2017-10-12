" formpy.vim - ClangFormat functionality with YetAnotherPythonFormatter with
"              text-objects.
" Author: Jakub Chlanda <j.chlanda@gmail.com>
" Version: 0.1
" License: This file is placed in the public domain.
" Source repository: https://github.com/jchlanda/formpy.vim
" Heavily inspired by: clang-format,
"                      yapf,
"                      Fraser Cormack's formative.vim
"                      (https://github.com/frasercrmck/formative.vim)

if exists("g:loaded_formpy")
  execute "nnoremap <silent> " . g:formpy_nor_key .
    \ " :set opfunc=formpy#FormPy<CR>g@"
  execute "vnoremap <silent> " . g:formpy_vis_key .
    \ " :call formpy#FormPy(visualmode(), 1)<CR>"
  execute "inoremap <silent> " . g:formpy_ins_key .
    \ " <ESC>:call formpy#FormPy('oneline')<CR>a"
  execute "nnoremap <silent> " . g:formpy_line_key .
    \ " :call formpy#FormPy('oneline')<CR>"
  execute "nnoremap <silent> " . g:formpy_file_key .
    \" :call formpy#FormPy('file')<CR>"
endif
