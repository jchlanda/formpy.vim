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

if exists("g:loaded_formative ")
  execute "nnoremap <silent> " . g:fmtv_clang_format_file_key .
    \ " :call formative#ClangFormat('file')<CR>"
  execute "nnoremap <silent> " . g:fmtv_clang_format_nor_key .
    \ " :set opfunc=formative#ClangFormat<CR>g@"
  execute "nnoremap <silent> " . g:fmtv_clang_format_line_key .
    \ " :call formative#ClangFormat('oneline')<CR>"
  execute "vnoremap <silent> " . g:fmtv_clang_format_vis_key .
    \ " :call formative#ClangFormat(visualmode(), 1)<CR>"
  execute "inoremap <silent> " . g:fmtv_clang_format_ins_key .
    \ " <ESC>:call formative#ClangFormat('oneline')<CR>a"
endif
