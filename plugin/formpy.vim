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
if exists("g:loaded_formpy") || &cp
  finish
endif

if !has("python")
  echoerr "formpy reuires Python to be enabled."
endif

let g:loaded_formpy = 1
" }}}

let g:formpy_nor_key  = get( g:, "formpy_nor_key", "<C-k>")
let g:formpy_vis_key  = get( g:, "formpy_vis_key", "<C-k>")
let g:formpy_ins_key  = get( g:, "formpy_ins_key", "<C-k>")
let g:formpy_line_key = get( g:, "formpy_line_key", "<C-k>k")
let g:formpy_file_key = get( g:, "formpy_file_key", "<C-k>u")

" Key mappings {{{
execute "nnoremap <silent> " . g:formpy_nor_key .
  \ " :<C-U>set opfunc=formpy#FormPy<CR>g@"
execute "vnoremap <silent> " . g:formpy_vis_key .
  \ " :<C-U>call formpy#FormPy(visualmode(), 1)<CR>"
execute "inoremap <silent> " . g:formpy_ins_key .
  \ " <ESC>:<C-U>call formpy#FormPy('oneline')<CR>a"
execute "nnoremap <silent> " . g:formpy_line_key .
  \ " :<C-U>call formpy#FormPy('oneline')<CR>"
execute "nnoremap <silent> " . g:formpy_file_key .
  \ " :<C-U>call formpy#FormPy('file')<CR>"
" }}}
