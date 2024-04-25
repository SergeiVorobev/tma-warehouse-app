from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3

from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
