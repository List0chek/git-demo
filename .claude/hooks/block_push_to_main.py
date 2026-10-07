"""
Claude Code PreToolUse hook: blocks the agent from pushing to main.

Claude Code sends the pending Bash call as JSON on stdin. Exit code 2 blocks the call,
and whatever is printed to stderr is shown to Claude as the reason.
"""
import json
import shlex
import subprocess
import sys

PROTECTED_BRANCH = "main"
COMMAND_SEPARATORS = {"&&", "||", ";", "|"}


def current_branch(cwd: str) -> str:
    """
    Get the branch checked out in a directory.

    Args:
        cwd: Directory to ask Git in.

    Returns:
        The branch name, or an empty string when HEAD is detached or cwd is not a repository.
    """
    result = subprocess.run(["git", "branch", "--show-current"], cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip()


def split_commands(command: str) -> list[list[str]]:
    """
    Split a shell command line into its separate commands.

    Args:
        command: The full command line Claude wants to run.

    Returns:
        One list of words per command.
    """
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
    lexer.whitespace_split = True
    commands: list[list[str]] = [[]]
    for word in lexer:
        if word in COMMAND_SEPARATORS:
            commands.append([])
        else:
            commands[-1].append(word)
    return commands


def is_push_to_protected_branch(words: list[str], cwd: str) -> bool:
    """
    Check whether one command pushes to the protected branch.

    Args:
        words: The words of a single command.
        cwd: Directory the command runs in.

    Returns:
        True when the command is a git push that targets the protected branch.
    """
    if "git" not in words or "push" not in words[words.index("git"):]:
        return False
    git_index = words.index("git")
    push_index = words.index("push", git_index)
    git_options = words[git_index + 1:push_index]
    if "-C" in git_options:
        cwd = git_options[git_options.index("-C") + 1]
    push_arguments = [word for word in words[push_index + 1:] if not word.startswith("-")]
    if "--all" in words or "--mirror" in words:
        return True
    refspecs = push_arguments[1:]
    if not refspecs:
        return current_branch(cwd) == PROTECTED_BRANCH
    for refspec in refspecs:
        destination = refspec.split(":")[-1].lstrip("+").removeprefix("refs/heads/")
        if destination == PROTECTED_BRANCH or (destination == "HEAD" and current_branch(cwd) == PROTECTED_BRANCH):
            return True
    return False


def main() -> None:
    """
    Read the pending tool call and block it when it pushes to the protected branch.
    """
    tool_call = json.load(sys.stdin)
    command = tool_call.get("tool_input", {}).get("command", "")
    cwd = tool_call.get("cwd", ".")
    try:
        commands = split_commands(command)
    except ValueError:
        return
    if any(is_push_to_protected_branch(words, cwd) for words in commands):
        print(
            f"Blocked by project hook: agents never push to {PROTECTED_BRANCH}. "
            "Push a feature branch and open a pull request instead.",
            file=sys.stderr
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
