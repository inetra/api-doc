#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import urllib2
import codecs

def load_channels():
	data = urllib2.urlopen('http://api.peers.tv/tvguide/2/channels.json?device=iphone')
	return json.load(data)['channels']

def get_value(dict, key, default):
    if key in  dict.keys():
        return dict[key]
    else:
        return default

def gen_channels_md(channels, output_name):
    from datetime import date
    output = codecs.open(output_name, 'w', 'utf-8')
    output.write(u'title: Список каналов\n')
    output.write(u'quotes language: french\n')
    output.write(u'version: {0}\n'.format(date.today().__str__()))
    output.write(u'status: поддерживается\n\n')
    output.write(u'# Список каналов\n\n')
    output.write(u'Идентификатор | Логотип | Название\n')
    output.write(u'--------------|---------|----------\n')
    for channel in channels:
        title = get_value(channel, 'title', '')
        output.write(u'{0} | ![{1}]({2}) | {3}\n'.format(get_value(channel, 'channelId', ''), title, get_value(channel, 'logoURL', ''), title))

def main():
    from argparse import ArgumentParser
    cli = ArgumentParser()
    cli.add_argument('output')
    args = cli.parse_args()

    channels = load_channels()
    gen_channels_md(channels, args.output)

if __name__ == '__main__':
    main()
