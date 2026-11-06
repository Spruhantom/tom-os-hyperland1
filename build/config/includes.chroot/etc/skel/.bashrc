# ████ Tom OS — bashrc ████
# Based on the Ubuntu default bashrc with a neon-punk welcome.

# ---------- welcome banner ----------
# In kitty, fastfetch shows the Tom OS logo + system info; on a plain TTY the
# block-letter banner is shown instead. Set TOMOS_NO_FASTFETCH=1 to skip it.
if [ -n "$PS1" ] && [ -n "$KITTY_WINDOW_ID" ] && [ -z "$TOMOS_NO_FASTFETCH" ] && command -v fastfetch >/dev/null 2>&1; then
    fastfetch
    # drop any late terminal-query replies so they don't land on the prompt
    read -r -s -t 0.1 -d '' -n 65536 _tomos_junk 2>/dev/null; unset _tomos_junk
    printf '\e[1;95mwelcome to TOM OS\e[0m \e[90m//\e[0m \e[1;96mneon punk edition\e[0m\n'
    printf '\e[90mtip:\e[0m \e[35mSUPER+ENTER\e[0m kitty \e[90m|\e[0m \e[35mSUPER+D\e[0m apps \e[90m|\e[0m \e[35mSUPER+W\e[0m WordDocEdit \e[90m|\e[0m \e[35mSUPER+L\e[0m lock\n'
    printf '\n'
elif [ -n "$PS1" ]; then
    printf '\n'
    printf '\e[1;95m█████  ███  █   █ \e[0m   \e[1;96m ███   ████ \e[0m\n'
    printf '\e[1;95m  █   █   █ ██ ██ \e[0m   \e[1;96m█   █ █     \e[0m\n'
    printf '\e[1;95m  █   █   █ █ █ █ \e[0m   \e[1;96m█   █  ███  \e[0m\n'
    printf '\e[1;95m  █   █   █ █   █ \e[0m   \e[1;96m█   █     █ \e[0m\n'
    printf '\e[1;95m  █    ███  █   █ \e[0m   \e[1;96m ███  ████  \e[0m\n'
    printf '\n'
    printf '\e[1;95mwelcome to TOM OS\e[0m \e[90m//\e[0m \e[1;96mneon punk edition\e[0m\n'
    printf '\e[90mtip:\e[0m \e[35mSUPER+ENTER\e[0m kitty \e[90m|\e[0m \e[35mSUPER+D\e[0m apps \e[90m|\e[0m \e[35mSUPER+W\e[0m WordDocEdit \e[90m|\e[0m \e[35mSUPER+L\e[0m lock\n'
    printf '\n'
fi

# ---------- history ----------
HISTCONTROL=ignoreboth
HISTSIZE=10000
HISTFILESIZE=20000
shopt -s histappend checkwinsize

# ---------- prompt ----------
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac
if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        color_prompt=yes
    fi
fi

PS1='\[\e[1;95m\]\u\[\e[0m\]@\[\e[1;96m\]\h\[\e[0m\]:\[\e[1;35m\]\w\[\e[0m\]\$ '

# ---------- aliases ----------
alias ls='ls --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias update='sudo apt update && sudo apt upgrade'

# ---------- misc ----------
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
fi

if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi
