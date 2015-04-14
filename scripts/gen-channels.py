#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import urllib2
import codecs

def load_channels():
    data = urllib2.urlopen('http://api.peers.tv/tvguide/2/channels.json?fields=channelId,title,logoURL&device=iphone')
    return json.load(data)['channels']

def get_value(dict, key, default):
    if key in  dict.keys():
        return dict[key]
    else:
        return default

def channels_formatted(channels):
    for channel in channels:
        title = channel['title']
        channelURL = get_value(channel, 'logoURL', '')
        yield u'{0} | ![{1}]({2}) | {3}\n'.format(channel['channelId'], title, channelURL, title)

def gen_channels_md(output_name):
    from datetime import date
    output = codecs.open(output_name, 'w', 'utf-8')
    output.write(u'title: Список каналов\n')
    output.write(u'quotes language: french\n')
    output.write(u'version: {0}\n'.format(date.today().__str__()))
    output.write(u'status: поддерживается\n\n')
    output.write(u'Идентификатор | Логотип | Название\n')
    output.write(u'--------------|---------|----------\n')

    channels = load_channels();
    formatted_channels = channels_formatted(channels)
    for channel in formatted_channels:
        output.write(channel)

def main():
    from argparse import ArgumentParser
    cli = ArgumentParser()
    cli.add_argument('output')
    args = cli.parse_args()

    gen_channels_md(args.output)

if __name__ == '__main__':
    main()
