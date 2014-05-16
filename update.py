#!/usr/bin/env python

import boto.route53
import importlib
import os
import os.path
import ConfigParser

def get_func(fullname):
	(mod_name, name) = fullname.rsplit('.', 1)
	mod = importlib.import_module(mod_name)
	return getattr(mod, name)

def update(aws_access_key_id, aws_secret_access_key, hostname, zone_id, ipv4_func, ipv6_func):
	conn = boto.route53.connection.Route53Connection(aws_access_key_id, aws_secret_access_key)

	rrs = boto.route53.record.ResourceRecordSets(conn, zone_id, comment='rt53-dynamic-dns')
	change = rrs.add_change(action='UPSERT', name=hostname, type='A')
	change.add_value(v4_func())
	change = rrs.add_change(action='UPSERT', name=hostname, type='AAAA')
	change.add_value(v6_func())
	commit_result = rrs.commit()
	print commit_result

if __name__=='__main__':
	p = ConfigParser.RawConfigParser()
	p.read(os.path.join(os.environ['HOME'], '.rt53-dynamic-dns'))
	v4_func = get_func(p.get('address', 'v4_func'))
	v6_func = get_func(p.get('address', 'v6_func'))
	update(p.get('aws', 'aws_access_key_id'),
		   p.get('aws', 'aws_secret_access_key'),
		   p.get('address', 'hostname'),
		   p.get('aws', 'zone_id'),
		   v4_func,
		   v6_func)
