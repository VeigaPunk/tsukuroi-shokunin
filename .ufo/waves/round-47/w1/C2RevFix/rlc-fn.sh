root_locator_class() { # root_locator_class PATH -> absolute|empty|relative|unsafe
  # An override path is caller data, not host evidence. Only an absolute path from a
  # conservative character set may be stat'd and printed; `=` and whitespace are rejected
  # so a path like `/x root_mode=0755` can neither forge a token nor reach stat. The raw
  # override is never echoed for the empty/relative/unsafe classes.
  case "$1" in
    '') printf 'empty' ;;
    /*)
      case "$1" in
        *[!A-Za-z0-9._/+-]*) printf 'unsafe' ;;
        *) printf 'absolute' ;;
      esac
      ;;
    *) printf 'relative' ;;
  esac
}

