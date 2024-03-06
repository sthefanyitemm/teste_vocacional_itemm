from flask import Flask
from src.controler.controler import *
from src.controler.erros import *
from flask import Blueprint, render_template, request, redirect, jsonify
from src.db import *

routes = {
        "home": "/",
        "cadastro": "/cadastro",
        "perguntas":"/perguntas",
        "resultados":"/resultados",
        "login":"/login",
        "reset":"/reset"      
    }

