#!/bin/bash

tor &
privoxy /etc/privoxy/config &
sleep 3
scrapy crawl darkrawl -s JOBDIR=.scrapy/darkrawl_job -s SCHEDULER_PERSIST=True
