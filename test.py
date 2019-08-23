#!/usr/bin/env python3
from mailcleaner import User, Commtouch, WWLists, MTAConfig, SystemConf

commtouch = Commtouch()
c = commtouch.all()
print(c)
newton = User.find_by_username_and_domain("newton", "toto.local")
print("Hello")
print(newton)
newton.username = "newton3"
newton.save()
print(newton)

wwlists = WWLists()
lists = wwlists.all()
print(lists)

exim_stage1 = MTAConfig().find_by_set_id_and_stage_id(set_id=1, stage_id=1)
print(exim_stage1)
exim_stage1.reject_bad_spf = False
exim_stage1.save()
print(exim_stage1)

system_conf = SystemConf.first()
print(system_conf)

from mailcleaner.config import MailCleanerConfig
mc_config = MailCleanerConfig.get_instance()
res_1 = mc_config.change_configuration("HOSTID", "42")
print(res_1)
print("REGISTERED: {}".format(mc_config))
res_2 = mc_config.change_configuration("UNKOWNKEY", "10")
print(res_2)
print("REGISTERED: {}".format(mc_config))
