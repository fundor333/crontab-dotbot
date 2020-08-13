# crontab-dotbot

Plugin for [`dotbot`](https://github.com/anishathalye/dotbot) to edit and sync crontab without deleting or editing manual added cronjob, only manage dotbot cron.

## Installation

1. Add `crontab-dotbot` as a submodule of your dotfiles repository.

```bash
git submodule add https://github.com/fundor333/crontab-dotbot.git
```

2. Modify your `install` script to enable the `crontab-dotbot` plugin.

```bash
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" --plugin-dir crontab-dotbot-c "${CONFIG}" "${@}"
```

## Usage

The plugin adds one directive use with `crontab` with two keyword:

- `cron`: The crontab regex 
- `command`: The command to run
For example:



```yaml
- crontab:
  - cron: 0 * * * *
    command: echo "Hello world"
```
