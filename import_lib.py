from flask import Flask, jsonify,render_template,request
import pickle
import os
import findspark
findspark.init()
from pyspark.sql import SparkSession
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from os.path import exists
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json
import jsonlines
import  pymongo
from datetime import datetime
from os.path import exists
