# formpy.vim

Provides [YAPF](https://github.com/google/yapf) vim integration in the same way as [formative.vim](https://github.com/frasercrmck/formative.vim) integrates [clang-format](http://clang.llvm.org/docs/ClangFormat.html#vim-integration).

The plugin supports the same set of actions as [formative.vim](https://github.com/frasercrmck/formative.vim), for example:

    <C-K>2j   - YAPF 2 lines downwards
    <C-K>ap   - YAPF around the current paragraph
    <C-K>/foo - YAPF from the current line until the first match of 'foo'

The only limitations come from python's syntax, so a valid [formative.vim](https://github.com/frasercrmck/formative.vim) action:

    <C-K>iB   - ClangFormat "inner Block"
would still pass the block to [YAPF](https://github.com/google/yapf), but will have slightly different range.

#### Formpy-Formative Integration

[formative.vim](https://github.com/frasercrmck/formative.vim) is great, in fact it is so good, that I had to write this plugin. Once you start using [formative.vim](https://github.com/frasercrmck/formative.vim), there is no way back, you have to have formatting done automatically for you. And it is XXI century, the time of manually inserting spaces (no tabs, no!) is over. The problem arises, when you get used to the mappings provided by [formative.vim](https://github.com/frasercrmck/formative.vim) and want to have the same mappings working in python. By default, whichever plugin is loaded last will, be responsible for formatting, regardless of the buffer's filetype. The solution provided here, is to have the desired mapping redefined in after-directory. If you already maintain entries for `c`, `cpp`, `python` you can extend those with the content of the corresponding files from [after_ftplugin](https://github.com/jchlanda/formpy.vim/tree/master/after_ftplugin), if not, copying the content of the directory to `<vim_root>/after/ftplugin` will do the trick.

#### Reqiorements

Unlike [formative.vim](https://github.com/frasercrmck/formative.vim), formpy comes with its own python runner, so ther is no need to point it to any external files. However, you will have to make sure that [YAPF](https://github.com/google/yapf) is installed and available on the path of your system. Formpy also requires vim compiled with python support.

#### Key Bindings

As per [formative.vim](https://github.com/frasercrmck/formative.vim) \<C-k> is set as a default 'leader' key in the plugin. Follow this key with whichever motion or text object you like, as in the examples above. It can be [customised](##Customisation).

#### Special Bindings

Again, as per [formative.vim](https://github.com/frasercrmck/formative.vim), 'quick' [YAPF](https://github.com/google/yapf) binding is provided via `g:formpy_line_key`. This works on the current line alone. Its default mapping is `<C-k>k`, which is designed to emulate vim's `c -> cc`, `d -> dd` line-wise operations. `<C-k>u` is used to invoke [YAPF](https://github.com/google/yapf) on the whole file, and can be reset with `g:fmtv_clang_format_file_key`.

#### [GIPHY](https://giphy.com/)

#TODO
![](https://cloud.githubusercontent.com/assets/1158422/5235521/00c36298-77fc-11e4-88f7-e23735c08e0e.gif)

## Installation

### [vim-plug](https://github.com/junegunn/vim-plug)

Add the following to your `.vimrc`:

    Plug 'jchlanda/formpy.vim'
Source your `.vimrc` and run:

    :PlugInstall


### [Vundle](https://github.com/gmarik/Vundle.vim)

Add the following to your `.vimrc`:

    Plugin 'jchlanda/formpy.vim'
Source your `.vimrc` and run:

    :PluginInstall

The plugin defines its own help tags, please remember to run: `:helptags` and `:help formpy`.

## Customisation

All of the variables used by formpy to construct specific key mappings can be overridden, please see:

    let g:formpy_nor_key  = <C-woof>
    let g:formpy_vis_key  = <C-woof>
    let g:formpy_ins_key  = <C-woof>
    let g:formpy_line_key = <C-woof>
    let g:formpy_file_key = <C-woof>
