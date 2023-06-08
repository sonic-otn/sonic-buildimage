#!/bin/bash

redis-cli -p 6379 save
redis-cli -p 5000 save
redis-cli -p 5001 save
redis-cli -p 5002 save
redis-cli -p 5003 save


