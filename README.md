# formpy.vim

Provides [YAPF](https://github.com/google/yapf) vim integration in the same way as [formative.vim](https://github.com/frasercrmck/formative.vim) integrates [clang-format](http://clang.llvm.org/docs/ClangFormat.html#vim-integration).

The plugin supports the same set of actions as [formative.vim](https://github.com/frasercrmck/formative.vim), for example:

    <C-k>2j   - YAPF 2 lines downwards
    <C-k>ap   - YAPF around the current paragraph
    <C-k>/foo - YAPF from the current line until the first match of 'foo'

The only limitations come from python's syntax, so a valid [formative.vim](https://github.com/frasercrmck/formative.vim) action:

    <C-k>iB   - ClangFormat "inner Block"
would still pass the block to [YAPF](https://github.com/google/yapf), but will have slightly different range.

#### Formpy-Formative Integration

[formative.vim](https://github.com/frasercrmck/formative.vim) is great, in fact it is so good, that I had to write this plugin. Once you start using [formative.vim](https://github.com/frasercrmck/formative.vim), there is no way back, you have to have formatting done automatically for you. And it is XXI century, the time of manually inserting spaces (no tabs, no!) is over. The problem arises, when you get used to the mappings provided by [formative.vim](https://github.com/frasercrmck/formative.vim) and want to have the same mappings working in python. By default, whichever plugin is loaded last will, be responsible for formatting, regardless of the buffer's filetype. The solution provided here, is to have the desired mappings redefined in [after-directory](https://github.com/jchlanda/formpy.vim/tree/master/after/ftplugin). It provides the mappings for `python` filetype only, letting [formative](https://github.com/frasercrmck/formative.vim) take care of `c`-language family filetypes.

An example of two buffers (`cpp` and `py`) calling into [formative.vim](https://github.com/frasercrmck/formative.vim) and formpy respectively.
![](https://raw.githubusercontent.com/jchlanda/formpy.vim/gif/assets/formpy_cpp_py.640.gif)

#### Requirements

Unlike [formative.vim](https://github.com/frasercrmck/formative.vim), formpy comes with its own python runner, so ther is no need to point it to any external files. However, you will have to make sure that [YAPF](https://github.com/google/yapf) is installed and available on the path of your system. Formpy also requires vim compiled with python support.

#### Key Bindings

As per [formative.vim](https://github.com/frasercrmck/formative.vim) \<C-k> is set as a default 'leader' key in the plugin. Follow this key with whichever motion or text object you like, as in the examples above. It can be [customised](##Customisation).

#### Special Bindings

Again, as per [formative.vim](https://github.com/frasercrmck/formative.vim), 'quick' [YAPF](https://github.com/google/yapf) binding is provided via `g:formpy_line_key`. This works on the current line alone. Its default mapping is `<C-k>k`, which is designed to emulate vim's `c -> cc`, `d -> dd` line-wise operations. `<C-k>u` is used to invoke [YAPF](https://github.com/google/yapf) on the whole file, and can be reset with `g:fmtv_clang_format_file_key`.

#### [GIPHY](https://giphy.com/)

![](https://raw.githubusercontent.com/jchlanda/formpy.vim/gif/assets/formpy_py.640.gif)

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

All of the variables used by formpy to construct specific key mappings can be overridden, please see:

[YAPF](https://github.com/google/yapf) allows for different formatting styles to be used, formpy exposes this functionality through `g:formpy_style` option. It can be set to either the name of the desired formatting style (for example `pep8` or `goole`), or to the fully qualified file name containing style settings. For full details on the available formatting options please run: `yapf --help` or `yapf --style-help`.

A sample formatting style file is included [here](https://github.com/jchlanda/formpy.vim/tree/master/doc/.style.yapf).

Formpy defaults to: `pep`. To change it:

    let g:formpy_style = /path/to/your_style.yapf
