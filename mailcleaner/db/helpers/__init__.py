import enum


class MCBooleanStringEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum("1","2") used in MTAConfig, administrator tables, etc.
    """
    true = "true"
    false = "false"


class MCYesNoEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum("yes","no") used in antivirus table.
    """
    yes = "yes"
    no = "no"


class MCAllowDenyEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('allow','deny') used in filename and filetype tables.
    """
    allow = "allow"
    deny = "deny"


class MCNoAddReplaceEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum("no","add","replace") used in antivirus table.
    """
    no = "no"
    add = "add"
    replace = "replace"


class MCYesNoDisarmEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum("yes","no","disarm") used in  table.
    """
    yes = "yes"
    no = "no"
    disarm = "disarm"


class MCAdminManagerHotlineEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('administrator','manager','hotline','user') used in feature_restriction table.
    """
    administrator = "administrator"
    manager = "manager"
    hotline = "hotline"
    user = "user"


class MCCountFrequency(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('count','frequency') used in rrd_stats table.
    """
    count = "count"
    frequency = "frequency"


class MCGaugeCounterDeriveEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('GAUGE','COUNTER','DERIVE','ABSOLUTE','COMPUTE') used in rrd_stats_element table.
    """
    GAUGE = "GAUGE"
    COUNTER = "COUNTER"
    DERIVE = "DERIVE"
    ABSOLUTE = "ABSOLUTE"
    COMPUTE = "COMPUTE"


class MCAverageMinMaxEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('AVERAGE','MIN','MAX','LAST') used in rrd_stats_element table.
    """
    AVERAGE = "AVERAGE"
    MIN = "MIN"
    MAX = "MAX"
    LAST = "LAST"


class MCLineAreaStackEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('line','area','stack') used in rrd_stats_element table.
    """
    line = "line"
    area = "area"
    stack = "stack"


class MCTCPEnum(enum.Enum):
    """
    MailCleaner MySQL Enum created for type enum('TCP','UDP','ICMP') use in external_access table.
    """
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
