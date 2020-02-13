## Installation

### bash

```sh
function q()
{
    source="python /home/jabernardo/Workspace/q/main.py"

    if [[ ( $# -eq 0 ) ]]; then
        history -w
        $($source $1)
    else
        cd $($source $1)
    fi
}
```

### fish

```sh
function q
        set -l source "python /home/jabernardo/Workspace/q/main.py"

        if test (count $argv) -eq 0
                history save
                eval (eval $source $argv --history "~/.local/share/fish/fish_history")
        else
                cd (eval $source $argv)
        end
end

```