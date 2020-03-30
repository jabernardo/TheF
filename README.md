# Shorthand ?! Press The F!
Shorthand application for navigating in your terminal. Jump into directories and auto-correct commands.

[![asciicast](https://asciinema.org/a/301975.svg)](https://asciinema.org/a/301975)

## Prerequisites
Before you continue, ensure you have met the following requirements:

- You have installed Python ^3.6
- You have install poetry

## Installation

### Clone Repository

```sh
# Clone repository
git clone https://github.com/jabernardo/TheF
cd TheF
# Install dependencies using poetry
pip install -r requirements.txt
```

## Hook up in the shell!

#### bash

```sh
function f()
{
    source="python /{installation path}/main.py"

    if [[ ( $# -eq 0 ) ]]; then
        history -w
        $($source $1)
    elif [[ ( $1 == -* ) || ( $# -gt 1 ) ]]; then
        $source $@
    else
        cd $($source $1)
    fi
}
```

#### fish

```sh
function f
        set -l source "python /{installation path}/main.py"

        if test (count $argv) -eq 0
                history save
                eval (eval $source $argv --history "~/.local/share/fish/fish_history")
        else
                cd (eval $source $argv)
        end
end
```

## Contibuting to TheF!
To contribute to TheF! Make sure to give a star and forked this repository.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## License
The `TheF` is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
