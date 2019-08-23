import enum


class MCBooleanStringEnum(enum.Enum):
    """
    MailCleaner MySQL Enum used for MTAConfig, administrator tables, etc.
    """
    true = "true"
    false = "false"