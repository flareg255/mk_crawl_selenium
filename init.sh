#!/bin/sh
sudo rm -rf /var/crawl/selenium_crawl/data/process/first_cat
sudo rm -rf /var/crawl/selenium_crawl/data/process/second_cat
sudo rm -rf /var/crawl/selenium_crawl/data/process/third_cat
sudo rm -rf /var/crawl/selenium_crawl/data/process/fourth_cat
sudo rm -rf /var/crawl/selenium_crawl/data/process/items

sudo mkdir /var/crawl/selenium_crawl/data/process/first_cat
sudo mkdir /var/crawl/selenium_crawl/data/process/second_cat
sudo mkdir /var/crawl/selenium_crawl/data/process/third_cat
sudo mkdir /var/crawl/selenium_crawl/data/process/fourth_cat
sudo mkdir /var/crawl/selenium_crawl/data/process/items

sudo rm -rf /var/crawl/selenium_crawl/data/archive/first_cat
sudo rm -rf /var/crawl/selenium_crawl/data/archive/second_cat
sudo rm -rf /var/crawl/selenium_crawl/data/archive/third_cat
sudo rm -rf /var/crawl/selenium_crawl/data/archive/fourth_cat
sudo rm -rf /var/crawl/selenium_crawl/data/archive/items

sudo mkdir /var/crawl/selenium_crawl/data/archive/first_cat
sudo mkdir /var/crawl/selenium_crawl/data/archive/second_cat
sudo mkdir /var/crawl/selenium_crawl/data/archive/third_cat
sudo mkdir /var/crawl/selenium_crawl/data/archive/fourth_cat
sudo mkdir /var/crawl/selenium_crawl/data/archive/items

sudo rm -rf /var/crawl/selenium_crawl/data/first_cat
sudo rm -rf /var/crawl/selenium_crawl/data/second_cat
sudo rm -rf /var/crawl/selenium_crawl/data/third_cat
sudo rm -rf /var/crawl/selenium_crawl/data/fourth_cat
sudo rm -rf /var/crawl/selenium_crawl/data/items

sudo mkdir /var/crawl/selenium_crawl/data/first_cat
sudo mkdir /var/crawl/selenium_crawl/data/second_cat
sudo mkdir /var/crawl/selenium_crawl/data/third_cat
sudo mkdir /var/crawl/selenium_crawl/data/fourth_cat
sudo mkdir /var/crawl/selenium_crawl/data/items

sudo chmod 777 /var/crawl/selenium_crawl/data/*
sudo chmod 777 /var/crawl/selenium_crawl/data/process/*
sudo chmod 777 /var/crawl/selenium_crawl/data/archive/*
